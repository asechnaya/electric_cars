import numpy as np
import matplotlib.pyplot as plt

from currencies import calculate_dependence


def create_graph(currency_1='gel', currency_2='rub'):
    x, y = calculate_dependence(currency_1)
    fig, ax = plt.subplots(figsize=(16, 16))
    x_ticks = np.arange(0, 25, 5)
    ax.set_xticks(x_ticks)
    plt.subplot(2, 1, 1)
    plt.tick_params(axis='x', direction='in')
    plt.grid(True)
    plt.plot(x, y, "r--")
    ymax = max(y)
    xpos = y.index(ymax)
    xmax = x[xpos]
    plt.annotate('max inflation', xy=(xmax, ymax), xytext=(xmax, ymax+.001*ymax))
    create_annotation(x, y, currency_1)
    plt.subplot(2, 1, 2)
    x1, y1 = calculate_dependence(currency_2)
    plt.bar(x1, y1, color='darkblue')
    create_annotation(x, y, currency_2)
    fig.tight_layout()
    plt.savefig('currencies.png')

    plt.show()


def create_annotation(x, y, currency):
    plt.title(f"USD/{currency} dependence")
    plt.ylabel(f"{currency} in one $")
    plt.xlabel("date")
    plt.xticks(rotation=45)

