from labrep_utils import *
from uncertainties import ufloat as uf


E = 1.602e-19
K = 1.381e-23
T = 25 + 273.15


red_dic = {
    "name": "lq1131",
    "resistance": 400
}

blue_dic = {
    "name": "560lb7d",
    "resistance": 330
}

red = dataframe_from_csv("../data/red.csv")
blue = dataframe_from_csv("../data/blue.csv")


def add_voltage_on_diode(df, dic):
    # napětí na diodě = napětí na zdroji - odpor * proud dekádou
    df["U_F"] = df["U_F_zdroj"] - dic["resistance"] * df["I_F"]


add_voltage_on_diode(red, red_dic)
add_voltage_on_diode(blue, blue_dic)


def plot_red_VA_char(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    lin_start = 27
    lin_stop = -12
    fit = FitCurve(
        f_line,
        red["U_F"][lin_start:lin_stop],
        red["I_F"][lin_start:lin_stop]
    )

    ax.plot(red["U_F"], red["I_F"], "k+", ms=3,
            label=r"VA chatakteristika \textbf{LQ1131}")
    ax.plot(*fit.curve(overrun=(0.2, 0.3)), c="grey",
            label="regrese lineárního průběhu")

    ax.set_xlabel(r"$U_F [\si{V}]$")
    ax.set_ylabel(r"$I_F [\si{A}]$")

    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        plt.savefig("../plot/red.pdf")

    return fit.params, fit.errors


param_red_VA, err_red_VA = plot_red_VA_char()
R_d_red = 1 / uf(param_red_VA[0], err_red_VA[0])
U_star_red = uf(param_red_VA[1], err_red_VA[1]) / \
    uf(param_red_VA[0], err_red_VA[0])


def plot_blue_VA_char(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    lin_start = 60
    fit = FitCurve(
        f_line,
        blue["U_F"][lin_start:],
        blue["I_F"][lin_start:]
    )

    ax.plot(blue["U_F"], blue["I_F"], "k+", ms=3,
            label=r"VA chatakteristika \textbf{560LB7D}")
    ax.plot(*fit.curve(overrun=(0.8, 0.05)), c="grey",
            label="regrese lineárního průběhu")

    ax.set_xlabel(r"$U_F [\si{V}]$")
    ax.set_ylabel(r"$I_F [\si{A}]$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        plt.savefig("../plot/blue.pdf")

    return fit.params, fit.errors


param_blue_VA, err_blue_VA = plot_blue_VA_char()
R_d_blue = 1 / uf(param_blue_VA[0], err_blue_VA[0])
U_star_blue = uf(param_blue_VA[1], err_blue_VA[1]) / \
    uf(param_blue_VA[0], err_blue_VA[0])


def plot_red_svet_char(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(red["I_F"], red["I_phi"], "k+", ms=3,
            label=r"Světelná charakteristika \textbf{LQ1131}")

    ax.set_xlabel(r"$I_F [\si{A}]$")
    ax.set_ylabel(r"$I_\Phi [\si{A}]$")
    ax.ticklabel_format(style="sci", axis="y", scilimits=(-2, 2))
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        plt.savefig("../plot/red_svet.pdf")


def plot_blue_svet_char(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(blue["I_F"], blue["I_phi"], "k+", ms=3,
            label=r"Světelná charakteristika \textbf{560LB7D}")

    ax.set_xlabel(r"$I_F [\si{A}]$")
    ax.set_ylabel(r"$I_\Phi [\si{A}]$")
    ax.ticklabel_format(style="sci", axis="y", scilimits=(-2, 2))
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        plt.savefig("../plot/blue_svet.pdf")


def plot_red_log(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    new_red = red.loc[red["I_F"] > 0]

    lin_start = 5
    lin_stop = 16

    fit = FitCurve(
        f_line,
        new_red["U_F"][lin_start:lin_stop],
        sp.log(new_red["I_F"])[lin_start:lin_stop]
    )

    ax.plot(new_red["U_F"], sp.log(new_red["I_F"]), "k+",
            ms=4, label=r"hodnoty pro \textbf{LQ1131}")
    ax.plot(*fit.curve(overrun=(0.2, 0.22)),
            c="grey", label="Regrese lineární části")

    ax.set_xlabel(r"$U_F [\si{V}]$")
    ax.set_ylabel(r"$\log I_F$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/red_log.pdf")

    return fit.params, fit.errors


param_red_log, err_red_log = plot_red_log()
n_red = 1 / uf(param_red_log[0], err_red_log[0])
R_di_red = R_d_red * n_red / 1.795


def plot_blue_log(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    new_blue = blue.loc[blue["I_F"] > 0]

    lin_start = 15
    lin_stop = 27

    fit = FitCurve(
        f_line,
        new_blue["U_F"][lin_start:lin_stop],
        sp.log(new_blue["I_F"])[lin_start:lin_stop]
    )

    ax.plot(new_blue["U_F"], sp.log(new_blue["I_F"]), "k+",
            ms=4, label=r"hodnoty pro \textbf{560LB7D}")
    ax.plot(*fit.curve(overrun=(0.1, 0.2)),
            c="grey", label="Regrese lineární části")

    ax.set_xlabel(r"$U_F [\si{V}]$")
    ax.set_ylabel(r"$\log I_F$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/blue_log.pdf")

    return fit.params, fit.errors


param_blue_log, err_blue_log = plot_blue_log()
n_blue = 1 / uf(param_blue_log[0], err_blue_log[0])
R_di_blue = R_d_blue * n_blue / 3.104


ft1 = dataframe_from_csv("../data/ft_0.1mA.csv")
ft2 = dataframe_from_csv("../data/ft_0.2mA.csv")
ft3 = dataframe_from_csv("../data/ft_0.3mA.csv")


def plot_fototranzistor(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(ft1["U"], ft1["I"], "k+", ms=4, label=r"$I_F = \SI{0.1}{mA}$")
    ax.plot(ft2["U"], ft2["I"], "kx", ms=3, label=r"$I_F = \SI{0.2}{mA}$")
    ax.plot(ft3["U"], ft3["I"], "k.", ms=4, label=r"$I_F = \SI{0.3}{mA}$")

    ax.set_xlabel(r"$U_{CE} [\si{V}]$")
    ax.set_ylabel(r"$I_{C0} [\si{A}]$")
    ax.legend(loc="center right", bbox_to_anchor=(0.98, 0.66))
    ax.ticklabel_format(style="sci", scilimits=(-2, 2))
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/fototr.pdf")
