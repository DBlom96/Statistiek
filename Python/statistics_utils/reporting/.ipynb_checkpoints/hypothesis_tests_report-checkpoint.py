import numpy as np
from scipy.stats import f

CRITICAL_REGIONS = {
    "linkszijdig": f"$(-\\infty, g)$",
    "tweezijdig": f"$(-\\infty, g_1) \\cup (g_2, \\infty)$",
    "rechtszijdig": f"$(g, \\infty)$"
}

def generate_hypothesis_test_latex(runner):
    """
    Generiek 6-stappen framework voor de uitwerking van hypothesetoetsen.
    Delegeert test-specifieke details naar daarvoor ontworpen helperfuncties.
    """
    # 1. Haal test-specifieke details op via de juiste handler
    details = _get_test_specific_details(runner)

    # 2. Stel de 6 stappen samen op basis van het framework
    step1 = _format_step_1(runner, details)
    step2 = _format_step_2(runner)
    step3 = _format_step_3(runner, details)
    step4 = _format_step_4(runner, details)
    step5 = _format_step_5(runner, details)
    step6 = _format_step_6(runner)

    # 3. Combineer tot de definitieve LaTeX-uitwerking
    latex_output = rf"""
    {step1}{step2}{step3}{step4}{step5}{step6}
    """
    return latex_output.strip()

exp_handlers = {}

def register_test_handler(*keywords):
    """Decorator om test-specifieke handlers te registreren."""
    def decorator(func):
        for kw in keywords:
            exp_handlers[kw.lower()] = func
        return func
    return decorator    

def _get_test_specific_details(runner):
    """Zoekt de juiste handler op basis van de testnaam of fallback naar generiek."""
    name_lower = runner.test_name.lower()
    for keyword, handler in exp_handlers.items():
        if keyword in name_lower:
            return handler(runner)
    return _get_default_details(runner)

# ==========================================
# 1. Z-TOETS HANDLER
# ==========================================
@register_test_handler("z-toets", "z-test")
def _handle_z_test(runner):
    st = runner.sample_statistics
    stat = runner.test_statistic
    crit = runner.critical_region
    pvalue = runner.pvalue
    test_type = runner.test_type
    
    mu_0, sigma, sample_mean, sample_size = st["mu_0"], st["sigma"], st["sample_mean"], st["sample_size"]
    value = stat["value"]
    
    intro = "Bij een $z$-toets toetsen we een bewering over het populatiegemiddelde $\\mu$ bij een bekende populatiestandaardafwijking $\\sigma$:"
    data_section = f"""
De volgende gegevens zijn uit de steekproef en de vraag bekend:
\\begin{{align*}}
    \\overline{{x}} &= {sample_mean:.4f} \\\\
    \\sigma &= {sigma:.4f} \\\\
    n &= {sample_size}
\\end{{align*}}
    """
    
    formula_desc = f"""
De theoretische toetsingsgrootheid bij een $z$-toets is gelijk aan:
\\begin{{align*}}
    Z = \\frac{{\\overline{{X}} - \\mu_0}}{{\\sigma / \\sqrt{{n}}}},
\\end{{align*}}
en volgt onder $H_0$ een standaardnormale verdeling $N(0, 1)$.
    """
    
    observed_calc = f"""
De geobserveerde toetsingsgrootheid is gelijk aan:
\\begin{{align*}}
    z = \\frac{{\\overline{{x}} - \\mu_0}}{{\\sigma / \\sqrt{{n}}}} =\\frac{{{sample_mean:.4f} - {mu_0}}}{{{sigma} / \\sqrt{{{sample_size}}}}} \\approx {value:.4f}.
\\end{{align*}}
    """

    # Kritieke gebied en p-waarde beschrijving voor Z
    if test_type == "linkszijdig":
        g = crit.get("critical_value_left", 0)
        crit_desc = f"""
\\begin{{align*}}
    g = \\invnorm(\\opp=\\alpha={runner.alpha}, \\mu=0, \\sigma=1) \\approx {g:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    p = P(Z \\leq z \\approx {value:.4f}) = \\normalcdf(\\lb=-\\GRinfinity, \\ub={value:.4f}, \\mu=0, \\sigma=1) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""
    elif test_type == "rechtszijdig":
        g = crit.get("critical_value_right", 0)
        crit_desc = f"""
