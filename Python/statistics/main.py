import numpy as np
from statistics import chi2, regressie
#compute_expected_frequencies, compute_chi2_test_statistic, compute_degrees_of_freedom, compute_chi2_p_value

if __name__ == "__main__":
   
    # Question 1
    data = np.array([
        [30, 20],  # Rij voor "Man"
        [25, 25]   # Rij voor "Vrouw"
    ])

    chi2.exam_question()

    # Regression
    # Example data
    X = [1, 2, 3, 4, 5]
    y = [2.2, 2.8, 3.6, 4.5, 5.1]

    x_value = 3.5   # Value where we want CI and PI
    alpha = 0.05
    confidence = int(100 * (1 - alpha))

    # Perform linear regression
    slope, intercept, _, _ = regressie.linear_regression(X, y)

    # Compute prediction and confidence intervals for a specific x-value
    pred_interval = regressie.prediction_interval(X, y, x_value)
    conf_interval = regressie.confidence_interval(X, y, x_value)

    # Plotting
    regressie.plot_regression(X, y, slope, intercept, [pred_interval], [conf_interval])