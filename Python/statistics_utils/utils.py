# utils.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from math import inf, sqrt, ceil, floor
import itertools as it
from scipy.stats import norm, t, binom, poisson, chi2, f
from scipy.stats import chi2_contingency, ttest_ind, rankdata
from sklearn.linear_model import LinearRegression

# Plotkleuren
primary_plot_color = "C0" # tab:blue
secondary_plot_color = "C8" # tab:olive
tertiary_plot_color = "C1" # tab:orange

acceptable_color = "C2" # tab:green
critical_color = "C3" # tab:red

# Transparency of shaded areas
opacity_level = 0.3

FIGURE_PATH = "../../../LaTeX/figures/"

def pretty_print(x, num_decimals = 4):
    """Formatteer floats netjes, zonder overbodige nullen."""
    pretty_x = (f"%.{num_decimals}f" % x).rstrip("0").rstrip(".")
    return pretty_x

def get_y_annotation(ax):
    ymin, ymax = ax.get_ylim()
    offset = 0.05 * (ymax - ymin)
    return ymin - offset, offset