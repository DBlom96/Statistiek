import numpy as np
from scipy.stats import norm, binom, chi2, chi2_contingency, t, expon, poisson


# Function to calculate mean, variance and standard deviation
def compute_sample_mean(sample):
    sample_mean = np.mean(sample)
    return sample_mean

def compute_sample_variance(sample):
    sample_mean = compute_sample_mean(sample)
    return sum( (x - sample_mean) ** 2 for x in sample) / (len(sample) - 1)

def compute_sample_std(sample):
    return np.sqrt(compute_sample_variance(sample))



