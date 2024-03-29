"""
This module serves as the basic import for scientific processing of data.
It groups various useful modules and defines helper functions.
"""

__version__ = "18.03.18"

import warnings

import scipy as sp
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
from scipy import array as arr

from uncertainties import ufloat as uf
from uncertainties import umath

import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd

from tabulate import tabulate

plt.rcParams["figure.figsize"] = (4 * 1.5, 2.5 * 1.5)
plt.rcParams["figure.dpi"] = 100
plt.rcParams["text.usetex"] = True
plt.rcParams['text.latex.unicode'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern"]
plt.rcParams["text.latex.preamble"] = r"""
\usepackage[decimalsymbol=comma]{siunitx}
"""


def latex_table(table, header=True, tablefmt="latex_booktabs", **kwargs):
    if header:
        print(tabulate(table, headers="keys", tablefmt=tablefmt, **kwargs))
    else:
        print(tabulate(table, tablefmt=tablefmt, **kwargs))


def dataframe_from_csv(csv, index_col=None, **kwargs):
    return pd.read_csv(csv, sep=r"\s*,\s*",
                       engine="python",
                       skip_blank_lines=True,
                       index_col=index_col,
                       comment="#",
                       ** kwargs)


def mean_and_error(values):
    array = sp.array(values)
    mean = array.mean()
    single_value_error = array.std(ddof=1)
    mean_error = single_value_error / sp.sqrt(len(array))

    return mean, mean_error


def f_line(x, a, b):
    """
    Simple line function, intended for ls regression.
    """
    return a * x + b


def f_para(x, a, b, c):
    """
    Quadratic function, intended for ls regression.
    """
    return a * x**2 + b * x + c


def f_cubic(x, a, b, c, d):
    """
    Cubic function, intended for ls regression
    """
    return a * x**3 + b * x**2 + c * x + d


def f_exp(x, a, b, c, d):
    """
    Exponential function with translation, intended for ls regression.
    """
    return a * sp.exp(b * (x + c)) + d


def f_exp_simple(x, a, b):
    """
    Exponential function without translation, intended for ls regression.
    """
    return a * sp.exp(b * x)


class FitCurve:
    """
    Class representing function fitted to some data. Objects are callable.
    Arguments are the same as for scipy.optimize.curve_fit.

    Parameters
    ---------
    f : callable
        Function to fit parameters to.
        Has to have format f(x, param1, param2, ...)
    xdata : M-length sequence
        X values of data points.
    ydata : M-length sequence
        Y values of data points.
    p0 : None, scalar or N-length sequence
        Initial guess for the parameters.
    sigma : None or M-length sequence
        Determines the uncertainty of ydata.
    """

    def __init__(self, f, xdata, ydata, *args, **kwargs):
        params, cov = curve_fit(f, xdata, ydata, *args, **kwargs)
        errors = [sp.sqrt(cov[i, i]) for i in range(len(cov))]

        if len(sp.where(cov == sp.inf)[0]) > 0:
            raise ValueError(
                "Fit unsuccessful, provide better initial parameters (p0)")

        self.params = params
        self.errors = errors
        self.xdata = sp.array(xdata)
        self.ydata = sp.array(ydata)
        self.f = lambda x: f(x, *params)

    def __call__(self, x):
        return self.f(x)

    def curve(self, start=None, end=None, res=100, overrun=0):
        """
        Calculates the curve of the fit, used as line of theoretical function.

        Parameters
        ----------
        start : float, optional
            The lowest x value. If none, lowest of original x data is used.
        end : float, optional
            The highest x value. If none, highest of original x data is used.
        resolution : int
            Number of points used in between start and end (inclusive).
        overrun : float, (float, float)
            fraction of x interval to add before start and after end. 
            If tuple, the values are used for start and end separately.
        """
        if start is None:
            start = self.xdata.min()
        if end is None:
            end = self.xdata.max()

        interval_length = end - start

        try:
            start -= overrun[0] * interval_length
            end += overrun[1] * interval_length
        except TypeError:
            start -= overrun * interval_length
            end += overrun * interval_length

        xes = sp.linspace(start, end, res)
        ys = self(xes)

        return xes, ys


class Spline(UnivariateSpline):
    """
    Thin wrapper around the scipy's UnivariateSpline. Original data is saved in xdata, ydata.
    Curve function was added.
    If passed x array is not strictly increasing, raises a warning and monotonizes
    the data automaticaly.

    Parameters
    ----------
    x : Sequence like
        x data
    y : Sequence like
        y data
    and other params of UnivariateSpline.
    """

    def __init__(self, x, y, *args, **kwargs):
        try:
            UnivariateSpline.__init__(self, x, y, *args, **kwargs)
        except ValueError as e:
            if str(e) == "x must be strictly increasing":
                warnings.warn("Spline: ValueError catched, monotonizing!")

                mono_x, mono_y = self._monotonize(x, y)
                UnivariateSpline.__init__(
                    self, mono_x, mono_y, *args, **kwargs
                )
            else:
                raise e

        self.xdata = sp.array(x)
        self.ydata = sp.array(y)

    def curve(self, start=None, end=None, res=100, overrun=0):
        """
        Calculates the curve of the spline, used as line of theoretical function
        or a lead for an eye.

        Parameters
        ----------
        start : float, optional
            The lowest x value. If none, lowest of original x data is used.
        end : float, optional
            The highest x value. If none, highest of original x data is used.
        resolution : int
            Number of points used in between start and end (inclusive).
        overrun : float, (float, float)
            fraction of x interval to add before start and after end. If tuple,
            the values are used for start and end separately.
        """
        if start is None:
            start = self.xdata.min()
        if end is None:
            end = self.xdata.max()

        interval_length = end - start

        try:
            start -= overrun[0] * interval_length
            end += overrun[1] * interval_length
        except TypeError:
            start -= overrun * interval_length
            end += overrun * interval_length

        xes = sp.linspace(start, end, res)
        ys = self(xes)

        return xes, ys

    def _monotonize(self, xdata, ydata):
        """
        Helper function to make passed x and y value array strictly increasing.
        New in 0.1.2

        Parameters:
        -----------
        xdata : sequence
            X points
        ydata : sequence
            Y points

        Returns:
        --------
        new_x : numpy.ndarray
            monotonized X points
        new_y : numpy.ndarray
            monotonized Y points
        """
        highest = xdata[0] - 1
        new_x = []
        new_y = []

        for x, y in zip(xdata, ydata):
            if x > highest:
                new_x.append(x)
                new_y.append(y)
                highest = x

        return sp.array(new_x), sp.array(new_y)


def main():
    pass


if __name__ == '__main__':
    main()
