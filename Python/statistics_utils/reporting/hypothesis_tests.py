import numpy as np

def generate_hypothesis_test_latex(runner, method):
    """
    Genereert een volledige 6-stappen LaTeX-uitwerking op basis van een uitgevoerde hypothesetoets.
    """
    st = runner.sample_statistics
    stat = runner.test_statistic
    crit = runner.critical_region
    
    # Bepaal tekst en symbolen op basis van test_type
    test_type = runner.test_type
    
    # --- STAP 1: Hypotheses ---
    h0_str = f"H_0: \\quad {runner.H0}"
    h1_str = f"H_1: \\quad {runner.H1}"
    
    # Specifieke inleiding per toetstype
    if "z" in runner.test_name.lower():
        intro_stap1 = "Bij een $z$-toets toetsen we de waarde van het populatiegemiddelde $\\mu$ ten opzichte van een nulwaarde $\\mu_0$."
    elif "één steekproef" in runner.test_name.lower():
        intro_stap1 = "Bij een enkelvoudige $t$-toets toetsen we het populatiegemiddelde $\\mu$ op basis van een steekproef met onbekende variantie."
    elif "twee steekproeven" in runner.test_name.lower():
        intro_stap1 = "Bij een tweesteekproeven $t$-toets vergelijken we de gemiddelden van twee onafhankelijke populaties."
    elif "f" in runner.test_name.lower():
        intro_stap1 = (
            "Bij een $F$-toets toetsen we of de varianties $\\sigma_A^2$ en $\\sigma_B^2$ gelijk zouden kunnen zijn, oftewel"
        )
    elif "chi^2" in runner.test_name.lower():
        intro_stap1 = "We formuleren de hypotheses voor de toets:"
    else:
        intro_stap1 = "We formuleren de nulhypothese en de alternatieve hypothese:"

    # --- STAP 2: Significantieniveau ---
    stap2_text = (
        f"Er is in de vraag gegeven dat we mogen werken met een significantieniveau $\\alpha = {runner.alpha}$.\\\\"
    )

    # --- STAP 3: Data verzamelen ---
    stap3_text = "De steekproefdata zijn gegeven in de vraag, namelijk "
    if "sample_mean" in st and "sample_size" in st:
        stap3_text += f"\nhet steekproefgemiddelde $\\overline{{x}} = {st['sample_mean']:.4f}$ en de steekproefgrootte $n = {st['sample_size']}$"
        if "sigma" in st:
            stap3_text += f", en verder is de standaardafwijking $\\sigma = {st['sigma']}$ bekend."
    elif "sample_mean" in st and "sample_std" in st and "sample_size" in st:
        stap3_text += f"\n het steekproefgemiddelde $\\overline{{x}} = {st['sample_mean']:.4f}$, de steekproefstandaardafwijking $s = {st['sample_std']:.4f}$ en de steekproefgrootte $n = {st['sample_size']}$"
    elif "sample_mean1" in st:
        stap3_text += (
            f"\nSteekproef 1: $\\overline{{x}}_1 = {st['sample_mean1']:.4f}$, $s_1 = {st['sample_std1']:.4f}$, $n_1 = {st['sample_size1']}$<br>"
            f"Steekproef 2: $\\overline{{x}}_2 = {st['sample_mean2']:.4f}$, $s_2 = {st['sample_std2']:.4f}$, $n_2 = {st['sample_size2']}$"
        )
    elif "sample_var1" in st:
        stap3_text += (
            f"\nSteekproef 1: $s_1^2 = {st['sample_var1']:.4f}$, $n_1 = {st['sample_size1']}$<br>"
            f"Steekproef 2: $s_2^2 = {st['sample_var2']:.4f}$, $n_2 = {st['sample_size2']}$"
        )
    else:
        stap3_text += "\nGegevens zijn direct verwerkt in de toets."

    # --- STAP 4: Toetsingsgrootheid ---
    upper = stat["upper"]
    upper_formula = stat["upper_formula"]
    lower = stat["lower"]
    lower_formula = stat["lower_formula"]
    lower_formula_filled = stat["lower_formula_filled"]
    value = stat["value"]
    dist_name = stat["distribution"]
    
    stap4_text = (
        f"De theoretische toetsingsgrootheid (hoofdletter!) bij een {runner.test_name} is\n" 
        f"\\begin{{align*}}\n"
        f"    {upper} = {upper_formula},\n"
        f"\\end{{align*}}\n"
        f"en volgt onder $H_0$ een {dist_name}-verdeling.\n"
        f"\n"
        f"De geobserveerde toetsingsgrootheid (kleine letter!) berekenen we dan als volgt\n"
        f"\\begin{{align*}}\n"
        f"    {lower} &= {lower_formula} \\\\ \n"
        f"            &= {lower_formula_filled} \\\\ \n"
        f"            &\\approx {value:.4f}.\n"
        f"\\end{{align*}}"
    )

    # --- STAP 5: Kritiek gebied & uitslag ---
    region_desc = crit.get("region", "Zie kritiek gebied.")
    rejected = runner.pvalue < runner.alpha
    p_value_text = (
        f"Aangezien we {test_type} toetsen, kunnen we de $p$-waarde als volgt berekenen:\n"
        f"\\begin{{align*}}\n"
        f"    p = P({upper} \\leq {lower}) \\approx {runner.pvalue}\n"
        f"\\end{{align*}}\n"
        f"Aangezien $p {'<' if runner.reject_H0 else '\\geq'} {"\\alpha/2" if runner.test_type == "two-sided" else "\\alpha"} = {runner.alpha}$, "
        f"wordt de nulhypothese $H_0$ {"niet" if not runner.reject_H0 else ""} verworpen."
    )
    
    critical_region_text = (
        f"Het kritieke gebied behorende bij een {test_type}e toets met significantieniveau $\\alpha = {runner.alpha}$ is van de vorm {f"$(-\\infty, g)$" if test_type == "linkszijdig" else ("$(g, \\infty)$" if test_type == "rechtszijdig" else "$(-\infty, g_1)$ en $(g_2, \\infty)$")}, waarbij we de grenswaarde{"n" if test_type == "tweezijdig" else ""} als volgt berekenen:\n"
        f"\\begin{{align*}}\n"
        f"    \ldots\n"
        f"\\end{{align*}}\n"
        f"Het kritieke gebied is dus gelijk aan $\\ldots$\n"
        f"Aangezien de geobserveerde toetsingsgrootheid ${lower} \\approx {value:.4f}$ {"niet" if not runner.reject_H0 else ""} in het kritieke gebied ligt, besluiten we om $H_0$ {"niet" if runner.reject_H0 else ""} te verwerpen."
    )

    # --- STAP 6: Conclusie in context ---
    conclusion_text = (
        f"Er is {'voldoende' if rejected else 'onvoldoende'} reden om op basis van deze steekproef "
        f"de nulhypothese te verwerpen in de context van het probleem."
    )

    # Samenvoegen in de strakke 6-stappenstructuur
    latex_output = rf"""
\subsubsection*{{Stap 1: formuleer de nulhypothese $H_0$ en de alternatieve hypothese $H_1$.}}
{intro_stap1}
\begin{{align*}}
    {h0_str} \\
    {h1_str} \rubric{{1}}
\end{{align*}}

\subsubsection*{{Stap 2: bepaal het significantieniveau $\alpha$.}}
{stap2_text}

\subsubsection*{{Stap 3: verzamel data voor het berekenen van de toetsingsgrootheid.}}
{stap3_text}

\subsubsection*{{Stap 4: bereken de toetsingsgrootheid.}}
{stap4_text}

\subsubsection*{{Stap 5: bepaal de toetsuitslag (met behulp van {"de $p$-waarde" if method == "pvalue" else "het kritieke gebied"}).}}
{p_value_text if method == "pvalue" else critical_value_text}

\subsubsection*{{Stap 6: vertaal de toetsuitslag terug naar de originele context van het probleem.}}
{conclusion_text}
"""
    return latex_output.strip()