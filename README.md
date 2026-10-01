# 🛍️ Customer Shopping Behavior Analysis

**Python · PostgreSQL · Power BI**

An end-to-end analytics project that turns raw retail transaction data into actionable business insights: from data cleaning and feature engineering in Python, to structured analysis in SQL, to an interactive Power BI dashboard for decision-makers.

![Dashboard Preview](images/dashboard.png)

---

## 📌 Table of Contents

- [Business Problem](#-business-problem)
- [Objectives & Key Questions](#-objectives--key-questions)
- [Deliverables](#-deliverables)
- [Tech Stack](#-tech-stack)
- [Project Workflow](#-project-workflow)
- [Data Preparation (Python)](#-data-preparation-python)
- [SQL Analysis](#-sql-analysis)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Key Insights](#-key-insights)
- [Business Recommendations](#-business-recommendations)
- [Getting Started](#-getting-started)
- [Author](#-author)

---

## 🧩 Business Problem

A retail company wants to understand its customers' shopping behavior to **improve sales, customer satisfaction, and long-term loyalty**. The central question:

> **"How can the company leverage consumer shopping data to identify trends, improve customer engagement, and optimize marketing and product strategies?"**

As the analyst, the task is to analyze the company's consumer behavior dataset to answer this overarching business question.

---

## 🎯 Objectives & Key Questions

| Theme | Questions Explored |
|---|---|
| **Customer segments** | How do revenue and spending differ by gender and age group? |
| **Loyalty & retention** | How many customers are New, Returning, or Loyal? Are repeat buyers more likely to subscribe? |
| **Purchase drivers** | Do discounts, shipping type, and subscription status influence how much customers spend? |
| **Product performance** | Which categories and products lead in revenue, volume, ratings, and discount reliance? |
| **Engagement** | Do subscribers spend more than non-subscribers? |

---

## 📦 Deliverables

| # | Deliverable | Status / Location |
|---|---|---|
| 1 | **Data Preparation & Modeling (Python):** clean and transform the raw dataset | [`notebooks/`](notebooks/) |
| 2 | **Data Analysis (SQL):** structure data in PostgreSQL and run queries on segments, loyalty, and purchase drivers | [`sql/`](sql/) |
| 3 | **Visualization & Insights (Power BI):** interactive dashboard | [`dashboard/`](dashboard/) |
| 4 | **Report & Presentation:** findings and business recommendations | [`reports/`](reports/) |

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, Pandas |
| Database | PostgreSQL, pgAdmin |
| Python–DB Connection | SQLAlchemy, psycopg2 |
| Querying | SQL (CTEs, window functions, subqueries, conditional aggregation) |
| Visualization | Power BI |
| Environment | Jupyter Notebook (Anaconda) |

---

## 🔄 Project Workflow

```
Raw CSV  →  Python (clean + engineer features)  →  PostgreSQL  →  SQL analysis  →  Power BI dashboard  →  Report & recommendations
```

1. **Load** the raw CSV into Pandas
2. **Explore** with `.info()`, `.describe()`, and null checks
3. **Clean** missing values and standardize column names
4. **Engineer** new features (`age_group`, `purchase_frequency_days`)
5. **Load** the cleaned data into PostgreSQL
6. **Analyze** with 10 business-driven SQL queries
7. **Visualize** results in an interactive Power BI dashboard
8. **Report** findings and recommendations to stakeholders


---

## 🐍 Data Preparation (Python)

### 1. Exploration
- Loaded the dataset with `pd.read_csv()`
- Inspected structure with `df.info()` and `df.describe(include='all')`
- Checked for missing values with `df.isnull().sum()`

### 2. Missing Value Treatment
Missing **Review Rating** values were imputed with the **median rating of each product category**, which preserves category-level patterns and is robust to outliers:

```python
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
```

### 3. Column Standardization
Columns were converted to `snake_case` for readability and SQL compatibility, and `purchase_amount_(usd)` was renamed to `purchase_amount`.

### 4. Feature Engineering

| New Feature | Description |
|---|---|
| `age_group` | Four quartile-based groups (**Young Adult, Adult, Middle-aged, Senior**) created with `pd.qcut` |
| `purchase_frequency_days` | Numeric conversion of `frequency_of_purchases` (e.g., Weekly → 7, Monthly → 30, Annually → 365) |

### 5. Redundant Column Removal
`discount_applied` and `promo_code_used` matched on every row, so `promo_code_used` was dropped.

### 6. Loading into PostgreSQL
The cleaned DataFrame was written to a `customer` table in PostgreSQL via SQLAlchemy and `df.to_sql()`.

---

## 🗄️ SQL Analysis

Ten business questions were answered in PostgreSQL:

| # | Business Question | Techniques |
|---|---|---|
| 1 | Total revenue: male vs. female customers | `GROUP BY`, `SUM` |
| 2 | Discount users who still spent above the average purchase amount | Subquery |
| 3 | Top 5 products by average review rating | `AVG`, `ROUND`, `LIMIT` |
| 4 | Average purchase amount: Standard vs. Express shipping | `IN`, `AVG` |
| 5 | Do subscribers spend more? Average spend and total revenue by status | Multiple aggregations |
| 6 | Top 5 products by share of discounted purchases | Conditional aggregation |
| 7 | Segment customers into New, Returning, Loyal | CTE, `CASE WHEN` |
| 8 | Top 3 most purchased products in each category | CTE, `ROW_NUMBER() OVER (PARTITION BY ...)` |
| 9 | Are repeat buyers (more than 5 previous purchases) likely to subscribe? | Filtering, `GROUP BY` |
| 10 | Revenue contribution of each age group | `GROUP BY`, `ORDER BY` |

**Loyalty segmentation logic (Q7):**

| Segment | Rule |
|---|---|
| New | 1 previous purchase |
| Returning | 2 to 10 previous purchases |
| Loyal | More than 10 previous purchases |

Full queries: [`sql/business_queries.sql`](sql/business_queries.sql)

---

## 📊 Power BI Dashboard

**KPIs**
- **3.9K** customers
- **$59.76** average purchase amount
- **3.75** average review rating

**Visuals**
- % of customers by subscription status (donut)
- Revenue by category and Sales by category (bar)
- Revenue by age group and Sales by age group (bar)

**Interactive slicers:** Subscription Status · Gender · Category · Shipping Type

---

## 💡 Key Insights

- **Subscription adoption is low:** only **27%** of customers are subscribed vs. **73%** who are not.
- **Clothing is the core category,** leading in both revenue and order count, followed by Accessories and Footwear. **Outerwear is the smallest** on both measures.
- **Young Adults generate the most revenue** of the four age groups, while order volume is fairly evenly spread across groups.
- Average **review rating is 3.75**, suggesting moderate satisfaction with room to improve.

> 📝 Add findings from your SQL outputs here (gender revenue split, subscriber vs. non-subscriber spend, discount-heavy products, loyalty segment counts, subscription rate among repeat buyers).

---

## 🚀 Business Recommendations

*Preliminary, based on the dashboard. Validate and refine with your SQL results.*

1. **Grow subscriptions.** With only 27% subscribed, target repeat buyers and Loyal customers with subscription offers. Use Q5 and Q9 to confirm subscribers spend more and that repeat buyers are receptive.
2. **Double down on Clothing and Accessories** in marketing and inventory, since they drive most revenue and orders.
3. **Review Outerwear strategy.** Investigate whether low performance stems from pricing, seasonality, assortment, or visibility.
4. **Tailor campaigns by age group,** prioritizing Young Adults for revenue while testing ways to lift spend in lower-revenue groups.
5. **Use discounts selectively.** Use Q2 and Q6 to see which products depend on discounts and where discounts can be reduced without hurting sales.
6. **Lift satisfaction.** Use ratings by product (Q3) to find and fix low-rated items, and promote top-rated ones.

---
## 🛠️ Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL and pgAdmin
- Power BI Desktop

### Installation

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install -r requirements.txt
```

Suggested `requirements.txt`:

```
pandas
psycopg2-binary
sqlalchemy
jupyter
python-dotenv
```

### Database Setup

1. Create a database named `customer_behavior` in pgAdmin.
2. Create a `.env` file in the project root (it is git-ignored, so it won't be committed):

```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=customer_behavior
```

3. Connect from Python:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

df.to_sql("customer", engine, if_exists="replace", index=False)
```

### Run the Project

1. Run the notebook in `notebooks/` to clean the data and load it into PostgreSQL.
2. Execute `sql/business_queries.sql` in pgAdmin or `psql`.
3. Open the `.pbix` file in Power BI Desktop and refresh the data source to point to your database.


## 👤 Author

**Rucha Dhage**
- GitHub: [@Ruchadhage](https://github.com/Ruchadhage)

