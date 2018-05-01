from labrep_utils import *

roztok = dataframe_from_csv("../data/roztok.csv")


def plot_roztok(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_line, roztok["koncentrace"], roztok["n"])
    print(fit.params)
    print(fit.errors)

    ax.plot(*fit.curve(), "--", c="grey", label="fit")
    ax.plot(roztok["koncentrace"], roztok["n"], "kx", label="hodnoty")

    ax.set_xlabel(r"Objemová koncentrace $[\si{\percent}]$")
    ax.set_ylabel(r"$n$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/roztok.pdf")

# ----- U2 ----- #


koule = dataframe_from_csv("../data/koule.csv")
koule["uhel"] = koule["stupne"] + koule["minuty"] / 60

alpha_koule = {
    0: 34 + 37 / 60,
    180: 34 + 22 / 60,
    90: 34 + 20 / 60,
    270: 34 + 38 / 60,
    45: 34 + 32 / 60,
    225: 34 + 26 / 60
}

n_koule = 1 / sp.sin(arr(list(alpha_koule.values())).mean() * sp.pi / 180)

sklo1 = dataframe_from_csv("../data/sklo1.csv")
sklo2 = dataframe_from_csv("../data/sklo2.csv")
sklo3 = dataframe_from_csv("../data/sklo3.csv")

for sklo in [sklo1, sklo2, sklo3]:
    sklo["uhel"] = sklo["stupne"] + sklo["minuty"] / 60

# ----- DVOJLOM ----- #

dvojlom = dataframe_from_csv("../data/dvojlom.csv")

dvojlom["smer1"] = dvojlom["smer1_stupne"] + dvojlom["smer1_minuty"] / 60
dvojlom["smer2"] = dvojlom["smer2_stupne"] + dvojlom["smer2_minuty"] / 60

index_lomu = pd.DataFrame()

index_lomu["uhel"] = dvojlom["otoceni"][:9]
index_lomu["alpha_1"] = (dvojlom["smer1"][:9].values + dvojlom["smer1"][9:].values) / 2
index_lomu["alpha_2"] = (dvojlom["smer2"][:9].values + dvojlom["smer2"][9:].values) / 2

index_lomu["n1"] = n_koule * sp.sin(index_lomu["alpha_1"] * sp.pi / 180)
index_lomu["n2"] = n_koule * sp.sin(index_lomu["alpha_2"] * sp.pi / 180)


def plot_index_lomu(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.errorbar(index_lomu["uhel"],
                index_lomu["n1"],
                yerr=0.001,
                elinewidth=1,
                fmt="kx",
                label="$n_o$")
    ax.errorbar(index_lomu["uhel"],
                index_lomu["n2"],
                yerr=0.001,
                elinewidth=1,
                fmt="k+",
                ms=7.5,
                label="$n_e$")

    ax.set_xlabel(r"$\varphi [\si{\degree}]$")
    ax.set_ylabel(r"$n$")
    ax.legend(loc="upper center")
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/index_lomu.pdf")
