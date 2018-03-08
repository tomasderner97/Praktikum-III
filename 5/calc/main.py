from labrep_utils import *

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

    ax.plot(red["U_F"], red["I_F"], "k+", ms=3)

    if show:
        plt.show()
    if save:
        plt.savefig("../plot/red.pdf")


def plot_blue_VA_char(show=False, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(blue["U_F"], blue["I_F"], "kx")

    if show:
        plt.show()
    if save:
        plt.savefig("../plot/blue.pdf")
