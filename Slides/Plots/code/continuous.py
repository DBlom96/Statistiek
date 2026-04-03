import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, t, chi2
from .base import KansverdelingPlotter  # Importeer de basis plotter

# Subklasse voor continue kansverdelingen
class ContinueKansverdelingPlotter(KansverdelingPlotter):
    def __init__(self, title="Continue kansverdeling", xlabel=r"$x$", ylabel=r"Kansdichtheid $f(x)$", **kwargs):
        super().__init__(title, xlabel, ylabel, **kwargs)       
    
    def highlight_interval(self, y=None, left=None, right=None, color="red", alpha=0.3, **kwargs):
        """Arceer de oppervlakte onder de curve tussen x=a en x=b."""
        if left is None:
            left = self.x[0]
        if right is None:
            right = self.x[-1]
        
        # Selecteer de waarden die binnen het interval liggen
        mask = (self.x >= left) & (self.x <= right)
        if y is not None:
            self.ax.fill_between(self.x, y, where=mask, color=color, alpha=alpha)
        else:
            self.ax.fill_between(self.x, self.y, where=mask, color=color, alpha=alpha, **kwargs)
            
    def plot_pdf(self, left=None, right=None, **kwargs):
        self.y = self.dist.pdf(self.x, **self.params)
        self.ax.plot(self.x, self.y)# , label=self.label)
    
    def plot_cdf(self, **kwargs):
        self.y = self.dist.cdf(self.x, **self.params)
        self.ax.plot(self.x, self.y)#, label=self.label)
                
# Specifieke klasse voor Normale verdeling
class NormaleVerdelingPlotter(ContinueKansverdelingPlotter):
    def __init__(self, mu=0, sigma=1, xlabel=r"$x$", ylabel=r"Kansdichtheid $f(x)$", **kwargs):
        title=f'Normale Verdeling ($\mu={mu}$, $\sigma={sigma}$)'
        super().__init__(title, xlabel, ylabel, **kwargs)
        self.mu = mu
        self.sigma = sigma
        self.params = {'loc': self.mu, 'scale': self.sigma}
        self.x = np.linspace(self.mu - 4*self.sigma, self.mu + 4 * self.sigma, self.num_xsteps)
        self.dist_type = 'normal_distribution'
        self.label = f'Normaal($\mu={self.mu}$, $\sigma={self.sigma}$)'
        self.dist = norm
    
    def compute_z_confidence_interval(self, hyp_type="tweezijdig", confidence=0.05):
        assert hyp_type in ["tweezijdig", "linkszijdig", "rechtszijdig"]
        if hyp_type == "tweezijdig":
            acceptable_left = self.dist.ppf(confidence / 2, **self.params)
            acceptable_right = self.dist.ppf(1 - confidence / 2, **self.params)
        elif hyp_type == "linkszijdig":
            acceptable_left = self.x[0]
            acceptable_right = self.dist.ppf(1 - confidence, **self.params)
        else:
            acceptable_left = self.dist.ppf(confidence, **self.params)
            acceptable_right = self.x[-1]
        return acceptable_left, acceptable_right
    
    def shade_regions(self, boundaries, ypos=-0.01, opacity=0.3):
        self.highlight_interval(left=boundaries[0], right=boundaries[1], color="red", alpha=opacity)
        self.highlight_interval(left=boundaries[1], right=boundaries[2], color="green", alpha=opacity)
        self.highlight_interval(left=boundaries[2], right=boundaries[3], color="red", alpha=opacity)

    def draw_critical_and_acceptable_regions(self, boundaries, ypos=-0.01):
        if boundaries[0] != boundaries[1]:
            self.ax.hlines(y=ypos, xmin=boundaries[0], xmax=boundaries[1], color='red', linewidth=5)
            self.ax.text((boundaries[0]+boundaries[1])/2, 2 * ypos, r"Verwerp $H_0$", color='red', fontsize=12, ha="center")

        self.ax.hlines(y=ypos, xmin=boundaries[1], xmax=boundaries[2], color='green', linewidth=5, label=r"Accepteer $H_0$")
        self.ax.text((boundaries[1]+boundaries[2])/2, 2 * ypos, f"Accepteer $H_0$", color='green', fontsize=12, ha="center")
        
        if boundaries[2] != boundaries[3]:
            self.ax.hlines(y=ypos, xmin=boundaries[2], xmax=boundaries[3], color='red', linewidth=5, label=r"Verwerp $H_0$")   
            self.ax.text((boundaries[2]+boundaries[3])/2, 2 * ypos, r"Verwerp $H_0$", color='red', fontsize=12, ha="center")
    
    def annotate_critical_region(self, boundaries, hyp_type="tweezijdig", ypos=-0.01, confidence=0.05):
        # Annotate critical region
        if hyp_type == "tweezijdig":
            self.ax.text((boundaries[0]+boundaries[1])/2, -2 * ypos, f"$\\alpha / 2 = {confidence / 2}$", color='red', fontsize=12, ha="center")
            self.ax.text((boundaries[2]+boundaries[3])/2, -2 * ypos, f"$\\alpha / 2 = {confidence / 2}$", color='red', fontsize=12, ha="center")
                       
        elif hyp_type == "linkszijdig":
            self.ax.text((boundaries[2]+boundaries[3])/2, -2 * ypos, f"$\\alpha={confidence}$", color='red', fontsize=12, ha="center")
        else:
            self.ax.text((boundaries[0]+boundaries[1])/2, -2 * ypos, f"$\\alpha={confidence}$", color='red', fontsize=12, ha="center")
        
    def make_z_confidence_interval(self, hyp_type="tweezijdig", confidence=0.05):
        assert hyp_type in ["tweezijdig", "linkszijdig", "rechtszijdig"]
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        # First: draw the normal curve under the null hypothesis and shade the critical region given the confidence level
        i = 0
        self.plot_pdf(color=color_cycle[i])
        
        if isinstance(self.mu, int):
            text = f"$\\mu = {int(self.mu)}$"
        else:
            text = f"$\\mu = {self.mu:.3f}$"
        
        self.add_vertical_line(xval=self.mu, text=text, color=color_cycle[i])
        
        # Shade the acceptable and critical region, and draw horizontal lines indicating the intervals       
        acceptable_left, acceptable_right = self.compute_z_confidence_interval(hyp_type=hyp_type, confidence=confidence)
        ypos = -0.01
        boundaries = [self.x[0], acceptable_left, acceptable_right, self.x[-1]]
        self.shade_regions(boundaries, ypos=ypos)
        self.draw_critical_and_acceptable_regions(boundaries, ypos=ypos)
        self.annotate_critical_region(boundaries, hyp_type=hyp_type, ypos=ypos, confidence=confidence)
                             
        # Removes x-axis for better visibility
        plt.xticks([])
        self.ax.set_ylim(bottom = 3 * ypos)
                       
    def make_hypothesis_plot(self, mu1=1, hyp_type="tweezijdig", confidence=0.05):       
        assert hyp_type in ["tweezijdig", "linkszijdig", "rechtszijdig"]
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        # First: draw the normal curve under the null hypothesis and shade the critical region given the confidence level
        i = 0
        self.plot_pdf(color=color_cycle[i])
        
        if isinstance(self.mu, int):
            text = f"$\\mu_0 = {int(self.mu)}$"
        else:
            text = f"$\\mu_0 = {self.mu:.3f}$"
        
        self.add_vertical_line(xval=self.mu, text=text, color=color_cycle[i])
        
        # Shade the acceptable and critical region, and draw horizontal lines indicating the intervals       
        acceptable_left, acceptable_right = self.compute_z_confidence_interval(hyp_type=hyp_type, confidence=confidence)
        ypos = -0.01
        boundaries = [self.x[0], acceptable_left, acceptable_right, self.x[-1]]
        self.draw_critical_and_acceptable_regions(boundaries, ypos=ypos)
        
        i += 1
        alternative_x = self.x + (mu1 - self.mu)
        alternative_y = self.dist.pdf(alternative_x, mu1, self.sigma)
        
        self.ax.plot(alternative_x, alternative_y)
        self.ax.fill_between(alternative_x, alternative_y, where=((alternative_x >= acceptable_left)&(alternative_x <= acceptable_right)), color=color_cycle[i], alpha=0.3)
                
        if isinstance(mu1, int):
            text = f"$\\mu_1 = {int(mu1)}$"
        else:
            text = f"$\\mu_1 = {mu1:.3f}$"
        
        self.add_vertical_line(xval=mu1, yval=self.dist.pdf(mu1, mu1, self.sigma), text=text, color=color_cycle[i])
        
        
        # Removes x-axis for better visibility
        plt.xticks([])
        self.ax.set_ylim(bottom = 3 * ypos)
        
