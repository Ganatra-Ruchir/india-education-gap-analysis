# Data sources

## Primary source: UDISE, Ministry of Education (2015-16)

The underlying data is India's **Unified District Information System for
Education (UDISE)** state-level school census for 2015-16 -- the same
administrative data collection that UDISE+ continues today. It covers
schools, teachers, enrollment, and board-exam results, collected by what
was then the Ministry of Human Resource Development (now the Ministry of
Education).

Literacy figures in this file are the **2011 Census** literacy rates, as
carried in this UDISE release -- not a UDISE-collected figure themselves.

- UDISE+: https://udiseplus.gov.in

## Access point / compiler: Kaggle

The raw state-level CSV (`data/2015_16_Statewise_Secondary.csv`) was
downloaded from the Kaggle dataset "Education in India" (uploaded by
rajanand), which republishes the original MHRD/DISE state and district
tables. Kaggle is the *compiler and access point*; **UDISE is the primary
source and the one to cite**.

- Kaggle dataset: https://www.kaggle.com/datasets/rajanand/education-in-india
- License: **CC BY-SA 4.0** (attribution required, share-alike) — the raw
  CSV in `data/` is redistributed here under that license; the project's
  own code is separately MIT-licensed (see `LICENSE`).

`data/2015_16_Statewise_Secondary_Metadata.csv` documents every one of the
raw file's ~630 column names, for anyone extending this analysis.

## What this project computes from the raw file

The raw file has ~630 columns of granular counts (schools, teachers by
qualification, enrollment by school category, exam results by stream and
category). This project derives four things from it:

| Derived column | How it's computed |
|---|---|
| `gender_gap` | `male_literacy_rate - female_literacy_rate` |
| `pupil_teacher_ratio` | `enr_all / tch_all` (secondary level, all schools) |
| `class10_pass_rate` | sum of `pass_*_py10` columns / sum of `apr_*_py10` columns x 100 (previous-year Class 10 board results, all categories and genders) |
| `class10_appeared` / `class10_passed` | sums of the `apr_*_py10` / `pass_*_py10` columns |

## Known data gaps (real, not bugs)

- **Telangana** has no literacy figures in this release -- it split from
  Andhra Pradesh in June 2014, and Census literacy wasn't yet reported
  separately for it here. It is excluded, not zero-filled.
- **Delhi** shows zero students appeared for the Class 10 exam in this
  cycle's data (a different board or reporting gap); its pass rate is
  recorded as missing, not 0%.

## This is a single-year cross-section

This file covers **2015-16 only**. There is no multi-year trend in this
project -- see `docs/METHODOLOGY.md` for what a single cross-section can
and cannot support.

## How to refresh the data

1. Download a newer UDISE+ state report (or the same Kaggle mirror for a
   different year, if available) as a CSV with the same column names.
2. Save it into `data/` and update the filename in `src/data.py`.
3. Re-run `python src/analysis.py` then `pytest -q`.

## Suggested citation

> Ministry of Education (formerly MHRD), Government of India. UDISE
> state-level school census, 2015-16. Accessed via Kaggle
> ("Education in India", rajanand).
