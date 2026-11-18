import numpy as np
from statistics_utils.calculations.correlation_and_regression_calc import (
    calculate_regression_coefficients,
    calculate_pearson_correlation,
    calculate_spearman_correlation,
    calculate_confidence_interval,
    calculate_prediction_interval
)

from statistics_utils.reporting.latex import pretty_print
    
def generate_latex_table(X, Y, labels):
    xlabel, ylabel = labels.values()
    n = len(X)
    alignment_chars = "{c|" + "c" * n + "}"
    latex_code = f"""
        \\begin{{center}}
            \\begin{{tabular}}{alignment_chars}
                \\toprule
                    \\textbf{{{xlabel}}} {" ".join([f"& ${x}$" for x in X])} \\
                \\midrule
                    \\textbf{{{ylabel}}} {" ".join([f"& ${y}$" for y in Y])} \\
                \\bottomrule
            \\end{{tabular}}
        \\end{{center}}
    """
    return latex_code

def generate_latex_table_regression(X, Y):
    X = np.array(X)
    Y = np.array(Y)
       
    latex_code = """
        \\begin{center}
            \\begin{tabular}{ccccc}
                \\toprule
                    $x$ & $y$ & $xy$ & $x^2$ & $y^2$ \\\\
                \\midrule
    """
    for x, y, xy, x2, y2 in zip(X, Y, X * Y, X ** 2, Y ** 2):
        x, y, xy, x2, y2 = map(lambda p: pretty_print(p), (x, y, xy, x2, y2))
        latex_code += f"\t\t${x}$ & ${y}$ & ${xy}$ & ${x2}$ & ${y2}$ \\\\\n"
    
    avg_X, avg_Y, avg_XY, avg_X2, avg_Y2 = map(lambda x: pretty_print(np.mean(x)), [X, Y, X * Y, X ** 2, Y ** 2])

    latex_code += f"""
                \\midrule
                    $\\overline{{x}} = {avg_X}$ & $\\overline{{y}} = {avg_Y}$ & $\\overline{{xy}} = {avg_XY}$ & $\\overline{{x^2}} = {avg_X2}$ & $\\overline{{y^2}} = {avg_Y2}$ \\\\
                \\bottomrule
            \\end{{tabular}}
        \\end{{center}}
    """    
    return latex_code

def regression_coefficients_latex(X, Y):  
    res = calculate_regression_coefficients(X, Y)
    beta_0, beta_1 = res["beta_0"], res["beta_1"]
    
    latex_code = f"""
        \\begin{{align*}}
            b &= \\frac{{\\overline{{xy}} - \\overline{{x}} \\cdot \\overline{{y}}}}{{\\overline{{x^2}} - (\\overline{{x}})^2}} \\\\
              &= \\frac{{{pretty_print(res['avg_XY'])} - {pretty_print(res['avg_X'])} \\cdot {pretty_print(res['avg_Y'])}}}{{{pretty_print(res['avg_X_squared'])} - ({pretty_print(res['avg_X'])})^2}} \\\\
              &= \\frac{{{pretty_print(res['numerator'])}}}{{{pretty_print(res['denominator'])}}} \\approx {pretty_print(beta_1)} \\\\
            a &= \\overline{{y}} - b \\cdot \\overline{{x}} \\\\
              &= {pretty_print(res['avg_Y'])} - {pretty_print(beta_1)} \\cdot {pretty_print(res['avg_X'])} \\\\
              &\\approx {pretty_print(beta_0)}.
        \\end{{align*}}

        De formule van de regressielijn behorende bij deze steekproef is dus gelijk aan $Y = {pretty_print(beta_0)}{beta_1:+.4f}X$.
    """
    return latex_code, beta_0, beta_1

