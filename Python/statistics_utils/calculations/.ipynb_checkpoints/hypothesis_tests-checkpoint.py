import numpy as np
import itertools as it
from scipy import stats

DISTS = {
    "norm": stats.norm,
    "t": stats.t,
    "chi2": stats.chi2,
    "f": stats.f
}

def compute_critical_region(dist_type, alpha=0.05, test_type='two-sided', **kwargs):
    """
    Generic method to compute statistical critical regions.
    
    Args:
        dist_type (str): 'norm', 't', 'chi2', or 'f'
        alpha (float): Significance level
        test_type (str): 'two-sided', 'left-sided', or 'right-sided'
        **kwargs: Distribution parameters (e.g., df, df1, df2)
        
    Returns:
        dict: Critical values and formatted string representation of the critical region.
    """
    assert dist_type in ["norm", "t", "chi2", "f"]
    dist = DISTS[dist_type]
    
    if dist == stats.t or dist == stats.chi2:
        assert "df" in kwargs
    if dist == stats.f:
        assert "dfn" in kwargs and "dfd" in kwargs
        
    if test_type == 'two-sided':
        critical_value_left = dist.ppf(alpha / 2, **kwargs)
        critical_value_right = dist.ppf(1 - alpha / 2, **kwargs)
        region_str = f"Critical region: $(-\\infty, {critical_value_left:.4f}] \\cup [{critical_value_right:.4f}, \\infty)$"
        return {"critical_value_left": critical_value_left, "critical_value_right": critical_value_right, "region": region_str}
    elif test_type == 'right-sided':
        critical_value_right = dist.ppf(1 - alpha, **kwargs)
        region_str = f"Critical region: $[{critical_value_right:.4f}, \\infty)$"
        return {"critical_value_right": critical_value_right, "region": region_str}
    else:  # 'left-sided'
        critical_value_left = dist.ppf(alpha, **kwargs)
        region_str = f"Critical region: $(-\\infty, {critical_value_left:.4f}]$"
        return {"critical_value_left": critical_value_left, "region": region_str}    

def compute_p_value(dist_type, stat, test_type='two-sided', **kwargs):
    """
    Generic method to compute p-values corresponding to given test statistic "stat". 
    For two-sided tests, uses min(left-tail, right-tail) probability.
    """
    assert dist_type in DISTS
    dist = DISTS[dist_type]
    
    if dist in (stats.t, stats.chi2):
        assert "df" in kwargs, "Parameter 'df' is required."
    if dist == stats.f:
        assert "dfn" in kwargs and "dfd" in kwargs, "Parameters 'dfn' and 'dfd' are required."
        
    cdf_val = dist.cdf(stat, **kwargs) # left-tail probability
    survival_val = 1 - cdf_val  # right-tail probability
    
    if test_type == 'two-sided':
        # Minimum of less-equal-than and greater-equal-than probabilities * 2
        return min(cdf_val, survival_val)
    elif test_type == 'right-sided':
        return survival_val
    elif test_type == 'left-sided':
        return cdf_val
    else:
        raise ValueError(f"Unsupported test_type: {test_type}")


