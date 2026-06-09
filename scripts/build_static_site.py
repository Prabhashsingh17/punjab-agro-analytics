"""Build static Plotly dashboard for GitHub Pages permanent hosting."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.io as pio

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "processed" / "sales_clean.csv"
OUT = BASE / "site"


def build():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))
        .agg(revenue=("net_revenue", "sum"), orders=("sale_id", "count"))
        .reset_index()
    )
    monthly["month"] = monthly["sale_date"].astype(str)

    equip = df.groupby("equipment")["net_revenue"].sum().reset_index()
    district = (
        df.groupby("district")["net_revenue"]
        .sum()
        .reset_index()
        .sort_values("net_revenue", ascending=False)
        .head(10)
    )
    season = df.groupby("season")["net_revenue"].sum().reset_index()
    payment = df.groupby("payment_mode")["sale_id"].count().reset_index(name="count")

    charts = [
        px.line(monthly, x="month", y="revenue", title="Monthly Revenue Trend", markers=True),
        px.bar(equip, x="equipment", y="net_revenue", title="Revenue by Equipment", color="net_revenue", color_continuous_scale="Greens"),
        px.bar(district, x="district", y="net_revenue", title="Top 10 Districts", color="net_revenue", color_continuous_scale="Greens"),
        px.pie(season, names="season", values="net_revenue", title="Revenue by Season", color_discrete_sequence=px.colors.sequential.Greens),
        px.pie(payment, names="payment_mode", values="count", title="Payment Mode", color_discrete_sequence=px.colors.sequential.Greens_r),
    ]

    chart_html = "\n".join(
        pio.to_html(c, include_plotlyjs=False, full_html=False, config={"displayModeBar": False})
        for c in charts
    )

    kpis = {
        "revenue": f"₹{df['net_revenue'].sum():,.0f}",
        "orders": f"{len(df):,}",
        "units": f"{df['quantity'].sum():,}",
        "customers": f"{df['customer_id'].nunique():,}",
        "avg_order": f"₹{df['net_revenue'].mean():,.0f}",
        "gopalganj": f"{df[df['district']=='Gopalganj']['net_revenue'].sum() / df['net_revenue'].sum() * 100:.1f}%",
    }

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Punjab Agro Centre Analytics</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:Segoe UI,sans-serif;background:#F1F8E9;color:#1B5E20}}
    .hero{{background:linear-gradient(135deg,#1B5E20,#43A047);color:#fff;padding:32px 24px;text-align:center}}
    .hero h1{{font-size:2rem;margin-bottom:8px}}
    .hero p{{opacity:.9}}
    .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;padding:24px;max-width:1200px;margin:auto}}
    .kpi{{background:#fff;border-radius:12px;padding:20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
    .kpi .val{{font-size:1.4rem;font-weight:700;color:#2E7D32}}
    .kpi .lbl{{font-size:.85rem;color:#666;margin-top:4px}}
    .charts{{max-width:1200px;margin:0 auto;padding:0 24px 40px;display:grid;gap:24px}}
    .chart{{background:#fff;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
    .footer{{text-align:center;padding:20px;color:#666;font-size:.9rem}}
    .badge{{display:inline-block;background:#C8E6C9;color:#1B5E20;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-top:8px}}
  </style>
</head>
<body>
  <div class="hero">
    <h1>🌾 PUNJAB AGRO CENTRE</h1>
    <p>Agricultural Equipment Sales Analytics | Gopalganj, Bihar</p>
    <p style="margin-top:6px;font-size:.9rem">Rotavator • Cultivator • Harvester • Zero Till • Threshing Machine • Tawa</p>
    <div class="badge">✅ Permanently Live on GitHub Pages</div>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="val">{kpis['revenue']}</div><div class="lbl">Total Revenue</div></div>
    <div class="kpi"><div class="val">{kpis['orders']}</div><div class="lbl">Total Orders</div></div>
    <div class="kpi"><div class="val">{kpis['units']}</div><div class="lbl">Units Sold</div></div>
    <div class="kpi"><div class="val">{kpis['customers']}</div><div class="lbl">Customers</div></div>
    <div class="kpi"><div class="val">{kpis['avg_order']}</div><div class="lbl">Avg Order Value</div></div>
    <div class="kpi"><div class="val">{kpis['gopalganj']}</div><div class="lbl">Gopalganj Share</div></div>
  </div>
  <div class="charts">{chart_html}</div>
  <div class="footer">
    Fresher Data Analyst Portfolio Project | Punjab Agro Centre, Gopalganj, Bihar<br/>
    Tools: Python • Pandas • SQL • Plotly • Streamlit
  </div>
</body>
</html>"""

    (OUT / "index.html").write_text(html, encoding="utf-8")
    print(f"Built: {OUT / 'index.html'}")


if __name__ == "__main__":
    build()
