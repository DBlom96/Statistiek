from utils import *

def confidence_interval(sample, alpha, sigma=None):
    sample_mean = compute_sample_mean(sample)
    n = len(sample)

    if sigma:
        z_score = norm.ppf(1 - alpha / 2)
        margin_of_error = z_score * (sigma / np.sqrt(n))
    else:
        sample_std = compute_sample_std(sample)
        t_score = t.ppf(1 - alpha / 2)
        margin_of_error = t_score * sample_std / np.sqrt(n)

    lower_bound = sample_mean - margin_of_error
    upper_bound = sample_mean + margin_of_error
    print(f"Het ${int(100*(1-alpha))}\%$-betrouwbaarheidsinterval voor het populatiegemiddelde $\\mu$ is gelijk aan $[{lower_bound:.4f}, {upper_bound:.4f}]$")