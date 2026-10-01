# Provenance, reconstruction and rights

## Historical team material

The report is the 2024 M3 Challenge submission labelled Team 17571. Kaushal Chitturu describes his contribution as leading the five-person team during the 14-hour challenge. It is team work, not a claim of sole authorship of the entire report or appendix.

The available source was a sequence of 29 original page screenshots, not the original editable document or vector PDF. `report/team-17571-report.pdf` embeds those pages in order. It is image-based; text search and accessibility are limited. No report prose, figures or historical code screenshots have been rewritten. `report/page-manifest.json` records SHA-256 hashes of the recovered source images and the assembled PDF. The eight appendix images are also retained independently without alterations.

Page map:

- 1–20: main report and discussion
- 21: references
- 22–29: original code appendix

## New code (2026)

The executable package is a modern reconstruction of selected calculations, not the original code files. Those were only available as screenshots. Four series were transcribed from pages 22, 24, 27 and 28. Each has a source-page field in the exported CSV. They total 58 observations.

The reconstruction retains linear least squares and the three-parameter exponential form `a × exp(b × t) + c`. It centres years on the first observation and uses scale-dependent initial parameters with an explicit evaluation budget for SciPy's nonlinear solver, instead of the screenshot's default initial guess. Full-precision results may differ from the rounded equations and forecast tables in the paper. Reproduction does not depend on matching every printed forecast number exactly.

One specific discrepancy: the Seattle homelessness array in the code appendix gives linear in-sample R² of approximately 0.911, while the report describes approximately 0.899. The reconstruction follows the appendix array and does not alter its observations to force a match to the prose. Both housing fit comparisons and the weak Albuquerque homelessness fit reproduce the reported rounded R² values.

The package adds validation, immutable data records, finite-value/overflow checks, residual plots, explicit limitation metadata and tests. These engineering additions were made in 2026; they were not part of the timed 2024 competition submission. Tests check implementation and selected historical fit scores, not real-world predictive accuracy.

Not reconstructed:

- Page 26's differently scoped “total calculated housing units” series
- Page 29's separate indicator regressions, whose scales and interpretation need further review
- Affordability, decision-tree and intervention discussion as a deployable model

## Interpretation limits

The original appendix's city labels do not by themselves establish matched geographic coverage. Count definitions and source vintages must be checked before reusing the data. Model-form differences are not uncertainty intervals. Weak time fits cannot establish causes; the original discussion's causal interpretations are not endorsed as proven findings here.

The report is an archive of a school competition exercise. It is not current research, investment advice or a policy recommendation.

## Rights and privacy

This publication follows the participant's request to share the team report as portfolio evidence. No open-source licence is asserted for the historical team report, third-party figures or cited material. Existing rights remain with their respective owners; this repository does not grant permission to redistribute them under a new licence.

The recovered report uses its anonymous team number. No names, emails or phone numbers were detected in the pages during the publication review. Personal session files and unrelated attachments are not included.
