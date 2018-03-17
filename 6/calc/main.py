from labrep_utils import *

VZD_STINITKA_OD_COCKY = 1
LAMBDA = 632.8e-9

kalibrace = dataframe_from_csv("../data/kalibrace_mikroskopu.txt")


def plot_kalibrace(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_line, kalibrace["mm"], kalibrace["dilky"])

    ax.plot(*fit.curve(), c="grey", label="Lineární regrese")
    ax.plot(kalibrace["mm"], kalibrace["dilky"],
            "k+", label="Naměřené hodnoty")

    ax.set_xlabel(r"Skutečná délka $[\si{mm}]$")
    ax.set_ylabel(r"Dílky stupnice mikroskopu")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/kalibrace.pdf")

    plt.close()
    return fit.params, fit.errors


fit_kalibrace_params, fit_kalibrace_errs = plot_kalibrace()
m_v_dilku = 1e-3 / fit_kalibrace_params[0]
kalibrace_chyba = fit_kalibrace_errs[0]


u1_mrizka_Dx = arr([])


# ----- MRIZKA ----- #


mrizka = dataframe_from_csv("../data/mrizka.txt")


def plot_mrizka(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(mrizka["position"], mrizka["intensity"],
            ".k", ms=1)

    ax.set_xlabel(r"x label")
    ax.set_ylabel(r"y label")
    # ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/mrizka.pdf")


def mrizka_konstanta_z_difrakce():
    peaky = arr([-25.782, -13.428, -1.329, 10.770, 22.869])
    vzdalenosti = sp.diff(peaky) * 1e-3
    vzd_prumer, vzd_chyba = mean_and_error(vzdalenosti)

    fi = vzd_prumer / VZD_STINITKA_OD_COCKY
    return LAMBDA / fi


# ----- TENKA STERBINA ----- #


sterbina_tenka = dataframe_from_csv("../data/sterbina_tenka.txt")


def plot_sterbina_tenka(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(sterbina_tenka["position"], sterbina_tenka["intensity"],
            ".k", ms=1)

    ax.set_xlabel(r"x label")
    ax.set_ylabel(r"y label")
    # ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/sterbina_tenka.pdf")


dvojs_blizke = dataframe_from_csv("../data/dvojs_blizke_maxima.txt")


def plot_dvojs_blizke(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(dvojs_blizke["position"], dvojs_blizke["intensity"],
            ".k", ms=1)

    ax.set_xlabel(r"x label")
    ax.set_ylabel(r"y label")
    # ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("")


# ----- ROZMERY ----- #

def mrizka_konstanta_z_mikroskopu():
    """vrací mřížkovou konstantu a chybu z měření rozměrů mikroskopem"""
    df = dataframe_from_csv("../data/mrizka_rozmer.txt")
    vzdalenost_dvou_vrypu = df["dilky"] - df["dilky"].shift(-1)
    vzdalenost_dvou_vrypu = vzdalenost_dvou_vrypu.dropna().values
    vzd_v_metrech = vzdalenost_dvou_vrypu * m_v_dilku
    return mean_and_error(vzd_v_metrech)
