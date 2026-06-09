# 🌾 PUNJAB AGRO CENTRE — Data Analytics Project

**Fresher Data Analyst Portfolio Project | End-to-End**

---

## Company Overview

| Field | Details |
|-------|---------|
| **Company** | Punjab Agro Centre |
| **Location** | Gopalganj, Bihar |
| **Business** | Agricultural Equipment Sales |
| **Products** | Rotavator, Cultivator, Harvester, Zero Till Seed Drill, Threshing Machine, Tawa (Plough) |
| **Customers** | Farmers, Dealers, Cooperatives — Bihar ke 17+ districts se |

Gopalganj me based ye company agricultural machinery bechti hai. Customers sirf Gopalganj se nahi — Siwan, Chapra, Muzaffarpur, Patna, Darbhanga aur Bihar ke aur kai districts se log yahan aake equipment le jaate hain.

---

## Project Objective

Is project ka goal hai **sales data ko analyze karke business decisions** me help karna:

1. Kaun sa equipment sabse zyada bikta hai?
2. Kaun se district se sabse zyada customers aate hain?
3. Kharif vs Rabi season me demand ka pattern kya hai?
4. Revenue trend kya hai — growth ho rahi hai ya nahi?
5. Payment mode aur customer type ka analysis

---

## Tech Stack

| Tool | Use Case |
|------|----------|
| **Python** | Data cleaning, EDA, visualization |
| **Pandas** | Data manipulation |
| **SQL** | Business queries (10 analytical queries) |
| **Plotly** | Interactive charts |
| **Streamlit** | Live dashboard |
| **Matplotlib/Seaborn** | Static EDA charts |

---

## Project Structure

```
punjab-agro-analytics/
├── app.py                    # Streamlit Dashboard (Main)
├── requirements.txt          # Python dependencies
├── render.yaml               # Deployment config
├── data/
│   ├── raw/                  # Raw CSV datasets
│   └── processed/            # Cleaned data
├── sql/
│   └── analysis_queries.sql  # 10 SQL business queries
├── src/
│   ├── generate_data.py      # Synthetic data generator
│   └── eda_analysis.py       # Python EDA script
├── outputs/
│   └── eda_dashboard.png     # Static charts
└── README.md
```

---

## Datasets

| File | Records | Description |
|------|---------|-------------|
| `customers.csv` | 350 | Customer info, district, type |
| `sales.csv` | ~1,170 | Sales transactions (2023-2024) |
| `inventory.csv` | 6 | Equipment stock levels |

**Columns in Sales Data:**
`sale_id, sale_date, year, month, quarter, season, customer_id, district, customer_type, equipment, quantity, unit_price, gross_amount, discount_pct, discount_amount, net_revenue, payment_mode, delivery_status`

---

## How to Run Locally

### Step 1: Install Dependencies
```bash
cd punjab-agro-analytics
python -m pip install -r requirements.txt
```

### Step 2: Generate Data
```bash
python src/generate_data.py
```

### Step 3: Run EDA Analysis
```bash
python src/eda_analysis.py
```

### Step 4: Launch Dashboard
```bash
streamlit run app.py
```

Dashboard open hoga: **http://localhost:8501**

---

## SQL Analysis (10 Queries)

File: `sql/analysis_queries.sql`

| # | Query | Business Question |
|---|-------|-------------------|
| 1 | Total Revenue KPIs | Overall performance |
| 2 | Monthly Revenue Trend | Growth pattern |
| 3 | Top Equipment | Best sellers |
| 4 | District-wise Sales | Geographic analysis |
| 5 | Seasonal Demand | Kharif vs Rabi |
| 6 | Customer Type | Farmer vs Dealer |
| 7 | Payment Mode | Cash vs UPI vs EMI |
| 8 | Top 10 Customers | VIP customers |
| 9 | Discount Impact | Pricing strategy |
| 10 | YoY Growth | Year-over-year comparison |

---

## Key Insights (Sample)

1. **Gopalganj** home district hai — ~25-30% revenue yahan se aata hai
2. **Rotavator aur Tawa** sabse zyada bikne wale products hain
3. **Kharif Prep (June-July)** me demand peak hoti hai
4. **Siwan, Chapra, Muzaffarpur** — top outstation districts
5. **EMI/Finance** option se high-value equipment ki sales badh sakti hai

---

## Dashboard Features

- 📊 **KPI Cards** — Revenue, Orders, Units, Avg Order Value
- 📈 **Monthly Revenue Trend** — Interactive line chart
- 🚜 **Equipment Analysis** — Bar + Pie charts
- 🗺️ **District Map** — Bihar districts comparison
- 📅 **Seasonality** — Kharif/Rabi heatmap
- 💳 **Payment Analysis** — Cash, UPI, EMI breakdown
- 🔍 **Filters** — Date, District, Equipment, Customer Type
- ⬇️ **CSV Export** — Filtered data download

---

## Live Demo (Permanent)

**Dashboard URL:** https://prabhashsingh17.github.io/punjab-agro-analytics/

24/7 live — GitHub Pages par hosted. PC band hone par bhi kaam karta hai.

---

## Deployment

### Option 1: Streamlit Community Cloud (Free)
1. GitHub pe repo push karein
2. [share.streamlit.io](https://share.streamlit.io) pe login karein
3. Repo select karein, main file: `app.py`
4. Deploy!

### Option 2: Render (Free)
1. GitHub repo connect karein
2. `render.yaml` automatically detect hoga
3. Deploy button click karein

---

## Skills Demonstrated (Resume Points)

- ✅ Data Collection & Cleaning
- ✅ Exploratory Data Analysis (EDA)
- ✅ SQL for Business Intelligence
- ✅ Data Visualization (Plotly, Matplotlib)
- ✅ Interactive Dashboard Development
- ✅ Business Insights & Recommendations
- ✅ End-to-End Project Deployment

---

## Author

**Data Analyst (Fresher)**  
Project: Punjab Agro Centre Sales Analytics  
Location: Gopalganj, Bihar

---

*Note: Ye project synthetic (demo) data use karta hai jo real business patterns par based hai. Real company data se replace karke production me use kiya ja sakta hai.*
