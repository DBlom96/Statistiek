def sample_mean(data):
    """Puntschatting van het populatiegemiddelde (mu) via steekproefgemiddelde."""
    return np.mean(data)

def sample_variance(data, ddof=1):
    """
    Puntschatting van de populatievariantie (σ²).
    ddof=1 voor steekproefvariantie (standaard).
    """
    return np.var(data, ddof=ddof)

def sample_std(data, ddof=1):
    return np.sqrt( sample_variance(data, ddof) )

def proportion_estimate(successes, num_trials):
    """
    Puntschatting van een populatieproportie (p̂).
    - Bij binaire data: successes = aantal successen, n = steekproefgrootte.
    - Bij array input: successes = lijst/array met 0/1 waarden.
    """
    if isinstance(successes, (list, np.ndarray, pd.Series)) and num_trials is None:
        successes = np.sum(successes)
        num_trials = len(successes)
    elif num_trials is None:
        raise ValueError("n is verplicht als je alleen het aantal successen geeft.")
    
    return successes / num_trials

# Confidence intervals
def confidence_interval_normal(sample=None, sample_mean=0, sigma=1, sample_size=100, interval_type="tweezijdig", alpha=0.05):

    confidence_level = 1 - alpha
    confidence_percentage = int(100 * confidence_level)
    
    if sigma:
        z = norm.ppf(1-alpha/2)
        left = sample_mean - z * sigma / sqrt(sample_size)
        right = sample_mean + z * sigma / sqrt(sample_size)

        latex_code = f"""
            Omdat $\\sigma = {sigma}$ bekend is, kunnen we de normale verdeling gebruiken.
            De $z$-waarde die hoort bij $\\SI{{{confidence_percentage}}}{{\\percent}}$ betrouwbaarheid, oftewel $\\alpha = {alpha}$, is (in het geval van tweezijdige intervallen) gelijk aan
            \\[
                z_{{\\alpha/2}} = \\invnorm(\\opp=1-\\frac{{\\alpha}}{{2}}) = \\invnorm(\\opp={1-alpha/2}) \\approx {pretty_print(z)}.
            \\]
            Het \\SI{{{confidence_percentage}}}{{\\percent}}-betrouwbaarheidsinterval wordt dan gegeven door
            \\begin{{align*}}
                [\\overline{{x}} - z_{{\\alpha/2}} \\cdot \\frac{{ \\sigma }}{{ \\sqrt{{ n }} }}, \\overline{{x}} + z_{{\\alpha/2}} \\cdot \\frac{{ \\sigma }}{{ \\sqrt{{ n }} }}] \\\\
                &= [{pretty_print(sample_mean)} - {pretty_print(z)} \\cdot \\frac{{ {pretty_print(sigma)} }}{{ \\sqrt{{ {pretty_print(sample_size)} }} }}, {pretty_print(sample_mean)} + {pretty_print(z)} \\cdot \\frac{{ {pretty_print(sigma)} }}{{ \\sqrt{{ {pretty_print(sample_size)} }} }}] \\\\
                &= [{pretty_print(left)}, {pretty_print(right)}].
            \\end{{align*}}
        """
    else:
        if sample_size >= 30:
            z = norm.ppf(1-alpha/2)
            left = sample_mean - z * sample_std / sqrt(sample_size)
            right = sample_mean + z * sample_std / sqrt(sample_size)
    
            latex_code = f"""
                Hoewel $\\sigma$ onbekend is, kunnen we toch met de normale benadering werken omdat de steekproefgrootte $n = {sample_size} \\ge 30$ is.
                Hierbij mogen we de onbekende $\\sigma$ schatten met de steekproefstandaardafwijking $s$.
                De $z$-waarde die hoort bij \\SI{{{confidence_percentage}}}{{\\percent}} betrouwbaarheid, oftewel $\\alpha = {alpha}$, is (in het geval van tweezijdige intervallen) gelijk aan
                \\[
                    z_{{\\alpha/2}} = \\invnorm(\\opp=1-\\frac{{\\alpha}}{{2}}) = \\invnorm(\\opp={1-alpha/2}) \\approx {pretty_print(z)}.
                \\]
                Het \\SI{{{confidence_percentage}}}{{\\percent}}-betrouwbaarheidsinterval wordt dan gegeven door
                \\begin{{align*}}
                    [\\overline{{x}} - z_{{\\alpha/2}} \\cdot \\frac{{ s }}{{ \\sqrt{{ n }} }}, \\overline{{x}} + z_{{\\alpha/2}} \\cdot \\frac{{ s }}{{ \\sqrt{{ n }} }}] \\\\
                    &= [{pretty_print(sample_mean)} - {pretty_print(z)} \\cdot \\frac{{ {pretty_print(sample_std)} }}{{ \\sqrt{{ {pretty_print(sample_size)} }} }}, {pretty_print(sample_mean)} + {pretty_print(z)} \\cdot \\frac{{ {pretty_print(sample_std)} }}{{ \\sqrt{{ {pretty_print(sample_size)} }} }}] \\\\
                    &= [{pretty_print(left)}, {pretty_print(right)}].
                \\end{{align*}}
            """
        else:
            tval = t.ppf(1-alpha/2, df=sample_size-1)
            left = sample_mean - tval * sample_std / sqrt(sample_size)
            right = sample_mean + tval * sample_std / sqrt(sample_size)
    
            latex_code = f"""
                Omdat $\\sigma$ onbekend is en de steekproefgrootte $n = {sample_size} < 30$ is, moeten we gebruik maken van de $t$-verdeling.
                De $t$-waarde die hoort bij \\SI{{{confidence_percentage}}}{{\\percent}} betrouwbaarheid, oftewel $\\alpha = {alpha}$, is (in het geval van tweezijdige intervallen) gelijk aan
                \\[
                    t = \\invt(\\opp=1-\\frac{{\\alpha}}{{2}}, \\df=n-1) = \\invt(\\opp={1-alpha/2}, \\df={sample_size-1}) \\approx {pretty_print(tval)}.
                \\]
                Het \\SI{{{confidence_percentage}}}{{\\percent}}-betrouwbaarheidsinterval wordt dan gegeven door
                \\begin{{align*}}
                    [\\samplemeanx - t \\cdot \\frac{{ \\samplestd }}{{ \\sqrt{{ n }} }}, \\samplemeanx + t \\cdot \\frac{{ \\samplestd }}{{ \\sqrt{{ n }} }}] \\\\
                    &= [{pretty_print(sample_mean)} - {pretty_print(tval)} \\cdot \\frac{{ {pretty_print(sample_std)} }}{{ \\sqrt{{ {pretty_print(sample_size)} }} }}, {pretty_print(sample_mean)} + {pretty_print(tval)} \\cdot \\frac{{ {pretty_print(sample_std)} }}{{ \\sqrt{{ {pretty_print(sample_size)} }} }}] \\\\
                    &= [{pretty_print(left)}, {pretty_print(right)}].
                \\end{{align*}}
            """
    print(latex_code)