\\begin{{align*}}
    g = \\invnorm(\\opp=1-\\alpha={1-runner.alpha}, \\mu=0, \\sigma=1) \\approx {g:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    p = P(Z \\geq z \\approx {value:.4f}) = \\normalcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\mu=0, \\sigma=1) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""
    else:
        g1 = crit.get("critical_value_left", 0)
        g2 = crit.get("critical_value_right", 0)
        crit_desc = f"""
\\begin{{align*}}
    g_1 = \\invnorm(\\opp=\\alpha/2={runner.alpha/2}, \\mu=0, \\sigma=1) \\approx {g1:.4f}, \\\\
    g_2 = \\invnorm(\\opp=1-\\alpha/2={1-runner.alpha/2}, \\mu=0, \\sigma=1) \\approx {g2:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    P(Z \\leq z \\approx {value:.4f}) = \\normalcdf(\\lb=-\\GRinfinity, \\ub={value:.4f}, \\mu=0, \\sigma=1) \\approx {pvalue["links"]:.4f}, \\\\
    P(Z \\geq z \\approx {value:.4f}) = \\normalcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\mu=0, \\sigma=1) \\approx {pvalue["rechts"]:.4f}.
\\end{{align*}}
De $p$-waarde is voor tweezijdige toetsen het minimum van deze kansen, oftewel $p \\approx {pvalue["p-waarde"]:.4f}.
"""

    return {
        "intro_h": intro, "data_section": data_section, "formula_section": formula_desc,
        "observed_section": observed_calc, "critical_region_section": crit_desc, "p_value_section": p_desc
    }


# ==========================================
# 2. T-TOETS (EÉN STEEKPROEF) HANDLER
# ==========================================
@register_test_handler("enkelvoudige t-toets", "one-sample t-test", "t-test")
def _handle_t_one_sample(runner):
    st = runner.sample_statistics
    stat = runner.test_statistic
    crit = runner.critical_region
    pvalue = runner.pvalue
    test_type = runner.test_type

    mu_0, sample_mean, sample_std, sample_size = st["mu_0"], st["sample_mean"], st["sample_std"], st["sample_size"]    
    value = stat["value"]
    df = stat["dist_params"]["df"]
    
    intro = "Bij een enkelvoudige $t$-toets toetsen we een bewering over het populatiegemiddelde $\\mu$ wanneer de populatiestandaardafwijking $\\sigma$ onbekend is:"
    
    data_section = f"""
De volgende gegevens zijn uit de steekproef en de vraag bekend:
\\begin{{align*}}
    \\overline{{x}} &= {sample_mean:.4f} \\\\
    s &= {sample_std:.4f} \\\\
    n &= {sample_size} & (\\df = n - 1 = {df} \\text{{vrijheidsgraden }} )
\\end{{align*}}
    """
    
    formula_desc = f"""
De theoretische toetsingsgrootheid bij een $t$-toets (één steekproef) is:
\\begin{{align*}}
    T = \\frac{{\\overline{{X}} - \\mu_0}}{{S / \\sqrt{{n}}}},
\\end{{align*}}
en volgt onder $H_0$ een $t$-verdeling met $\\df = n-1 = {df}$ vrijheidsgraden.
    """
    
    observed_calc = f"""
De geobserveerde toetsingsgrootheid is gelijk aan:
\\begin{{align*}}
    t = \\frac{{\\overline{{x}} - \\mu_0}}{{s / \\sqrt{{n}}}} = \\frac{{{sample_mean:.4f} - {mu_0}}}{{{sample_std:.4f} / \\sqrt{{{sample_size}}}}} \\approx {value:.4f}.
\\end{{align*}}
    """

# Kritieke gebied en p-waarde beschrijving voor Z
    if test_type == "linkszijdig":
        g = crit.get("critical_value_left", 0)
        crit_desc = f"""
\\begin{{align*}}
    g = \\invt(\\opp=\\alpha={runner.alpha}, \\df={df}) \\approx {g:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    p = P(T \\leq t \\approx {value:.4f}) = \\tcdf(\\lb=-\\GRinfinity, \\ub={value:.4f}, \\df={df}) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""
    elif test_type == "rechtszijdig":
        g = crit.get("critical_value_right", 0)
        crit_desc = f"""
