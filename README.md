<div align="center">

# 🛒 Olist E-commerce Analytics Platform

### Lakehouse analytics with Databricks, Delta Lake & Streamlit

[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://olist-analytics-platform.streamlit.app/)
[![Databricks](https://img.shields.io/badge/Databricks-Lakehouse-FF3621?logo=databricks&logoColor=white)](https://databricks.com)
[![Delta Lake](https://img.shields.io/badge/Delta_Lake-Storage-00ADD8?logo=delta&logoColor=white)](https://delta.io)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![CI](https://github.com/Mohith-akash/olist-analytics-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Mohith-akash/olist-analytics-platform/actions/workflows/ci.yml)

**[Live Dashboard](https://olist-analytics-platform.streamlit.app/)** · **[Dataset](https://www.kaggle.com/olistbr/brazilian-ecommerce)**

</div>

---

## 🎯 Overview

A complete analytics platform analyzing **100,000+ orders** from Brazilian e-commerce marketplace Olist (2016-2018). Built to demonstrate:

- **Lakehouse Architecture** - Databricks with Delta Lake storage
- **Medallion Pattern** - Bronze → Silver → Gold data layers
- **SQL Expertise** - Complex transformations, CTEs, JOINs
- **Data Visualization** - Interactive Streamlit dashboard
- **CI/CD** - GitHub Actions for linting and testing

---

## 📊 Dashboard Preview

### KPIs & Insights
![Dashboard Hero](docs/images/screenshot_hero.png)

### Charts & Analytics
![Dashboard Charts](docs/images/screenshot_charts.png)

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center"><img src="https://img.shields.io/badge/-Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white" /><br/>Lakehouse Platform</td>
<td align="center"><img src="https://img.shields.io/badge/-Delta_Lake-00ADD8?style=for-the-badge&logo=delta&logoColor=white" /><br/>Storage Format</td>
<td align="center"><img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" /><br/>Web Dashboard</td>
<td align="center"><img src="https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /><br/>Backend</td>
</tr>
</table>

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────────────────────┐
                    │              Databricks Lakehouse                   │
                    │                                                     │
CSV Files ─────────►│  ┌──────────┐   ┌──────────┐   ┌──────────────┐    │
                    │  │  Bronze  │──►│  Silver  │──►│    Gold      │    │
                    │  │  (raw)   │   │ (clean)  │   │ (analytics)  │    │
                    │  │ 9 tables │   │ 7 tables │   │  4 tables    │    │
                    │  └──────────┘   └──────────┘   └──────────────┘    │
                    │                                       │            │
                    │              Delta Lake Storage       │            │
                    └───────────────────────────────────────┼────────────┘
                                                            │
                                                            ▼
                                                    ┌──────────────┐
                                                    │  Streamlit   │
                                                    │  Dashboard   │
                                                    └──────────────┘
```

### Medallion Architecture

| Layer | Tables | Description |
|-------|--------|-------------|
| **Bronze** | 9 tables | Raw data ingested from CSV files |
| **Silver** | 7 tables | Cleaned, typed, and validated data |
| **Gold** | 4 tables | Business-ready facts and dimensions |

### Data Models (Gold Layer)

| Model | Description |
|-------|-------------|
| `fct_orders` | Order facts with revenue metrics |
| `dim_customers` | Customer dimension with segmentation |
| `dim_products` | Product dimension with sales tiers |
| `dim_sellers` | Seller dimension with performance ratings |

---

## 🔐 Data Governance

The marts live under **Unity Catalog**, which adds governance on top of the lakehouse:

- **Ownership & documentation** - every Gold table carries an owner plus table and column descriptions
- **Access boundaries** - Bronze/Silver/Gold are separate schemas, so raw data and business-ready data can be granted independently
- **Lineage** - Unity Catalog records table-level lineage from Bronze through Gold automatically
- **Audit trail** - queries against the warehouse are visible in Databricks query history

Relevant for any EU/GDPR context: "where does customer data live, who can read it, and what feeds this dashboard" can be answered directly from the catalog.

---

## 🚀 Quick Start

### 1. Clone & Setup Environment

```bash
git clone https://github.com/Mohith-akash/olist-analytics-platform.git
cd olist-analytics-platform

python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

### 2. Configure Databricks Connection

Create `.streamlit/secrets.toml`:

```toml
DATABRICKS_HOST = "your-workspace.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/your-warehouse-id"
DATABRICKS_TOKEN = "your-access-token"
```

### 3. Run the Dashboard

```bash
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
olist_analytics_platform/
├── 📊 streamlit_app.py              # Dashboard entry point
├── 📋 requirements.txt              # Python dependencies
│
├── 📂 app/                          # Core modules
│   ├── components.py                # Reusable UI helpers
│   ├── database.py                  # Databricks SQL connection
│   ├── styles.py                    # CSS styling
│   └── utils.py                     # Formatting utilities
│
├── 📂 tabs/                         # Dashboard components
│   ├── home.py                      # KPIs and overview
│   ├── analytics.py                 # Analysis charts
│   ├── query.py                     # Data explorer
│   └── about.py                     # Project info
│
├── 📂 databricks/                   # SQL notebooks (reference)
│   ├── 01_bronze_layer.sql
│   ├── 02_silver_layer.sql
│   └── 03_gold_layer.sql
│
└── 📂 docs/images/                  # Screenshots
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
