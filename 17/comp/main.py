from labrep_utils import *

u1 = dataframe_from_csv("../data/u1.csv")


def plot_u1_l450(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_exp_simple, u1["n"], u1["l450"], p0=(1, -1))

    print(fit.params)
    print(fit.errors)

    ax.plot(*fit.curve(), c="grey", label="Exponenciální fit")
    ax.plot(u1["n"], u1["l450"], "kx", label="Naměřené hodnoty")

    ax.set_xlabel(r"Počet skleněných destiček")
    ax.set_ylabel(r"$\theta_i [1]$")
    ax.set_xticks(u1["n"])
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/u1_l450.pdf")


def plot_u1_l520(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_exp_simple, u1["n"], u1["l520"], p0=(1, -1))
    print(fit.params)
    print(fit.errors)

    ax.plot(*fit.curve(), c="grey", label="Exponenciální fit")
    ax.plot(u1["n"], u1["l520"], "kx", label="Naměřené hodnoty")

    ax.set_xlabel(r"Počet skleněných destiček")
    ax.set_ylabel(r"$\theta_i [1]$")
    ax.set_xticks(u1["n"])
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/u1_l520.pdf")


def plot_u1_l600(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_exp_simple, u1["n"], u1["l600"], p0=(1, -1))

    print(fit.params)
    print(fit.errors)

    ax.plot(*fit.curve(), c="grey", label="Exponenciální fit")
    ax.plot(u1["n"], u1["l600"], "kx", label="Naměřené hodnoty")

    ax.set_xlabel(r"Počet skleněných destiček")
    ax.set_ylabel(r"$\theta_i [1]$")
    ax.set_xticks(u1["n"])
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/u1_l600.pdf")


u2 = dataframe_from_csv("../data/u2.csv")


def plot_u2(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(u2["lambda"], u2["cervene"], c="red", label="Světle červené sklo")
    ax.plot(u2["lambda"], u2["tm_cervene"], c="darkred", label="Tmavě červené sklo")
    ax.plot(u2["lambda"], u2["modre"], c="dodgerblue", label="Modré sklo")
    ax.plot(u2["lambda"], u2["zelene"], c="green", label="Zelené sklo")
    ax.plot(u2["lambda"], u2["zlute"], c="gold", label="Žluté sklo")

    ax.set_xlabel(r"$\lambda [\si{nm}]$")
    ax.set_ylabel(r"$A [1]$")

    ax.set_xlim(380, 950)
    ax.set_ylim(top=3)
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/u2.pdf")


def comp_R(n):
    return (n - 1)**2 / (n + 1)**2