\\begin{{align*}}
    g = \\invt(\\opp=1-\\alpha={1-runner.alpha}, \\df={df}) \\approx {g:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    p = P(T \\geq t \\approx {value:.4f}) = \\tcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df={df}) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""
    else:
        g1 = crit.get("critical_value_left", 0)
        g2 = crit.get("critical_value_right", 0)
        crit_desc = f"""
\\begin{{align*}}
    g_1 = \\invt(\\opp=\\alpha/2={runner.alpha/2}, \\df={df}) \\approx {g1:.4f}, \\\\
    g_2 = \\invt(\\opp=1-\\alpha/2={1-runner.alpha/2}, \\df={df}) \\approx {g2:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    P(T \\leq t \\approx {value:.4f}) = \\tcdf(\\lb=-\\GRinfinity, \\ub={value:.4f}, \\df={df}) \\approx {pvalue["links"]:.4f}, \\\\
    P(T \\geq t \\approx {value:.4f}) = \\tcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df={df}) \\approx {pvalue["rechts"]:.4f}.
\\end{{align*}}
De $p$-waarde is voor tweezijdige toetsen het minimum van deze kansen, oftewel $p \\approx {pvalue["p-waarde"]:.4f}.
"""

    return {
        "intro_h": intro, "data_section": data_section, "formula_section": formula_desc,
        "observed_section": observed_calc, "critical_region_section": crit_desc, "p_value_section": p_desc
    }
    
