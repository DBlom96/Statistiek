import functools

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

# Setting up a random number generator with a fixed state for reproducibility.
rng = np.random.default_rng(seed=19680801)
# Fixing bin edges.
HIST_BINS = np.linspace(-1, 20, 22)
sample_size = 100_000

# Histogram our Poisson data with numpy.
poisson_data = rng.poisson(2.5, sample_size)
npoisson, _ = np.histogram(poisson_data, HIST_BINS)

# Do the same for the binomial approximations
n_start = 3
binom_data = rng.binomial(n_start, 2.5 / n_start, sample_size)
nbinom, _ = np.histogram(binom_data, HIST_BINS)

def animate(frame_number, bar_container):
    # Simulate new data coming in.
    n_exp = frame_number + n_start
    binom_data = rng.binomial(n_exp, 2.5 / n_exp, sample_size)
    nbinom, _ = np.histogram(binom_data, HIST_BINS)
    ax[1].set_title(r"Kansverdeling voor $X \sim$ Binomial(%d, $\frac{2.5}{%d}$)" % (n_exp, n_exp))
    max_height = 0
    for count, rect in zip(nbinom, bar_container.patches):
        rect.set_height(count / sample_size)
        max_height = max(max_height, count / sample_size)

    ax[1].set_ylim(top=0.27) # 1.1*max_height)
    return bar_container.patches

# Output generated via `matplotlib.animation.Animation.to_jshtml`.
fig, ax = plt.subplots(1, 2)
_, _, poisson_bar_container = ax[0].hist(poisson_data, HIST_BINS, align='left', lw=1,
                              ec="yellow", fc="green", alpha=0.5, density=True)
_, _, bar_container = ax[1].hist(binom_data, HIST_BINS, align='left', lw=1,
                              ec="yellow", fc="red", alpha=0.5)
# ax.set_ylim(top=.5)  # set safe limit to ensure that all data is visible.
# ax.set_title("Poissonverdeling voor verschillende $\lambda$")

ax[0].set_title("Kansverdeling voor $X \sim$ Poisson(2.5)")
ax[0].set_xlabel("Aantal events $k$")
ax[0].set_ylabel("Kans $\mathbb{P}(X = k)$")
ax[1].set_xlabel("Aantal successen $k$")
ax[1].set_ylabel("Kans $\mathbb{P}(X = k)$")

anim = functools.partial(animate, bar_container=bar_container)
ani = animation.FuncAnimation(fig, anim, interval=500, frames=50)

plt.tight_layout()
plt.show()
