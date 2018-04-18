from labrep_utils import *

A = uf(1.659, 0.003) * 1e-6

rtut_minuty = dataframe_from_csv("../data/rtut.csv")
rtut = pd.DataFrame()
rtut["vlevo"] = rtut_minuty["vlevo_stupne"] + rtut_minuty["vlevo_minuty"] / 60
rtut["vpravo"] = rtut_minuty["vpravo_stupne"] + rtut_minuty["vpravo_minuty"] / 60
rtut["vpravo"] -= 360

rtut["phi"] = rtut["vlevo"] - rtut["vpravo"]
rtut["phi"] /= 2


def vlnova_delka(fi):
    result = A * umath.sin(fi * sp.pi / 180)
    return result.n, result.s


rtut["lambda"], rtut["s_lambda"] = sp.vectorize(vlnova_delka)(rtut["phi"])


def plot_kalibrace(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fit = FitCurve(f_line, rtut["phi"], rtut["lambda"] * 1e9)

    print(fit.params, fit.errors)

    ax.plot(*fit.curve(), ":", c="grey", label="regrese")
    ax.plot(rtut["phi"], rtut["lambda"] * 1e9, "kx", label="hodnoty")

    ax.set_xlabel(r"$\varphi [\si{\degree}]$")
    ax.set_ylabel(r"$\lambda [\si{\nano\metre}]$")
    ax.legend()
    fig.tight_layout()

    if show:
        plt.show()
    if save:
        fig.savefig("../plot/kalibrace.pdf")
