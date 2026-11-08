"""
reporting/hypothesis_tests.py
Generates professional LaTeX snippets for hypothesis test solutions.
"""

def _base_report_template(test_name, stat_symbol, stat_val, p_val, alpha, region_str, decision_str, extra_info=""):
    """Internal helper to build a standardized LaTeX align block for grading keys."""
    decision_latex = "\\text{\\bf Reject } H_0" if decision_str == "Reject" else "\\text{\\bf Fail to reject } H_0"
    return f"""
\\begin{{align*}}
    \\textbf{{Test Type:}} & \\text{{{test_name}}} \\\\
    {extra_info}
    \\textbf{{{stat_symbol}:}} & {stat_val:.4f} \\\\
    \\textbf{{p-value:}} & {p_val:.4e} (\\alpha = {alpha}) \\\\
    \\textbf{{Critical Region:}} & {region_str} \\\\
    \\textbf{{Decision:}} & {decision_latex}
\\end{{align*}}
"""

def report_z_test(result, alpha=0.05):
    decision = "Reject" if result["p_value"] < alpha else "Fail"
    extra = f"\\textbf{{Parameters:}} & \\overline{{x}} = {result['x_bar']:.4f}, \\, n = {result['n']} \\\\"
    return _base_report_template(
        test_name="one-sample $z$-test",
        stat_symbol="$z$",
        stat_val=result["statistic"],
        p_val=result["p_value"],
        alpha=alpha,
        region_str=result["region"],
        decision_str=decision,
        extra_info=extra
    )

def report_t_test_one_sample(result, alpha=0.05):
    decision = "Reject" if result["p_value"] < alpha else "Fail"
    extra = f"\\textbf{{Parameters:}} & \\overline{{x}} = {result['x_bar']:.4f}, \\, s = {result['s']:.4f}, \\, n = {result['n']} \\\\\n\\textbf{{Degrees of Freedom:}} & \\text{{df}} = {result['df']} \\\\"
    return _base_report_template(
        test_name="one-sample $t$-test",
        stat_symbol="$t$",
        stat_val=result["statistic"],
        p_val=result["p_value"],
        alpha=alpha,
        region_str=result["region"],
        decision_str=decision,
        extra_info=extra
    )

def report_t_test_two_sample(result, alpha=0.05):
    decision = "Reject" if result["p_value"] < alpha else "Fail"
    extra = f"\\text{{Degrees of Freedom:}} & \\text{{df}} = {result['df']:.2f} \\\\\n"
    return _base_report_template(
        test_name=result["test"],
        stat_symbol="$t$",
        stat_val=result["statistic"],
        p_val=result["p_value"],
        alpha=alpha,
        region_str=result["region"],
        decision_str=decision,
        extra_info=extra
    )

def report_chi_square_gof(result, alpha=0.05):
    decision = "Reject" if result["p_value"] < alpha else "Fail"
    extra = f"\\text{{Degrees of Freedom:}} & \\text{{df}} = {result['df']} \\\\\n"
    return _base_report_template(
        test_name="chi-square goodness-of-fit test",
        stat_symbol="$\\chi^2$",
        stat_val=result["statistic"],
        p_val=result["p_value"],
        alpha=alpha,
        region_str=result["region"],
        decision_str=decision,
        extra_info=extra
    )

def report_chi_square_independence(result, alpha=0.05):
    decision = "Reject" if result["p_value"] < alpha else "Fail"
    extra = f"\\text{{Degrees of Freedom:}} & \\text{{df}} = {result['df']} \\\\\n"
    return _base_report_template(
        test_name="chi-square independence test",
        stat_symbol="$\\chi^2$",
        stat_val=result["statistic"],
        p_val=result["p_value"],
        alpha=alpha,
        region_str=result["region"],
        decision_str=decision,
        extra_info=extra
    )

def report_f_test_variances(result, alpha=0.05):
    decision = "Reject" if result["p_value"] < alpha else "Fail"
    dfn, dfd = result["df"]
    extra = f"\\text{{Degrees of Freedom:}} & \\text{{df}}_1 = {dfn}, \\, \\text{{df}}_2 = {dfd} \\\\\n"
    return _base_report_template(
        test_name="$f$-test for equal variances",
        stat_symbol="F",
        stat_val=result["statistic"],
        p_val=result["p_value"],
        alpha=alpha,
        region_str=result["region"],
        decision_str=decision,
        extra_info=extra
    )