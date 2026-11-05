# utils.py

import numpy as np
import pandas as pd

from math import inf, sqrt, ceil, floor
import itertools as it
from scipy.stats import norm, t, binom, poisson, chi2, f
from scipy.stats import chi2_contingency, ttest_ind, rankdata
from sklearn.linear_model import LinearRegression

def pretty_print(x, num_decimals = 4):
    """Formatteer floats netjes, zonder overbodige nullen."""
    pretty_x = (f"%.{num_decimals}f" % x).rstrip(".")
    return pretty_x

