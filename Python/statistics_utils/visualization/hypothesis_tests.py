import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, f, norm, t

# Importeer jouw reeds bestaande class uit het berekeningsbestand
from statistics_utils.calculations.hypothesis_tests import HypothesisTestRunner

# ==========================================
# STYLING & CONFIGURATIE
# ==========================================
SUPTITLE_FONT_SIZE = 26
TITLE_FONT_SIZE = 20
AXIS_FONT_SIZE = 16
TEXT_FONT_SIZE = 14

PRIMARY_PLOT_COLOR = "C0"
ACCEPTABLE_COLOR = "C2"
CRITICAL_COLOR = "C3"
OPACITY_LEVEL = 0.3

TOETSINGSGROOTHEID_LABEL = {
    "norm": {"upper": "Z", "lower": "z"},
    "t": {"upper": "T", "lower": "t"},
    "chi2": {"upper": "X^2", "lower": "\\chi^2"},
    "f": {"upper": "F", "lower": "f"}
}

# ==========================================
# DE SCHONE PLOT-FUNCTIE (GEBRUIKT HET OBJECT)
# ==========================================
def plot_hypothesis_test(
    runner, display_mode="both", filename="toets_resultaat.png"
):
    """Genereert de visualisatie op basis van een geinstantieerde HypothesisTestRunner."""
    test_name = runner["test"]
    test_type = runner["test_type"] 
    test_statistic = runner["statistic"]
    p_value = runner["p_value"]
    alpha = runner["alpha"]
    critical_value_left = runner.get("critical_value_left", -np.inf)
    critical_value_right = runner.get("critical_value_right", np.inf)
    critical_region = runner["region"]

    if "z-test" in test_name:
        dist_type = "norm"
        dist = norm
        pdf_params = {"loc": 0, "scale": 1}
        df = None
    elif "t-test" in test_name:
        dist_type = "t"
        dist = t
        df = runner["df"]
        pdf_params = {"df": df}
    elif "chi-square" in test_name:
        dist_type = "chi2"
        dist = chi2
        df = runner["df"]
        pdf_params = {"df": df}
    elif "f-test" in test_name:
        dist_type = "f"
        dist = f
        dfn, dfd = runner["df"]
        pdf_params = {"dfn": dfn, "dfd": dfd}
    else:
        raise ValueError(f"Onbekend toetstype in runner: {test_name}")

    
        
    fig, ax = plt.subplots(figsize=(16, 9))
    buffer = 1.3

    # Bepaal het x-domein op basis van de distributie in de runner
    if test_name == "z-test":
        xmin, xmax = -4, 4
    elif "t-test" in test_name:
        xmin = max(buffer * t.ppf(alpha / 2, df=df), -5)
        xmax = -xmin
    elif "chi-square" in test_name:
        xmin, xmax = 0, max(critical_value_right * buffer, test_statistic * buffer, 10)
    elif "f-test" in test_name:
        xmin, xmax = 0, max(critical_value_right * buffer, test_statistic * buffer, 5)

    x = np.linspace(xmin, xmax, 1_000)
    pdf_H0 = dist.pdf(x, **pdf_params)

    ax.plot(x, pdf_H0, color=PRIMARY_PLOT_COLOR, alpha=OPACITY_LEVEL)

    fig.suptitle(f"Hypothesetoets ({test_name}, {test_type})", fontsize=SUPTITLE_FONT_SIZE)
    ax.set_title(f"Toetsingsgrootheid ${TOETSINGSGROOTHEID_LABEL[dist_type]["lower"]} = {test_statistic:.4f}$", fontsize=TITLE_FONT_SIZE)
    ax.set_xlabel(f"Toetsingsgrootheid ${TOETSINGSGROOTHEID_LABEL[dist_type]["lower"]}$", fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel("Kansdichtheid", fontsize=AXIS_FONT_SIZE)

    ymin, ymax = 0, 1.1 * max(pdf_H0) if len(pdf_H0) > 0 else 1
    offset = 0.1 * (ymax - ymin) if ymax > ymin else 0.1
    ytext, ylines = ymin - 1.7 * offset, ymin - offset
    ax.set_ylim(ymin - 2 * offset, ymax)

    # 1. Kritiek gebied (indien gevraagd)
    if display_mode in ["critical", "both"]:
        if critical_value_left > xmin:
            ax.fill_between(x, 0, pdf_H0, where=(x < critical_value_left), color=CRITICAL_COLOR, alpha=OPACITY_LEVEL, label=critical_region)
            ax.hlines(ylines, xmin, critical_value_left, color=CRITICAL_COLOR, linewidth=5)
            ax.text((critical_value_left + xmin) / 2, ytext, "Verwerp $H_0$", color=CRITICAL_COLOR, fontsize=TEXT_FONT_SIZE, ha="center")

        if critical_value_right < xmax:
            ax.fill_between(x, 0, pdf_H0, where=(x > critical_value_right), color=CRITICAL_COLOR, alpha=OPACITY_LEVEL)
            ax.hlines(ylines, critical_value_right, xmax, color=CRITICAL_COLOR, linewidth=5)
            ax.text((critical_value_right + xmax) / 2, ytext, "Verwerp $H_0$", color=CRITICAL_COLOR, fontsize=TEXT_FONT_SIZE, ha="center")

            ax.hlines(ylines, max(xmin, critical_value_left), min(xmax, critical_value_right), color=ACCEPTABLE_COLOR, linewidth=5)
            ax.text((max(xmin, critical_value_left) + min(xmax, critical_value_right)) / 2, ytext, "Accepteer $H_0$", color=ACCEPTABLE_COLOR, fontsize=TEXT_FONT_SIZE, ha="center")

    # 2. P-waarde & toetsingsgrootheid (indien gevraagd)
    if display_mode in ["p_value", "both"]:
        ytest_stat = ymin - 0.5 * offset
        pdf_stat = dist.pdf(test_statistic, **pdf_params)

        ax.plot([test_statistic, test_statistic], [0, pdf_stat], color=PRIMARY_PLOT_COLOR, linestyle="--", linewidth=1)
        ax.text(test_statistic,ytest_stat, f"${TOETSINGSGROOTHEID_LABEL[dist_type]["lower"]}\\approx{test_statistic:.4f}$", color=PRIMARY_PLOT_COLOR, fontsize=TEXT_FONT_SIZE, ha="center")

        p_left = dist.cdf(test_statistic, **pdf_params)
        p_right = 1 - dist.cdf(test_statistic, **pdf_params)

        if dist_type in ["chi2", "f"]:
            p_val = p_right
            where_cond = x >= test_statistic
        else:
            p_val = (p_left * 2 if test_type == "tweezijdig" else (p_left if test_type == "linkszijdig" else p_right))
        where_cond = ((x <= test_statistic) if test_statistic <= 0 else (x >= test_statistic))
        ax.fill_between(x, 0, pdf_H0, where=where_cond, color=PRIMARY_PLOT_COLOR, alpha=OPACITY_LEVEL, label=f"$p$-waarde = {p_val:.4f}")

    ax.legend(prop={"size": 12})
    plt.xticks(fontsize=TEXT_FONT_SIZE)
    plt.yticks(fontsize=TEXT_FONT_SIZE)
    plt.savefig(filename)
    plt.close()