"""Descriptive statistics."""

import numpy as np

def sample_mean(data):
    """Return the arithmetic mean of the observations."""
    return np.mean(data)

def sample_variance(data, ddof=1):
    return np.var(data, ddof=ddof)

def sample_std(data, ddof=1):
    """Return the standard deviation."""
    return np.sqrt(sample_variance(data, ddof=ddof))

def sample_median(data):
    data = data.sort()
    n = len(data)
    mid = n // 2
    if n % 2 == 0:
        return (x[mid-1]+x[mid]) / 2
    else:
        return x[mid]

def sample_quartiles(data):
    data = data.sort()
    med = sample_median(data)
    n = len(data)
    mid = n // 2
    if n % 2 == 1:
        # Odd length: include the median in both halves
        lower_half = data[:mid + 1]
        upper_half = data[mid:]
    else:
        # Even length: split cleanly down the middle
        lower_half = data[:mid]
        upper_half = data[mid:]
    Q1 = sample_median(lower_half)
    Q3 = sample_median(upper_half)
    return Q1, Q3

def proportion_estimate(data = None, k = None, num_trials=None):
    """Estimate a proportion from a success count or binary observations."""
    if data is None:
        assert k is not None and num_trials is not None
        return k / num_trials
    else:
        assert np.all(data in [0,1])
        return sample_mean(data)

def quartiles_tukey(data):
    """Return (Q1, median, Q3) using Tukey's median-of-halves convention.
    For an odd sample size, the overall median is included in both halves.
    """
    data = data.sort()
    med = sample_median(data)
    Q1, Q3 = sample_quartiles(data)
    return Q1, med, Q3

def detect_outliers(data):
    """Return outlier observations according to the 1.5*IQR rule.
    Returns a NumPy array containing observations outside the Tukey fences.
    """
    q1, _, q3 = quartiles_tukey(data)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return data[(data < lower) | (data > upper)]
