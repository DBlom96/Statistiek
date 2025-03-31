from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression(x, y):
    # Fit the regression model

    model = LinearRegression()
    x = np.array(x).reshape(-1, 1)

    model.fit(x, y)

    slope = model.coef_[0]
    intercept = model.intercept_

    # Generate explanation
    explanation = (
        f"Een analyse van de lineaire regressie:\n"
        f"De regressielijn is gelijk aan $y = {slope:.2f}x + {intercept:.2f}$\n"
        f"1. De helling ({slope:.2f}) representeert de verandering in $y$ voor een stijging in $x$ van een eenheid.\n"
        f"2. Het snijpunt ({intercept:.2f}) met de $y$-as representeert de voorspelde waarde van $y$ in het geval dat $x = 0$.\n"
        f"3. Het model is gefit met behulp van de kleinstekwadratenmethode."
    )
    return {"slope": slope, "intercept": intercept, "explanation": explanation}