confidence_interval_normal(sample_mean=14.1, sample_std=1.4, sample_size=18, alpha=0.05)

def minimale_steekproefgrootte(sample_std=1, sigma=None, afwijking=1, alpha=0.05):
    confidence_level = 1 - alpha
    confidence_percentage = int(100 * confidence_level)

    if sigma:
        z = norm.ppf(1-alpha/2)
        n = (z * sigma / afwijking) ** 2
        latex_code = f"""
            Omdat $\\sigma = {sigma}$ bekend is, kunnen we de normale verdeling gebruiken.
            De $z$-waarde die hoort bij \\SI{{{confidence_percentage}}}{{\\percent}} betrouwbaarheid, oftewel $\\alpha = {alpha}$, is (in het geval van tweezijdige intervallen) gelijk aan
            \\[
                z_{{\\alpha/2}} = \\invnorm(\\opp=1-\\frac{{\\alpha}}{{2}}) = \\invnorm(\\opp={1-alpha/2}) \\approx {pretty_print(z)}.
            \\]
            De minimale benodigde steekproefgrootte $n$ zodat het \\SI{{{confidence_percentage}}}{{\\percent}}-betrouwbaarheidsinterval maximaal $\\pm {afwijking}$ afwijkt is gelijk aan:
            \\begin{{align*}}
                n \\ge \\left( \\frac{{ z_{{\\alpha/2}} \\cdot \\sigma }}{{ a }} \\right)^2 = \\left( \\frac{{ {pretty_print(z)} \\cdot {pretty_print(sigma)} }}{{ {afwijking} }}\\right)^2 \\approx {pretty_print(n)}. 
            \\end{{align*}}

            Naar boven afronden geeft een minimale steekproefgrootte van $n = {int(ceil(n))}$.
        """
    else:
        sample_size = 2
        tval = t.ppf(1-alpha/2, df=sample_size-1)
        width = sample_std / sqrt(sample_size) * tval
        while width > afwijking:
            sample_size += 1
            tval = t.ppf(1-alpha/2, df=sample_size-1)
            width = sample_std / sqrt(sample_size) * tval

        print(width, sample_size)
        previous_width = sample_std / sqrt(sample_size-1) * t.ppf(1-alpha/2, df=sample_size-2)
        latex_code = f"""
            Omdat $\\sigma = {sigma}$ onbekend is, moeten we terugvallen op de $t$-verdeling.
            Hiertoe voeren we op de grafische rekenmachine het volgende in in het functiescherm:
            \\[
                y_1 = s / \\sqrt{{X}} \\cdot \\invt(\\opp=1-\\alpha/2, \\df=X-1) = 1.4 / \\sqrt{{X}} \\cdot \\invt(\\opp={pretty_print(1-alpha/2)}, \\df=X-1)
            \\]
            Met behulp van de tabelfunctie krijgen we dan als volgt:
            \\begin{{align*}}
                X = {sample_size-1}: &\\quad {sample_std} / \\sqrt{{{sample_size-1}}} \\cdot \\invt(\\opp={pretty_print(1-alpha/2)}, \\df={sample_size-2}) \\approx {previous_width}. \\\\
                X = {sample_size}: &\\quad {sample_std} / \\sqrt{{{sample_size}}} \\cdot \\invt(\\opp={pretty_print(1-alpha/2)}, \\df={sample_size-1}) \\approx {width}.
            \\end{{align*}}
            We vinden dus een minimale steekproefgrootte van $n = {sample_size}$.
        """
    print(latex_code)

