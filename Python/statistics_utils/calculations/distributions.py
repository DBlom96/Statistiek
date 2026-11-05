"""Probability calculations for custom and standard distributions.

The module offers one interface for probabilities and quantiles regardless of
whether a distribution is custom or supplied by SciPy.

Examples
--------
A standard normal distribution::

    normal = get_distribution("normal", mu=0, sigma=1)
    probability(normal, lower=-1.96, upper=1.96)
    boundary_values(normal, area=0.05, tail="center")

A binomial distribution::

    X = get_distribution("binomial", n=10, p=0.3)
    probability(X, lower=2, upper=5)
    boundary_values(X, area=0.05, tail="right")

A custom discrete distribution::

    custom = {0: 0.2, 1: 0.5, 2: 0.3}
    probability(custom, lower=1)
    boundary_values(custom, area=0.05, tail="right")

A custom continuous distribution::

    exponential = CustomContinuousDistribution(
        pdf=lambda x: 10 * np.exp(-10 * (x - 5)),
        support=(5, np.inf),
    )
    probability(exponential, lower=5.1)
    boundary_values(exponential, area=0.05, tail="right")

For custom continuous distributions, the PDF must integrate to one over the
provided support. CDF values and quantiles are calculated numerically.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import binom, chi2, f, norm, poisson, t

@dataclass
class CustomContinuousDistribution:
    """A continuous distribution specified by a PDF and its support.

    Parameters
    ----------
    pdf:
        A callable probability density function accepting a scalar x.
    support:
        Tuple ``(lower, upper)``. Either bound may be infinite, but the
        lower bound must be smaller than the upper bound.

    The PDF is numerically checked to integrate to one during initialization.
    The CDF is evaluated by numerical integration and quantiles by root
    finding. This is suitable for the custom distributions used in the
    teaching notebooks, including distributions with one infinite endpoint.
    """

    pdf: Callable[[float], float]
    support: tuple[float, float]

    def __post_init__(self):
        if not callable(self.pdf):
            raise TypeError("pdf must be callable")
        if len(self.support) != 2:
            raise ValueError("support must be a (lower, upper) tuple")

        lower, upper = map(float, self.support)
        if np.isnan(lower) or np.isnan(upper) or lower >= upper:
            raise ValueError("support must satisfy lower < upper")
        if lower == np.inf or upper == -np.inf:
            raise ValueError("support must have a valid lower and upper bound")

        self.support = (lower, upper)
        total, _ = quad(self._pdf_scalar, lower, upper)
        if not np.isclose(total, 1.0, atol=1e-6, rtol=1e-6):
            raise ValueError(
                "The PDF must integrate to 1 over its support; "
                f"the numerical integral is {total:.8g}."
            )

    def _pdf_scalar(self, x: float) -> float:
        value = float(self.pdf(x))
        if not np.isfinite(value) or value < 0:
            raise ValueError("pdf must return finite, non-negative values")
        return value

    def cdf(self, x):
        """Evaluate the cumulative distribution function at x."""
        values = np.asarray(x, dtype=float)

        def evaluate(value):
            lower, upper = self.support
            if value <= lower:
                return 0.0
            if value >= upper:
                return 1.0
            result, _ = quad(self._pdf_scalar, lower, float(value))
            return float(np.clip(result, 0.0, 1.0))

        result = np.vectorize(evaluate, otypes=[float])(values)
        return float(result) if result.ndim == 0 else result

    def sf(self, x):
        """Evaluate the survival function P(X > x)."""
        result = 1.0 - np.asarray(self.cdf(x))
        return float(result) if result.ndim == 0 else result

    def ppf(self, q):
        """Evaluate quantiles by numerical root finding."""
        probabilities = np.asarray(q, dtype=float)
        if np.any(~np.isfinite(probabilities)) or np.any(
            (probabilities < 0) | (probabilities > 1)
        ):
            raise ValueError("q must lie in [0, 1]")

        def evaluate(probability_value):
            lower, upper = self.support
            if probability_value == 0:
                return lower
            if probability_value == 1:
                return upper

            # Establish a finite bracket. This also supports one- or
            # two-sided unbounded supports.
            if np.isneginf(lower) and np.isposinf(upper):
                left, right = -1.0, 1.0
                while self.cdf(left) > probability_value:
                    left *= 2
                while self.cdf(right) < probability_value:
                    right *= 2
            elif np.isneginf(lower):
                right = upper
                step = max(1.0, abs(right))
                left = right - step
                while self.cdf(left) > probability_value:
                    step *= 2
                    left = right - step
            elif np.isposinf(upper):
                left = lower
                step = max(1.0, abs(left))
                right = left + step
                while self.cdf(right) < probability_value:
                    step *= 2
                    right = left + step
            else:
                left, right = lower, upper

            return float(
                brentq(
                    lambda value: self.cdf(value) - probability_value,
                    left,
                    right,
                )
            )

        result = np.vectorize(evaluate, otypes=[float])(probabilities)
        return float(result) if result.ndim == 0 else result

    def pdf_value(self, x):
        """Evaluate the PDF, returning zero outside the declared support."""
        values = np.asarray(x, dtype=float)
        lower, upper = self.support
        result = np.vectorize(
            lambda value: self._pdf_scalar(float(value))
            if lower <= value <= upper
            else 0.0,
            otypes=[float],
        )(values)
        return float(result) if result.ndim == 0 else result


def get_distribution(name: str, **parameters):
    """Return a frozen SciPy distribution.

    Supported names and parameters:

    - ``normal``: ``mu`` and ``sigma`` (or SciPy's ``loc`` and ``scale``)
    - ``binomial``: ``n`` and ``p``
    - ``poisson``: ``mu`` (or ``lambda_``)
    - ``t``: ``df``
    - ``f``: ``dfn`` and ``dfd``
    - ``chi2``: ``df``

    SciPy's ``loc`` and ``scale`` parameters are also passed through where
    supported. For example, ``get_distribution("normal", mu=10, sigma=2)``.
    """
    key = name.lower().replace("-", "_").replace(" ", "_")
    params = dict(parameters)

    if key in {"normal", "norm", "gaussian"}:
        if "mu" in params:
            params["loc"] = params.pop("mu")
        if "mean" in params:
            params["loc"] = params.pop("mean")
        if "sigma" in params:
            params["scale"] = params.pop("sigma")
        if "sd" in params:
            params["scale"] = params.pop("sd")
        if params.get("scale", 1) <= 0:
            raise ValueError("sigma/scale must be positive")
        return norm(**params)

    if key in {"binomial", "binom"}:
        if "n" not in params or "p" not in params:
            raise TypeError("binomial requires parameters n and p")
        if int(params["n"]) != params["n"] or params["n"] < 0:
            raise ValueError("n must be a non-negative integer")
        if not 0 <= params["p"] <= 1:
            raise ValueError("p must lie in [0, 1]")
        return binom(**params)

    if key in {"poisson", "pois"}:
        if "lambda_" in params:
            params["mu"] = params.pop("lambda_")
        if "mu" not in params:
            raise TypeError("poisson requires parameter mu (or lambda_)")
        if params["mu"] < 0:
            raise ValueError("mu must be non-negative")
        return poisson(**params)

    if key in {"t", "student_t", "student"}:
        if "df" not in params:
            raise TypeError("t distribution requires parameter df")
        if params["df"] <= 0:
            raise ValueError("df must be positive")
        return t(**params)

    if key in {"f", "fisher", "fisher_f"}:
        if "dfn" not in params or "dfd" not in params:
            raise TypeError("F distribution requires parameters dfn and dfd")
        if params["dfn"] <= 0 or params["dfd"] <= 0:
            raise ValueError("dfn and dfd must be positive")
        return f(**params)

    if key in {"chi2", "chisquare", "chi_square", "chi_squared"}:
        if "df" not in params:
            raise TypeError("chi-square distribution requires parameter df")
        if params["df"] <= 0:
            raise ValueError("df must be positive")
        return chi2(**params)

    raise ValueError(
        "Unknown distribution. Choose normal, binomial, poisson, t, f, or chi2."
    )


def _scipy_distribution_kind(distribution):
    """Identify a frozen SciPy distribution without relying on private classes."""
    scipy_dist = getattr(distribution, "dist", None)
    if scipy_dist is None:
        return None
    if not callable(getattr(distribution, "cdf", None)) or not callable(
        getattr(distribution, "ppf", None)
    ):
        return None
    if callable(getattr(scipy_dist, "pmf", None)):
        return "discrete"
    if callable(getattr(scipy_dist, "pdf", None)):
        return "continuous"
    return None


def _validate_discrete_distribution(distribution, atol=1e-9):
    if not isinstance(distribution, Mapping) or not distribution:
        raise ValueError("A custom discrete distribution must be a non-empty mapping")

    outcomes = np.asarray(list(distribution.keys()), dtype=float)
    probabilities = np.asarray(list(distribution.values()), dtype=float)
    if not np.all(np.isfinite(outcomes)):
        raise ValueError("Discrete outcomes must be finite numeric values")
    if not np.all(np.isfinite(probabilities)) or np.any(probabilities < 0):
        raise ValueError("Probabilities must be finite and non-negative")
    if not np.isclose(probabilities.sum(), 1.0, atol=atol):
        raise ValueError("Probabilities must sum to 1")

    order = np.argsort(outcomes)
    return outcomes[order], probabilities[order]


def validate_distribution(probability_dict, atol=1e-9):
    """Validate a custom discrete distribution; return True if it is valid."""
    _validate_discrete_distribution(probability_dict, atol=atol)
    return True


def compute_expected_value(probability_dict):
    """Compute E[X] for a custom discrete distribution {x: P(X=x)}."""
    outcomes, probabilities = _validate_discrete_distribution(probability_dict)
    return float(np.dot(outcomes, probabilities))


def compute_variance(probability_dict):
    """Compute Var(X) for a custom discrete distribution {x: P(X=x)}."""
    outcomes, probabilities = _validate_discrete_distribution(probability_dict)
    mean = np.dot(outcomes, probabilities)
    return float(np.dot((outcomes - mean) ** 2, probabilities))


def compute_standard_deviation(probability_dict):
    """Compute the standard deviation of a custom discrete distribution."""
    return float(np.sqrt(compute_variance(probability_dict)))


def probability(distribution, lower=None, upper=None, closed="both"):
    """Compute a probability over an interval or tail.

    Parameters
    ----------
    distribution:
        A custom discrete mapping, a ``CustomContinuousDistribution``, or a
        frozen SciPy distribution returned by :func:`get_distribution`.
    lower, upper:
        Interval boundaries. Use ``None`` for an unbounded side. If both are
        ``None``, the result is 1.
    closed:
        Endpoint convention: ``"both"`` for [lower, upper], ``"left"`` for
        [lower, upper), ``"right"`` for (lower, upper], or ``"neither"`` for
        (lower, upper). This matters only for discrete distributions.

    Examples
    --------
    ``probability(normal, upper=1.5)`` computes P(X <= 1.5).
    ``probability(binom, lower=3, upper=6)`` computes P(3 <= X <= 6).
    ``probability(custom_pdf, lower=5.1)`` computes P(X >= 5.1).
    """
    if closed not in {"both", "left", "right", "neither"}:
        raise ValueError("closed must be 'both', 'left', 'right', or 'neither'")
    if lower is not None and upper is not None and lower > upper:
        raise ValueError("lower must not exceed upper")

    if isinstance(distribution, Mapping):
        outcomes, probabilities = _validate_discrete_distribution(distribution)
        mask = np.ones(outcomes.size, dtype=bool)
        if lower is not None:
            mask &= outcomes >= lower if closed in {"both", "left"} else outcomes > lower
        if upper is not None:
            mask &= outcomes <= upper if closed in {"both", "right"} else outcomes < upper
        return float(probabilities[mask].sum())

    if isinstance(distribution, CustomContinuousDistribution):
        cdf_function = distribution.cdf
        sf_function = distribution.sf
    elif _scipy_distribution_kind(distribution) == "continuous":
        cdf_function = distribution.cdf
        sf_function = distribution.sf
    elif _scipy_distribution_kind(distribution) == "discrete":
        # SciPy's discrete distributions used here have integer support.
        # Translate real-valued interval endpoints to integer cutoffs.
        if lower is None:
            lower_cdf = 0.0
        elif closed in {"both", "left"}:
            lower_cdf = float(distribution.cdf(np.ceil(lower) - 1))
        else:
            lower_cdf = float(distribution.cdf(np.floor(lower)))

        if upper is None:
            upper_cdf = 1.0
        elif closed in {"both", "right"}:
            upper_cdf = float(distribution.cdf(np.floor(upper)))
        else:
            upper_cdf = float(distribution.cdf(np.ceil(upper) - 1))

        if lower is None and upper is None:
            return 1.0
        result = upper_cdf - lower_cdf
        return float(np.clip(result, 0.0, 1.0))
    else:
        raise TypeError(
            "Unsupported distribution. Use a probability mapping, "
            "CustomContinuousDistribution, or a frozen SciPy distribution."
        )

    # Continuous variables assign zero probability to a single endpoint, so
    # endpoint inclusion does not change the answer.
    if lower is None and upper is None:
        return 1.0
    if lower is None:
        return float(cdf_function(upper))
    if upper is None:
        return float(sf_function(lower))

    # Use survival probabilities for intervals in the upper tail to reduce
    # cancellation when both CDF values are close to one.
    if lower > 0:
        result = sf_function(lower) - sf_function(upper)
    else:
        result = cdf_function(upper) - cdf_function(lower)
    return float(np.clip(result, 0.0, 1.0))


def boundary_values(distribution, area=0.05, tail="center"):
    """Compute quantile boundaries for a left, right, or central tail area.

    ``area`` is the probability in the selected tail. For ``tail="center"``
    it is the combined probability in both tails. For example, a 95% central
    interval uses ``area=0.05``.

    For discrete distributions, the inverse-CDF convention is used: the
    returned quantile is the smallest value whose CDF is at least the target
    probability. Actual tail probabilities can therefore differ from
    ``area`` because of probability mass at individual values.

    Returns one number for a one-sided tail, or ``(lower, upper)`` for a
    central interval.
    """
    if not 0 < area < 1:
        raise ValueError("area must be between 0 and 1")
    if tail not in {"left", "right", "center"}:
        raise ValueError("tail must be 'left', 'right', or 'center'")

    if isinstance(distribution, Mapping):
        outcomes, probabilities = _validate_discrete_distribution(distribution)
        cumulative = np.cumsum(probabilities)

        def quantile(q):
            index = np.searchsorted(cumulative, q, side="left")
            return float(outcomes[min(index, len(outcomes) - 1)])

    elif isinstance(distribution, CustomContinuousDistribution):
        quantile = distribution.ppf
    elif _scipy_distribution_kind(distribution) in {"continuous", "discrete"}:
        quantile = distribution.ppf
    else:
        raise TypeError(
            "Unsupported distribution. Use a probability mapping, "
            "CustomContinuousDistribution, or a frozen SciPy distribution."
        )

    if tail == "left":
        return float(quantile(area))
    if tail == "right":
        return float(quantile(1 - area))
    return float(quantile(area / 2)), float(quantile(1 - area / 2))


def compute_probability(distribution, lower=None, upper=None, closed="both"):
    """Alias of :func:`probability` with an explicit compute_ prefix."""
    return probability(distribution, lower=lower, upper=upper, closed=closed)


def compute_probabilities(left=None, right=None, mu=0, sigma=1, distribution=None):
    """Compatibility wrapper for the former normal-only function.

    New code should pass a distribution as the first argument to
    :func:`probability`. This wrapper retains the previous ``left``/``right``
    and ``mu``/``sigma`` interface, while allowing any supported distribution
    via the ``distribution`` keyword.
    """
    if distribution is None:
        distribution = get_distribution("normal", mu=mu, sigma=sigma)
    return probability(distribution, lower=left, upper=right)


def compute_boundary_values(area=0.05, mu=0, sigma=1, tail="left", distribution=None):
    """Compatibility wrapper for the former normal-only boundary function.

    New code should call ``boundary_values(distribution, area, tail)``.
    If no distribution is supplied, a normal distribution N(mu, sigma^2) is
    used, preserving the old call pattern.
    """
    if distribution is None:
        distribution = get_distribution("normal", mu=mu, sigma=sigma)
    return boundary_values(distribution, area=area, tail=tail)


def probability_equal(distribution, value):
    """Return P(X = value). For continuous distributions this is zero."""
    return probability(distribution, lower=value, upper=value)


def probability_less_equal(distribution, value):
    """Return P(X <= value)."""
    return probability(distribution, upper=value)


def probability_greater_equal(distribution, value):
    """Return P(X >= value)."""
    return probability(distribution, lower=value)


# Short aliases for use in notebooks.
def P_equals(distribution, value):
    """Return P(X = value); this is zero for continuous distributions."""
    return probability(distribution, lower=value, upper=value)


def P_leq(distribution, value):
    """Return P(X <= value)."""
    return probability(distribution, upper=value)


def P_geq(distribution, value):
    """Return P(X >= value)."""
    return probability(distribution, lower=value)


def sample_discrete(probability_dict, size=1, random_state=None):
    """Draw random values from a custom discrete distribution."""
    outcomes, probabilities = _validate_discrete_distribution(probability_dict)
    if not isinstance(size, (int, np.integer)) or size < 0:
        raise ValueError("size must be a non-negative integer")
    rng = np.random.default_rng(random_state)
    return rng.choice(outcomes, size=size, p=probabilities)


# # Custom polynomial distribution used in the PMTPS mortar-impact example.
# def point_of_impact(x):
#     """PDF: 15/92 * (4 - x**2 - 3*x**4), for -1 <= x <= 1."""
#     values = np.asarray(x, dtype=float)
#     density = (15 / 92) * (4 - values**2 - 3 * values**4)
#     result = np.where((values >= -1) & (values <= 1), density, 0.0)
#     return float(result) if result.ndim == 0 else result


# def point_of_impact_cdf(x):
#     """CDF of the custom polynomial distribution on [-1, 1]."""
#     values = np.asarray(x, dtype=float)
#     result = 0.5 + (15 / 92) * (
#         4 * values - values**3 / 3 - 3 * values**5 / 5
#     )
#     result = np.where(values <= -1, 0.0, np.where(values >= 1, 1.0, result))
#     return float(result) if result.ndim == 0 else result


# def inverse_cdf(u):
#     """Inverse CDF of the custom polynomial distribution on [-1, 1]."""
#     probabilities = np.asarray(u, dtype=float)
#     if np.any(~np.isfinite(probabilities)) or np.any(
#         (probabilities < 0) | (probabilities > 1)
#     ):
#         raise ValueError("u must lie in [0, 1]")

#     def evaluate(q):
#         if q == 0:
#             return -1.0
#         if q == 1:
#             return 1.0
#         return float(
#             brentq(lambda value: point_of_impact_cdf(value) - q, -1, 1)
#         )

#     result = np.vectorize(evaluate, otypes=[float])(probabilities)
#     return float(result) if result.ndim == 0 else result


# def mortar_grenades(n, random_state=None):
#     """Generate n samples from the custom polynomial distribution."""
#     if not isinstance(n, (int, np.integer)) or n < 0:
#         raise ValueError("n must be a non-negative integer")
#     rng = np.random.default_rng(random_state)
#     return inverse_cdf(rng.random(n))


# # Backwards compatibility: the old generic names referred to the polynomial
# # distribution specifically. New code should prefer point_of_impact_cdf.
# cdf = point_of_impact_cdf
