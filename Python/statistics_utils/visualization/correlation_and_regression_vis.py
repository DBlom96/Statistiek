import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from sklearn.linear_model import LinearRegression

from statistics_utils.visualization.style import (
    apply_plot_style,
    style_axis_arrows,
    PRIMARY_PLOT_COLOR,
    ACCEPTABLE_COLOR,
    CRITICAL_COLOR,
    OPACITY
)

from statistics_utils.reporting.latex import pretty_print

# Activeer de huisstijl voor alle plots in deze module
apply_plot_style()

def add_midpoint_lines_and_quadrants(mean_X, mean_Y):
    left, right = plt.xlim()
    bottom, top = plt.ylim()

    plt.axvline(mean_X, linestyle="--", color=SECONDARY_PLOT_COLOR)
    plt.axhline(mean_Y, linestyle="--", color=SECONDARY_PLOT_COLOR)

    p, q = 0.2, 0.8
    quadrant_labels = [
        (p * mean_X + (1 - p) * right, (1 - q) * mean_Y + q * top, "> 0", "> 0"),
        (p * mean_X + (1 - p) * left, (1 - q) * mean_Y + q * top, "< 0", "> 0"),
        (p * mean_X + (1 - p) * left, q * mean_Y + (1 - q) * bottom, "< 0", "< 0"),
        (p * mean_X + (1 - p) * right, q * mean_Y + (1 - q) * bottom, "> 0", "< 0"),
    ]
    for x, y, dx, dy in quadrant_labels:
        plt.text(x, y, f"$x_i - \\overline{{x}} {dx}$\\n$y_i - \\overline{{y}} {dy}$", ha="center", va="center")

    plt.text(mean_X + 0.03 * (right - mean_X), bottom + 0.03 * (top - bottom), f"$\\overline{{x}}$", color=SECONDARY_PLOT_COLOR, ha="left", va="center")
    plt.text(left + 0.03 * (right - left), mean_Y + 0.03 * (top - mean_Y), f"$\\overline{{y}}$", color=SECONDARY_PLOT_COLOR, ha="center", va="bottom")

def fit_regression_and_plot_line(X, Y):
    model = LinearRegression()
    model.fit(X, Y)
    x_vals = np.linspace(np.min(X), np.max(X), 200).reshape(-1, 1)
    y_hat = model.predict(x_vals)

    m, b = model.coef_[0], model.intercept_
    label = f"Regressielijn: $\\hat{{Y}} = {pretty_print(b)}{m:+.4f}X$"
    plt.plot(x_vals, y_hat, color=CRITICAL_COLOR, label=label)

    return model, x_vals.ravel(), y_hat

def plot_residuals(X, Y, model):
    for i, (xi, yi) in enumerate(zip(X[:, 0], Y)):
        y_pred = model.predict([[xi]])[0]
        label = "Afstanden: $e_i = y_i - (a + b \\cdot x_i)$" if i == 0 else None
        plt.plot([xi, xi], [yi, y_pred], linestyle="--", color=PRIMARY_PLOT_COLOR, alpha=0.6, label=label)
    
def plot_y0(x_0, model):
    left, right = plt.xlim()
    bottom, top = plt.ylim()
    y_0 = model.predict([[x_0]])[0]

    plt.plot([x_0, x_0], [bottom, top], linestyle="--", color=PRIMARY_PLOT_COLOR)
    plt.scatter([x_0], [y_0], color="purple",
             label=f"Puntschatting voor $Y$ voor gegeven $X = {x_0}$: ${pretty_print(y_0)}$")

