# M3 Challenge 2024 — housing and homelessness

[![Checks](https://github.com/kc5587/m3-housing-homelessness-2024/actions/workflows/ci.yml/badge.svg)](https://github.com/kc5587/m3-housing-homelessness-2024/actions/workflows/ci.yml)

A historical team modelling report, with a small, tested Python reconstruction of selected appendix calculations.

**[Read the full 29-page report](report/team-17571-report.pdf)** · [Original code appendix](appendix/README.md) · [Provenance and limitations](PROVENANCE.md)

## The problem

Our five-person team investigated housing supply, affordability and homelessness in Seattle and Albuquerque for the 2024 MathWorks Math Modeling Challenge. I led the team during the 14-hour competition. Our reported result was a top-30 finish among 600+ teams.

The useful modelling question was not just which curve fit best. It was how much a conclusion changed when the model form changed. We compared linear and exponential housing-supply fits and considered the trade-off between fit quality, interpretability and extrapolation. The report also discusses affordability and potential interventions.

The original submission is preserved, including its assumptions and shortcomings. This repository does **not** present the report as current housing advice or as a validated causal analysis.

## What is original, and what is new?

| Material | Origin |
| --- | --- |
| Full report and code screenshots | 2024 team submission, recovered from 29 page images |
| `appendix/page-22.png` to `page-29.png` | Unchanged original code-appendix images |
| `src/m3_analysis/` | Selected calculations reconstructed and packaged in 2026, not an exact transcription of every original script |
| Tests, dependency lock and CI | Added in 2026 for reproducibility |

The new code covers four annual series: housing units for both cities (2010–2022) and homelessness counts for both cities (2007–2022). Housing series are fitted with linear and exponential curves; homelessness series with linear regression. It exports the transcribed observations, full-precision fit parameters, residual plots and historical extrapolations for 2034, 2044 and 2074.

This demonstrates Python, NumPy, pandas, scikit-learn, SciPy nonlinear optimisation, Matplotlib, input validation and automated testing. It is deliberately a compact reconstruction rather than a new research claim.

## Run offline

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/). No API keys, accounts or downloads of external datasets are required after installing dependencies.

```sh
uv sync --locked --group dev
uv run m3-reproduce --output-dir outputs
uv run pytest --cov=m3_analysis --cov-report=term-missing
uv run ruff check .
uv run ruff format --check .
```

Outputs are local and ignored by Git:

- `appendix_data.csv`: all 58 transcribed observations with source page numbers
- `results.json`: six fits, their residuals and illustrative extrapolations
- Six PNGs: observed values, fitted values and residuals

For example, the reconstructed Albuquerque homelessness time trend has in-sample R² of approximately 0.042. That weak fit is a reason to question a simple time-only model, **not** evidence for a particular cause of homelessness. Seattle's exponential housing fit has in-sample R² of approximately 0.966; a high historical fit score does not establish long-range forecast reliability.

## Research limitations

- Model disagreement is not a statistical confidence interval
- In-sample R² does not measure held-out forecast accuracy
- A 50-year extrapolation is highly sensitive to model form and structural change
- City labels, geography and count definitions need source-level verification before combining series
- Parts of the original report mix people and housing units or use inconsistent labels; they are preserved, not silently corrected
- Page 29 fits separate one-variable regressions; it should not be described as a fitted multivariate model
- No causal effect, policy impact or deployed decision system is demonstrated

See [PROVENANCE.md](PROVENANCE.md) for the exact reconstruction scope, solver differences and rights notes. The original report's references appear on page 21.
