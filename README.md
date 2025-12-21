<div align="center">

# 🛒 Olist E-commerce Analytics Platform

### End-to-end data pipeline with dbt, MotherDuck & Streamlit

[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://olist-analytics.streamlit.app/)
[![dbt](https://img.shields.io/badge/dbt-Docs-FF694B?logo=dbt&logoColor=white)](https://mohith-akash.github.io/olist-analytics-platform/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![MotherDuck](https://img.shields.io/badge/MotherDuck-DuckDB-FFC107?logo=duckdb&logoColor=black)](https://motherduck.com)

**[Live Dashboard](https://olist-analytics.streamlit.app/)** · **[dbt Docs](https://mohith-akash.github.io/olist-analytics-platform/)** · **[Dataset](https://www.kaggle.com/olistbr/brazilian-ecommerce)**

</div>

---

## 🎯 Overview

A complete analytics platform analyzing **100,000+ orders** from Brazilian e-commerce marketplace Olist (2016-2018). Built to demonstrate:

- **Data Engineering** - ETL pipelines, dimensional modeling
- **SQL Expertise** - dbt transformations, CTEs, JOINs
- **Data Visualization** - Interactive dashboards
- **Cloud Warehousing** - MotherDuck (serverless DuckDB)

---

## 📊 Dashboards


### Streamlit Web Dashboard
Interactive web dashboard with KPIs, gauge charts, and data exploration.

![Streamlit Dashboard](streamlit_dashboard.png)

**Features:**
- 6 KPI cards with key metrics
- Seller rating gauge chart
- Revenue trends & category breakdown
- SQL code showcase
- CSV data export

### Power BI Desktop
Local analytics dashboard for deeper exploration.

![Power BI Dashboard](dashboard_preview.png)

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center"><img src="https://img.shields.io/badge/-MotherDuck-FFC107?style=for-the-badge&logo=duckdb&logoColor=black" /><br/>Cloud Warehouse</td>
<td align="center"><img src="https://img.shields.io/badge/-dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" /><br/>Transformations</td>
<td align="center"><img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" /><br/>Web Dashboard</td>
<td align="center"><img src="https://img.shields.io/badge/-Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" /><br/>Desktop BI</td>
</tr>
</table>

---

## 🏗️ Architecture

```
CSV Files → Python Ingestion → MotherDuck → dbt Transformations → Dashboards
                                    │
                           ┌────────┴────────┐
                           │   Data Layers    │
                           ├─────────────────┤
                           │ raw_olist       │  9 source tables
                           │ staging         │  8 stg_* models
                           │ marts           │  4 business models
                           └─────────────────┘
```

### Data Models

| Layer | Models |
|-------|--------|
| **Staging** | `stg_orders` · `stg_customers` · `stg_products` · `stg_sellers` · `stg_payments` · `stg_reviews` · `stg_order_items` · `stg_geolocation` |
| **Marts** | `fct_orders` · `dim_customers` · `dim_products` · `dim_sellers` |

---

## 🚀 Quick Start

```bash
# 1. Activate environment
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

# 2. Load data to MotherDuck
python ingest.py

# 3. Build dbt models
cd olist_dbt
dbt run
dbt test
```

---

## 📁 Project Structure

```
olist_analytics_platform/
├── 📊 streamlit_app.py              # Web dashboard
├── 📥 ingest.py                     # Data loader
├── 📈 OLIST E-commerce Dashboard.pbix
├── 🖼️ dashboard_preview.png
├── 📋 requirements.txt
│
├── 📂 data/                         # Raw CSVs
├── 📂 olist_dbt/
│   └── models/
│       ├── staging/                 # 8 staging models
│       └── marts/                   # 4 mart models
└── 📂 .github/workflows/            # CI/CD
```

---

## 📚 Dataset

> **Olist Brazilian E-commerce Dataset**  
> 100K+ orders · 9 tables · 2016-2018  
> [Kaggle](https://www.kaggle.com/olistbr/brazilian-ecommerce)

---

<div align="center">

### Built by [Mohith Akash](https://github.com/Mohith-Akash)

⭐ Star this repo if you found it helpful!

</div>