minimale_steekproefgrootte(sample_std=1.4, sigma=None, afwijking=0.1, alpha=0.05)

def prediction_interval_normal(mu=0, sigma=1, alpha=0.05, width=8, height=5, filename="test_prediction_interval.png"):
    variable_name = "Z" if mu == 0 and sigma == 1 else "X"

    xmin, xmax = mu - 4 * sigma, mu + 4 * sigma
    x = np.linspace(xmin, xmax, 1000)
    y = norm.pdf(x, mu, sigma)
    confidence_level = 1 - alpha
    confidence_percentage = int(100 * confidence_level)

    left = norm.ppf(alpha / 2, mu, sigma)
    right = norm.ppf(1 - alpha / 2, mu, sigma)
    
    # Plot characterization
    fig, ax = plt.subplots(figsize=(width, height))
    
    ax.plot(x, y, color=primary_plot_color)
    ax.fill_between(x, y, where=((x >= left)&(x<=right)), color=acceptable_color, alpha=opacity_level)
    ax.fill_between(x, y, where=((x <= left)|(x>=right)), color=critical_color, alpha=opacity_level)

    ymin, ymax = ax.get_ylim()
    ytext, offset = get_y_annotation(ax)
    ax.set_ylim(ymin - 2 * offset, ymax)

    ax.plot([left, left], [0, norm.pdf(left, mu, sigma)], color=primary_plot_color, linestyle='--', label = f"$-z_{{\\alpha/2}} \\approx {pretty_print(left)}$")
    ax.text(left, ytext, "$-z_{\\alpha/2}$", color=primary_plot_color, ha="center", va="center")
    ax.text( (xmin+left) / 2, -ytext, f"opp$=\\alpha/2={alpha/2}$", color=critical_color, ha="center", va="center")

    ax.text( (left+right) / 2, -ytext, f"opp$=1-\\alpha={1-alpha}$", color=acceptable_color, ha="center", va="center")

    ax.plot([right, right], [0, norm.pdf(right, mu, sigma)], color=primary_plot_color, linestyle='--', label = f"$z_{{\\alpha/2}} \\approx {pretty_print(right)}$")
    ax.text(right, ytext, "$z_{\\alpha/2}$", color=primary_plot_color, ha="center", va="center")
    ax.text( (xmax+right) / 2, -ytext, f"opp$=\\alpha/2={alpha/2}$", color=critical_color, ha="center", va="center")

    if mu == 0 and sigma == 1:
        ax.set_title(f'${confidence_percentage}\\%$-voorspellingsinterval voor $Z \\sim N(0,1)$')
    else:
        ax.set_title(f'${confidence_percentage}\\%$-voorspellingsinterval voor $\\overline{{X}} \\sim N(\\mu={mu}, \\sigma={sigma})$')
    # plt.title(f"Voorspellingsinterval: $[{left:.4f}, {right:.4f}]$")

    if variable_name == "Z":
        ax.set_xlabel('$z$')
        ax.set_ylabel('Standaardnormale kansdichtheidsdfunctie $f(z)$')
    else:
        ax.set_xlabel('$x$')
        ax.set_ylabel('Normale kansdichtheidsdfunctie $f(x)$')
    
    plt.legend()#loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    plt.tight_layout()

    # Save figure
    plt.savefig(filename)

