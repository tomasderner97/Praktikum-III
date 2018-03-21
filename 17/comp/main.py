from labrep_utils import *

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