# ==========================================
# 3. T-TOETS (TWEE STEEKPROEVEN) HANDLER
# ==========================================
@register_test_handler("t-toets voor twee onafhankelijke steekproeven (gelijke varianties)", "t-toets voor twee onafhankelijke steekproeven (ongelijke varianties)")
def _handle_t_two_sample(runner):
    st = runner.sample_statistics
    stat = runner.test_statistic
    crit = runner.critical_region
    pvalue = runner.pvalue
    test_type = runner.test_type
    
    sample_mean1, sample_std1, sample_size1 = st["sample_mean1"], st["sample_std1"], st["sample_size1"]
    sample_mean2, sample_std2, sample_size2 = st["sample_mean2"], st["sample_std2"], st["sample_size2"]
    sample_var1, sample_var2 = sample_std1 ** 2, sample_std2 ** 2
    equal_var = st["equal_var"]
    value = stat["value"]
    df = stat["dist_params"]["df"]
    
    intro = "Bij een $t$-toets voor twee onafhankelijke steekproeven vergelijken we de gemiddelden $\\mu_A$ en $\\mu_B$ van twee onafhankelijke populaties $A$ en $B$:"
    
    data_section = f"""
De volgende gegevens zijn uit de steekproef en de vraag bekend:
\\begin{{align*}}
    \\overline{{x}}_A &= {sample_mean1:.4f}, \\quad s_A^2 = {sample_var1:.4f}, \\quad n = {sample_size1} \\\\
    \\overline{{x}}_B &= {sample_mean2:.4f}, \\quad s_B^2 = {sample_var2:.4f}, \\quad m = {sample_size2}
\\end{{align*}}
    """

    if equal_var:
        formula_desc = f"""
De theoretische toetsingsgrootheid bij een $t$-toets voor twee onafhankelijke steekproeven (gelijke varianties) is:
\\begin{{align*}}
    T = \\frac{{\\left(\\overline{{X}}_A - \\overline{{X}}_B\\right)  - (\\mu_A - \\mu_B)}}{{\\sqrt{{\\frac{{S_P^2}}{{n}} + \\frac{{S_P^2}}{{m}}}}}},
\\end{{align*}}
en volgt onder $H_0$ een $t$-verdeling met $\\df = n+m-2 = {df}$ vrijheidsgraden.
    """
    
        observed_calc = f"""
Omdat we mogen uitgaan van gelijke varianties, moeten we eerst de gepoolde variantie uitrekenen:
\\begin{{align*}}
    s_P^2 = \\frac{{(n-1) \\cdot s_A^2 + (m-1) \\cdot s_B^2}}{{n+m-2}} = \\frac{{({sample_size1}-1) \\cdot {sample_var1:.4f} + ({sample_size2}-1) \\cdot {sample_var2:.4f}}}{{{sample_size1}+{sample_size2}-2}} \\approx {st["pooled_variance"]:.4f}.
\\end{{align*}}

De geobserveerde toetsingsgrootheid is gelijk aan:
\\begin{{align*}}
    t &= \\frac{{\\left(\\overline{{x}}_A - \\overline{{x}}_B\\right)  - (\\mu_A - \\mu_B)}}{{\\sqrt{{\\frac{{s_P^2}}{{n}} + \\frac{{s_P^2}}{{m}}}}}} \\\\
      &= \\frac{{\\left({sample_mean1:.4f} - {sample_mean2:.4f} \\right) - (0)}}{{ \\sqrt{{ \\frac{{{st["pooled_variance"]:.4f}}}{{{sample_size1}}} + \\frac{{{st["pooled_variance"]:.4f}}}{{{sample_size2}}} }}
      &\\approx {value:.4f}.
\\end{{align*}}
    """
    else:
        formula_desc = f"""
De theoretische toetsingsgrootheid bij een $t$-toets voor twee onafhankelijke steekproeven (ongelijke varianties) is:
\\begin{{align*}}
    T = \\frac{{\\left(\\overline{{X}}_A - \\overline{{X}}_B\\right)  - (\\mu_A - \\mu_B)}}{{\\sqrt{{\\frac{{S_A^2}}{{n}} + \\frac{{S_B^2}}{{m}}}}}},
\\end{{align*}}
en volgt onder $H_0$ een $t$-verdeling met $\\df = n+m-2 = {df}$ vrijheidsgraden.
    """
    
        observed_calc = f"""
De geobserveerde toetsingsgrootheid is gelijk aan:
\\begin{{align*}}
    t &= \\frac{{\\left(\\overline{{x}}_A - \\overline{{x}}_B\\right)  - (\\mu_A - \\mu_B)}}{{\\sqrt{{\\frac{{s_A^2}}{{n}} + \\frac{{s_B^2}}{{m}}}}}} \\\\
      &= \\frac{{\\left({sample_mean1:.4f} - {sample_mean2:.4f} \\right) - (0)}}{{ \\sqrt{{ \\frac{{{sample_var1:.4f}}}{{{sample_size1}}} + \\frac{{{sample_var2:.4f}}}{{{sample_size2}}} }}
      &\\approx {value:.4f}.
\\end{{align*}}
    """
        
    # Kritieke gebied en p-waarde beschrijving voor Z
    if test_type == "linkszijdig":
        g = crit.get("critical_value_left", 0)
        crit_desc = f"""
\\begin{{align*}}
    g = \\invt(\\opp=\\alpha={runner.alpha}, \\df={df}) \\approx {g:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    p = P(T \\leq t \\approx {value:.4f}) = \\tcdf(\\lb=-\\GRinfinity, \\ub={value:.4f}, \\df={df}) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""
    elif test_type == "rechtszijdig":
        g = crit.get("critical_value_right", 0)
        crit_desc = f"""
\\begin{{align*}}
    g = \\invt(\\opp=1-\\alpha={1-runner.alpha}, \\df={df}) \\approx {g:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    p = P(T \\geq t \\approx {value:.4f}) = \\tcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df={df}) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""
    else:
        g1 = crit.get("critical_value_left", 0)
        g2 = crit.get("critical_value_right", 0)
        crit_desc = f"""
\\begin{{align*}}
    g_1 = \\invt(\\opp=\\alpha/2={runner.alpha/2}, \\df={df}) \\approx {g1:.4f}, \\\\
    g_2 = \\invt(\\opp=1-\\alpha/2={1-runner.alpha/2}, \\df={df}) \\approx {g2:.4f}.
\\end{{align*}}
        """
        p_desc = f"""
\\begin{{align*}}
    P(T \\leq t \\approx {value:.4f}) = \\tcdf(\\lb=-\\GRinfinity, \\ub={value:.4f}, \\df={df}) \\approx {pvalue["links"]:.4f}, \\\\
    P(T \\geq t \\approx {value:.4f}) = \\tcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df={df}) \\approx {pvalue["rechts"]:.4f}.
\\end{{align*}}
De $p$-waarde is voor tweezijdige toetsen het minimum van deze kansen, oftewel $p \\approx {pvalue["p-waarde"]:.4f}.
"""
        
    return {
        "intro_h": intro, "data_section": data_section, "formula_section": formula_desc,
        "observed_section": observed_calc, "critical_region_section": crit_desc, "p_value_section": p_desc
    }

