<p align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4facfe,100:00f2fe&height=220&section=header&text=Customer%20Churn%20Data%20Profiler&fontSize=40&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Data%20Preprocessing%20%7C%20Feature%20Engineering%20%7C%20EDA&descAlignY=60&descSize=20"/>
</p>

<div align="center">

# 🧪 Customer Purchase Behavior & Churn — Data Profiler

### 🚀 Data Preprocessing & Feature Engineering Practical Exam using Python

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge"/>
<img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>

<br>

<img src="https://img.shields.io/badge/Sources-CSV%20%7C%20JSON%20%7C%20SQL%20%7C%20API-success?style=flat-square"/>
<img src="https://img.shields.io/badge/Dataset-3000%20Customers-blue?style=flat-square"/>
<img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square"/>
<img src="https://img.shields.io/badge/License-MIT-orange?style=flat-square"/>

</div>

---

# 📌 Table of Contents

- [🎯 Objective](#-objective)
- [📄 Problem Statement](#-problem-statement)
- [🎯 Machine Learning Problem](#-machine-learning-problem)
- [✨ Project Features](#-project-features)
- [📊 Dataset Overview](#-dataset-overview)
- [📋 Data Sources](#-data-sources)
- [📂 Project Structure](#-project-structure)
- [🛠 Technologies Used](#-technologies-used)
- [🧮 Tensors](#-tensors)
- [🧹 Data Cleaning](#-data-cleaning)
- [📈 Exploratory Data Analysis](#-exploratory-data-analysis-eda)
- [🧾 Data Profiling Report](#-data-profiling-report)
- [💡 Key Insights](#-key-insights)
- [📊 Final Results](#-final-results)
- [⚙ Installation](#-installation)
- [▶ How to Run](#-how-to-run)
- [👨‍💻 Author](#-author)
- [⭐ Support](#-support)

---

# 🎯 Objective

This project involves conducting **Data Preprocessing and Feature Engineering** on a real-world-style dataset. The aim is to **understand, clean, transform, and analyze** the dataset before it can be used for machine learning — with an emphasis on **data profiling, handling multiple formats, and performing EDA**.

---

# 📄 Problem Statement

Acting as a **Junior Data Analyst** at a consumer insights company, this project works with a dataset of **customer purchase behavior** collected from **multiple sources — CSV, JSON, a SQL database, and an API**. The goal is to frame a machine learning problem (predict customer churn) and perform data preprocessing and profiling to make the dataset ML-ready.

The concepts of **data analysis, tensors, data cleaning, and exploratory data analysis (EDA)** are applied throughout to extract insights.

---

# 🎯 Machine Learning Problem

> **Predict whether a customer will churn**, based on their purchase behavior (total purchases, spend, income, support interactions, satisfaction, and membership details).

This is framed as a **binary classification** problem, with `Churn` (Yes/No) as the target variable.

---

# ✨ Project Features

| Feature | Description |
|----------|-------------|
| 📥 Multi-Source Ingestion | CSV, JSON, SQLite (SQL), and simulated API |
| 🧹 Data Cleaning | Missing values, duplicates, inconsistent types, irrelevant columns |
| 🧮 Tensors | Scalar, Vector, Matrix, 3-D Tensor demos using NumPy |
| 📊 EDA | Univariate, Bivariate & Multivariate analysis with visualizations |
| 🧾 Data Profiling | Custom-built profiling report (missing values, stats, correlations, warnings) |
| 🎯 ML Framing | Churn prediction problem statement |
| 🐍 Python Implementation | Complete Jupyter Notebook |

---

# 📊 Dataset Overview

The dataset simulates **customer purchase behavior** for a consumer insights company, spread across four different source formats that are merged into one ML-ready table.

---

# 📋 Data Sources

| Source | Format | Key Fields |
|---------|--------|-----------|
| `customers_transactions.csv` | CSV | Customer_ID, Age, Gender, Region, Income, Total_Purchases, Avg_Order_Value, Total_Spend, Signup_Date, Churn |
| `customers_profile.json` | JSON | Customer_ID, Membership_Tier, Preferred_Category, Newsletter_Subscribed |
| `customers_support.db` | SQLite (SQL) | Customer_ID, Support_Tickets, Satisfaction_Score |
| `api_region_enrichment.json` | Simulated REST API | Region → Country, Currency, Timezone |

> **Note on the API source:** this exam environment has no outbound internet access, so the notebook attempts a live `requests.get()` call exactly as it would run in production, then gracefully falls back to a cached local JSON snapshot of the same dummy API response — the full try/live → fallback pattern is visible in the notebook.

All four sources are merged on `Customer_ID` (and `Region` for the API source) into a single master dataframe.

---

# 📊 Dataset Summary

| Property | Value |
|-----------|-------|
| 📁 Formats Combined | CSV + JSON + SQL + API (4 sources) |
| 📊 Total Customers | 3,000 (after cleaning) |
| 📋 Total Features (merged) | 18 |
| ❌ Missing Values (raw) | ~230 cells across 4 columns → 0 after cleaning |
| 🔁 Duplicate Records (raw) | 25 → 0 after cleaning |
| 🎯 Target Variable | Churn (Yes/No) — ≈ 45.6% churn rate |
| 📈 Ready for ML | ✅ Yes |

---

# 📂 Project Structure

```text
Customer-Churn-Data-Profiler
│
├── Data
│      ├── raw
│      │      customers_transactions.csv
│      │      customers_profile.json
│      │      customers_support.db
│      │      api_region_enrichment.json
│      └── processed
│             customer_churn_master_clean.csv
│
├── Notebook
│      Data_Profiling_Customer_Churn.ipynb
│
├── Images
│      univariate_distributions.png
│      bivariate_analysis.png
│      correlation_heatmap.png
│      pairplot.png
│
├── Report
│      Theory_Concepts_Report.pdf
│      profile_missing_values.csv
│      profile_correlation.csv
│      profile_warnings.txt
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
| 🐼 Pandas | Data Manipulation & CSV/JSON/SQL I/O |
| 🔢 NumPy | Tensors & Numerical Computing |
| 🗄 SQLite3 | SQL Data Source |
| 🌐 Requests | API Data Source (with offline fallback) |
| 📉 Matplotlib | Charts |
| 📊 Seaborn | Statistical Visualization |

---

# 📚 Python Libraries

| Library | Purpose |
|----------|----------|
| Pandas | Data Cleaning & Multi-Source Merging |
| NumPy | Tensor Operations |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Charts |
| SQLite3 | SQL Database Access |
| Requests | REST API Access |

---

# 🧮 Tensors

| Rank | Name | Example in this Project |
|------|------|--------------------------|
| 0-D | Scalar | One customer's `Total_Purchases` value |
| 1-D | Vector | One customer's `[Age, Income, Total_Purchases]` |
| 2-D | Matrix | 5 customers × 4 numeric features |
| 3-D | Tensor | Two stacked 5×2 customer-feature batches |

Tensors are the core data structure of ML/DL frameworks — every model operation (dot products, matrix multiplication, gradients) is fundamentally a tensor operation, so understanding shape and rank is a prerequisite before feeding tabular data into a model.

---

# 🧹 Data Cleaning

| Issue Found | Action Taken |
|--------------|-------------|
| 25 duplicate rows | Dropped |
| Missing `Age`, `Income`, `Avg_Order_Value` (numeric) | Imputed with **median** |
| Missing `Gender` (categorical) | Imputed with **mode** |
| Inconsistent `Gender` labels (`M`/`F` vs `Male`/`Female`) | Standardized |
| `Signup_Date` stored as text | Converted to `datetime` |
| `Row_Notes` (constant, irrelevant) | Dropped |

---

# 📈 Exploratory Data Analysis (EDA)

## 📊 Univariate Analysis

Distribution plots of **Age**, **Income**, and **Total Purchases** — Age is roughly bell-shaped, Income is right-skewed with a longer tail of higher earners, and Total Purchases behaves like a right-skewed count variable.

## 📈 Bivariate Analysis

- **Gender vs Total Purchases** — purchase volume is broadly similar across genders.
- **Income vs Churn** — churned customers show a slightly wider/lower income spread.

## 🔥 Multivariate Analysis

- **Correlation Heatmap** across all numeric features — `Total_Purchases` and `Total_Spend` are the most strongly correlated pair.
- **Pair Plots** colored by `Churn` to visualize feature interactions and separability.

---

# 🧾 Data Profiling Report

A **custom-built profiling function** (playing the role of `ydata-profiling`'s `ProfileReport`, since this offline exam environment can't install external packages) summarizes:

- ✅ Row/column counts & duplicate rows
- ✅ Missing values (count & percentage per column)
- ✅ Descriptive statistics for every column
- ✅ Correlation matrix of numeric features
- ✅ Data-quality warnings (high skew, high missingness, high correlation pairs, high-cardinality identifier columns)

Outputs are saved to `Report/profile_missing_values.csv`, `Report/profile_correlation.csv`, and `Report/profile_warnings.txt`.

---

# 💡 Key Insights

## ⭐ Insight 1
The overall **churn rate is ≈ 45.6%** — a large share of the customer base is at risk, making churn prediction a high-value use case for this business.

## 💰 Insight 2
**Total_Purchases and Total_Spend are the most strongly correlated pair** of features — a churn model should watch for this redundancy.

## 🏢 Insight 3
**Income shows only a mild relationship with churn** — behavioral features (purchase frequency, support tickets, satisfaction) likely matter more than raw income.

## 📈 Insight 4
The dataset was **successfully cleaned end-to-end**: 25 duplicates removed, missing values imputed, types fixed, and one irrelevant column dropped — leaving it ML-ready.

## ⏰ Insight 5
**Multi-source integration (CSV + JSON + SQL + API) merged cleanly** on shared keys, demonstrating a realistic Junior Data Analyst data-acquisition workflow.

---

# 📊 Final Results

| Task | Status |
|-----------|--------|
| Data Acquisition (CSV, JSON, SQL, API) | ✅ Completed |
| Initial Exploration (.head/.info/.describe) | ✅ Completed |
| Data Cleaning | ✅ Completed |
| Tensors Demo (NumPy) | ✅ Completed |
| Univariate / Bivariate / Multivariate EDA | ✅ Completed |
| Data Profiling Report | ✅ Completed |
| ML Problem Framing | ✅ Completed |
| Business Insights | ✅ Generated |

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Customer-Churn-Data-Profiler.git
```

## 2️⃣ Open Project Folder

```bash
cd Customer-Churn-Data-Profiler
```

## 3️⃣ Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn requests
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
| NumPy | Tensors & Numerical Computing |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Charts |
| Requests | API Access |
| Jupyter Notebook | Development Environment |

*(`sqlite3` and `json` are part of the Python standard library — no install needed.)*

---

# ▶️ How to Run

### Step 1

```bash
jupyter notebook
```

### Step 2

Open

```
Notebook/Data_Profiling_Customer_Churn.ipynb
```

### Step 3

```
Run → Run All Cells
```

### Step 4

The notebook will automatically

✅ Load all 4 data sources & merge them

✅ Explore & Clean the data

✅ Demonstrate Tensors with NumPy

✅ Run Univariate, Bivariate & Multivariate EDA

✅ Generate the Data Profiling Report

✅ Display Business Insights

---

# 🎓 Learning Outcomes

- 📥 Loading & merging datasets from multiple sources (CSV, JSON, SQL, API)
- 🧮 Understanding the role of tensors in machine learning
- 🧹 Data cleaning and preprocessing
- 📊 EDA (Univariate, Bivariate, Multivariate) with visualizations
- 🧾 Building automated profiling reports for decision-making
- 🎯 Framing a machine learning problem from raw data

---

# 🏆 Project Conclusion

This project demonstrates a complete, realistic **Data Preprocessing & Feature Engineering** workflow — from ingesting four differently-formatted data sources, through cleaning and EDA, to a self-built data profiling report — all in service of framing a **customer churn prediction** machine learning problem.

The work highlights that most of the value in an ML pipeline is created *before* modeling even begins: careful multi-source integration, rigorous cleaning, and thorough exploratory analysis are what make a dataset genuinely ML-ready.

---

# 👨‍💻 Author

<div align="center">

## **PR. 1 — Data Profiler**

### 🧪 Data Preprocessing & Feature Engineering Practical Exam

Submitted as a hands-on deliverable applying multi-source data acquisition, cleaning, EDA, tensors, and profiling to a customer-churn dataset.

---

### 🛠 Skills

🐍 Python

🗄 SQL

📊 Pandas & NumPy

📈 Data Visualization

🧾 Data Profiling

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
