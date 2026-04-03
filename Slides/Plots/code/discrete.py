import numpy as np
from scipy.stats import binom, poisson
from .base import KansverdelingPlotter  # Importeer de basis plotter

# Subklasse voor discrete kansverdelingen
class DiscreteKansverdelingPlotter(KansverdelingPlotter):
    def __init__(self, title="Discrete kansverdeling", xlabel=r"$x$", ylabel=r"Kansfunctie $f(x)$", **kwargs):
        super().__init__(title, xlabel, ylabel, **kwargs)
    
    def highlight_interval(self, left, right):
        if left is None:
            left = self.x[0]
        if right is None:
            right = self.x[-1]
        
        # Selecteer de waarden die binnen het interval liggen
        inside_indices = (self.x >= left) & (self.x <= right)
        x_normal = self.x[~inside_indices]
        y_normal = self.y[~inside_indices]
        
        x_highlight = self.x[inside_indices]
        y_highlight = self.y[inside_indices]
        
        self.ax.stem(x_normal, y_normal, linefmt='blue' , markerfmt='bo', basefmt=" ")
        self.ax.stem(x_highlight, y_highlight, linefmt='red' , markerfmt='ro', basefmt=" ")
        
    def plot_pmf(self, left=None, right=None):
        """Maak de stem plot (probability measure function)."""       
        self.y = self.dist.pmf(self.x, **self.params)
        self.highlight_interval(left=left, right=right)

# Specifieke klasse voor Binomiale verdeling
class BinomialeVerdelingPlotter(DiscreteKansverdelingPlotter):
    def __init__(self, n=100, p=0.5, xlabel=r"$k$", ylabel=r"Kans $f(k)$", **kwargs):
        title=f'Binomiale Verdeling ($n={n}$, $p={p}$)' 
        super().__init__(title, xlabel, ylabel, **kwargs)
        self.n = n
        self.p = p
        self.params = {'n': self.n, 'p': self.p}
        self.x = np.arange(0, self.n + 1)
        self.dist_type = 'binomial_distribution'
        self.label = f'Binomiaal(n={self.n}, p={self.p})'
        self.dist = binom

# Specifieke klasse voor Poisson verdeling
class PoissonVerdelingPlotter(DiscreteKansverdelingPlotter):
    def __init__(self, mu=1, xlabel=r"$k$", ylabel=r"Kans $f(k)$", **kwargs):
        title = f'Poissonverdeling ($\mu={mu}$)'
        super().__init__(title, xlabel, ylabel, **kwargs)
        self.mu = mu
        self.params = {'mu': mu}
        self.x = np.arange(0, self.mu + 3 * np.sqrt(self.mu) + 1)
        self.dist_type = 'poisson_distribution'
        self.label = f'Poisson($\mu={self.mu}$)'
        self.dist = poisson