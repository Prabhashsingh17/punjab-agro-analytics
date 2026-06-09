# Punjab Agro Centre — Project Report (Fresher Portfolio)

## 1. Problem Statement

Punjab Agro Centre, Gopalganj (Bihar) me agricultural equipment bechta hai. Company ke paas sales data tha lekin usse actionable insights nahi nikal pa rahe the:

- Kaun sa product sabse zyada bikta hai?
- Bihar ke kaun se districts se zyada customers aate hain?
- Season ke hisaab se inventory kaise plan karein?
- Revenue badh rahi hai ya nahi?

**Goal:** Data analysis se sales improve karna aur better business decisions lena.

---

## 2. Approach (End-to-End Pipeline)

```
Data Collection → Data Cleaning → SQL Analysis → Python EDA → Dashboard → Insights
```

| Phase | Tool | Output |
|-------|------|--------|
| Data Generation | Python | 3 CSV files (customers, sales, inventory) |
| Data Cleaning | Pandas | Null check, cancelled orders remove |
| SQL Analysis | SQL | 10 business queries |
| EDA | Python + Matplotlib | Summary report + charts |
| Dashboard | Streamlit + Plotly | Interactive live dashboard |
| Deployment | Streamlit / Render | Public URL |

---

## 3. Data Overview

- **Time Period:** Jan 2023 — Dec 2024
- **Sales Records:** 1,179 transactions
- **Customers:** 350 (17 Bihar districts)
- **Products:** 6 equipment types
- **Total Revenue:** ~₹16.99 Crore

---

## 4. Key Findings

### Revenue & Geography
- **Gopalganj** (home district) = **28.2%** of total revenue
- Top outstation districts: Chapra, Samastipur, Muzaffarpur, Siwan
- 17 Bihar districts se customers aate hain — wide geographic reach

### Product Performance
| Equipment | Revenue Share |
|-----------|---------------|
| Harvester | Highest (premium product) |
| Rotavator | High volume |
| Zero Till Seed Drill | Growing demand |
| Tawa (Plough) | Budget segment leader |

### Seasonality
- **Rabi Prep (Oct-Nov)** aur **Kharif Prep (Jun-Jul)** me demand badhti hai
- Harvester aur Rotavator seasonal peaks alag hain — inventory planning zaroori

### Customer & Payment
- **72%** customers Farmers hain
- **Cash + UPI** = 65% transactions
- **EMI/Finance** sirf 13.5% — high-value equipment ke liye opportunity

---

## 5. Recommendations

1. **District Agents:** Siwan, Chapra, Muzaffarpur me part-time sales agents rakhein
2. **Seasonal Campaigns:** June aur October me 2 mahine pehle marketing start karein
3. **EMI Tie-ups:** Banks/NBFC se Harvester ke liye easy EMI — ₹7+ Cr revenue product hai
4. **Stock Planning:** Rotavator + Tawa ka stock Kharif se pehle double karein
5. **Dealer Channel:** Dealers sirf 18% hain lekin bulk orders dete hain — dealer network expand karein

---

## 6. Resume Bullet Points

> • Built end-to-end sales analytics dashboard for Punjab Agro Centre (agricultural equipment, Gopalganj Bihar) analyzing 1,179 transactions across 17 districts using Python, SQL, and Streamlit.

> • Identified Gopalganj contributes 28% revenue; recommended district-wise sales agents for top 4 outstation districts, projected to improve reach by 15-20%.

> • Created 10 SQL business queries and interactive Plotly dashboard with filters for equipment, season, district, and payment mode analysis.

---

## 7. Tools & Skills

`Python` `Pandas` `SQL` `Streamlit` `Plotly` `Matplotlib` `Seaborn` `Data Cleaning` `EDA` `Business Intelligence` `Data Visualization`
