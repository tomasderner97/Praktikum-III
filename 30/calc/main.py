from protokol import *

LAMBDA = (588.9950 + 589.5924) / 2 * 1e-9
N_SKLA = 1.523

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

    # ---
    fit_A2 = FitCurve(
        f_line,
        newton.index + 1,
        newton["sn4"]**2 / LAMBDA
    )

    ax.plot(*fit_A2.curve(), ":", c="grey")
    ax.plot(fit_A2.xdata, fit_A2.ydata, "k+", label="A2")

    print(fit_A2.params)
    print(fit_A2.errors)

    # ---
    fit_B1 = FitCurve(
        f_line,
        newton.index + 1,
        newton["sn3"]**2 / LAMBDA
    )

    ax.plot(*fit_B1.curve(), "--", c="grey")
    ax.plot(fit_B1.xdata, fit_B1.ydata, "ko", label="B1")

    print(fit_B1.params)
    print(fit_B1.errors)

    # ---
    fit_B2 = FitCurve(
        f_line,
        newton.index + 1,
        newton["bn3"]**2 / LAMBDA
    )

    ax.plot(*fit_B2.curve(), "-.", c="grey")
    ax.plot(fit_B2.xdata, fit_B2.ydata, "k^", label="B2")

    print(fit_B2.params)
    print(fit_B2.errors)

    # ---

    ax.set_xlabel(r"$k[1]$")
    ax.set_ylabel(r"$\frac{\rho_k^2}{\lambda} [\si{m}]$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()

    if save:
        fig.savefig("../plot/newton.pdf")

# ----- ÚKOL 3 ----- #


kalibrace = dataframe_from_csv("../data/kalibrace.csv", header=None)


def plot_kalibrace():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_line, (kalibrace.index + 1) * 100, kalibrace[0])
    print(fit.params[0], fit.errors[0])
    ax.plot((kalibrace.index + 1) * 100, kalibrace[0], "-+k")
    ax.set_xlabel("Skutečná hodnota $[\si{\micro\metre}]$")
    ax.set_ylabel("Hodnota zobrazená počítačem $[\si{\micro\metre}]$")
    plt.tight_layout()
    plt.savefig("../plot/kalibrace.pdf")
    # plt.show()

# ----- ÚKOL 4 ----- #


def mohutnost(r1, r2):
    return (N_SKLA - 1) * (1 / r1 + 1 / r2)


r_1a = uf(0.073, 0.001)
r_1b = uf(0.079, 0.001)
r_2a = uf(0.097, 0.001)
r_2b = uf(0.048, 0.001)

moh_a = mohutnost(r_1a, r_1b)
moh_b = mohutnost(r_2a, r_2b)