def plot_intervals(X, Y, x_vals, y_hat, model, x_0, plot_prediction_interval, plot_confidence_interval):
    n = len(X)
    x_mean = np.mean(X)
    Sxx = np.sum((X - x_mean) ** 2)
    residuals = Y - model.predict(X)
    s_squared = np.sum(residuals ** 2) / (n - 2)
    s = np.sqrt(s_squared)
    t_val = t.ppf(0.975, df=n - 2)

    se_mean = s * np.sqrt(1/n + (x_vals - x_mean)**2 / Sxx)
    se_pred = s * np.sqrt(1 + 1/n + (x_vals - x_mean)**2 / Sxx)

    ci_upper, ci_lower = y_hat + t_val * se_mean, y_hat - t_val * se_mean
    pi_upper, pi_lower = y_hat + t_val * se_pred, y_hat - t_val * se_pred

    if plot_prediction_interval:
        plt.fill_between(x_vals, pi_lower, pi_upper, color=CRITICAL_COLOR, alpha=0.2,
                         label='Voorspellingsinterval (voor $Y \\mid X$)')
        if x_0 is not None:
            y_0 = model.predict([[x_0]])[0]
            se_pred_0 = s * np.sqrt(1 + 1/n + (x_0 - x_mean)**2 / Sxx)
            lower, upper = y_0 - t_val * se_pred_0, y_0 + t_val * se_pred_0
            plt.plot([x_0, x_0], [lower, upper], color=CRITICAL_COLOR, linestyle="--", alpha=0.3,
                     label=f'Voorspellingsinterval (voor $Y \\mid X={x_0}$): [{pretty_print(lower)}, {pretty_print(upper)}]')

    if plot_confidence_interval:
        plt.fill_between(x_vals, ci_lower, ci_upper, color=ACCEPTABLE_COLOR, alpha=0.3,
                         label='Betrouwbaarheidsinterval (voor $E(Y \\mid X)$)')
        if x_0 is not None:
            y_0 = model.predict([[x_0]])[0]
            se_mean_0 = s * np.sqrt(1/n + (x_0 - x_mean)**2 / Sxx)
            lower, upper = y_0 - t_val * se_mean_0, y_0 + t_val * se_mean_0
            plt.plot([x_0, x_0], [lower, upper], color=ACCEPTABLE_COLOR, linestyle="--", alpha=0.3,
                     label=f'Betrouwbaarheidsinterval (voor $E[Y \\mid X={x_0}$): [{pretty_print(lower)}, {pretty_print(upper)}]')

def plot_linear_regression(
    X, Y, labels, x_0=None,
    plot_midpoint_lines=False, plot_least_squares=False, plot_regression_line=False, 
    plot_point_estimate=False, plot_prediction_interval=False, plot_confidence_interval=False,
    filename="test.png"
):
    X_arr = np.array(X).reshape(-1, 1)
    Y_arr = np.array(Y)

    mean_X, mean_Y = np.mean(X_arr), np.mean(Y_arr)

    fig, ax = plt.subplots()
    ax.scatter(X_arr, Y_arr, color=PRIMARY_PLOT_COLOR)
    ax.set_title(f'Spreidingsdiagram: {labels["X"]} vs. {labels["Y"]}')
    
    ax.set_xlabel(labels["X"])
    ax.set_ylabel(labels["Y"])

    tooth_height = 0.01
    tooth_width  = 0.015
    xs = np.array([0, tooth_width, 1.5*tooth_width, 2*tooth_width, 3*tooth_width, 4*tooth_width])
    ys = np.array([0, 0, tooth_height, -tooth_height, 0, 0])
    
    ax.plot(xs + 0.025, ys, transform=ax.transAxes, color='k', clip_on=False)
    ax.plot(ys, xs + 0.025, transform=ax.transAxes, color='k', clip_on=False)

    if plot_midpoint_lines:
        add_midpoint_lines_and_quadrants(mean_X, mean_Y)
              
    if plot_regression_line:
        model, x_vals, y_hat = fit_regression_and_plot_line(X_arr, Y_arr)
    
        if plot_least_squares:
            plot_residuals(X_arr, Y_arr, model)

        if x_0 is not None and plot_point_estimate:
            plot_y0(x_0, model)
    
        if plot_prediction_interval or plot_confidence_interval:
            plot_intervals(X_arr, Y_arr, x_vals, y_hat, model, x_0, plot_prediction_interval, plot_confidence_interval)

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

    plt.savefig(filename, bbox_inches='tight')
    plt.close()