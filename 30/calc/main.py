from protokol import *

LAMBDA = (588.9950 + 589.5924) / 2 * 1e-9

# ----- ÚKOL 1 ----- #

vrstva1 = dataframe_from_csv("../data/vrstva1.csv", index_col=0)
vrstva2 = dataframe_from_csv("../data/vrstva2.csv", index_col=0)


def add_x1_x2(df):
    df["x1"] = df["v"] - df["mv"]
    df["x2"] = df["mv"] - df["mv"].shift(-1)


add_x1_x2(vrstva1)
add_x1_x2(vrstva2)


def mean_error(arr):
    mean = arr.mean()
    std = arr.std(ddof=1)
    meandev = std / len(arr)
    error = (meandev**2 + 0.1**2)**(1 / 2)
    return mean, error


v1_x1_mean, v1_x1_error = mean_error(vrstva1["x1"])
v1_x2_mean, v1_x2_error = mean_error(vrstva1["x2"].dropna())
v2_x1_mean, v2_x1_error = mean_error(vrstva2["x1"])
v2_x2_mean, v2_x2_error = mean_error(vrstva2["x2"].dropna())

from uncertainties import ufloat as uf
t1 = (
    uf(v1_x1_mean, v1_x1_error) / uf(v1_x2_mean, v1_x2_error)
) * (
    LAMBDA / 2
)
t2 = (
    uf(v2_x1_mean, v2_x1_error) / uf(v2_x2_mean, v2_x2_error)
) * (
    LAMBDA / 2
)

# ----- ÚKOL 2 ----- #

newton = dataframe_from_csv("../data/newton.csv")
newton = newton * 1e-6


def plot_newton(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit_A1 = FitCurve(
        f_line,
        newton.index + 1,
        newton["bn4"]**2 / LAMBDA
    )

    ax.plot(*fit_A1.curve(), c="grey")
    ax.plot(fit_A1.xdata, fit_A1.ydata, "kx", label="A1")

    print(fit_A1.params)
    print(fit_A1.errors)

    if show:
        plt.show()

    if save:
        fig.savefig("../plot/vrstva1.pdf")

# ----- ÚKOL 3 ----- #


kalibrace = dataframe_from_csv("../data/kalibrace.csv", header=None)


def plot_kalibrace():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_line, (kalibrace.index + 1) * 100, kalibrace[0])
    print(fit.params[0], fit.errors[0])
    ax.plot((kalibrace.index + 1) * 100, kalibrace[0])
    ax.set_xlabel("Skutečná hodnota $[\si{\micro\metre}]$")
    ax.set_ylabel("Hodnota zobrazená počítačem $[\si{\micro\metre}]$")
    plt.tight_layout()
    plt.savefig("../plot/kalibrace.pdf")
    # plt.show()
