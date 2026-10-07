# 🌍 Global Government Budget Analytics

A Python and MySQL-based analytics project for exploring **government budgets, sector allocations, spending trends, anomalies, volatility, and future budget projections** across countries.

The project includes a Python ETL pipeline, normalized MySQL database, statistical analysis modules, and an interactive Streamlit dashboard.

## 🚀 Features

* CSV-to-MySQL ETL pipeline using Python and Pandas
* Normalized MySQL database for countries, budgets, and sector allocations
* Historical budget trend analysis
* 5-year rolling averages
* Sector dominance analysis using SQL window functions
* Statistical anomaly detection using Z-scores
* Cross-sector correlation analysis
* Rolling budget volatility analysis
* Polynomial budget projections with scenario shocks
* Defense vs. civilian spending analysis
* Interactive Streamlit dashboard with Plotly visualizations

## 🛠️ Tech Stack

**Python | Pandas | NumPy | MySQL | SQLAlchemy | SQL | Streamlit | Plotly**

## 🔄 Project Workflow

```text
CSV Data
   ↓
Python ETL
   ↓
MySQL Database
   ↓
SQL & Statistical Analysis
   ↓
Streamlit Dashboard
```

## 📊 Database Structure

```text
Countries
    ↓
Budgets
    ↓
Sector Allocations
```

The database stores country information, yearly total budgets, and detailed sector-level allocations.

## 📈 Key Analytics

* Budget growth and historical trends
* Sector allocation patterns
* Z-score based outlier detection
* Cross-sector Pearson correlation
* Rolling volatility and statistics
* Polynomial trend projections
* Civilian-to-defense spending ratios