def pearson_correlation_latex(X, Y):
    res = calculate_pearson_correlation(X, Y)
    r = res["r"]
    
    latex_code = f"""
        \\begin{{align*}}
            r(x,y)  &= \\frac{{ \\overline{{x \\cdot y}} - \\overline{{x}} \\cdot \\overline{{y}} }}{{ \\sqrt{{ (\\overline{{x^2}} - \\overline{{x}}^2) \\cdot (\\overline{{y^2}} - \\overline{{y}}^2) }} }}\\\\
                    &= \\frac{{ {pretty_print(res['avg_XY'])} - {pretty_print(res['avg_X'])} \\cdot {pretty_print(res['avg_Yy']) if 'avg_Yy' in res else pretty_print(res['avg_Y'])} }}{{ \\sqrt{{ ({pretty_print(res['avg_X_squared'])} - {pretty_print(res['avg_X'])}^2) \\cdot ({pretty_print(res['avg_Y_squared'])} - {pretty_print(res['avg_Y'])}^2) }} }} \\\\
                    &= \\frac{{{pretty_print(res['numerator'])}}}{{{pretty_print(res['denominator'])}}} \\\\
                    &\\approx {pretty_print(r)}.
        \\end{{align*}}
    """
    return latex_code

def spearman_correlation_latex(X, Y):
    res = calculate_spearman_correlation(X, Y)
    ranks_X, ranks_Y, d, d_squared, sum_d_squared, n, rho = (
        res["ranks_X"], res["ranks_Y"], res["d"], res["d_squared"], res["sum_d_squared"], res["n"], res["rho"]
    )
    alignment_chars = "c" + "c" * n
    
    latex_code = f"""
        De eerste stap bij het berekenen van Spearman's correlatieco\\\"effici\\\"ent is het bepalen van de rankings van de uitkomsten voor $X$ en $Y$:
        \\begin{{center}}
            \\begin{{tabular}}{{{alignment_chars}}}
                \\toprule
                    {{\\bfseries Rangnummers $X$-waarden}} {" ".join([f"& ${i}$" for i in ranks_X])} \\\\
                    {{\\bfseries Rangnummers $Y$-waarden}} {" ".join([f"& ${i}$" for i in ranks_Y])} \\\\
                \\midrule
                    {{\\bfseries Verschillen $d_i$}} {" ".join([f"& ${diff}$" for diff in d])} \\\\
                    {{\\bfseries Kwadratische verschillen $d_i^2$}} {" ".join([f"& ${diff2}$" for diff2 in d_squared])} \\\\
                \\bottomrule
            \\end{{tabular}}
        \\end{{center}}

        De som van de kwadratische rangnummerverschillen is gelijk aan $\\sum_i d_i^2 = {sum_d_squared}$.
        Aangezien de steekproefgrootte gelijk is aan $n = {n}$, is de rangcorrelatieco\\\"effici\\\"ent van Spearman gelijk aan
        \\begin{{align*}}
            r_s &= 1 - \\frac{{ 6 \\cdot \\sum_i d_i^2 }}{{ n^3 - n }}  \\\\
                &= 1 - \\frac{{ 6 \\cdot {sum_d_squared} }}{{ {n}^3 - {n} }}  \\\\
                &\\approx {pretty_print(rho)}.
        \\end{{align*}}
    """
    return latex_code

