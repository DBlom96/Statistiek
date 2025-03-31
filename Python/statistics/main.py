import numpy as np
import Python.statistics.statistics.chi2
#compute_expected_frequencies, compute_chi2_test_statistic, compute_degrees_of_freedom, compute_chi2_p_value

if __name__ == "__main__":
   
    # Question 1
    data = np.array([
        [30, 20],  # Rij voor "Man"
        [25, 25]   # Rij voor "Vrouw"
    ])

    statistics.chi2.exam_question()