# ==========================================
# 4. CHI-SQUARE GOF TEST HANDLER
# ==========================================
@register_test_handler("chikwadraat goodness-of-fit test")
def _handle_chi2_gof(runner):
    st = runner.sample_statistics
    stat = runner.test_statistic
    crit = runner.critical_region
    pvalue = runner.pvalue
    test_type = runner.test_type
    observed, expected = st["observed"], st["expected"]
    
    df = len(st["observed"]) - st["num_estimated_parameters"] - 1
    value = stat["value"]
    
    intro = "Bij een $\\chi^2$-aanpassingstoets (Goodness-of-Fit) toetsen we of de waargenomen frequenties van uitkomsten van een discrete variable een bepaalde discrete kansverdeling volgt:"
    
    data_section = f"""
De geobserveerde en verwachte frequenties zijn ingevoerd, met $\\df = {df}$ vrijheidsgraden.
    """
    
    formula_desc = f"""
Voordat we de toetsingsgrootheid kunnen berekenen, hebben we eerst de verwachte frequenties nodig van de mogelijke uitkomsten onder $H_0$.

\\begin{{center}}
    \\begin{{tabular}}{{ccc}}
        \\toprule
            \\textbf{{Uitkomst $i$}} & \\textbf{{Observed}} ($o_i$) & \\textbf{{Expected}} ($e_i$) \\\\
        \\midrule
            {"\n".join(f"{i} & {observed[i]:.4f} & {expected[i]:.4f}" for i in range(len(observed)))}
        \\bottomrule
    \\end{{tabular}}
\\end{{center}}

De toetsingsgrootheid is:
\\begin{{align*}}
    X^2 = \\sum \\frac{{(O_i - E_i)^2}}{{E_i}},
\\end{{align*}}
en volgt onder $H_0$ een $\\chi^2$-verdeling met $\\df = {df}$ (altijd rechtszijdig).
    """
    
    observed_calc = f"""
De geobserveerde toetsingsgrootheid is gelijk aan:
\\begin{{align*}}
    \\chi^2 &= \\sum \\frac{{(o_i - e_i)^2}}{{e_i}} \\\\
            &= \\frac{{({observed[0]}-{expected[0]:.4f})^2}}{{{expected[0]:.4f}}} + \\ldots + \\frac{{({observed[-1]}-{expected[-1]:.4f})^2}}{{{expected[-1]:.4f}}}
            &\\approx {value:.4f}.
\\end{{align*}}
    """

    g = crit["critical_value_right"]
    crit_desc = f"""
\\begin{{align*}}
    \\chi^2\\textrm{{cdf}}(\\lb=g, \\ub=\\GRinfinity, \\df={df}) = \\alpha = {runner.alpha} \\Rightarrow g \\approx {g:.4f}. 
\\end{{align*}}
    """
    
    p_desc = f"""
\\begin{{align*}}
    p = P(X^2 \\geq \\chi^2 \\approx {value:.4f}) = \\chi^2\\textrm{{cdf}}(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df={df}) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""

    return {
        "intro_h": intro, "data_section": data_section, "formula_section": formula_desc,
        "observed_section": observed_calc, "critical_region_section": crit_desc, "p_value_section": p_desc
    }

# ==========================================
# 4. CHI-SQUARE INDEPENDENCE TEST HANDLER
# ==========================================
def generate_contingency_table_latex(row_names, col_names, data_matrix):
    data = np.array(data_matrix)
    row_sums = data.sum(axis=1, keepdims=True)
    col_sums = data.sum(axis=0, keepdims=True)
    
    assert len(row_names) == data.shape[0], "Aantal rijnamen moet matchen met rijen in data."
    assert len(col_names) == data.shape[1], "Aantal kolomnamen moet matchen met kolommen in data."
    
    # Als er een totaalkolom is, voegen we deze toe aan de kolomnamen
    headers = [f"\\textbf{{{col}}}" for col in col_names] + ["\\textbf{Totaal}"]
    
    header_line = " & " + " & ".join(headers) + " \\\\"
    
    # Bouw de rijen op
    rows_latex = []
    for i, row_name in enumerate(row_names):
        row_cells = [f"\\textbf{{{row_name}}}"]
        count = 0
        
        # Voeg data-waardes toe (geformatteerd op 4 decimalen of als integer)
        for val in data[i]:
            count += val
            if isinstance(val, (int, np.integer)):
                row_cells.append(str(val))
            else:
                row_cells.append(f"{val:.4f}")
        row_cells.append(f"{row_sums[i][0]}")                
        rows_latex.append(" & ".join(row_cells) + " \\\\")
        
    # Maak de tabelopmaak string: bijv. m{0.28\textwidth}|ccc|c
    num_data_cols = len(col_names)
    tabular_format = f"c{"c" * num_data_cols}c"
        
    # Stel de rijen samen met \midrule
    body_content = "\n            ".join(rows_latex)
    
    # Optionele totaalrij toevoegen
    total_row_latex = ""
    tot_cells = ["\\textbf{Totaal}"]
    count = 0
    for val in col_sums[0]:
        print(val)
        if isinstance(val, (int, np.integer)):
            tot_cells.append(str(val))
        else:
            tot_cells.append(f"{val:.4f}")
    tot_cells.append(f"{col_sums.sum()}")
    total_row_latex = f"""
        \\midrule
        {" & ".join(tot_cells)} \\\\"""

    # Samenvoegen tot het complete LaTeX blok
    latex_code = f"""
