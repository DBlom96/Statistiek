import numpy as np
import itertools as it
from scipy import stats

DISTS = {
    "norm": stats.norm,
    "t": stats.t,
    "chi2": stats.chi2,
    "f": stats.f
}

def compute_critical_region(dist_type, alpha=0.05, test_type='tweezijdig', **kwargs):
    """
    Generic method to compute statistical critical regions.
    """
    assert dist_type in ["norm", "t", "chi2", "f"]
    dist = DISTS[dist_type]
    
    if dist == stats.t or dist == stats.chi2:
        assert "df" in kwargs
    if dist == stats.f:
        assert "dfn" in kwargs and "dfd" in kwargs
        
    if test_type == 'tweezijdig':
        critical_value_left = dist.ppf(alpha / 2, **kwargs)
        critical_value_right = dist.ppf(1 - alpha / 2, **kwargs)
        region_str = f"$(-\\infty, {critical_value_left:.4f}) \\cup ({critical_value_right:.4f}, \\infty)$"
        return {"critical_value_left": critical_value_left, "critical_value_right": critical_value_right, "region": region_str}
    elif test_type == 'rechtszijdig':
        critical_value_right = dist.ppf(1 - alpha, **kwargs)
        region_str = f"$({critical_value_right:.4f}, \\infty)$"
        return {"critical_value_left": -np.inf, "critical_value_right": critical_value_right, "region": region_str}
    else:  # 'linkszijdig'
        critical_value_left = dist.ppf(alpha, **kwargs)
        region_str = f"$(-\\infty, {critical_value_left:.4f})$"
        return {"critical_value_left": critical_value_left, "critical_value_right": np.inf, "region": region_str}    

def compute_p_value(dist_type, stat, test_type='tweezijdig', **kwargs):
    """
    Generic method to compute p-values corresponding to given test statistic "stat". 
    """
    assert dist_type in DISTS and test_type in ["tweezijdig", "linkszijdig", "rechtszijdig"]
    dist = DISTS[dist_type]
    
    if dist in (stats.t, stats.chi2):
        assert "df" in kwargs, "Parameter 'df' is required."
    if dist == stats.f:
        assert "dfn" in kwargs and "dfd" in kwargs, "Parameters 'dfn' and 'dfd' are required."
        
    cdf_val = dist.cdf(stat, **kwargs)        # left-tail probability
    survival_val = 1 - cdf_val                # right-tail probability

    if test_type == "tweezijdig":
        return {"links": cdf_val, "rechts": survival_val, "p-waarde": min(cdf_val, survival_val)}
    elif test_type == "linkszijdig":
        return {"links": cdf_val, "rechts": survival_val, "p-waarde": cdf_val}
    elif test_type == "rechtszijdig":
        return {"links": cdf_val, "rechts": survival_val, "p-waarde": survival_val}
    
