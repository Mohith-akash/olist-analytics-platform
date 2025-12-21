# 🛒 Olist E-commerce Data Warehouse

A **Modern Data Stack (MDS)** analytics platform built with **dbt** and **MotherDuck** (Cloud DuckDB) for analyzing 100,000+ Brazilian e-commerce orders.

## 🎯 Project Overview

This project transforms raw e-commerce data into a clean, analytics-ready data warehouse using industry-standard practices:

- **3-Layer Architecture**: Raw → Staging → Marts
- **Dimensional Modeling**: Fact and dimension tables
- **Data Quality**: dbt tests for validation
- **Documentation**: Full column-level documentation

## 🔗 Live Demo

| Demo | Description |
|------|-------------|
| 📖 [**dbt Docs**](https://mohith-akash.github.io/olist-analytics-platform/) | Interactive data lineage, models, and documentation |
| 📊 **Power BI Dashboard** | *Coming soon - Publish to Web* |

> **Note:** dbt docs are auto-deployed via GitHub Actions on every push to main.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MotherDuck Cloud                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  RAW LAYER  │    │   STAGING   │    │       MARTS         │ │
│  │  raw_olist  │───▶│   stg_*     │───▶│  fct_* / dim_*      │ │
│  │             │    │             │    │                     │ │
│  │ • orders    │    │ • stg_orders│    │ • fct_orders        │ │
│  │ • customers │    │ • stg_custs │    │ • dim_customers     │ │
│  │ • products  │    │ • stg_items │    │ • dim_products      │ │
│  │ • sellers   │    │ • stg_prods │    │ • dim_sellers       │ │
│  │ • payments  │    │ • stg_pays  │    │                     │ │
│  │ • reviews   │    │ • stg_sells │    │                     │ │
│  │             │    │ • stg_revs  │    │                     │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Power BI Dashboard

The project includes an interactive Power BI dashboard (`OLIST E-commerce Dashboard.pbix`) featuring:
- **KPI Cards**: Total Revenue, Orders, and Customers
- **Bar Chart**: Top Product Categories by Revenue
- **Pie Charts**: Seller Distribution, Revenue by State
- **Line Chart**: Monthly Order Trend

![Dashboard Preview](dashboard_preview.png)

## 📊 Data Models

### Staging Layer (`models/staging/`)
Clean and standardize raw data:

| Model | Description |
|-------|-------------|
| `stg_orders` | Order transactions with status and timestamps |
| `stg_customers` | Customer profiles with location |
| `stg_order_items` | Line items with pricing |
| `stg_products` | Product catalog with dimensions |
| `stg_payments` | Payment details and methods |
| `stg_sellers` | Seller profiles with location |
| `stg_reviews` | Customer review scores and comments |

### Marts Layer (`models/marts/`)
Business-ready analytics tables:

| Model | Description |
|-------|-------------|
| `fct_orders` | Fact table with order line items, products, and financials |
| `dim_customers` | Customer dimension with lifetime value and classification |
| `dim_products` | Product dimension with sales metrics and popularity tier |
| `dim_sellers` | Seller dimension with performance metrics and tier |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MotherDuck account (free tier available)

### Setup

1. **Clone and enter the project**
   ```bash
   cd olist_analytics_platform
   ```

2. **Activate virtual environment**
   ```powershell
   # Windows PowerShell
   .\venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Load raw data to MotherDuck** (first time only)
   ```bash
   python ingest.py
   ```

4. **Build the data warehouse**
   ```bash
   cd olist_dbt
   dbt run
   ```

5. **Run tests**
   ```bash
   dbt test
   ```

## 📈 Example Queries

Once built, you can answer business questions instantly:

```sql
-- Top 10 customers by lifetime value
SELECT customer_unique_id, city, state, lifetime_value, customer_type
FROM dim_customers
ORDER BY lifetime_value DESC
LIMIT 10;

-- Revenue by product category
SELECT product_category_name, 
       SUM(total_revenue) as category_revenue,
       COUNT(*) as products_count
FROM dim_products
GROUP BY 1
ORDER BY 2 DESC;

-- Top sellers by tier
SELECT seller_tier, 
       COUNT(*) as seller_count,
       AVG(avg_review_score) as avg_rating
FROM dim_sellers
GROUP BY 1;
```

## 🧪 Data Quality

This project includes dbt tests for:
- **Uniqueness**: Primary keys are unique
- **Not Null**: Critical fields are populated
- **Accepted Values**: Status/type fields have valid values
- **Relationships**: Foreign keys reference valid records

Run all tests:
```bash
dbt test
```

## 📁 Project Structure

```
olist_analytics_platform/
├── data/                    # Raw CSV files
├── ingest.py               # Data loader script
├── olist_dbt/              # dbt project
│   ├── models/
│   │   ├── staging/        # Staging models
│   │   │   ├── stg_*.sql
│   │   │   ├── sources.yml
│   │   │   └── schema.yml
│   │   └── marts/          # Business models
│   │       ├── fct_*.sql
│   │       ├── dim_*.sql
│   │       └── schema.yml
│   ├── dbt_project.yml
│   └── profiles.yml
└── venv/                   # Python virtual environment
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **MotherDuck** | Cloud data warehouse (DuckDB) |
| **dbt** | Data transformation & testing |
| **Python** | Data ingestion |
| **SQL** | Business logic |

## 📚 Dataset

The [Olist Brazilian E-commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) contains:
- 100,000+ orders from 2016-2018
- Customer, product, seller, and review data
- Real anonymized commercial data

---

Built as an Analytics Engineering portfolio project 🚀
