"""Simple historical curve fits, not validated policy forecasting models."""

import warnings
from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import OptimizeWarning, curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from m3_analysis.data import AnnualSeries

MAX_FUNCTION_EVALUATIONS = 20_000
INITIAL_GROWTH_RATE = 0.02
CurveModel = Literal["linear", "exponential"]


def _exponential(
    x: NDArray[np.float64], a: float, b: float, c: float
) -> NDArray[np.float64]:
    return a * np.exp(b * x) + c


@dataclass(frozen=True)
class CurveFit:
    model: CurveModel
    origin_year: int
    parameters: tuple[float, ...]
    r_squared: float
    fitted_values: tuple[float, ...]
    residuals: tuple[float, ...]

    def predict(self, years: tuple[int, ...]) -> tuple[float, ...]:
        if not years:
            return ()
        x = np.asarray(years, dtype=float) - self.origin_year
        if not np.isfinite(x).all():
            raise ValueError("Prediction years must be finite")
        try:
            with np.errstate(over="raise", invalid="raise"):
                if self.model == "linear":
                    slope, intercept = self.parameters
                    result = slope * x + intercept
                else:
                    result = _exponential(x, *self.parameters)
        except FloatingPointError as exc:
            raise ValueError("Prediction overflow; extrapolation is unsafe") from exc
        if not np.isfinite(result).all():
            raise ValueError("Prediction returned nonfinite values")
        return tuple(float(value) for value in result)


def _result(
    series: AnnualSeries, model: CurveModel, parameters: tuple[float, ...]
) -> CurveFit:
    x = np.asarray(series.years, dtype=float) - series.years[0]
    y = np.asarray(series.values, dtype=float)
    if model == "linear":
        fitted = parameters[0] * x + parameters[1]
    else:
        fitted = _exponential(x, *parameters)
    return CurveFit(
        model,
        series.years[0],
        tuple(float(p) for p in parameters),
        float(r2_score(y, fitted)),
        tuple(float(v) for v in fitted),
        tuple(float(v) for v in y - fitted),
    )


def fit_linear(series: AnnualSeries) -> CurveFit:
    x = np.asarray(series.years, dtype=float) - series.years[0]
    model = LinearRegression().fit(x.reshape(-1, 1), series.values)
    return _result(series, "linear", (model.coef_[0], model.intercept_))


def fit_exponential(series: AnnualSeries) -> CurveFit:
    x = np.asarray(series.years, dtype=float) - series.years[0]
    # Scale-dependent initialisation differs from the screenshot's default p0.
    initial = (series.values[0], INITIAL_GROWTH_RATE, 0)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", OptimizeWarning)
            parameters, _ = curve_fit(
                _exponential,
                x,
                series.values,
                p0=initial,
                maxfev=MAX_FUNCTION_EVALUATIONS,
            )
    except (RuntimeError, ValueError, OptimizeWarning) as exc:
        raise ValueError(f"Exponential fit failed for {series.key}") from exc
    return _result(series, "exponential", tuple(float(p) for p in parameters))