def regression_confidence_interval_latex(X, Y, beta_0, beta_1, x0, confidence=0.95):
    res = calculate_confidence_interval(X, Y, beta_0, beta_1, x0, confidence)
    y_pred, sample_std_error, sample_std_mean, t_crit, margin_error, ci = (
        res["y_pred"], res["sample_std_error"], res["sample_std_mean"], res["t_crit"], res["margin_error"], res["ci"]
    )
    confidence_percentage = int(100 * confidence)
    alpha = 1 - confidence
    n = res["n"]
    
    latex_code = f"""
        De eerste stap is om de puntschatting voor $Y$ te bepalen aan de hand van de regressielijn $Y = {pretty_print(beta_0)}{beta_1:+.4f}X$ door $X = {x0}$ in te vullen.
        Dit geeft ons een puntschatting van $y_0 = {pretty_print(beta_0)} {beta_1:+.4f} \\cdot {x0} \\approx {pretty_print(y_pred)}$.
        Daarnaast kunnen we de standaardafwijking $\\sigma$ van de storingsterm $\\varepsilon$ schatten:
        \\begin{{align*}}
            s_{{\\varepsilon}} &= \\sqrt{{ \\frac{{n}}{{n-2}} \\cdot \\left( \\overline{{y^2}} - a \\cdot \\overline{{y}} - b \\cdot \\overline{{xy}} \\right) }} \\\\
                               &= \\sqrt{{ \\frac{{{n}}}{{{n-2}}} \\cdot \\left( {pretty_print(res['mean_Y2'])} - {pretty_print(beta_0)} \\cdot {pretty_print(res['mean_Y'])} - {pretty_print(beta_1)} \\cdot {pretty_print(res['mean_XY'])} \\right) }} \\\\ 
                               &\\approx {pretty_print(sample_std_error)}.
        \\end{{align*}}

        Vervolgens kunnen we een puntschatting berekenen van de standaardafwijking van de verwachtingswaarde van $Y$ voor gegeven $X = x_0$:
        \\begin{{align*}}
        s_{{\\mu}}  &= s_{{\\varepsilon}} \\cdot \\sqrt{{ \\frac{{1}}{{n}} \\cdot \\left( 1 + \\frac{{(x_0 - \\overline{{x}})^2}}{{\\overline{{x^2}} - \\overline{{x}}^2}} \\right) }} \\\\
                    &= {pretty_print(sample_std_error)} \\cdot \\sqrt{{ \\frac{{1}}{{{n}}} \\cdot \\left( 1 + \\frac{{({pretty_print(x0)} - {pretty_print(res['mean_X'])})^2}}{{{pretty_print(res['mean_X2'])} - {pretty_print(res['mean_X'])}^2}} \\right) }} \\\\ 
                    &\\approx {pretty_print(sample_std_mean)}.   
        \\end{{align*}}

        Omdat we de standaardafwijkingen geschat hebben en de storingstermen normaal verdeeld zijn, moeten we werken met de $t$-verdeling met $df = n - 2 = {n-2}$ vrijheidsgraden.
        De $t$-waarde die hoort bij een betrouwbaarheidsniveau $\\alpha = {alpha}$ is gelijk aan
        \\[
            t = \\invt(\\opp = 1 - \\alpha / 2, \\df = n - 2) = \\invt(\\opp = {1 - alpha/2}, \\df = {n-2}) \\approx {pretty_print(t_crit)}.
        \\]
        Het \\SI{{{confidence_percentage}}}{{\\percent}}-betrouwbaarheidsinterval voor de gemiddelde $Y$ voor gegeven $X = x_0$ kan dus worden beschreven door
        \\begin{{align*}}
            &[y_0 - t \\cdot s_{{\\mu}}, y_0 - t \\cdot s_{{\\mu}}] \\
            &= [{pretty_print(y_pred)} - {pretty_print(t_crit)} \\cdot {pretty_print(sample_std_mean)}, {pretty_print(y_pred)} + {pretty_print(t_crit)} \\cdot {pretty_print(sample_std_mean)}] \\
            &\\approx [{pretty_print(ci[0])}, {pretty_print(ci[1])}].
        \\end{{align*}}
        
        Met \\SI{{{confidence_percentage}}}{{\\percent}} betrouwbaarheid ligt het gemiddelde van $Y$ voor gegeven $X = {x0}$ tussen ${pretty_print(ci[0])}$ en ${pretty_print(ci[1])}$.       
    """
    return latex_code, y_pred, ci

