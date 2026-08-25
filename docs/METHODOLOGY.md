# Methodology

## The questions

Using real 2015-16 UDISE state-level data:

1. Which states lead and lag on literacy?
2. How wide is the male-female literacy gap, and does it track overall literacy?
3. Does a more crowded secondary classroom (higher pupil-teacher ratio) track a lower Class 10 pass rate?

## What we did

- **Loading & cleaning** (`src/data.py`): selected the relevant columns out
  of a ~630-column raw file, stripped/title-cased inconsistent state-name
  formatting, coerced numeric types, and bounded literacy and
  pupil-teacher ratio to sane ranges.
- **Derived metrics**: pupil-teacher ratio and Class 10 pass rate are not
  present as columns in the raw data -- they're computed from enrollment,
  teacher, and exam-result counts (see `docs/DATA_SOURCES.md` for the exact
  formulas).
- **Correlation**: plain Pearson correlation between two state-level
  variables, reported as-is.

## What this data can and cannot claim

- **This is a single-year cross-section (2015-16).** There is no trend
  analysis in this project, because this dataset doesn't have one --
  earlier versions of this project fabricated a multi-year trend from
  synthetic data, which this rebuild deliberately does not repeat.
- **Correlation is not causation**, and with 34-35 data points a
  correlation coefficient is noisy. Both the literacy/gender-gap and
  PTR/pass-rate findings are reported at face value, including the
  PTR/pass-rate result, which is weak (r ~ -0.13) and does **not** support
  a "crowded classrooms cause lower pass rates" claim in this data.
- **Class 10 pass rate mixes states with very different appearance rates**
  (e.g. how many eligible students actually sit the exam) -- a state
  could show a high pass rate simply because weaker students don't appear
  for the exam at all. This project does not correct for that; it's a
  real limitation of using pass rate as an outcome proxy.
- **Literacy here is a 2011 Census figure**, four to five years older than
  the 2015-16 school-census figures it's shown alongside. The two are not
  from the same year.

## Known data gaps

See `docs/DATA_SOURCES.md` for the Telangana and Delhi gaps -- both are
excluded/marked missing deliberately, not zero-filled or interpolated.

## Reproducibility

`python src/analysis.py && pytest -q` reproduces every chart, number, and
finding from the cached CSV in `data/`. The test suite checks derived
columns (gender gap, pass rate) against independent manual calculations,
and checks that known data gaps stay excluded rather than silently
reappearing as fabricated values.