\\begin{{center}}
    \\renewcommand{{\\arraystretch}}{{1}}
    \\begin{{tabular}}{{{tabular_format}}}
        \\toprule
            {header_line}
        \\midrule
            {body_content}{total_row_latex}
        \\bottomrule
    \\end{{tabular}}
\\end{{center}}
    """
    
    return latex_code.strip()
    
@register_test_handler("chikwadraattoets voor onafhankelijkheid")
def _handle_chi2_independence(runner):
    st = runner.sample_statistics
    stat = runner.test_statistic
    crit = runner.critical_region
    pvalue = runner.pvalue
    test_type = runner.test_type
    observed, expected = st["observed"], st["expected"]
    row_names, col_names = st["row_names"], st["col_names"]
    nrows, ncols = observed.shape
    df = (nrows-1)*(ncols-1)
    value = stat["value"]
    
    intro = "Bij een $\\chi^2$-toets voor onafhankelijkheid toetsen we of twee categorische variabelen onafhankelijk zijn van elkaar:"
    
    data_section = f"""
De geobserveerde en verwachte frequenties zijn ingevoerd, met $\\df = {df}$ vrijheidsgraden.
    """
    
    formula_desc = f"""
Voordat we de toetsingsgrootheid kunnen berekenen, hebben we eerst de verwachte frequenties nodig van de mogelijke uitkomsten onder $H_0$.
Deze berekenen we met de volgende formule:
\\[
    E_{{ij}} = \\frac{{ \\text{{rijtotaal}}(i) \\cdot \\text{{kolomtotaal}}(j) }}{{ \\text{{totaal}} }}.
\\]
Dit geeft ons de volgende tabel van verwachte frequenties:
{generate_contingency_table_latex(row_names, col_names, expected)}

De toetsingsgrootheid is:
\\begin{{align*}}
    X^2 = \\sum \\frac{{(O_{{ij}} - E_{{ij}})^2}}{{E_{{ij}}}},
\\end{{align*}}
en volgt onder $H_0$ een $\\chi^2$-verdeling met $\\df = (r-1)\\cdot(k-1)={df}$,
waar $r$ het aantal rijen en $k$ het aantal kolommen is.
    """
    
    observed_calc = f"""
De geobserveerde toetsingsgrootheid is gelijk aan:
\\begin{{align*}}
    \\chi^2 &= \\sum \\frac{{(o_{{ij}} - e_{{ij}})^2}}{{e_{{ij}}}} \\\\
            &= \\frac{{({observed[0,0]}-{expected[0,0]:.4f})^2}}{{{expected[0,0]:.4f}}} + \\ldots + \\frac{{({observed[-1,-1]}-{expected[-1,-1]:.4f})^2}}{{{expected[-1,-1]:.4f}}}
            &\\approx {value:.4f}.
\\end{{align*}}
    """

    g = crit["critical_value_right"]
    crit_desc = f"""
