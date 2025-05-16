import functools

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

# Setting up a random number generator with a fixed state for reproducibility.
rng = np.random.default_rng(seed=19680801)
# Fixing bin edges.
HIST_BINS = np.linspace(-1, 100, 102)
sample_size = 100_000

# Histogram our data with numpy.
data = rng.poisson(1, sample_size)
n, _ = np.histogram(data, HIST_BINS)

def animate(frame_number, bar_container):
    # Simulate new data coming in.
    data = rng.poisson(frame_number + 1, sample_size)
    n, _ = np.histogram(data, HIST_BINS)
    ax.set_title("Kansverdeling voor $X \sim$ Poisson$(\lambda$ = %d)" % (frame_number+1))
    # ax.set_ylim(0, 1.5 / (.6*frame_number + 1))
    max_height = 0
    for count, rect in zip(n, bar_container.patches):
        rect.set_height(count / sample_size)
        max_height = max(max_height, count / sample_size)

    ax.set_ylim(top=1.1*max_height)
    return bar_container.patches

# Output generated via `matplotlib.animation.Animation.to_jshtml`.
fig, ax = plt.subplots()
_, _, bar_container = ax.hist(data, HIST_BINS, lw=1,
                              ec="yellow", fc="green", alpha=0.5)
# ax.set_ylim(top=.5)  # set safe limit to ensure that all data is visible.
# ax.set_title("Poissonverdeling voor verschillende $\lambda$")
ax.set_xlabel("Aantal successen $k$")
ax.set_ylabel("Kans $\mathbb{P}(X = k)$")
anim = functools.partial(animate, bar_container=bar_container)
ani = animation.FuncAnimation(fig, anim, interval=500, frames=50)

plt.show()
