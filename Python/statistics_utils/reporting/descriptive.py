from ..calculations import sample_mean, sample_variance, sample_std
from .latex import pretty_print

def latex_sample_mean(data):
    n = len(data)
    mean = pretty_print(sample_mean(data))
    latex_code = f"""
        We berekenen het steekproefgemiddelde $\\overline{{x}}$ als volgt:
        \\begin{{align*}}
            \\overline{{x}} = \\frac{{x_1+x_2+\\ldots+x_n}}{{n}} = \\frac{{ {data[0]} + {data[1]} + \\ldots + {data[-1]} }}{{ {n} }} \\approx {mean}.
        \\end{{align*}}
    """
    return latex_code

def latex_sample_variance(data, ddof=1):
    n = len(data)
    mean = pretty_print(sample_mean(data))
    var = pretty_print(sample_variance(data, ddof))
    latex_code = f"""
        We berekenen de steekproefvariantie $s^2$ als volgt:
        \\begin{{align*}}
            s^2 &= \\frac{{ (x_1 - \\overline{{x}})^2 + (x_2 - \\overline{{x}})^2 + \\ldots + (x_n - \\overline{{x}})^2 }}{{ n - {ddof} }} \\\\
                &= \\frac{{ ({data[0]} - {mean})^2 + ({data[1]} - {mean})^2 + \\ldots + ({data[-1]} - {mean})^2 }}{{ {n} - {ddof} }} \\\\
                &\\approx {var}.
        \\end{{align*}}
    """
    return latex_code

def latex_sample_std(data, ddof=1):
    n = len(data)
    var = pretty_print(sample_variance(data, ddof))
    std = pretty_print(sample_std(data, ddof))
    latex_code = f"""
        We berekenen de steekproefstandaardafwijking $s$ door te wortel van de steekproefvariantie $s^2$ te nemen:
        \\begin{{align*}}
            s = \\sqrt{{ s^2 }} = \\sqrt{{ {var} }} \\approx {std}.
        \\end{{align*}}
    """
    return latex_code