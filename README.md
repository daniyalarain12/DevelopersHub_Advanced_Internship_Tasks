# Data Science & Machine Learning Portfolio

## Overview
This repository contains a collection of Jupyter Notebooks and a Python application demonstrating end-to-end data science, predictive modeling, and data visualization capabilities. Each file showcases distinct machine learning methodologies, including classification, time-series forecasting, and interactive data dashboarding.

## Repository Contents

### 1. `Term Deposit Prediction.ipynb`
**Objective:** Predict whether a client will subscribe to a bank term deposit based on direct marketing campaigns.
**Methodology:**
- **Data Wrangling & EDA:** Handles a dataset (`bank-full.csv`) of over 45,000 records. Performs rigorous Exploratory Data Analysis, missing value evaluation, and datatype transformations.
- **Feature Engineering:** Adjusts fields like `pdays` and evaluates the statistical distribution of numeric and categorical variables.
- **Target Audience:** Ideal for financial sector analytics to optimize marketing strategies.

### 2. `Loan_Dataset .ipynb`
**Objective:** Analyze loan origination data to predict credit risk, specifically the likelihood of a 12-month default (`default_12m`).
**Methodology:**
- **Data Source:** Operates on `origination_data-2.csv` (135,000 records).
- **Feature Extraction:** Derives critical financial health indicators such as Monthly Income, Equated Monthly Installment (EMI), Debt-to-Income Ratio (DTI), and Subprime risk indicators based on credit scores and DTI/EMI thresholds.
- **Predictive Modeling:** Deploys an AdaBoost Classifier to assess loan default probabilities, culminating in a detailed classification report mapping accuracy, precision, and recall.

### 3. `Time Series.ipynb`
**Objective:** Forecast metrics derived from household power consumption data using advanced time-series techniques.
**Methodology:**
- **Data Preparation:** Ingests `household_power_consumption.csv` (over 1M records) and parses compound date-time strings into functional Pandas Datetime objects. 
- **Time-Based Feature Engineering:** Constructs temporal features such as Hour of the day, Day of the Week, and Weekend indicators to capture cyclical power usage trends.
- **Modeling:** Employs XGBoost (`XGBRegressor`/`XGBClassifier`) for predictive forecasting and evaluates the model using Mean Absolute Error (MAE) and accuracy scoring.

### 4. `app.py`
**Objective:** A dynamic, interactive executive dashboard for global sales and profitability tracking.
**Methodology:**
- **Framework:** Built using `Streamlit` for the web interface and `Plotly Express` for data visualization.
- **Data Source:** Pulls from `superstore.csv`, applying resilient data loading and datetime parsing.
- **Visual Analytics:** - Dynamic sidebar filtering engine (Region, Category, Segment, Ship Mode).
  - High-level KPIs.
  - Granular visualizations including operational profit matrices (Segment vs. Ship Mode) and transaction volume density histograms.

## Requirements & Dependencies
To run these notebooks and the Streamlit app, the following Python libraries are required:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `xgboost`
- `streamlit`
- `plotly`

## How to Use
1. Ensure all dependencies are installed via `pip install -r requirements.txt` (or install manually).
2. For the Notebooks (`.ipynb`): Launch Jupyter Notebook or JupyterLab, open the desired file, and execute the cells sequentially.
3. For the Dashboard (`app.py`): Run the command `streamlit run app.py` in your terminal to launch the web application locally.
