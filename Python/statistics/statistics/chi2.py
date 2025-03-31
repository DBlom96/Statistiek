import numpy as np
from scipy.stats import chi2

def compute_expected_frequencies(data):
    row_totals = data.sum(axis=1)
    col_totals = data.sum(axis=0)
    grand_total = data.sum()
    nrows, ncols = data.shape

    # Calculate expected frequencies
    expected = np.zeros_like(data, dtype=float)
    for row in range(nrows):
        for col in range(ncols):
            expected[row, col] = (row_totals[row] * col_totals[col]) / grand_total
    
    # Display results
    print("Geobserveerde frequenties:")
    print(data)
    print("Verwachte frequenties:")
    print(expected)
    return expected

def compute_chi2_test_statistic(data, expected):
    stat = np.sum( (data - expected) ** 2 / expected ) 
    print(f"De $\\chi^2$-toetsingsgrootheid is gelijk aan {stat:.4f}")
    return stat

def compute_degrees_of_freedom(data):
    nrows, ncols = data.shape
    df = (nrows-1)*(ncols-1)
    print(f"Het aantal vrijheidsgraden is gelijk aan $\\text{{df}}={df}$")
    return df

def compute_chi2_p_value(test_statistic, df):
    p_value = 1 - chi2.cdf(test_statistic, df)
    print(f"""De $p$-waarde die hoort bij een toetsingsgrootheid $\\chi^2 = {test_statistic:.4f}$
          op basis van de chikwadraatverdeling met {df} {"vrijheidsgraad" if df == 1 else "vrijheidsgraden"} is gelijk aan 
          $p = \\chi^2\\cdf({test_statistic:.4f}; 10^{{99}}; \\text{{df}}={df})\\approx {p_value:.4f}$.
          """
    )

    return p_value

def exam_question():
    data = np.array([
        [30, 20],  # Rij voor "Man"
        [25, 25]   # Rij voor "Vrouw"
    ])

    # Bereken de verwachte frequenties 
    expected = compute_expected_frequencies(data)

    # Bereken de chikwadraat toetsingsgrootheid
    stat = compute_chi2_test_statistic(data, expected)

    # Bepaal het aantal vrijheidsgraden
    df = compute_degrees_of_freedom(data)

    # Bepaal de p-waarde
    p_value = compute_chi2_p_value(stat, df)