def regression_prediction_interval_latex(X, Y, beta_0, beta_1, x0, confidence=0.95):
    res = calculate_prediction_interval(X, Y, beta_0, beta_1, x0, confidence)
    y_pred, sample_std_error, sample_std_pred, t_crit, margin_error, pi = (
        res["y_pred"], res["sample_std_error"], res["sample_std_pred"], res["t_crit"], res["margin_error"], res["pi"]
    )
    confidence_percentage = int(100 * confidence)
    alpha = 1 - confidence
    n = res["n"]
    pi_left, pi_right = pi
    
    latex_code = f"""
        De eerste stap is om de puntschatting voor $Y$ te bepalen aan de hand van de regressielijn $Y = {pretty_print(beta_0)}{beta_1:+.4f} \\cdot X$ door $X = {x0}$ in te vullen.
        Dit geeft ons een puntschatting van $y_0 = {pretty_print(beta_0)} {beta_1:+.4f} \\cdot {x0} \\approx {pretty_print(y_pred)}$.
        Daarnaast kunnen we de standaardafwijking $\\sigma$ van de storingsterm $\\varepsilon$ schatten:
        \\begin{{align*}}
            s_{{\\varepsilon}} &= \\sqrt{{ \\frac{{n}}{{n-2}} \\cdot \\left( \\overline{{y^2}} - a \\cdot \\overline{{y}} - b \\cdot \\overline{{xy}} \\right) }} \\ 
                               &= \\sqrt{{ \\frac{{{n}}}{{{n-2}}} \\cdot \\left( {pretty_print(res['mean_Y2'])} - {pretty_print(beta_0)} \\cdot {pretty_print(res['mean_Y'])} - {pretty_print(beta_1)} \\cdot {pretty_print(res['mean_XY'])} \\right) }} \\ 
                               &\\approx {pretty_print(sample_std_error)}. 
        \\end{{align*}}

        Vervolgens kunnen we een puntschatting berekenen van de standaardafwijking van $Y$ voor gegeven $X = x_0$:
        \\begin{{align*}}
            s_{{f}} &= s_{{\\varepsilon}} \\cdot \\sqrt{{ 1 + \\frac{{1}}{{n}} \\cdot \\left( 1 + \\frac{{(x_0 - \\overline{{x}})^2}}{{\\overline{{x^2}} - \\overline{{x}}^2}} \\right) }} \\\\
                    &= {pretty_print(sample_std_error)} \\cdot \\sqrt{{ 1 + \\frac{{1}}{{{n}}} \\cdot \\left( 1 + \\frac{{({x0} - {pretty_print(res['mean_X'])})^2}}{{{pretty_print(res['mean_X2'])} - {pretty_print(res['mean_X'])}^2}} \\right) }} \\\\
                    &\\approx {pretty_print(sample_std_pred)}.         
        \\end{{align*}}

        Omdat we de standaardafwijkingen geschat hebben en de storingstermen normaal verdeeld zijn, moeten we werken met de $t$-verdeling met $df = n - 2 = {n-2}$ vrijheidsgraden.
        De $t$-waarde die hoort bij een betrouwbaarheidsniveau $\\alpha = {alpha}$ is gelijk aan
        \\[
            t = \\invt(\\opp = 1 - \\alpha / 2, \\df = n - 2) = \\invt(\\opp = {1 - alpha/2}, \\df = {n-2}) \\approx {pretty_print(t_crit)}.
        \\]
        Het \\SI{{{confidence_percentage}}}{{\\percent}}-betrouwbaarheidsinterval voor de gemiddelde $Y$ voor gegeven $X = x_0$ kan dus worden beschreven door
        \\begin{{align*}}
            &[y_0 - t \\cdot s_{{f}}; y_0 - t \\cdot s_{{f}}] \\ 
            &= [{pretty_print(y_pred)} - {pretty_print(t_crit)} \\cdot {pretty_print(sample_std_pred)}; {pretty_print(y_pred)} + {pretty_print(t_crit)} \\cdot {pretty_print(sample_std_pred)}] \\ 
            &\\approx [{pretty_print(pi_left)}, {pretty_print(pi_right)}]. 
        \\end{{align*}}
        
        Met \\SI{{{confidence_percentage}}}{{\\percent}} betrouwbaarheid ligt een toekomstige uitkomst van $Y$ voor gegeven $X = {x0}$ tussen ${pretty_print(pi_left)}$ en ${pretty_print(pi_right)}$.
    """
    return latex_code, y_pred, (pi_left, pi_right)