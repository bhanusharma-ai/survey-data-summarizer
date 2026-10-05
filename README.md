# Survey Data Summarizer

A Python tool that generates an instant **quality + summary report** for survey data.
Built from 8 years of market research data processing experience — it automates
the manual checks that traditionally take hours in SPSS/Excel.

## What it does

- **Base size & structure** — respondent count and variable list
- **Descriptive statistics** — mean, std, min, max, quartiles for all numeric fields
- **Frequency tables** — counts for every categorical variable
- **Missing data check** — flags incomplete fields
- **Straightliner detection** — flags low-variation respondents across grid questions
  (a standard data-quality check in survey research)

## Supports multiple formats

Works with the file types research teams actually use:

- `.csv`
- `.xlsx` / `.xls` (Excel)
- `.sav` (SPSS) — **preserves variable labels**

## Tech

Python · Pandas · pyreadstat

## Usage

​```python
from survey_summarizer import summarize_survey

summarize_survey("survey.csv", grid_cols=["q1", "q2", "q3"])
summarize_survey("survey.sav", grid_cols=["q1", "q2", "q3"])
​```

`grid_cols` is optional — pass your grid/scale question columns to enable
straightliner detection. Leave it out to skip that check.

## Install

​```bash
pip install pandas pyreadstat openpyxl
​```

## Note

The demo uses a public sample dataset so the script runs out-of-the-box.
Straightliner detection is designed for survey grid questions (q1, q2, q3…).
No client or confidential data is included in this repository.

*Built by Bhanu Sharma — Market Research & Data Analytics, AI/automation.*