class HypothesisTestRunner:

    @staticmethod
    def z_test(mu_0, sigma, alpha=0.05, test_type='two-sided', sample=None, x_bar=None, n=None):
        """
        Performs a one-sample Z-test. 
        Accepts either raw data via `sample` OR pre-computed summary statistics (`x_bar` and `n`).
        """
        if sample is not None:
            sample = np.array(sample)
            x_bar = np.mean(sample)
            n = len(sample)
        elif x_bar is not None and n is not None:
            pass  # Use provided summary stats directly
        else:
            raise ValueError("You must provide either a raw 'sample' (list/array) OR both 'x_bar' and 'n'.")
            
        # Compute test statistic
        z_stat = (x_bar - mu_0) / (sigma / np.sqrt(n))
        
        # Compute p-value and critical region using your generic helpers
        p_val = compute_p_value('norm', z_stat, test_type=test_type)
        crit = compute_critical_region('norm', alpha=alpha, test_type=test_type)
        
        return {"test": "z-test", "test_type": test_type, "statistic": z_stat, "p_value": p_val, "alpha": alpha, "x_bar": x_bar, "n": n, **crit}

    @staticmethod
    def t_test_one_sample(mu_0, alpha=0.05, test_type='two-sided', sample=None, x_bar=None, s=None, n=None):
        """
        Performs a one-sample Student's t-test.
        Accepts either raw data via `sample` OR summary statistics (`x_bar`, `s`, and `n`).
        """
        if sample is not None:
            sample = np.array(sample)
            x_bar = np.mean(sample)
            s = np.std(sample, ddof=1)  # Sample standard deviation (Bessel's correction, ddof=1)
            n = len(sample)
        elif x_bar is not None and s is not None and n is not None:
            pass  # Use provided summary stats directly
        else:
            raise ValueError("You must provide either a raw 'sample' OR all three summary stats: 'x_bar', 's', and 'n'.")
            
        df = n - 1
        
        # Compute t test statistic
        t_stat = (x_bar - mu_0) / (s / np.sqrt(n))
        
        # Compute p-value and critical region using your generic helpers
        p_val = compute_p_value('t', t_stat, test_type=test_type, df=df)
        crit = compute_critical_region('t', alpha=alpha, test_type=test_type, df=df)
        
        return {"test": "one-sample t-test", "test_type": test_type, "statistic": t_stat, "p_value": p_val, "alpha": alpha, "df": df, "x_bar": x_bar, "s": s, "n": n, **crit}

    @staticmethod
    def t_test_two_sample(sample1=None, xbar1=None, s1=None, n1=None, sample2=None, xbar2=None, s2=None, 
                              n2=None, equal_var=True, alpha=0.05, test_type='two-sided'):

        if sample1 is not None and sample2 is not None:
            sample1, sample2 = np.array(sample1), np.array(sample2)
            x_bar1, x_bar2 = np.mean(sample1), np.mean(sample2)
            s1, s2 = np.std(sample1, ddof=1), np.std(sample2, ddof=1)  # Sample standard deviation (Bessel's correction, ddof=1)
            n1, n2 = len(sample1), len(sample2)
        elif x_bar1 is not None and s1 is not None and n1 is not None and x_bar2 is not None and s2 is not None and n2 is not None:
            pass  # Use provided summary stats directly
        else:
            raise ValueError("You must provide either two raw samples 'sample1' and 'sample2' OR all six summary stats: 'x_bar1', 's1', 'n1', \
                                'x_bar2', 's2', 'n2'.")

        if equal_var:
            pooled_variance = ((n1 - 1) * (s1 ** 2) + (n2 - 1) * (s2 ** 2)) / (n1+n2-2)
            t_stat = ((x_bar1 - x_bar2) - 0) / (np.sqrt(pooled_variance / n1 + pooled_variance / n2))
            df = n1 + n2 - 2
        else:
            t_stat = ((x_bar1 - x_bar2) - 0) / (np.sqrt( (s1 ** 2) / n1 + (s2 ** 2) / n2))
            df = min(n1-1, n2-1)
        
        p_val = compute_p_value('t', t_stat, test_type=test_type, df=df)
        crit = compute_critical_region('t', alpha=alpha, test_type=test_type, df=df)
        test_name = "two-sample t-test (equal variances)" if equal_var else "two-sample $t$-test (unequal variances)"
        return {"test": test_name, "test_type": test_type, "statistic": t_stat, "p_value": p_val, "alpha": alpha, "df": df, **crit}

    @staticmethod
    def chi_square_gof(observed, expected, num_estimated_parameters = 0, alpha=0.05):
        assert len(observed) == len(expected)
        chi2_stat = sum( (oi - ei) ** 2 / ei for (oi, ei) in zip(observed, expected))
        chi2_stat, _ = stats.chisquare(f_obs=observed, f_exp=expected)
        df = len(observed) - num_estimated_parameters - 1
        # Goodness of fit is inherently right-tailed
        p_val = compute_p_value('chi2', chi2_stat, test_type='right-sided', df=df)
        crit = compute_critical_region('chi2', alpha=alpha, test_type='right-sided', df=df)
        return {"test": "chi-square goodness-of-fit test", "test_type": test_type, "statistic": chi2_stat, "p_value": p_val, "alpha": alpha, "df": df, **crit}

    @staticmethod
    def chi_square_independence(observed, expected, alpha=0.05):
        assert observed.shape == expected.shape
        nrows, ncols = observed.shape
        chi2_stat = sum((observed[r,c] - expected[r,c]) ** 2 / (expected[r,c]) for (r,c) in it.product(range(nrows), range(ncols)))
        df = (nrows-1)*(ncols-1)
        # Test of independence is right-tailed
        p_val = compute_p_value('chi2', chi2_stat, test_type='right-sided', df=df)
        crit = compute_critical_region('chi2', alpha=alpha, test_type='right-sided', df=df)
        return {"test": "chi-square independence test", "test_type": test_type, "statistic": chi2_stat, "p_value": p_val, "alpha": alpha, "df": df, **crit}

    @staticmethod
    def f_test_variances(sample1, sample2, alpha=0.05, test_type='two-sided'):
        var1 = np.var(sample1, ddof=1)
        var2 = np.var(sample2, ddof=1)
        f_stat = var1 / var2
        dfn = len(sample1) - 1
        dfd = len(sample2) - 1
        
        p_val = compute_p_value('f', f_stat, test_type=test_type, dfn=dfn, dfd=dfd)
        crit = compute_critical_region('f', alpha=alpha, test_type=test_type, dfn=dfn, dfd=dfd)
        return {"test": "f-test for equal variances", "test_type": test_type, "statistic": f_stat, "p_value": p_val, "alpha": alpha, "df": (dfn, dfd), **crit}