# Olist E-commerce Analytics Platform

Analytics dashboard for Brazilian e-commerce data using **dbt**, **MotherDuck**, and **Streamlit**.

## Live Demo

| Demo | Link |
|------|------|
| 📊 **Dashboard** | [olist-analytics.streamlit.app](https://olist-analytics.streamlit.app/) |
| 📖 **dbt Docs** | [mohith-akash.github.io/olist-analytics-platform](https://mohith-akash.github.io/olist-analytics-platform/) |

## Features

**Streamlit Dashboard:**
- 6 KPIs (revenue, orders, customers, ratings)
- Gauge chart for seller performance
- Interactive filters and charts
- SQL code showcase
- CSV data export

**Power BI Dashboard:**

![Power BI Dashboard](dashboard_preview.png)

## Tech Stack

| Tool | Purpose |
|------|---------|
| MotherDuck | Cloud DuckDB warehouse |
| dbt Core | SQL transformations |
| Streamlit | Web dashboard |
| Power BI | Desktop analytics |
| Plotly | Interactive charts |

## Data Model

| Layer | Models |
|-------|--------|
| Staging | `stg_orders`, `stg_customers`, `stg_products`, `stg_sellers`, `stg_payments`, `stg_reviews`, `stg_order_items`, `stg_geolocation` |
| Marts | `fct_orders`, `dim_customers`, `dim_products`, `dim_sellers` |

## Setup

```bash
# Activate environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Load data to MotherDuck
python ingest.py

# Run dbt
cd olist_dbt
dbt run
dbt test
```

## Project Structure

```
olist_analytics_platform/
├── streamlit_app.py     # Web dashboard
├── ingest.py            # CSV loader
├── requirements.txt
├── dashboard_preview.png
├── OLIST E-commerce Dashboard.pbix
├── data/                # Raw CSVs
└── olist_dbt/
    └── models/
        ├── staging/     # 8 staging models
        └── marts/       # 4 mart models
```

## Dataset

[Olist Brazilian E-commerce](https://www.kaggle.com/olistbr/brazilian-ecommerce) - 100K+ orders from 2016-2018.

---

Built by [Mohith Akash](https://github.com/Mohith-Akash)