def prediction_interval_t(df=5, alpha=0.05, width=8, height=5, filename="test_prediction_interval_t.png"):
    variable_name = "T"

    xmin, xmax = -4, 4
    x = np.linspace(xmin, xmax, 1000)
    y = t.pdf(x, df)
    confidence_level = 1 - alpha
    confidence_percentage = int(100 * confidence_level)

    left = t.ppf(alpha / 2, df)
    right = -left
    
    # Plot characterization
    fig, ax = plt.subplots(figsize=(width, height))
    
    ax.plot(x, y, color=primary_plot_color)
    ax.fill_between(x, y, where=((x >= left)&(x<=right)), color=acceptable_color, alpha=opacity_level)
    ax.fill_between(x, y, where=((x <= left)|(x>=right)), color=critical_color, alpha=opacity_level)

    ymin, ymax = ax.get_ylim()
    ytext, offset = get_y_annotation(ax)
    ax.set_ylim(ymin - 2 * offset, ymax)

    ax.plot([left, left], [0, t.pdf(left, df)], color=primary_plot_color, linestyle='--', label = f"$-t_{{n-1,\\alpha/2}} \\approx {pretty_print(left)}$")
    ax.text(left, ytext, "$-t_{n-1,\\alpha/2}$", color=primary_plot_color, ha="center", va="center")
    ax.text( (xmin+left) / 2, -ytext, f"opp$=\\alpha/2={alpha/2}$", color=critical_color, ha="center", va="center")

    ax.text( (left+right) / 2, -ytext, f"opp$=1-\\alpha={1-alpha}$", color=acceptable_color, ha="center", va="center")

    ax.plot([right, right], [0, t.pdf(right, df)], color=primary_plot_color, linestyle='--', label = f"$t_{{n-1,\\alpha/2}} \\approx {pretty_print(right)}$")
    ax.text(right, ytext, "$t_{n-1,\\alpha/2}$", color=primary_plot_color, ha="center", va="center")
    ax.text( (xmax+right) / 2, -ytext, f"opp$=\\alpha/2={alpha/2}$", color=critical_color, ha="center", va="center")

    ax.set_title(f'${confidence_percentage}\\%$-voorspellingsinterval voor $T \\sim t(\\text{{df}}=n-1)$')
    # plt.title(f"Voorspellingsinterval: $[{left:.4f}, {right:.4f}]$")

    ax.set_xlabel('$t$')
    ax.set_ylabel('Kansdichtheidsfunctie $f(t)$')
    
    plt.legend()#loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    plt.tight_layout()

    # Save figure
    plt.savefig(filename)
    