import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from .continuous import NormaleVerdelingPlotter  # Importeer de basis plotter

class ZToetsPlotter(NormaleVerdelingPlotter):
    def __init__(self, mu_0, sigma, n, alpha=0.05):
        title=f"Z-toets: $H_0$: $\\mu={mu_0} vs $H_1$: $\\mu \neq {mu_0}$"
        self.mu_0 = mu_0  # Null hypothesis mean (H0)
        self.sigma = sigma  # Population standard deviation
        self.n = n  # Sample size
        self.alpha = alpha  # Significance level (Type I error)

    def compute_z_critical(self, hyp_type="two_tailed"):
        """Compute critical z values based on the hypothesis type"""
        if hyp_type == "two_tailed":
            z_critical_left = norm.ppf(self.alpha / 2)
            z_critical_right = norm.ppf(1 - self.alpha / 2)
            return z_critical_left, z_critical_right
        elif hyp_type == "left_tailed":
            z_critical_left = norm.ppf(self.alpha)
            return z_critical_left, None
        elif hyp_type == "right_tailed":
            z_critical_right = norm.ppf(1 - self.alpha)
            return None, z_critical_right

    def plot_z_test(self, mu_1=None, hyp_type="two_tailed", beta=None):
        """Plot the z-test for means with Type I and Type II errors visualized"""
        # Define the x-axis range for the plot
        x = np.linspace(-4, 4, 1000)
        y = norm.pdf(x)

        # Plot the standard normal distribution (H0)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, label=r"Standard Normal Distribution under $H_0$", color='blue')

        # Get critical z-values
        z_critical_left, z_critical_right = self.compute_z_critical(hyp_type)

        # Highlight Type I error regions (rejection regions)
        if hyp_type == "two_tailed":
            ax.fill_between(x, y, where=(x < z_critical_left), color='red', alpha=0.3, label=r"Type I Error ($\alpha$)")
            ax.fill_between(x, y, where=(x > z_critical_right), color='red', alpha=0.3)
            ax.axvline(z_critical_left, color='red', linestyle='--', label="Critical Value (Left)")
            ax.axvline(z_critical_right, color='red', linestyle='--', label="Critical Value (Right)")
        elif hyp_type == "left_tailed":
            ax.fill_between(x, y, where=(x < z_critical_left), color='red', alpha=0.3, label=r"Type I Error ($\alpha$)")
            ax.axvline(z_critical_left, color='red', linestyle='--', label="Critical Value")
        elif hyp_type == "right_tailed":
            ax.fill_between(x, y, where=(x > z_critical_right), color='red', alpha=0.3, label=r"Type I Error ($\alpha$)")
            ax.axvline(z_critical_right, color='red', linestyle='--', label="Critical Value")

        # Plot the alternative hypothesis distribution (if given)
        if mu_1 is not None:
            z_mu_1 = (mu_1 - self.mu_0) / (self.sigma / np.sqrt(self.n))
            y_alt = norm.pdf(x - z_mu_1)
            ax.plot(x, y_alt, label=r"Alternative Distribution under $H_1$", color='green')

            # Type II error (failing to reject H0 when H1 is true)
            if beta is not None:
                if hyp_type == "two_tailed":
                    self.ax.fill_between(x, y_alt, where=(x > z_critical_left) & (x < z_critical_right),
                                    color='orange', alpha=0.3, label=r"Type II Error ($\beta$)")
                elif hyp_type == "left_tailed":
                    self.ax.fill_between(x, y_alt, where=(x > z_critical_left),
                                    color='orange', alpha=0.3, label=r"Type II Error ($\beta$)")
                elif hyp_type == "right_tailed":
                    self.ax.fill_between(x, y_alt, where=(x < z_critical_right),
                                    color='orange', alpha=0.3, label=r"Type II Error ($\beta$)")

        # Label regions
        self.ax.text(-3.5, 0.02, 'Reject $H_0$', color='red', fontsize=12)
        self.ax.text(3.5, 0.02, 'Reject $H_0$', color='red', fontsize=12)
        if hyp_type == "two_tailed":
            self.ax.text(0, 0.15, 'Fail to Reject $H_0$', color='green', fontsize=12, ha='center')

        # Set labels and title
        self.ax.set_title(f"Hypothesetoets: Z-toets voor $\\mu$ ($H_0$: $\\mu = {self.mu_0}$)")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel(r"Kansdichtheid $f(x)$")
        self.ax.legend()

        plt.show()