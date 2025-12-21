# Olist E-commerce Analytics Platform

Analytics platform for Brazilian e-commerce data using **dbt** + **MotherDuck**.

## 🔗 Live Demo

- 📊 **Streamlit Dashboard**: [olist-analytics.streamlit.app](https://olist-analytics.streamlit.app/)
- 📖 **dbt Docs**: [mohith-akash.github.io/olist-analytics-platform](https://mohith-akash.github.io/olist-analytics-platform/)

## Dashboard Features

- 6 KPIs with revenue, orders, customers, ratings
- Gauge chart for seller ratings
- Revenue trend and category breakdown
- SQL code showcase (dbt models)
- Data export to CSV

## Power BI Dashboard

Also includes a Power BI desktop dashboard (`OLIST E-commerce Dashboard.pbix`):

![Power BI Dashboard](dashboard_preview.png)

## Tech Stack

| Tool | Purpose |
|------|---------|
| **MotherDuck** | Cloud data warehouse (DuckDB) |
| **dbt Core** | SQL transformations |
| **Streamlit** | Web dashboard |
| **Power BI** | Desktop analytics |
| **Plotly** | Interactive charts |

## Setup

```bash
# Activate venv
.\venv\Scripts\activate

# Load data (first time)
python ingest.py

# Run dbt
cd olist_dbt
dbt run
dbt test
```

## Project Structure

```
olist_analytics_platform/
├── streamlit_app.py              # Web dashboard
├── ingest.py                     # Load CSVs to MotherDuck
├── OLIST E-commerce Dashboard.pbix  # Power BI dashboard
├── data/                         # Raw CSVs
└── olist_dbt/
    └── models/
        ├── staging/              # stg_*.sql
        └── marts/                # fct_*.sql, dim_*.sql
```

## Dataset

[Olist Brazilian E-commerce](https://www.kaggle.com/olistbr/brazilian-ecommerce) - 100K+ orders (2016-2018)

---

Built by [Mohith Akash](https://github.com/Mohith-Akash)