\\begin{{align*}}
    \\chi^2\\textrm{{cdf}}(\\lb=g, \\ub=\\GRinfinity, \\df={df}) = \\alpha = {runner.alpha} \\Rightarrow g \\approx {g:.4f}. 
\\end{{align*}}
    """
    
    p_desc = f"""
\\begin{{align*}}
    p = P(X^2 \\geq \\chi^2 \\approx {value:.4f}) = \\chi^2\\textrm{{cdf}}(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df={df}) \\approx {pvalue["p-waarde"]:.4f}.
\\end{{align*}}
"""

    return {
        "intro_h": intro, "data_section": data_section, "formula_section": formula_desc,
        "observed_section": observed_calc, "critical_region_section": crit_desc, "p_value_section": p_desc
    }


# ==========================================
# 5. F-TOETS HANDLER
# ==========================================
@register_test_handler("$F$-toets voor gelijke varianties")
def _handle_f_test(runner):
    crit = runner.critical_region
    st = runner.sample_statistics
    stat = runner.test_statistic
    dfn, dfd = stat["dist_params"].values()
    test_type = runner.test_type
    value = stat["value"]
    left, right, pvalue = runner.pvalue.values()
    
    intro = (
        f"Bij een $F$-toets toetsen we of de populatievarianties $\\sigma_A^2$ en $\\sigma_B^2$ van twee populaties $A$ en $B$ gelijk zouden kunnen zijn:"
    )
    
    data_table = f"""
De steekproefgegevens waar we mee gaan werken hebben we zojuist al bepaald in de vorige opgave:
\\begin{{center}}
    \\begin{{tabular}}{{|c|c|c|}}
        \\toprule
            $s_A^2 = {st.get('sample_var1', 0):.4f}$ & $n = {st.get('sample_size1', 0)}$ & $\\df_1 = {st.get('sample_size1', 0)-1}$ \\\\
            $s_B^2 = {st.get('sample_var2', 0):.4f}$ & $m = {st.get('sample_size2', 0)}$ & $\\df_2 = {st.get('sample_size2', 0)-1}$ \\\\
        \\bottomrule
    \\end{{tabular}}
\\end{{center}}
    """
    
    formula_desc = f"""
De theoretische toetsingsgrootheid (hoofdletter!) bij een $F$-toets is gelijk aan:
\\begin{{align*}}
    F = \\frac{{S_A^2}}{{S_B^2}},
\\end{{align*}}
en volgt onder $H_0$ een $F$-verdeling met respectievelijk $\\df_1 = n - 1 = {dfn}$ en $\\df_2 = m - 1 = {dfd}$ vrijheidsgraden.
    """
    
    observed_calc = f"""
De geobserveerde toetsingsgrootheid (kleine letter!) is gelijk aan
\\begin{{align*}}
    f = \\frac{{s_A^2}}{{s_B^2}} = \\frac{{{st["sample_var1"]:.4f}}}{{{st["sample_var2"]:.4f}}} \\approx {stat['value']:.4f}.
\\end{{align*}}
    """

    # F-toets is altijd tweezijdig!
    g1 = crit["critical_value_left"]
    g2 = crit["critical_value_right"]
    critical_region_desc = f"""
\\begin{{align*}}
    Fcdf(\\lb=0, \\ub=g_1, \\df_1={dfn}, \\df_2={dfd}) = \\alpha/2 = {runner.alpha/2} &\\Rightarrow g_1 \\approx {g1:.4f} \\\\
    Fcdf(\\lb=g_2, \\ub=\\GRinfinity, \\df_1={dfn}, \\df_2={dfd}) = \\alpha/2 = {runner.alpha/2} &\\Rightarrow g_2 \\approx {g2:.4f} \\\\
\\end{{align*}}
    """
    
    pvalue_desc = f"""
\\begin{{align*}}
     P(F \\leq f \\approx {value:.4f}) = Fcdf(\\lb=0, \\ub={value:.4f}, \\df_1={dfn}, \\df_2={dfd}) &\\approx {left:.4f} \\\\
     P(F \\geq f \\approx {value:.4f}) = Fcdf(\\lb={value:.4f}, \\ub=\\GRinfinity, \\df_1={dfn}, \\df_2={dfd}) &\\approx {right:.4f}
