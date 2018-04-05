from labrep_utils import *

u2 = dataframe_from_csv("../data/u2.csv")


def f_u2_fit(x, a, b, c, d):
    return a * sp.cos(b * x + c)**2 + d


def plot_u2(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_u2_fit, u2["angle"], u2["intensity"], p0=(500, 3 / 200, 0, 500))

    ax.plot(*fit.curve(), c="grey", label=r"Fit funkcí $\cos^2 \psi$")
    ax.plot(u2["angle"], u2["intensity"], "k+", label="Naměřené hodnoty")

    ax.set_xlabel(r"$\psi$")
    ax.set_ylabel(r"$I$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/u2.pdf")

    return fit.params, fit.errors


u3 = dataframe_from_csv("../data/u3.csv")


def plot_u3_45deg(show=False, save=False):
    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_subplot(111, projection="polar")

    ax.plot(u3["angle"] / 180 * sp.pi, u3["45deg"], ":k", label="$\SI{45}{\degree}$")
    ax.plot(u3["angle"] / 180 * sp.pi, u3["15deg"], "--k", label="$\SI{15}{\degree}$")

    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/u3.pdf")
