from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

if __name__ == "__main__":

    # # print pandas Series of start date of wars and conflicts

    # war_counter = {0: 242, 1: 148, 2: 49, 3: 15, 4: 4}
    # print(war_counter)


    # fig, ax = plt.subplots()
    # keys = ['0', '1','2','3','4', ">= 5"]
    # counts = [242, 148, 49, 15, 4, 0]
    # bar_labels = ['0', '1','2','3','4',">= 5"]

    # ax.bar(keys, counts, label=bar_labels)

    # ax.set_xlabel("Aantal oorlogen en conflicten")
    # ax.set_ylabel("Frequentie")
    # ax.set_title("Aantal oorlogen en conflicten per jaar (1482 -1939)")
    
    # plt.savefig('plot_wars.pdf')

    x1 = np.random.poisson(lam=1, size=100000)
    x2 = np.random.poisson(lam=2, size=100000)
    x5 = np.random.poisson(lam=5, size=100000)
    x10 = np.random.poisson(lam=10, size=100000)

    c1 = Counter(x1)
    c2 = Counter(x2)
    c5 = Counter(x5)
    c10 = Counter(x10)
    
    fig, ax = plt.subplots(2,2)
    # keys = ['0', '1','2','3','4', ">= 5"]
    # counts = [242, 148, 49, 15, 4, 0]
    # bar_labels = ['0', '1','2','3','4',">= 5"]

    ax[0,0].bar(c1.keys(), [x / 100000 for x in c1.values()])
    ax[0,0].set_title("$\lambda = 1$")

    ax[0,1].bar(c2.keys(), [x / 100000 for x in c2.values()])
    ax[0,1].set_title("$\lambda = 2$")

    ax[1,0].bar(c5.keys(), [x / 100000 for x in c5.values()])
    ax[1,0].set_title("$\lambda = 5$")

    ax[1,1].bar(c10.keys(), [x / 100000 for x in c10.values()])
    ax[1,1].set_title("$\lambda = 10$")

    plt.tight_layout(pad=0.4, w_pad=2.5)
    # ax.set_xlabel("Aantal oorlogen en conflicten")
    # ax.set_ylabel("Frequentie")
    # ax.set_title("Aantal oorlogen en conflicten per jaar (1482 -1939)")
    
    plt.savefig('histograms_poissons.pdf')


