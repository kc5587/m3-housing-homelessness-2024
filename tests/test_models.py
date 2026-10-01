from dataclasses import FrozenInstanceError

import pytest

from m3_analysis.data import SERIES, AnnualSeries
from m3_analysis.models import fit_exponential, fit_linear


def test_linear_recovers_known_line() -> None:
    series = AnnualSeries("test", "Test", (2010, 2011, 2012), (10, 12, 14), 0)
    fit = fit_linear(series)
    assert fit.parameters == pytest.approx((2, 10))
    assert fit.r_squared == pytest.approx(1)
    assert fit.predict((2013, 2014)) == pytest.approx((16, 18))
    assert fit.residuals == pytest.approx((0, 0, 0))


def test_exponential_reproduces_historical_fit_quality() -> None:
    fit = fit_exponential(SERIES[0])
    assert fit.r_squared == pytest.approx(0.966, abs=0.001)
    assert all(value > 0 for value in fit.predict((2034, 2044, 2074)))


def test_albuquerque_homelessness_has_weak_time_fit() -> None:
    fit = fit_linear(SERIES[3])
    assert fit.r_squared == pytest.approx(0.042, abs=0.001)


@pytest.mark.parametrize(
    ("years", "values"),
    [
        ((), ()),
        ((2010, 2011), (1, 2)),
        ((2010, 2011, 2012), (1, 2)),
        ((2010, 2010, 2012), (1, 2, 3)),
        ((2012, 2011, 2010), (1, 2, 3)),
        ((2010, 2011, 2012), (1, float("nan"), 3)),
        ((2010, 2011, 2012), (1, float("inf"), 3)),
        ((2010, 2011, 2012), (1, -2, 3)),
        ((2010, 2011, 2012), (1, 1, 1)),
    ],
)
def test_invalid_series_is_rejected(years, values) -> None:
    with pytest.raises(ValueError):
        AnnualSeries("invalid", "Invalid", years, values, 0)


def test_series_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        SERIES[0].label = "Changed"


def test_series_rejects_mutable_input() -> None:
    with pytest.raises(ValueError, match="immutable"):
        AnnualSeries("invalid", "Invalid", [2010, 2011, 2012], (1, 2, 3), 0)


def test_exponential_fit_failure_is_explicit(monkeypatch) -> None:
    def fail(*args, **kwargs):
        raise RuntimeError("Solver did not converge")

    monkeypatch.setattr("m3_analysis.models.curve_fit", fail)
    with pytest.raises(ValueError, match="Exponential fit failed"):
        fit_exponential(SERIES[0])


def test_prediction_rejects_nonfinite_year() -> None:
    with pytest.raises(ValueError):
        fit_linear(SERIES[0]).predict((float("nan"),))


def test_prediction_handles_empty_request() -> None:
    assert fit_linear(SERIES[0]).predict(()) == ()


def test_exponential_prediction_reports_overflow() -> None:
    with pytest.raises(ValueError, match="overflow"):
        fit_exponential(SERIES[0]).predict((1_000_000,))
