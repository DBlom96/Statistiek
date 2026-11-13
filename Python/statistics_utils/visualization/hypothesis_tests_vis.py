import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, f, norm, t

# Importeer jouw reeds bestaande class uit het berekeningsbestand
from statistics_utils.calculations.hypothesis_tests_calc import HypothesisTestRunner

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
    test_name = runner.test_name
    test_type = runner.test_type
    test_statistic = runner.test_statistic["value"]
    dist_params = runner.test_statistic["dist_params"]
    left, right, p_value = runner.pvalue.values()
    alpha = runner.alpha
    critical_value_left, critical_value_right, critical_region = runner.critical_region.values()

    if "z-toets" in test_name:
        dist_type = "norm"
        dist = norm
        pdf_params = {"loc": 0, "scale": 1}
        df = None
    elif "t-toets" in test_name:
        dist_type = "t"
        dist = t
        df = dist_params["df"]
        pdf_params = dist_params
    elif "chikwadraat" in test_name:
        dist_type = "chi2"
        dist = chi2
        df = dist_params["df"]
        pdf_params = dist_params
    elif "$F$-toets voor gelijke varianties" in test_name:
        dist_type = "f"
        dist = f
        dfn, dfd = dist_params["dfn"], dist_params["dfd"]
        pdf_params = dist_params
    else:
        raise ValueError(f"Onbekend toetstype in runner: {test_name}")
        
    fig, ax = plt.subplots(figsize=(16, 9))
    buffer = 1.3

    # Bepaal het x-domein op basis van de distributie in de runner
    if test_name == "z-toets":
        xmin, xmax = -4, 4
        print("hello")
    elif "t-toets" in test_name:
        xmin = max(buffer * t.ppf(alpha / 2, df=df), -5)
        xmax = -xmin
    elif "chikwadraat" in test_name:
        xmin, xmax = 0, max(critical_value_right * buffer, test_statistic * buffer, 10)
    elif "$F$-toets" in test_name:
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

        if xmin <= test_statistic <= xmax:
            ax.text(test_statistic,ytest_stat, f"${TOETSINGSGROOTHEID_LABEL[dist_type]["lower"]}\\approx{test_statistic:.4f}$", color=PRIMARY_PLOT_COLOR, fontsize=TEXT_FONT_SIZE, ha="center")
        elif test_statistic < xmin:
            ax.text(xmin, ytest_stat, f"$\\leftarrow{TOETSINGSGROOTHEID_LABEL[dist_type]["lower"]}\\approx{test_statistic:.4f}$", color=PRIMARY_PLOT_COLOR, fontsize=TEXT_FONT_SIZE, ha="left")
        else:
            ax.text(xmax, ytest_stat, f"${TOETSINGSGROOTHEID_LABEL[dist_type]["lower"]}\\approx{test_statistic:.4f}\\rightarrow$", color=PRIMARY_PLOT_COLOR, fontsize=TEXT_FONT_SIZE, ha="right")

        if test_type == "linkszijdig" or (test_type == "tweezijdig" and p_value == left):
            where_cond = (x <= test_statistic)
        else:
            where_cond = (x >= test_statistic)
        ax.fill_between(x, 0, pdf_H0, where=where_cond, color=PRIMARY_PLOT_COLOR, alpha=OPACITY_LEVEL, label=f"$p$-waarde = {p_value:.4f}")

    ax.legend(prop={"size": 12})
    plt.xticks(fontsize=TEXT_FONT_SIZE)
    plt.yticks(fontsize=TEXT_FONT_SIZE)
    plt.savefig(filename)
    plt.close()