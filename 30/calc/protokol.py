VERSION = "0.1.0"

import scipy as sp
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import UnivariateSpline as USpline
from scipy import array as arr

import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import uncertainties
from uncertainties import ufloat as uf
import uncertainties.umath as um
from uncertainties import unumpy
from uncertainties.unumpy import nominal_values as noms
from uncertainties.unumpy import std_devs as stds

from tabulate import tabulate

plt.rcParams["figure.figsize"] = (4*1.5,2.5*1.5)
plt.rcParams["figure.dpi"] = 100
plt.rcParams["text.usetex"] = True
plt.rcParams['text.latex.unicode'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern"]
plt.rcParams["text.latex.preamble"] = r"""
\usepackage[decimalsymbol=comma]{siunitx}
"""

def table_print(table, header=True, tablefmt="simple", **kwargs):
    if (header):
        print(tabulate(table, headers="keys", tablefmt=tablefmt, **kwargs))
    else:
        print(tabulate(table, tablefmt=tablefmt, **kwargs))

def relative(self):
    return self.s / self.n

uncertainties.core.Variable.rel = relative

def eval_mean(values, syst_err=0, scale=1):
    """
    Calculates the mean of the values provided and the standard deviation of said mean. 
    Optional systematic error is considered in the result.

    Parameters
    ----------
    values : array like
        Values for evaluation
    syst_err : float, optional
        Optional systematic error, it's square root is added to the square root of the mean's standard deviation.
    scale : float, optional
        Optional factor, by which the values should be multiplied. Used for unit conversion.

    Returns
    -------
    result : ufloat Variable
    """
    vals_arr = arr(values) * scale
    scaled_syst_err = syst_err * scale
    mean = vals_arr.mean()
    std_err = vals_arr.std(ddof=1)
    std_of_mean = std_err / sp.sqrt(len(vals_arr))

    complete_err = sp.sqrt(scaled_syst_err**2 + std_of_mean**2)

    return uf(mean, complete_err)

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

        if len(sp.where(cov==sp.inf)[0]) > 0:
            raise ValueError("Fit unsuccessful, provide better initial parameters (p0)")
        self.params = [uf(param, err) for param, err in zip(params, errors)]
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
            fraction of x interval to add before start and after end. If tuple, the values are used for start and end separately.
        """
        if start == None:
            start = self.xdata.min()
        if end == None:
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

    Parameters
    ----------
    x : Sequence like
        x data
    y : Sequence like
        y data
    and other params of UnivariateSpline.
    """

    def __init__(self, x, y, *args, **kwargs):
        UnivariateSpline.__init__(self, x, y, *args, **kwargs)

        self.xdata = sp.array(x)
        self.ydata = sp.array(y)

    def curve(self, start=None, end=None, res=100, overrun=0):
        """
        Calculates the curve of the spline, used as line of theoretical function or a lead for an eye.

        Parameters
        ----------
        start : float, optional
            The lowest x value. If none, lowest of original x data is used.
        end : float, optional
            The highest x value. If none, highest of original x data is used.
        resolution : int
            Number of points used in between start and end (inclusive).
        overrun : float, (float, float)
            fraction of x interval to add before start and after end. If tuple, the values are used for start and end separately.
        """
        if start == None:
            start = self.xdata.min()
        if end == None:
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


def round_uncert(value):
    return (0,0)
    

def split_df_uncert(df):
    new = pd.DataFrame()
    
    for col in list(df.columns):
        err = stds(df[col])
        if sp.count_nonzero(err) > 0: 
            nom_list = []
            std_list = []
            for v in df[col]:
                nom_val, std_val = round_uncert(v)
                nom_list.append(nom_val)
                std_list.append(std_val)
            new[col] = nom_list
            new[f"s_{col}"] = std_list
        else:
            new[col] = df[col]
    
    return new
        

def latex_table(df):
    ready_df = split_df_uncert(df)


def main():
    x = [1,2,3,4,5]
    y = [8,2,6,4,7]

    spl = Spline(x,y)
    spl.set_smoothing_factor(0.1)

    plt.plot(*spl.curve())
    plt.plot(x, y)

    plt.show()


if __name__ == '__main__':
    main()
