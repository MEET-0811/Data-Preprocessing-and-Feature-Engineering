<p align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4facfe,100:00f2fe&height=220&section=header&text=Patient%20Health%20Data%20Cleanser&fontSize=40&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Missing%20Value%20Imputation%20%7C%20Outlier%20Treatment%20%7C%20ML-Ready%20Data&descAlignY=60&descSize=18"/>
</p>

<div align="center">

# 🩺 Patient Health Records — Data Cleanser

### 🚀 A Rigorous Missing-Value & Outlier Treatment Pipeline for Clinical ML Data

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
<img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>

<br>

<img src="https://img.shields.io/badge/Imputation-6%20Strategies-success?style=flat-square"/>
<img src="https://img.shields.io/badge/Outliers-4%20Methods-success?style=flat-square"/>
<img src="https://img.shields.io/badge/Dataset-2500%20Patients-blue?style=flat-square"/>
<img src="https://img.shields.io/badge/Data%20Loss-0%25-brightgreen?style=flat-square"/>
<img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square"/>
<img src="https://img.shields.io/badge/License-MIT-orange?style=flat-square"/>

</div>

---

# 📌 Table of Contents

- [🎯 Objective](#-objective)
- [📄 Problem Statement](#-problem-statement)
- [🧭 Analyst's Note — Why This Approach](#-analysts-note--why-this-approach)
- [📋 Dataset Structure](#-dataset-structure)
- [📂 Project Structure](#-project-structure)
- [🛠 Technologies Used](#-technologies-used)
- [🧩 Part A — Missing Value Treatment](#-part-a--missing-value-treatment)
- [🎯 Part B — Outlier Treatment](#-part-b--outlier-treatment)
- [✅ Part C — Final Clean Dataset](#-part-c--final-clean-dataset)
- [📉 Data Visualizations](#-data-visualizations)
- [💡 Key Findings](#-key-findings)
- [📊 Final Results](#-final-results)
- [⚙ Installation](#-installation)
- [▶ How to Run](#-how-to-run)
- [👨‍💻 Author](#-author)
- [⭐ Support](#-support)

---

# 🎯 Objective

This project practices **Data Preprocessing and Feature Engineering** with a deliberate focus on the two issues that quietly sink more clinical ML models than any algorithm choice ever will: **missing values** and **outliers**. Six imputation strategies and four outlier-treatment techniques are applied, compared side-by-side, and the results are used to make an evidence-based case for which approach to ship.

---

# 📄 Problem Statement

Working as a **Data Analyst for a healthcare company**, this project takes a **patient health records** dataset containing missing values and outliers introduced by inconsistent reporting and measurement error. The task is to **clean the dataset** using a range of missing-data imputation methods and outlier-handling techniques, preparing it for a downstream ML task: **predicting heart-disease risk**.

The dataset contains:
- **Patient demographic details** — Age, Gender, Region
- **Medical attributes** — BMI, Blood Pressure, Cholesterol Level, Glucose Level
- **Target variable** — Disease Risk (0 = Low, 1 = High)

---

# 🧭 Analyst's Note — Why This Approach

> A dataset doesn't tell you which cleaning method is "correct" — it tells you the trade-offs. Six years into any data career, the real skill isn't knowing that `KNNImputer` exists; it's knowing *when a mean imputation is good enough and when it will quietly flatten a signal your model needed.*

A few judgment calls made in this project, and the reasoning behind them:

- **Mean vs. Median vs. KNN vs. MICE for BMI, Cholesterol, Glucose:** All four were run and compared side-by-side rather than picking one on faith. Mean/median imputation is fast and defensible for MCAR (missing-completely-at-random) data, but it silently shrinks variance and erases the natural correlation between age, BMI, and blood pressure. **MICE** was selected as the production strategy because it imputes each variable as a function of the others — preserving the physiological relationships a disease-risk model will eventually depend on.
- **Most-Frequent for categoricals (Gender, Region):** For low-cardinality categoricals with no strong dependency structure, mode imputation is the pragmatic choice — anything fancier (like a classifier-based imputer) would be over-engineering for 5–6% missingness.
- **Winsorization over outlier removal:** This is the decision most junior pipelines get wrong. Deleting rows flagged by the IQR rule dropped **7.3% of patients** here — and a meaningful share of those "outliers" (very high glucose, elevated cholesterol) are exactly the clinically real high-risk patients this model exists to catch. Capping at the 1st/99th percentile neutralizes the *statistical* distortion of extreme/erroneous values without discarding the *clinical* signal. In healthcare data specifically, an "outlier" is often the most important row in the table — treat it with restraint.
- **Z-score vs. IQR for detection, not treatment:** Both are reported for every column because they disagree in informative ways — Z-score (3σ) only flags the most extreme tail, while IQR is sensitive to skew. Comparing them is itself a diagnostic: a big gap between the two counts is a hint the column is skewed rather than genuinely populated with data-entry errors.

---

# 📋 Dataset Structure

| Field | Data Type | Description | Missingness / Outliers |
|-------|-----------|--------------|--------------------------|
| `patient_id` | String | Unique identifier per patient | None |
| `age` | Integer | Age of the patient (years) | ~7% missing |
| `gender` | Categorical | Male / Female | ~5% missing |
| `region` | Categorical | North / South / East / West | ~6% missing |
| `bmi` | Float | Body Mass Index (weight/height²) | ~8% missing + outliers (extreme high/low) |
| `blood_pressure` | Float | Average systolic blood pressure (mmHg) | Outliers (extreme high values) |
| `cholesterol` | Float | Cholesterol level (mg/dL) | ~9% missing + outliers |
| `glucose` | Float | Fasting glucose level (mg/dL) | ~10% missing + outliers |
| `disease_risk` | Binary Int | Target: 0 = Low Risk, 1 = High Risk | Complete, used as target |

---

# 📂 Project Structure

```text
Patient-Health-Data-Cleanser
│
├── Data
│      ├── raw
│      │      patient_health_records.csv
│      └── processed
│             patient_health_records_clean.csv
│
├── Notebook
│      Data_Cleanser_Patient_Records.ipynb
│
├── Images
│      missing_values_summary.png
│      imputation_comparison_bmi.png
│      outliers_before_after.png
│      clean_correlation_heatmap.png
│
├── Report
│      Theory_Concepts_Report.pdf
│      missing_value_summary.csv
│      imputation_comparison_bmi.csv
│      outlier_detection_summary.csv
│      before_after_outlier_treatment.csv
│
├── README.md
│
└── requirements.txt
```

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| 🐍 Python | Programming |
| 📘 Jupyter Notebook | Development |
| 🐼 Pandas | Data Manipulation |
| 🔢 NumPy | Numerical Computing |
| 🧠 Scikit-Learn | SimpleImputer, KNNImputer, IterativeImputer (MICE) |
| 📉 Matplotlib | Charts |
| 📊 Seaborn | Statistical Visualization |

---

# 🧩 Part A — Missing Value Treatment

## Step 1 — Identify & Quantify

| Column | Missing % |
|--------|-----------:|
| glucose | 10.0% |
| cholesterol | 9.0% |
| bmi | 8.0% |
| age | 7.0% |
| region | 6.0% |
| gender | 5.0% |

## Step 2 — Six Imputation Strategies, Applied & Compared

| # | Technique | Applied To | Notes |
|---|-----------|-----------|-------|
| 1 | **Simple Imputer — Numerical** | Age, BMI, Cholesterol, Glucose | Mean & Median variants compared |
| 2 | **Simple Imputer — Categorical** | Region | Most-frequent value |
| 3 | **Most Frequent Imputation** | Gender | Mode substitution |
| 4 | **Missing Indicator + Random Sample Imputation** | All numeric columns | Adds a `_was_missing` flag per column, fills from the observed distribution |
| 5 | **KNN Imputer** | Age, BMI, Cholesterol, Glucose | k = 5, multivariate, distance-weighted |
| 6 | **MICE (Iterative Imputer)** | Age, BMI, Cholesterol, Glucose | Chained-equations, models each column on the others |

**✅ Production choice:** MICE (numeric) + Most-Frequent (categorical) — see [Analyst's Note](#-analysts-note--why-this-approach) for the reasoning.

---

# 🎯 Part B — Outlier Treatment

## Step 3 — Detection

| Column | Z-score Flags (\|z\|>3) | IQR Flags (1.5×IQR) |
|--------|-----------------------:|---------------------:|
| bmi | 16 | 68 |
| blood_pressure | 20 | 45 |
| cholesterol | 20 | 40 |
| glucose | 15 | 37 |

## Step 4 — Treatment Methods Applied

| Method | Mechanism | Rows Affected |
|--------|-----------|----------------|
| **Z-score method** | Flags points beyond 3 standard deviations | Detection only |
| **IQR method** | Flags points beyond 1.5×IQR from Q1/Q3 | Detection + comparison removal (183 rows / 7.3%) |
| **Percentile method** | Caps below 1st / above 99th percentile | Basis for Winsorization |
| **Winsorization** | Clips extreme values to the percentile bounds instead of deleting rows | **0 rows dropped** ✅ |

**✅ Production choice:** Winsorization (1st/99th percentile capping) — retains 100% of patients while controlling the statistical influence of extreme values.

---

# ✅ Part C — Final Clean Dataset

| Check | Before | After |
|--------|--------|-------|
| Missing values | 925 cells across 6 columns | **0** |
| Extreme BMI (>60 or <13) | Present | Capped |
| Extreme Blood Pressure (>200 mmHg) | Present | Capped |
| Extreme Cholesterol (>380 mg/dL) | Present | Capped |
| Extreme Glucose (>280 mg/dL) | Present | Capped |
| Row count | 2,500 | **2,500 (0% loss)** |
| ML-ready | ❌ | ✅ |

---

# 📉 Data Visualizations

| Visualization | Purpose |
|--------------|---------|
| 📊 Missing Value Bar Chart | Quantify missingness per column |
| 📈 KDE Overlay | Compare BMI distribution across 4 imputation strategies |
| 📦 Box Plots (Before/After) | Visualize outlier compression from Winsorization, per column |
| 🔥 Correlation Heatmap | Confirm feature relationships survived cleaning |

---

# 💡 Key Findings

## ⭐ Finding 1
**MICE preserved cross-feature correlations** that single-value imputation (mean/median) measurably flattened — critical for a model that will lean on the Age–BMI–Blood Pressure relationship.

## 🎯 Finding 2
**IQR-based outlier removal would have cost 7.3% of the patient population** — in a healthcare context, that's not noise reduction, it's information loss, since several "outliers" are legitimate high-risk patients.

## 📊 Finding 3
**Z-score and IQR disagreed by 2–4x on flagged-point counts** across every column, confirming the underlying medical variables are moderately right-skewed rather than cleanly normal — a detail that should inform any future modeling choice (e.g., preferring tree-based models or log-transforms over raw linear assumptions).

## 🧮 Finding 4
After Winsorization, standard deviations dropped meaningfully (e.g., blood pressure σ: 14.4 → 11.7) **without shifting the median at all** — exactly the intended effect: extreme-value influence reduced, central signal untouched.

## ✅ Finding 5
The final dataset carries **zero missing values, zero dropped rows, and no unphysiological extremes** — a clean, defensible, audit-ready input for the disease-risk classification model that follows this pipeline.

---

# 📊 Final Results

| Task | Status |
|-----------|--------|
| Missing Value Identification & Reporting | ✅ Completed |
| 6 Imputation Strategies Implemented & Compared | ✅ Completed |
| Outlier Detection (Z-score, IQR) | ✅ Completed |
| Outlier Treatment (Percentile, Winsorization) | ✅ Completed |
| Before vs After Comparison | ✅ Completed |
| Final ML-Ready Dataset | ✅ Delivered |
| Summary Report & Recommendations | ✅ Completed |

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Patient-Health-Data-Cleanser.git
```

## 2️⃣ Open Project Folder

```bash
cd Patient-Health-Data-Cleanser
```

## 3️⃣ Install Required Libraries

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

or

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

| Library | Purpose |
|----------|----------|
| Pandas | Data Manipulation |
| NumPy | Numerical Computing |
| Scikit-Learn | Simple / KNN / Iterative (MICE) Imputers |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Charts |
| Jupyter Notebook | Development Environment |

---

# ▶️ How to Run

### Step 1

```bash
jupyter notebook
```

### Step 2

Open

```
Notebook/Data_Cleanser_Patient_Records.ipynb
```

### Step 3

```
Run → Run All Cells
```

### Step 4

The notebook will automatically

✅ Load and profile missing values

✅ Apply and compare 6 imputation strategies

✅ Detect and treat outliers with 4 methods

✅ Produce before/after comparisons and visualizations

✅ Export the final ML-ready dataset

---

# 🎓 Learning Outcomes

- 🧩 Multiple missing-value imputation strategies (simple, indicator-based, multivariate)
- 🧠 KNN and MICE implementation for multivariate imputation
- 🎯 Outlier detection via Z-score and IQR
- ✂️ Outlier treatment via Percentile capping and Winsorization
- ⚖️ Before vs after dataset-quality comparison
- 📦 Delivering a machine-learning-ready dataset with a profiling summary

---

# 🏆 Project Conclusion

Cleaning is where most of the real analytical judgment in a data project happens — not in the eventual model. This project deliberately over-builds the missing-value and outlier-treatment stage (six imputers, four outlier techniques) specifically to make that judgment visible and defensible: every method is implemented, compared side-by-side, and the final choice is justified against the shape of the actual data rather than picked as a default.

The result is a **patient health-records dataset with zero missing values, zero unphysiological extremes, and zero patients discarded** — ready to support a heart-disease-risk classification model without quietly baking in the biases that sloppy cleaning introduces.

---

# 👨‍💻 Author

<div align="center">

## **PR. 2 — Data Cleanser**

### 🩺 Data Preprocessing & Feature Engineering Practical Exam

Approached with the same rigor a senior healthcare-analytics team would expect in production: every cleaning decision compared, justified, and documented — not just applied.

---

### 🛠 Skills

🐍 Python

🧠 Scikit-Learn (Imputation)

📊 Statistical Outlier Detection

📈 Data Visualization

🩺 Healthcare Data Quality

</div>

---

# ⭐ Support

If you found this project useful,

⭐ Star this Repository

🍴 Fork the Project

💬 Share it with others

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project with proper attribution.

---

<div align="center">

# 🚀 Thank You for Visiting!

### ⭐ If you liked this project, don't forget to Star the Repository ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4facfe,100:00f2fe&height=140&section=footer"/>

</div>
