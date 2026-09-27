# Online Food Delivery Dataset — Data Cleaning & Analysis

> **MCA Internship Project**  
> Exploratory data analysis of customer behaviour in the Bengaluru online food delivery market.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Dataset Description](#2-dataset-description)
3. [Project Structure](#3-project-structure)
4. [How to Run](#4-how-to-run)
5. [Data Cleaning — Issues Found & Fixed](#5-data-cleaning--issues-found--fixed)
6. [Key Analysis Findings](#6-key-analysis-findings)
7. [Conclusion](#7-conclusion)
8. [Requirements](#8-requirements)

---

## 1. Project Overview

This project performs **data cleaning** and **exploratory data analysis (EDA)** on the
[Online Food Ordering Dataset](https://www.kaggle.com/datasets/srisyra02/online-food-ordering-dataset)
sourced from Kaggle.

The goal is to:
- Identify and fix all data quality issues in the raw CSV **without modifying the original file**
- Analyse customer demographics, income, education, and family patterns
- Understand what factors influence whether a customer orders food online
- Present findings suitable for an MCA internship report

**Original CSV is never modified.** All fixes are applied in Python and written to a separate clean file.

---

## 2. Dataset Description

| Property               | Value                                  |
|------------------------|----------------------------------------|
| Source                 | Kaggle — srisyra02                     |
| Region                 | Bengaluru, India                       |
| Raw records            | 388 rows                               |
| Clean records          | 285 rows (after removing 103 duplicates)|
| Columns (clean)        | 13                                     |
| License                | CC BY 4.0                              |

### Columns

| Column                     | Type    | Description                              |
|----------------------------|---------|------------------------------------------|
| Age                        | Integer | Customer's age (18–33)                   |
| Gender                     | Text    | Male / Female                            |
| Marital Status             | Text    | Single / Married / Prefer not to say     |
| Occupation                 | Text    | Student / Employee / Self Employed / House wife |
| Monthly Income             | Text    | Income category (No Income → >50,000)    |
| Educational Qualifications | Text    | School / Graduate / Post Graduate / Ph.D |
| Family size                | Integer | Number of household members (1–6)        |
| Customer Type              | Text    | New / Regular / Frequent                 |
| latitude                   | Float   | Geographic latitude (Bengaluru area)     |
| longitude                  | Float   | Geographic longitude (Bengaluru area)    |
| Pin code                   | Integer | 6-digit area pin code                    |
| Output                     | Boolean | Yes = orders online / No = does not      |
| Feedback                   | Text    | Positive / Negative                      |

---

## 3. Project Structure

```
online-food-delivery-project/
│
├── online food delivery dataset.csv   ← Original raw file (NEVER modified)
├── online_food_delivery_clean.csv     ← Cleaned output (285 rows, 13 columns)
│
├── clean_food_dataset.py              ← Main Python cleaning script
├── cleaning_report.txt                ← Auto-generated audit trail of all fixes
│
├── requirements.txt                   ← Dependencies (standard library only)
└── README.md                          ← This file
```

---

## 4. How to Run

### Prerequisites
- Python 3.11 or higher
- No third-party packages needed — uses standard library only

### Step 1 — Clone / download the project
Place all files in the same folder.

### Step 2 — Run the cleaning script
```bash
python clean_food_dataset.py
```

### Step 3 — Check the outputs
| Output file                     | What it contains                              |
|---------------------------------|-----------------------------------------------|
| `online_food_delivery_clean.csv`| Cleaned dataset ready for analysis            |
| `cleaning_report.txt`           | Full audit trail with counts and distributions|

> The original `online food delivery dataset.csv` is **read-only** — it will not be changed.

---

## 5. Data Cleaning — Issues Found & Fixed

Five data quality issues were identified in the raw file:

### Issue 1 — Ghost Column (Trailing Comma in Header)
- **Problem:** The header line ended with a trailing comma, creating a 14th unnamed empty column
  that silently duplicated the `Output` column in every single row.
- **Impact:** Any tool loading the CSV would see 14 columns instead of 13 and produce wrong results.
- **Fix:** Detected the empty header key and dropped it from all rows.

### Issue 2 — Trailing Whitespace in Feedback Values
- **Problem:** 71 rows had `"Negative "` (with a trailing space) instead of `"Negative"`.
  To a computer these are two different strings, breaking all grouping and filtering.
- **Fix:** Applied `.strip()` to every cell value across the entire dataset.
- **Cells corrected:** 71

### Issue 3 — Spelling Typo in Occupation
- **Problem:** `"Self Employeed"` (double 'e') appeared instead of `"Self Employed"` in 54 rows,
  creating a phantom second occupation category.
- **Fix:** Replaced all instances of `"Self Employeed"` with `"Self Employed"`.
- **Rows corrected:** 54

### Issue 4 — Duplicate Rows
- **Problem:** 103 rows were exact copies of earlier rows (all 13 columns identical).
  This inflates every statistic and biases any model trained on the data.
- **Fix:** Kept only the first occurrence of each unique row and removed duplicates.
- **Rows removed:** 103 (27% of the raw dataset)

### Issue 5 — Output / Feedback Logical Mismatch (Flagged, NOT deleted)
- **Problem:** 44 rows had `Output=Yes` but `Feedback=Negative`, or `Output=No` but `Feedback=Positive`.
- **Decision:** These are **real customer opinions** (e.g. a customer who orders online but is
  unhappy, or one who stopped ordering but still has positive views). They were **not deleted**.
- **Action:** Flagged in `cleaning_report.txt` with their row numbers for human review.
- **Rows flagged:** 44

### Cleaning Summary

| Action                        | Count        |
|-------------------------------|--------------|
| Raw rows loaded               | 388          |
| Ghost columns removed         | 1            |
| Whitespace cells fixed        | 71           |
| Typos corrected               | 54           |
| Duplicate rows removed        | **103**      |
| Rows flagged (mismatch)       | 44           |
| **Final clean rows**          | **285**      |

---

## 6. Key Analysis Findings

All findings are based on the **285 unique cleaned records**.

| # | Finding | Key Statistic |
|---|---------|---------------|
| 1 | Online ordering is mainstream | **76%** of customers order online |
| 2 | Students are the #1 segment | **88%** ordering rate · 50% of dataset |
| 3 | Age 26–29 is a churn window | Rate drops from **86% → 50%** at career entry |
| 4 | Single customers order far more than married | **85% vs 61%** |
| 5 | Lower income groups order MORE (student effect) | No-income group: **85%** ordering rate |
| 6 | Family of 4 is the sweet spot | **87%** ordering rate |
| 7 | Post Graduates lead in adoption | **83%** ordering rate |
| 8 | Feedback is mostly positive but 44 rows signal risk | **81%** positive overall |

### Top Recommendations

1. **Student Priority Programme** — zero delivery fees for verified students
2. **26–29 Retention Campaign** — after-work dinner promotions, loyalty points doubling
3. **4-Person Family Meal Bundles** — value combos targeting nuclear families
4. **Married Couple Promotions** — weekend date-night deals, healthy meal plans
5. **Follow up 44 flagged customers** — churn prevention + win-back outreach

---

## 7. Conclusion

This project demonstrated the full data pipeline from raw, messy CSV data to clean, analysable
records. The cleaning phase removed **27% of rows as duplicates** — a reminder that blindly
trusting raw data leads to misleading conclusions.

The EDA showed that **age, occupation, and marital status** are the strongest predictors of
online ordering behaviour. Young, single students aged 22–25 are the most engaged users.
The counter-intuitive income finding (lower income = more ordering) is explained by the
demographic composition: "No Income" customers are almost entirely students.

**Limitations:** 285 records from one city (Bengaluru). Results may not generalise to other
regions. The "Uneducated" category (only 2 records) is not statistically meaningful.
Future work should use a larger dataset and apply machine learning models (logistic regression,
random forest) to predict ordering probability per customer profile.

---

## 8. Requirements

This project requires **Python 3.11+** and uses only the standard library:

| Module      | Used For                          |
|-------------|-----------------------------------|
| `csv`       | Reading and writing CSV files     |
| `collections`| Counter, defaultdict for frequency analysis |
| `re`        | Regex validation (pin codes, lat/lon) |
| `os`        | File path operations              |

No `pip install` needed. See [`requirements.txt`](requirements.txt) for optional packages
(pandas, matplotlib, seaborn, scikit-learn) if you wish to extend the analysis.

---

*Dataset source: [Kaggle — Online Food Ordering Dataset](https://www.kaggle.com/datasets/srisyra02/online-food-ordering-dataset) · License: CC BY 4.0*  
*MCA Internship Project · Made with IBM Bob*