class HypothesisTestRunner:
    def __init__(self):
        self.test_name = None
        self.test_type = "tweezijdig"
        self.H0 = None
        self.H1 = None
        self.alpha = 0.05
        self.sample_statistics = {}
        self.test_statistic = {}
        self.critical_region = {}
        self.pvalue = None
        self.reject_H0 = False

    def _reset_state(self, test_name, test_type, alpha, h0, h1):
        """Helper to cleanly reset instance attributes before running a new test."""
        self.test_name = test_name
        self.test_type = test_type
        self.alpha = alpha
        self.H0 = h0
        self.H1 = h1
        self.sample_statistics = {}
        self.test_statistic = {}
        self.critical_region = {}
        self.pvalue = None
        self.reject_H0 = False

    def z_test(self, mu_0, sigma, alpha=0.05, test_type='tweezijdig', sample=None, sample_mean=None, sample_size=None):
        """
        Performs a one-sample Z-test.
        """
        h0 = "\\mu = \\mu_0" if test_type == "tweezijdig" else ("\\mu \\leq \\mu_0" if test_type == "rechtszijdig" else "\\mu \\geq \\mu_0")
        h1 = "\\mu \\neq \\mu_0" if test_type == "tweezijdig" else ("\\mu > \\mu_0" if test_type == "rechtszijdig" else "\\mu < \\mu_0")
        self._reset_state("z-toets", test_type, alpha, h0, h1)
        
        if sample is not None:
            arr = np.array(sample)
            self.sample_statistics["sample"] = arr
            self.sample_statistics["sample_mean"] = np.mean(arr)
            self.sample_statistics["sample_size"] = len(arr)
        elif sample_mean is not None and sample_size is not None:
            self.sample_statistics["sample_mean"] = sample_mean
            self.sample_statistics["sample_size"] = sample_size
        else:
            raise ValueError("You must provide either a raw 'sample' (list/array) OR both 'sample_mean' and 'sample_size'.")
            
        self.sample_statistics["mu_0"] = mu_0
        self.sample_statistics["sigma"] = sigma   
        sample_mean = self.sample_statistics["sample_mean"]
        sample_size = self.sample_statistics["sample_size"]

        z_stat = (sample_mean - mu_0) / (sigma / np.sqrt(sample_size))
        self.test_statistic = {
            "upper": "Z",
            "upper_formula": f"\\frac{{\\overline{{X}} - \\mu_0}}{{\\sigma / \\sqrt{{n}}}}",
            "lower": "z",
            "lower_formula": f"\\frac{{\\overline{{x}} - \\mu_0}}{{\\sigma / \\sqrt{{n}}}}",
            "lower_formula_filled": f"\\frac{{{self.sample_statistics["sample_mean"]} - {mu_0}}}{{{sigma} / \\sqrt{{{self.sample_statistics["sample_size"]}}}}}",
            "value": z_stat,
            "distribution": "N(0,1)",
            "dist_params": {"mu": 0, "sigma": 1}
        }
        self.pvalue = compute_p_value('norm', z_stat, test_type=test_type)
        self.critical_region = compute_critical_region('norm', alpha=alpha, test_type=test_type)
        self.reject_H0 = (self.pvalue["p-waarde"] < self.alpha/2) if test_type == "tweezijdig" else (self.pvalue["p-waarde"] < self.alpha)

        return self

    def t_test_one_sample(self, mu_0, alpha=0.05, test_type='tweezijdig', sample=None, sample_mean=None, sample_std=None, sample_size=None):
        """
        Performs a one-sample Student's t-test.
        """
        h0 = "\\mu = \\mu_0" if test_type == "tweezijdig" else ("\\mu \\leq \\mu_0" if test_type == "rechtszijdig" else "\\mu \\geq \\mu_0")
        h1 = "\\mu \\neq \\mu_0" if test_type == "tweezijdig" else ("\\mu > \\mu_0" if test_type == "rechtszijdig" else "\\mu < \\mu_0")
        self._reset_state("enkelvoudige t-toets", test_type, alpha, h0, h1)

        if sample is not None:
            arr = np.array(sample)
            self.sample_statistics["sample"] = arr
            self.sample_statistics["sample_mean"] = np.mean(arr)
            self.sample_statistics["sample_std"] = np.std(arr, ddof=1)
            self.sample_statistics["sample_size"] = len(arr)
        elif sample_mean is not None and sample_std is not None and sample_size is not None:
            self.sample_statistics["sample_mean"] = sample_mean
            self.sample_statistics["sample_std"] = sample_std
            self.sample_statistics["sample_size"] = sample_size
        else:
            raise ValueError("You must provide either a raw 'sample' OR all three summary stats: 'sample_mean', 'sample_std', and 'sample_size'.")
            
        self.sample_statistics["mu_0"] = mu_0
        
        sample_mean = self.sample_statistics["sample_mean"]
        sample_std = self.sample_statistics["sample_std"]
        sample_size = self.sample_statistics["sample_size"]
        df = sample_size - 1
        t_stat = (sample_mean - mu_0) / (sample_std / np.sqrt(sample_size))
        
        self.test_statistic = {
            "upper": "T",
            "lower": "t",
            "value": t_stat,
            "distribution": f"t(\\df=n-1)",
            "dist_params": {"df": df}
        }
        self.pvalue = compute_p_value('t', t_stat, test_type=test_type, df=df)
        self.critical_region = compute_critical_region('t', alpha=alpha, test_type=test_type, df=df)
        self.reject_H0 = (self.pvalue["p-waarde"] < self.alpha/2) if test_type == "tweezijdig" else (self.pvalue["p-waarde"] < self.alpha)

        return self

    def t_test_two_sample(self, sample1=None, sample_mean1=None, sample_std1=None, sample_size1=None, sample2=None, sample_mean2=None, sample_std2=None, sample_size2=None, equal_var=True, alpha=0.05, test_type='tweezijdig'):
        """
        Performs an independent two-sample Student's t-test.
        """
        name = "t-toets voor twee onafhankelijke steekproeven (gelijke varianties)" if equal_var else "t-toets voor twee onafhankelijke steekproeven (ongelijke varianties)"
        h0 = "\\mu_1 = \\mu_2" if test_type == "tweezijdig" else ("\\mu_1 \\leq \\mu_2" if test_type == "rechtszijdig" else "\\mu_1 \\geq \\mu_2")
        h1 = "\\mu_1 \\neq \\mu_2" if test_type == "tweezijdig" else ("\\mu_1 > \\mu_2" if test_type == "rechtszijdig" else "\\mu_1 < \\mu_2")
        self._reset_state(name, test_type, alpha, h0, h1)

        if sample1 is not None and sample2 is not None:
            arr1, arr2 = np.array(sample1), np.array(sample2)
            self.sample_statistics["sample1"] = arr1
            self.sample_statistics["sample2"] = arr2
            self.sample_statistics["sample_mean1"], self.sample_statistics["sample_mean2"] = np.mean(arr1), np.mean(arr2)
            self.sample_statistics["sample_std1"], self.sample_statistics["sample_std2"] = np.std(arr1, ddof=1), np.std(arr2, ddof=1)
            self.sample_statistics["sample_size1"], self.sample_statistics["sample_size2"] = len(arr1), len(arr2)
        elif all(v is not None for v in [sample_mean1, sample_std1, sample_size1, sample_mean2, sample_std2, sample_size2]):
            self.sample_statistics["sample_mean1"], self.sample_statistics["sample_mean2"] = sample_measample_size1, sample_measample_size2
            self.sample_statistics["sample_std1"], self.sample_statistics["sample_std2"] = sample_std1, sample_std2
            self.sample_statistics["sample_size1"], self.sample_statistics["sample_size2"] = sample_size1, sample_size2
        else:
            raise ValueError("You must provide either two raw samples 'sample1' and 'sample2' OR all six summary stats: 'sample_mean1', 'sample_std1', 'sample_size1', 'sample_mean2', 'sample_std2', 'sample_size2'.")

        self.sample_statistics["equal_var"] = equal_var

        m1, m2 = self.sample_statistics["sample_mean1"], self.sample_statistics["sample_mean2"]
        sd1, sd2 = self.sample_statistics["sample_std1"], self.sample_statistics["sample_std2"]
        cnt1, cnt2 = self.sample_statistics["sample_size1"], self.sample_statistics["sample_size2"]

        if equal_var:
            pooled_var = ((cnt1 - 1) * (sd1 ** 2) + (cnt2 - 1) * (sd2 ** 2)) / (cnt1 + cnt2 - 2)
            self.sample_statistics["pooled_variance"] = pooled_var
            t_stat = (m1 - m2) / np.sqrt(pooled_var / cnt1 + pooled_var / cnt2)
            df = cnt1 + cnt2 - 2
        else:
            t_stat = (m1 - m2) / np.sqrt((sd1 ** 2) / cnt1 + (sd2 ** 2) / cnt2)
            df = min(cnt1 - 1, cnt2 - 1)
            
        self.test_statistic = {
            "upper": "T",
            "lower": "t",
            "value": t_stat,
            "distribution": f"t(\\df=n+m-2={df})" if equal_var else f"t(\\df=\\min(n-1,m-1)={df})",
            "dist_params": {"df": df}
        }
        self.pvalue = compute_p_value('t', t_stat, test_type=test_type, df=df)
        self.critical_region = compute_critical_region('t', alpha=alpha, test_type=test_type, df=df)
        self.reject_H0 = (self.pvalue["p-waarde"] < self.alpha/2) if test_type == "tweezijdig" else (self.pvalue["p-waarde"] < self.alpha)

        return self

    def chi_square_gof(self, observed, expected, num_estimated_parameters=0, alpha=0.05, test_type='rechtszijdig'):
        """
        Performs a Chi-square Goodness-of-Fit test (altijd rechtszijdig).
        """
        obs_arr = np.array(observed)
        exp_arr = np.array(expected)
        assert len(obs_arr) == len(exp_arr)

        h0 = "\\text{De data volgt de veronderstelde verdeling}"
        h1 = "\\text{De data volgt niet de veronderstelde verdeling}"
        self._reset_state("chikwadraat goodness-of-fit test", "rechtszijdig", alpha, h0, h1)

        self.sample_statistics["observed"] = obs_arr
        self.sample_statistics["expected"] = exp_arr
        self.sample_statistics["num_estimated_parameters"] = num_estimated_parameters

        chi2_stat = sum((oi - ei) ** 2 / ei for (oi, ei) in zip(obs_arr, exp_arr))
        df = len(obs_arr) - num_estimated_parameters - 1
        
        self.test_statistic = {
            "upper": "X^2",
            "lower": "\\chi^2",
            "value": chi2_stat,
            "distribution": f"\\chi^2(\\df=n-p-1={df})",
            "dist_params": {"df": df}
        }
        self.pvalue = compute_p_value('chi2', chi2_stat, test_type='rechtszijdig', df=df)
        self.critical_region = compute_critical_region('chi2', alpha=alpha, test_type='rechtszijdig', df=df)
        self.reject_H0 = self.pvalue["p-waarde"] < self.alpha
        
        return self

    def chi_square_independence(self, observed, expected=None, row_names=None, col_names=None, alpha=0.05, test_type='rechtszijdig'):
        """
        Performs a Chi-square test of independence (always rechtszijdig).
        Computes expected frequencies automatically if not provided.
        """
        obs_arr = np.array(observed)
        if expected is None:
            row_sums = obs_arr.sum(axis=1, keepdims=True)
            col_sums = obs_arr.sum(axis=0, keepdims=True)
            exp_arr = (row_sums @ col_sums) / obs_arr.sum()
        else:
            exp_arr = np.array(expected)
            
        assert obs_arr.shape == exp_arr.shape

        h0 = "\\text{De twee variabelen zijn onafhankelijk}"
        h1 = "\\text{De twee variabelen zijn afhankelijk}"
        self._reset_state("chikwadraattoets voor onafhankelijkheid", "rechtszijdig", alpha, h0, h1)

        self.sample_statistics["observed"] = obs_arr
        self.sample_statistics["expected"] = exp_arr
        self.sample_statistics["row_names"] = row_names
        self.sample_statistics["col_names"] = col_names

        nrows, ncols = obs_arr.shape
        chi2_stat = sum((obs_arr[r, c] - exp_arr[r, c]) ** 2 / exp_arr[r, c] for (r, c) in it.product(range(nrows), range(ncols)))
        df = (nrows - 1) * (ncols - 1)
        
        self.test_statistic = {
            "upper": "X^2",
            "lower": "\\chi^2",
            "value": chi2_stat,
            "distribution": f"\\chi^2({df})",
            "dist_params": {"df": df}
        }
        self.pvalue = compute_p_value('chi2', chi2_stat, test_type='rechtszijdig', df=df)
        self.critical_region = compute_critical_region('chi2', alpha=alpha, test_type='rechtszijdig', df=df)
        self.reject_H0 = self.pvalue["p-waarde"] < self.alpha

        return self

    def f_test_variances(self, sample1=None, sample_var1=None, sample_size1=None, sample2=None, sample_var2=None, sample_size2=None, alpha=0.05, test_type='tweezijdig'):
        """
        Performs an F-test for equality of two variances.
        Accepts either raw samples OR summary variances and sample sizes.
        """
        h0 = "\\sigma_A^2 = \\sigma_B^2" if test_type == "tweezijdig" else ("\\sigma_A^2 \\leq \\sigma_B^2" if test_type == "rechtszijdig" else "\\sigma_A^2 \\geq \\sigma_B^2")
        h1 = "\\sigma_A^2 \\neq \\sigma_B^2" if test_type == "tweezijdig" else ("\\sigma_A^2 > \\sigma_B^2" if test_type == "rechtszijdig" else "\\sigma_A^2 < \\sigma_B^2")
        self._reset_state("$F$-toets voor gelijke varianties", test_type, alpha, h0, h1)

        if sample1 is not None and sample2 is not None:
            arr1, arr2 = np.array(sample1), np.array(sample2)
            self.sample_statistics["sample1"] = arr1
            self.sample_statistics["sample2"] = arr2
            self.sample_statistics["sample_var1"] = np.var(arr1, ddof=1)
            self.sample_statistics["sample_var2"] = np.var(arr2, ddof=1)
            self.sample_statistics["sample_size1"] = len(arr1)
            self.sample_statistics["sample_size2"] = len(arr2)
        elif all(v is not None for v in [sample_var1, sample_size1, sample_var2, sample_size2]):
            self.sample_statistics["sample_var1"] = var1
            self.sample_statistics["sample_var2"] = var2
            self.sample_statistics["sample_size1"] = n1
            self.sample_statistics["sample_size2"] = n2
        else:
            raise ValueError("You must provide either 'sample1' and 'sample2' OR all four summary stats: 'sample_var1', 'sample_size1', 'sample_var2', 'sample_size2'.")

        v1, v2 = self.sample_statistics["sample_var1"], self.sample_statistics["sample_var2"]
        dfn = self.sample_statistics["sample_size1"] - 1
        dfd = self.sample_statistics["sample_size2"] - 1
        f_stat = v1 / v2
        
        self.test_statistic = {
            "upper": "F",
            "lower": "f",
            "value": f_stat,
            "distribution": f"F(\\df_1={dfn}, \\df_2={dfd})",
            "dist_params": {"dfn": dfn, "dfd": dfd}
        }
        self.pvalue = compute_p_value('f', f_stat, test_type=test_type, dfn=dfn, dfd=dfd)
        self.critical_region = compute_critical_region('f', alpha=alpha, test_type=test_type, dfn=dfn, dfd=dfd)
        self.reject_H0 = (self.pvalue["p-waarde"] < self.alpha/2) if test_type == "tweezijdig" else (self.pvalue["p-waarde"] < self.alpha)

        return self