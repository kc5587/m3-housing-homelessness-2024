"""Offline reproduction of selected regressions from the 2024 appendix."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from m3_analysis.data import SERIES, AnnualSeries
from m3_analysis.models import CurveFit, fit_exponential, fit_linear

FORECAST_YEARS = (2034, 2044, 2074)
LIMITATIONS = (
    "Disagreement between model forms is not a confidence interval",
    "In-sample R-squared is not evidence of out-of-sample forecast accuracy",
    "50-year extrapolations are historical illustrations, not policy forecasts",
    "Geographic scope and count definitions need external source validation",
)


def _plot(series: AnnualSeries, fit: CurveFit, output: Path) -> None:
    figure, axes = plt.subplots(2, 1, figsize=(9, 6), layout="constrained")
    axes[0].plot(series.years, series.values, "o", label="Appendix observations")
    axes[0].plot(series.years, fit.fitted_values, label=f"{fit.model} fit")
    axes[0].set(title=series.label, ylabel="Count")
    axes[0].legend()
    axes[1].plot(series.years, fit.residuals, "o-")
    axes[1].axhline(0, color="grey", linewidth=1)
    axes[1].set(xlabel="Year", ylabel="Residual (observed − fitted)")
    figure.suptitle(f"Historical fit only · in-sample R² = {fit.r_squared:.3f}")
    try:
        figure.savefig(output, dpi=150)
    finally:
        plt.close(figure)


def _fits() -> tuple[tuple[AnnualSeries, CurveFit], ...]:
    return tuple(
        (series, fit_function(series))
        for series in SERIES
        for fit_function in (
            (fit_linear, fit_exponential)
            if series.key.endswith("housing")
            else (fit_linear,)
        )
    )


def build_outputs(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    fits = _fits()
    observations = tuple(
        {"series": s.key, "year": year, "value": value, "source_page": s.source_page}
        for s in SERIES
        for year, value in zip(s.years, s.values, strict=True)
    )
    pd.DataFrame(observations).to_csv(output / "appendix_data.csv", index=False)
    results = {
        "historical_team_submission": True,
        "current_policy_forecast": False,
        "reconstruction_year": 2026,
        "limitations": LIMITATIONS,
        "fits": tuple({"series": s.key, **asdict(f)} for s, f in fits),
        "forecasts": tuple(
            {"series": s.key, "model": f.model, "year": year, "value": value}
            for s, f in fits
            for year, value in zip(
                FORECAST_YEARS, f.predict(FORECAST_YEARS), strict=True
            )
        ),
    }
    (output / "results.json").write_text(
        json.dumps(results, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    for series, fit in fits:
        _plot(series, fit, output / f"{series.key}_{fit.model}.png")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args(argv)
    build_outputs(args.output_dir)
    print(f"Historical reconstruction written to {args.output_dir}")


if __name__ == "__main__":
    main()