\\end{{align*}}
De $p$-waarde is gelijk aan het minimum van deze twee kansen, oftewel $p \\approx {pvalue:.4f}. 
    """
    
    return {
        "intro_h": intro,
        "data_section": data_table,
        "formula_section": formula_desc,
        "observed_section": observed_calc,
        "critical_region_section": critical_region_desc,
        "p_value_section": pvalue_desc
    }

def _get_default_details(runner):
    """Fallback handler voor generieke of ongedefinieerde toetsen (zoals z-toets of chi-kwadraat)."""
    stat = runner.test_statistic
    st = runner.sample_statistics
    
    return {
        "intro_h": "We formuleren de nulhypothese en alternatieve hypothese voor deze toets:",
        "data_section": f"Gegevens: {st}",
        "formula_section": f"Toetsingsgrootheid ${stat['upper']}$ volgt verdeling {stat['distribution']}.",
        "observed_section": f"Geobserveerde waarde: {stat['upper'].lower()} = {stat['lower']:.4f}.",
        "critical_region_section": f"Kritieke gebied: {crit["region"]}.",
        "p_value_section": f"$p$-waarde: {runner.pvalue:.4f}."
    }


# ==========================================
# FRAMEWORK BOUWSTENEN (DE 6 STAPPEN)
# ==========================================

def _format_step_1(runner, details):
    step1 = f"""
\\subsubsection*{{Stap 1: formuleer de nulhypothese $H_0$ en de alternatieve hypothese $H_1$.}}
{details['intro_h']}
\\begin{{align*}}
    H_0: &{runner.H0} \\\\
    H_1: &{runner.H1}
\\end{{align*}}
    """
    return step1
    
def _format_step_2(runner):
    step2 = f"""
\\subsubsection*{{Stap 2: bepaal het significantieniveau $\\alpha$.}}
Er is in de vraag gegeven dat we mogen werken met een significantieniveau $\\alpha = {runner.alpha}$.
    """
    return step2

def _format_step_3(runner, details):
    step3 = f"""
\\subsubsection*{{Stap 3: verzamel data voor het berekenen van de toetsingsgrootheid.}}
{details['data_section']}
    """
    return step3

def _format_step_4(runner, details):
    step4 = f"""
\\subsubsection*{{Stap 4: bereken de toetsingsgrootheid.}}
{details['formula_section']}
{details['observed_section']}
    """
    return step4

def _format_step_5(runner, details):
    crit = runner.critical_region
    region_desc = crit.get("region", "Zie kritiek gebied.")
    test_type = runner.test_type
    pvalue = runner.pvalue["p-waarde"]
      
    step5 = f"""
\\subsubsection*{{Stap 5: bepaal de toetsuitslag.}}

\\textbf{{Methode 1: kritieke gebied}} \\\\
Aangezien we {test_type} toetsen, is het kritieke gebied van de vorm {CRITICAL_REGIONS[test_type]}, waarbij
{details["critical_region_section"]}
Het kritieke gebied is dus gelijk aan {crit["region"]}. 
De geobserveerde toetsingsgrootheid ${runner.test_statistic["lower"]} \\approx {runner.test_statistic["value"]:.4f}$ ligt{" niet " if not runner.reject_H0 else " "}in het kritieke gebied, dus
we besluiten om de nulhypothese $H_0${" niet " if not runner.reject_H0 else " "}te verwerpen.

\\textbf{{Methode 2: de $p$-waarde}} \\\\
Aangezien we {test_type} toetsen, kunnen we de $p$-waarde als volgt berekenen:
{details["p_value_section"]}
De $p$-waarde is dus gelijk aan $p \\approx {pvalue:.4f}$.
Aangezien $p {"<" if runner.reject_H0 else "\\geq"} \\alpha = {runner.alpha}$,
wordt de nulhypothese $H_0$ {"niet" if not runner.reject_H0 else ""} verworpen.
    """
    return step5

def _format_step_6(runner):
    conclusion = (
        f"Er is {'voldoende' if runner.reject_H0 else 'onvoldoende'} reden om op basis van deze steekproef "
        f"de nulhypothese te verwerpen in de context van het probleem."
    )
    step6 = f"""
\\subsubsection*{{Stap 6: vertaal de toetsuitslag terug naar de originele context van het probleem.}}
{conclusion}
    """
    return step6