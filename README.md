# Healthcare Dataset Analysis 🏥

An exploratory data analysis (EDA) of 55,500 patient healthcare records using Python and pandas. This project cleans, explores, and visualizes patterns in patient billing, medical conditions, insurance coverage, and hospital admissions.

## Overview

Healthcare costs and patient outcomes are among the most important data problems in the US. This project digs into a real-world style dataset to surface patterns that could help administrators, insurers, and patients better understand how billing, admission types, and medical conditions relate to each other.

## Dataset

| Field | Description |
|---|---|
| Name, Age, Gender | Patient demographics |
| Blood Type | Patient blood type |
| Medical Condition | Diagnosed condition (6 categories) |
| Date of Admission / Discharge Date | Admission and discharge dates |
| Doctor / Hospital | Assigned provider info |
| Insurance Provider | Patient's insurer (5 providers) |
| Billing Amount | Total billed amount ($) |
| Admission Type | Elective, Urgent, or Emergency |
| Medication | Prescribed medication |
| Test Results | Normal, Abnormal, or Inconclusive |

**Records:** 55,500  
**Columns:** 15  

## What the Analysis Does

- **Data Cleaning** — fixes inconsistent name capitalization, parses dates, calculates length of stay, and flags data quality issues (negative billing amounts)
- **Distribution Analysis** — breaks down patients by medical condition, admission type, and age group
- **Billing Insights** — compares average billing across conditions and insurance providers
- **Length of Stay** — visualizes how long patients stay by admission type
- **Visualizations** — produces a 6-panel summary chart saved as `healthcare_analysis.png`

## Key Findings

- **55,392** clean records after removing 108 flagged billing anomalies
- Obesity carries the highest average billing at **$25,860**, while Cancer averages the lowest at **$25,214**
- Medicare patients average the highest billing (**$25,668**) across all insurers
- Average length of stay is consistent across admission types (~15.5 days), suggesting other factors drive stay duration
- Test results are nearly evenly split: 33.6% Abnormal, 33.4% Normal, 33.1% Inconclusive

## Output

Running the script generates `healthcare_analysis.png` — a 6-panel visualization including:
1. Patient distribution by medical condition
2. Average billing by condition
3. Admission type breakdown (pie chart)
4. Average billing by insurance provider
5. Patient age distribution with mean line
6. Length of stay by admission type (box plots)

## How to Run

```bash
# Clone the repo
git clone https://github.com/MarcusMM1/healthcare-analysis
cd healthcare-analysis

# Install dependencies
pip install pandas matplotlib seaborn

# Add the dataset (healthcare_dataset.csv) to the project folder
# Then run:
python analysis.py
```

## Dependencies

- Python 3.8+
- pandas
- matplotlib
- seaborn

## About

Built by **Marcus Mitchell** as part of a Python data science project exploring real-world healthcare data patterns.  
[LinkedIn](https://www.linkedin.com/in/marcus-mitchell-10246b232/) | [GitHub](https://github.com/MarcusMM1)
