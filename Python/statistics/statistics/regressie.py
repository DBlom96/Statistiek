import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Linear regression function
def linear_regression(X, y):
    """
    Perform linear regression on given data.
    Parameters:
    X (array): Independent variable(s)
    y (array): Dependent variable
    
    Returns:
    tuple: slope, intercept, residuals, and fitted values
    """
    X = np.vstack([np.ones(len(X)), X]).T  # Add a column of ones for the intercept
    beta = np.linalg.inv(X.T @ X) @ X.T @ y  # Solve for slope and intercept
    intercept, slope = beta
    y_hat = X @ beta  # Fitted values
    residuals = y - y_hat  # Residuals
    return slope, intercept, residuals, y_hat

# Prediction interval function
def prediction_interval(X, y, x_value, alpha=0.05):
    """
    Calculate the prediction interval for a given x-value.
    Parameters:
    X (array): Independent variable(s)
    y (array): Dependent variable
    x_value (float): The specific x-value for which to calculate the interval
    alpha (float): Significance level (default 0.05)
    
    Returns:
    tuple: Lower bound and upper bound of the prediction interval
    """
    slope, intercept, residuals, y_hat = linear_regression(X, y)
    n = len(X)
    mean_x = np.mean(X)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum(residuals ** 2)
    se_estimate = np.sqrt(ss_res / (n - 2))
    
    # Standard error for prediction
    se_pred = se_estimate * np.sqrt(1 + 1/n + (x_value - mean_x) ** 2 / np.sum((X - mean_x) ** 2))
    
    t_value = stats.t.ppf(1 - alpha/2, df=n - 2)  # t-distribution critical value
    y_pred = slope * x_value + intercept
    lower_bound = y_pred - t_value * se_pred
    upper_bound = y_pred + t_value * se_pred
    
    return lower_bound, upper_bound

# Confidence interval function
def confidence_interval(X, y, x_value, alpha=0.05):
    """
    Calculate the confidence interval for the mean of the dependent variable at a given x-value.
    Parameters:
    X (array): Independent variable(s)
    y (array): Dependent variable
    x_value (float): The specific x-value for which to calculate the interval
    alpha (float): Significance level (default 0.05)
    
    Returns:
    tuple: Lower bound and upper bound of the confidence interval
    """
    slope, intercept, residuals, y_hat = linear_regression(X, y)
    n = len(X)
    mean_x = np.mean(X)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum(residuals ** 2)
    se_estimate = np.sqrt(ss_res / (n - 2))
    
    # Standard error for the mean
    se_mean = se_estimate * np.sqrt(1/n + (x_value - mean_x) ** 2 / np.sum((X - mean_x) ** 2))
    
    t_value = stats.t.ppf(1 - alpha/2, df=n - 2)  # t-distribution critical value
    y_pred = slope * x_value + intercept
    lower_bound = y_pred - t_value * se_mean
    upper_bound = y_pred + t_value * se_mean
    
    return lower_bound, upper_bound

# Plotting function
def plot_regression(X, y, slope, intercept, prediction_intervals=None, confidence_intervals=None):
    """
    Plot the data points, regression line, and intervals (if provided).
    Parameters:
    X (array): Independent variable(s)
    y (array): Dependent variable
    slope (float): Slope of the regression line
    intercept (float): Intercept of the regression line
    prediction_intervals (list of tuples): Prediction intervals for a given x-value
    confidence_intervals (list of tuples): Confidence intervals for the mean for a given x-value
    """
    plt.scatter(X, y, color='blue', label='Data Points')
    
    # Plot the regression line
    x_vals = np.linspace(np.min(X), np.max(X), 100)
    y_vals = slope * x_vals + intercept
    plt.plot(x_vals, y_vals, color='red', label='Regression Line')
    
    if prediction_intervals:
        for i, x_val in enumerate(X):
            lower, upper = prediction_intervals[i]
            plt.plot([x_val, x_val], [lower, upper], color='green', linestyle='--', label='Prediction Interval' if i == 0 else "")
    
    if confidence_intervals:
        for i, x_val in enumerate(X):
            lower, upper = confidence_intervals[i]
            plt.plot([x_val, x_val], [lower, upper], color='orange', linestyle='-', label='Confidence Interval' if i == 0 else "")
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(loc='best')
    plt.title('Linear Regression with Prediction and Confidence Intervals')
    plt.show()

