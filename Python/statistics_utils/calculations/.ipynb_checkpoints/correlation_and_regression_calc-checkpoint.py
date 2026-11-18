import numpy as np
from scipy.stats import rankdata, t

def calculate_regression_coefficients(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    
    avg_X = np.mean(X)
    avg_Y = np.mean(Y)
    avg_XY = np.mean(X * Y)
    avg_X_squared = np.mean(X ** 2)
    avg_Y_squared = np.mean(Y ** 2)
    
    numerator = avg_XY - avg_X * avg_Y
    denominator = avg_X_squared - avg_X**2
    beta_1 = numerator / denominator
    beta_0 = avg_Y - beta_1 * avg_X
    
    return {
        "beta_0": beta_0,
        "beta_1": beta_1,
        "avg_X": avg_X,
        "avg_Y": avg_Y,
        "avg_XY": avg_XY,
        "avg_X_squared": avg_X_squared,
        "avg_Y_squared": avg_Y_squared,
        "numerator": numerator,
        "denominator": denominator
    }

def calculate_pearson_correlation(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    avg_X, avg_Y, avg_XY, avg_X_squared, avg_Y_squared = np.mean(X), np.mean(Y), np.mean(X*Y), np.mean(X**2), np.mean(Y**2)
    
    numerator = avg_XY - (avg_X * avg_Y)
    denominator = np.sqrt((avg_X_squared - avg_X**2) * (avg_Y_squared - avg_Y**2))
    r = numerator / denominator if denominator != 0 else 0.0
    
    return {
        "r": r,
        "avg_X": avg_X,
        "avg_Y": avg_Y,
        "avg_XY": avg_XY,
        "avg_X_squared": avg_X_squared,
        "avg_Y_squared": avg_Y_squared,
        "numerator": numerator,
        "denominator": denominator
    }

def calculate_spearman_correlation(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    if len(X) != len(Y):
        raise ValueError("Beide lijsten moeten dezelfde lengte hebben.")
    
    ranks_X, ranks_Y = rankdata(X), rankdata(Y)
    d = ranks_X - ranks_Y
    d_squared = d ** 2
    sum_d_squared = np.sum(d_squared)
    n = len(X)
    
    numerator = 6 * sum_d_squared
    denominator = n * (n**2 - 1)
    rho = 1 - (numerator / denominator) if denominator != 0 else 0.0
    
    return {
        "rho": rho,
        "ranks_X": ranks_X,
        "ranks_Y": ranks_Y,
        "d": d,
        "d_squared": d_squared,
        "sum_d_squared": sum_d_squared,
        "n": n
    }

def calculate_confidence_interval(X, Y, beta_0, beta_1, x0, confidence=0.95):
    X = np.array(X)
    Y = np.array(Y)
    n = len(X)
    mean_X = np.mean(X)
    mean_Y = np.mean(Y)
    mean_X2 = np.mean(X ** 2)
    mean_XY = np.mean(X * Y)
    mean_Y2 = np.mean(Y ** 2)
    
    error_terms = Y - (beta_0 + beta_1 * X)
    sample_std_error = np.sqrt(np.sum(error_terms ** 2) / (n - 2))
    sample_std_mean = sample_std_error * np.sqrt(1 / n * (1 + ((x0 - mean_X) ** 2 / (mean_X2 - mean_X ** 2))))
    
    y_pred = beta_0 + beta_1 * x0   
    t_crit = t.ppf((1 + confidence) / 2, df=n - 2)
    margin_error = t_crit * sample_std_mean
    
    return {
        "y_pred": y_pred,
        "sample_std_error": sample_std_error,
        "sample_std_mean": sample_std_mean,
        "t_crit": t_crit,
        "margin_error": margin_error,
        "ci": (y_pred - margin_error, y_pred + margin_error),
        "mean_X": mean_X,
        "mean_Y": mean_Y,
        "mean_X2": mean_X2,
        "mean_XY": mean_XY,
        "mean_Y2": mean_Y2,
        "n": n
    }

def calculate_prediction_interval(X, Y, beta_0, beta_1, x0, confidence=0.95):
    X = np.array(X)
    Y = np.array(Y)
    n = len(X)
    mean_X = np.mean(X)
    mean_Y = np.mean(Y)
    mean_X2 = np.mean(X ** 2)
    mean_XY = np.mean(X * Y)
    mean_Y2 = np.mean(Y ** 2)

    error_terms = Y - (beta_0 + beta_1 * X)
    sample_std_error = np.sqrt(np.sum(error_terms ** 2) / (n - 2))
    sample_std_pred = sample_std_error * np.sqrt(1 + 1 / n * (1 + ((x0 - mean_X) ** 2 / (mean_X2 - mean_X ** 2))))

    y_pred = beta_0 + beta_1 * x0
    t_crit = t.ppf((1 + confidence) / 2, df=n - 2)
    margin_error = t_crit * sample_std_pred
    
    return {
        "y_pred": y_pred,
        "sample_std_error": sample_std_error,
        "sample_std_pred": sample_std_pred,
        "t_crit": t_crit,
        "margin_error": margin_error,
        "pi": (y_pred - margin_error, y_pred + margin_error),
        "mean_X": mean_X,
        "mean_Y": mean_Y,
        "mean_X2": mean_X2,
        "mean_XY": mean_XY,
        "mean_Y2": mean_Y2,
        "n": n
    }