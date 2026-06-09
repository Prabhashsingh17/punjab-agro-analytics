"""Build Data & Business Analytics dashboard for GitHub Pages."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.io as pio

BASE = Path(__file__).resolve().parent.parent
SALES = BASE / "data" / "processed" / "sales_clean.csv"
INVENTORY = BASE / "data" / "raw" / "inventory.csv"
OUT = BASE / "site"
CHART_HEIGHT = 400


def chart_html(fig):
    fig.update_layout(height=CHART_HEIGHT, margin=dict(l=40, r=20, t=50, b=40))
    inner = pio.to_html(fig, include_plotlyjs=False, full_html=False, config={"displayModeBar": True, "responsive": True})
    return f'<div class="chart-card">{inner}</div>'


def build():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(SALES, parse_dates=["sale_date"])
    inv = pd.read_csv(INVENTORY)

    monthly = df.groupby(df["sale_date"].dt.to_period("M")).agg(revenue=("net_revenue", "sum")).reset_index()
    monthly["month"] = monthly["sale_date"].astype(str)

    clv = df.groupby("customer_id")["net_revenue"].sum().reset_index()
    clv["segment"] = pd.cut(clv["net_revenue"], [0, 1e5, 3e5, float("inf")], labels=["Low Value", "Medium Value", "High Value"])
    seg = clv.groupby("segment", observed=True).size().reset_index(name="customers")

    cust_type = df.groupby("customer_type")["net_revenue"].sum().reset_index()
    equip = df.groupby("equipment")["net_revenue"].sum().reset_index()
    district = df.groupby("district")["net_revenue"].sum().reset_index().sort_values("net_revenue", ascending=False).head(10)

    merged = df.merge(inv[["equipment", "avg_unit_cost"]], on="equipment")
    merged["profit"] = (merged["unit_price"] - merged["avg_unit_cost"]) * merged["quantity"]
    margin = merged.groupby("equipment").agg(revenue=("net_revenue", "sum"), profit=("profit", "sum")).reset_index()
    margin["margin_pct"] = (margin["profit"] / margin["revenue"] * 100).round(1)

    yoy = df.groupby(["year", "equipment"])["net_revenue"].sum().unstack(fill_value=0)
    if 2023 in yoy.columns and 2024 in yoy.columns:
        yoy_g = ((yoy[2024] - yoy[2023]) / yoy[2023].replace(0, 1) * 100).reset_index(name="yoy_pct")
        yoy_g.columns = ["equipment", "yoy_pct"]
    else:
        yoy_g = equip.copy()
        yoy_g["yoy_pct"] = 0

    charts_desc = [
        chart_html(px.line(monthly, x="month", y="revenue", title="Descriptive: Monthly Revenue Trend", markers=True)),
        chart_html(px.bar(equip, x="equipment", y="net_revenue", title="Descriptive: Revenue by Product", color="net_revenue", color_continuous_scale="Greens")),
        chart_html(px.bar(district, x="district", y="net_revenue", title="Descriptive: Top 10 Districts (Market Share)", color="net_revenue", color_continuous_scale="Greens")),
    ]
    charts_diag = [
        chart_html(px.pie(seg, names="segment", values="customers", title="Diagnostic: Customer Segmentation (CLV)", color_discrete_sequence=px.colors.sequential.Greens)),
        chart_html(px.bar(cust_type, x="customer_type", y="net_revenue", title="Diagnostic: Revenue by Customer Type", color="customer_type", color_discrete_sequence=["#1B5E20", "#43A047", "#66BB6A"])),
        chart_html(px.bar(margin, x="equipment", y="margin_pct", title="Diagnostic: Profit Margin % by Equipment", color="margin_pct", color_continuous_scale="Greens")),
        chart_html(px.bar(yoy_g, x="equipment", y="yoy_pct", title="Diagnostic: Year-over-Year Growth %", color="yoy_pct", color_continuous_scale="RdYlGn")),
    ]

    kpis = {
        "revenue": df["net_revenue"].sum(),
        "orders": len(df),
        "customers": int(df["customer_id"].nunique()),
        "districts": int(df["district"].nunique()),
        "avg_order": df["net_revenue"].mean(),
        "margin": margin["profit"].sum() / margin["revenue"].sum() * 100,
    }

    districts = sorted(df["district"].unique().tolist())
    equipment = sorted(df["equipment"].unique().tolist())
    records = df[["sale_date", "district", "equipment", "customer_type", "net_revenue", "quantity", "payment_mode", "season"]].copy()
    records["sale_date"] = records["sale_date"].dt.strftime("%Y-%m-%d")
    data_json = records.to_json(orient="records")

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Punjab Agro Centre — Data & Business Analytics</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',system-ui,sans-serif;background:#F1F8E9;color:#1B5E20}}
    .hero{{background:linear-gradient(135deg,#1B5E20,#43A047);color:#fff;padding:28px 20px;text-align:center}}
    .hero h1{{font-size:clamp(1.3rem,4vw,1.9rem)}}
    .badge{{display:inline-block;background:#C8E6C9;color:#1B5E20;padding:6px 14px;border-radius:20px;font-size:.8rem;margin-top:10px;font-weight:600}}
    .framework{{max-width:1200px;margin:16px auto;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
    .fw-card{{background:#fff;border-radius:10px;padding:14px;text-align:center;border-left:4px solid #2E7D32;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
    .fw-card h3{{font-size:.95rem;color:#2E7D32}}
    .fw-card p{{font-size:.78rem;color:#666;margin-top:4px}}
    .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;padding:16px 20px;max-width:1200px;margin:auto}}
    .kpi{{background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.07)}}
    .kpi .val{{font-size:1.2rem;font-weight:700;color:#2E7D32}}
    .kpi .lbl{{font-size:.75rem;color:#666;margin-top:4px}}
    .filters{{max-width:1200px;margin:0 auto 10px;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}}
    .filters label{{font-size:.78rem;font-weight:600;display:block;margin-bottom:4px}}
    .filters select{{width:100%;padding:9px;border:1px solid #A5D6A7;border-radius:8px;background:#fff;color:#1B5E20}}
    .section{{max-width:1200px;margin:20px auto 8px;padding:0 20px}}
    .section h2{{font-size:1.1rem;color:#1B5E20;border-bottom:2px solid #A5D6A7;padding-bottom:6px}}
    .charts{{max-width:1200px;margin:0 auto;padding:8px 20px 20px;display:grid;gap:16px}}
    .chart-card{{background:#fff;border-radius:12px;padding:12px;box-shadow:0 2px 10px rgba(0,0,0,.07);min-height:{CHART_HEIGHT + 30}px}}
    .insights{{max-width:1200px;margin:0 auto 24px;padding:0 20px}}
    .insights ul{{background:#fff;border-radius:12px;padding:18px 18px 18px 32px;box-shadow:0 2px 10px rgba(0,0,0,.07);line-height:1.8;font-size:.92rem}}
    .footer{{text-align:center;padding:18px;color:#666;font-size:.82rem;border-top:1px solid #C8E6C9}}
    .plotly-graph-div{{min-height:{CHART_HEIGHT}px !important}}
  </style>
</head>
<body>
  <div class="hero">
    <h1>🌾 PUNJAB AGRO CENTRE</h1>
    <p>Data Analytics & Business Analytics Dashboard</p>
    <p style="font-size:.88rem;opacity:.9">Gopalganj, Bihar | Agricultural Equipment Business Intelligence</p>
    <div class="badge">✅ Live Project — Data + Business Analytics</div>
  </div>

  <div class="framework">
    <div class="fw-card"><h3>📊 Descriptive</h3><p>Kya hua? Revenue, orders, trends</p></div>
    <div class="fw-card"><h3>🔍 Diagnostic</h3><p>Kyun hua? Segments, margins, growth</p></div>
    <div class="fw-card"><h3>💡 Prescriptive</h3><p>Kya karein? Business actions</p></div>
  </div>

  <div class="filters">
    <div><label>District</label><select id="fDistrict"><option value="all">All</option>{"".join(f'<option>{d}</option>' for d in districts)}</select></div>
    <div><label>Equipment</label><select id="fEquip"><option value="all">All</option>{"".join(f'<option>{e}</option>' for e in equipment)}</select></div>
    <div><label>Customer Type</label><select id="fType"><option value="all">All</option><option>Farmer</option><option>Dealer</option><option>Cooperative</option></select></div>
    <div><label>Payment</label><select id="fPay"><option value="all">All</option><option>Cash</option><option>UPI</option><option>Bank Transfer</option><option>EMI/Finance</option></select></div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="val" id="kRev">₹{kpis['revenue']:,.0f}</div><div class="lbl">Total Revenue</div></div>
    <div class="kpi"><div class="val" id="kOrd">{kpis['orders']:,}</div><div class="lbl">Orders</div></div>
    <div class="kpi"><div class="val" id="kCust">{kpis['customers']:,}</div><div class="lbl">Customers</div></div>
    <div class="kpi"><div class="val">{kpis['districts']}</div><div class="lbl">Districts</div></div>
    <div class="kpi"><div class="val" id="kAvg">₹{kpis['avg_order']:,.0f}</div><div class="lbl">Avg Order Value</div></div>
    <div class="kpi"><div class="val">{kpis['margin']:.1f}%</div><div class="lbl">Est. Profit Margin</div></div>
  </div>

  <div class="section"><h2>📊 Descriptive Analytics — Performance Overview</h2></div>
  <div class="charts">{"".join(charts_desc)}</div>

  <div class="section"><h2>🔍 Diagnostic Analytics — Root Cause & Segments</h2></div>
  <div class="charts">{"".join(charts_diag)}</div>

  <div class="insights">
    <h2 style="margin-bottom:10px">💡 Prescriptive Analytics — Business Recommendations</h2>
    <ul>
      <li><b>Customer Segmentation:</b> High Value customers ko loyalty discount do — repeat business badhega</li>
      <li><b>Geographic Expansion:</b> Chapra, Samastipur, Muzaffarpur me sales agents appoint karo</li>
      <li><b>Profit Focus:</b> Harvester highest margin product hai — EMI schemes se sales badhao</li>
      <li><b>Inventory Planning:</b> Kharif season (Jun-Jul) se pehle Rotavator stock double karo</li>
      <li><b>Dealer Channel:</b> Dealers bulk orders dete hain — dealer network expand karo</li>
      <li><b>Payment Strategy:</b> EMI sirf 13.5% transactions me hai — finance tie-up karo</li>
    </ul>
  </div>

  <div class="footer">
    Data Analytics & Business Analytics Portfolio | Punjab Agro Centre, Gopalganj<br/>
    Python • Pandas • SQL • Plotly • Business Intelligence | github.com/Prabhashsingh17/punjab-agro-analytics
  </div>

  <script>
    const RAW = {data_json};
    const fmt = n => '₹' + Math.round(n).toLocaleString('en-IN');
    const els = ['fDistrict','fEquip','fType','fPay'].map(id => document.getElementById(id));
    function filterData() {{
      const [d,e,t,p] = els.map(el => el.value);
      return RAW.filter(r => (d==='all'||r.district===d) && (e==='all'||r.equipment===e) && (t==='all'||r.customer_type===t) && (p==='all'||r.payment_mode===p));
    }}
    function updateKPIs(data) {{
      const rev = data.reduce((s,r)=>s+r.net_revenue,0);
      document.getElementById('kRev').textContent = fmt(rev);
      document.getElementById('kOrd').textContent = data.length.toLocaleString('en-IN');
      document.getElementById('kCust').textContent = new Set(data.map(r=>r.district+r.customer_type)).size.toLocaleString('en-IN');
      document.getElementById('kAvg').textContent = data.length ? fmt(rev/data.length) : '₹0';
    }}
    els.forEach(el => el.addEventListener('change', () => updateKPIs(filterData())));
    window.addEventListener('load', () => document.querySelectorAll('.plotly-graph-div').forEach(d => Plotly.Plots.resize(d)));
  </script>
</body>
</html>"""

    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Built: {OUT / 'index.html'}")


if __name__ == "__main__":
    build()