# Specifieke klasse voor Exponentiele verdeling
class ExponentieleVerdelingPlotter(ContinueKansverdelingPlotter):
    def __init__(self, lam=1, xlabel=r"$x$", ylabel=r"Kansdichtheid $f(x)$", **kwargs):
        title=f"Exponenti\u00eble verdeling ($\lambda={lam}$)"
        super().__init__(title, xlabel, ylabel, **kwargs)
        self.lam = lam
        self.params = {'scale': 1.0 / self.lam}
        self.x = np.linspace(0, 5 / self.lam, self.num_xsteps)
        self.dist_type = 'exponential_distribution'
        self.label = f"Exponentieel($\lambda={self.lam}$)"
        self.dist = expon

# Specifieke klasse voor t-verdeling
class TVerdelingPlotter(ContinueKansverdelingPlotter):
    def __init__(self, df=10, xlabel=r"$x$", ylabel=r"Kansdichtheid $f(x)$", **kwargs):
        title=f'T-verdeling ($df={df}$)'
        super().__init__(title, xlabel, ylabel, **kwargs)
        self.df = df
        self.params = {'df': self.df}
        if self.df < 5:
            self.x = np.linspace(-5, 5, self.num_xsteps)
        else:
            self.x = np.linspace(-4, 4, self.num_xsteps)
        self.dist_type = 't_distribution'
        self.label = f"t($df={self.df}$)"
        self.dist = t

# Specifieke klasse voor Exponentiele verdeling
class ChikwadraatVerdelingPlotter(ContinueKansverdelingPlotter):
    def __init__(self, df=10, xlabel=r"$x$", ylabel=r"Kansdichtheid $f(x)$", **kwargs):
        title=f"Chi-kwadraatverdeling ($df={df}$)"
        super().__init__(title, xlabel, ylabel, **kwargs)
        self.df = df
        self.params = {'df': self.df}
        self.x = np.linspace(0, self.df + 4 * np.sqrt(2 * self.df), self.num_xsteps)
        self.dist_type = 'chi2_distribution'
        self.label = f"Chikwadraat($df={self.df}$)"
        self.dist = chi2