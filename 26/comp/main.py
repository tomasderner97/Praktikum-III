from labrep_utils import *

T_1 = 100e-9
T_2 = 5.44e-6
L = 1212


apertura = dataframe_from_csv("../data/apertura.csv")


def f_gaussian(x, a, b, c):
    return a * sp.exp(-(x - b)**2 / (2 * c**2))


def plot_apertura(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fx = sp.append(apertura["angle"][:-4], apertura["angle"][-2:])
    fy = sp.append(apertura["U"][:-4], apertura["U"][-2:])

    fit = FitCurve(f_gaussian, fx, fy)

    ax.plot(apertura["angle"], 0.141 / sp.exp(1)**2 * sp.ones(len(apertura)),
            ":", c="grey")
    ax.plot(*fit.curve(), "--", c="grey", label="Regrese")
    ax.plot(apertura["angle"], apertura["U"], "kx", label="Naměřené hodnoty")

    ax.set_xlabel(r"$\varphi [\si{\degree}]$")
    ax.set_ylabel(r"$U [\si{V}]$")
    ax.legend(loc="upper left")
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/apertura.pdf")


teploty = dataframe_from_csv("../data/teploty.csv")
teploty *= 1e-3


def plot_teploty(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    U_10deg = teploty[["I", "U_10deg"]].dropna()
    U_20deg = teploty[["I", "U_20deg"]].dropna()
    U_30deg = teploty[["I", "U_30deg"]].dropna()

    ax.plot(U_10deg["I"], U_10deg["U_10deg"], label=r"$ t = \SI{10}{\celsius} $")
    ax.plot(U_20deg["I"], U_20deg["U_20deg"], label=r"$ t = \SI{20}{\celsius} $")
    ax.plot(U_30deg["I"], U_30deg["U_30deg"], label=r"$ t = \SI{30}{\celsius} $")

    ax.set_xlabel(r"$I [\si{A}]$")
    ax.set_ylabel(r"$U [\si{V}]$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/teploty.pdf")
