"""Build interactive static dashboard for GitHub Pages permanent hosting."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.io as pio

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "processed" / "sales_clean.csv"
OUT = BASE / "site"
CHART_HEIGHT = 420


def chart_html(fig):
    fig.update_layout(height=CHART_HEIGHT, margin=dict(l=40, r=20, t=50, b=40))
    inner = pio.to_html(
        fig, include_plotlyjs=False, full_html=False, config={"displayModeBar": True, "responsive": True}
    )
    return f'<div class="chart-card">{inner}</div>'


def build():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))
        .agg(revenue=("net_revenue", "sum"))
        .reset_index()
    )
    monthly["month"] = monthly["sale_date"].astype(str)

    equip = df.groupby("equipment")["net_revenue"].sum().reset_index()
    district = (
        df.groupby("district")["net_revenue"].sum().reset_index().sort_values("net_revenue", ascending=False).head(10)
    )
    season = df.groupby("season")["net_revenue"].sum().reset_index()
    payment = df.groupby("payment_mode")["sale_id"].count().reset_index(name="count")

    charts = [
        chart_html(px.line(monthly, x="month", y="revenue", title="Monthly Revenue Trend", markers=True)),
        chart_html(px.bar(equip, x="equipment", y="net_revenue", title="Revenue by Equipment", color="net_revenue", color_continuous_scale="Greens")),
        chart_html(px.bar(district, x="district", y="net_revenue", title="Top 10 Districts", color="net_revenue", color_continuous_scale="Greens")),
        chart_html(px.pie(season, names="season", values="net_revenue", title="Revenue by Season", color_discrete_sequence=px.colors.sequential.Greens)),
        chart_html(px.pie(payment, names="payment_mode", values="count", title="Payment Mode", color_discrete_sequence=px.colors.sequential.Greens_r)),
    ]

    kpis = {
        "revenue": df["net_revenue"].sum(),
        "orders": len(df),
        "units": int(df["quantity"].sum()),
        "customers": int(df["customer_id"].nunique()),
        "avg_order": df["net_revenue"].mean(),
        "gopalganj": df[df["district"] == "Gopalganj"]["net_revenue"].sum() / df["net_revenue"].sum() * 100,
    }

    districts = sorted(df["district"].unique().tolist())
    equipment = sorted(df["equipment"].unique().tolist())
    records = df[
        ["sale_date", "district", "equipment", "customer_type", "net_revenue", "quantity", "payment_mode", "season"]
    ].copy()
    records["sale_date"] = records["sale_date"].dt.strftime("%Y-%m-%d")
    data_json = records.to_json(orient="records")

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Punjab Agro Centre Analytics</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',system-ui,sans-serif;background:#F1F8E9;color:#1B5E20}}
    .hero{{background:linear-gradient(135deg,#1B5E20,#43A047);color:#fff;padding:28px 20px;text-align:center}}
    .hero h1{{font-size:clamp(1.4rem,4vw,2rem)}}
    .hero p{{opacity:.9;margin-top:6px}}
    .badge{{display:inline-block;background:#C8E6C9;color:#1B5E20;padding:6px 14px;border-radius:20px;font-size:.8rem;margin-top:10px;font-weight:600}}
    .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;padding:20px;max-width:1200px;margin:auto}}
    .kpi{{background:#fff;border-radius:12px;padding:18px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.07);transition:transform .2s}}
    .kpi:hover{{transform:translateY(-2px)}}
    .kpi .val{{font-size:1.3rem;font-weight:700;color:#2E7D32}}
    .kpi .lbl{{font-size:.8rem;color:#666;margin-top:4px}}
    .filters{{max-width:1200px;margin:0 auto 10px;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
    .filters label{{font-size:.8rem;font-weight:600;display:block;margin-bottom:4px}}
    .filters select{{width:100%;padding:10px;border:1px solid #A5D6A7;border-radius:8px;background:#fff;color:#1B5E20}}
    .charts{{max-width:1200px;margin:0 auto;padding:10px 20px 30px;display:grid;gap:20px}}
    .chart-card{{background:#fff;border-radius:12px;padding:12px;box-shadow:0 2px 10px rgba(0,0,0,.07);min-height:{CHART_HEIGHT + 40}px}}
    .insights{{max-width:1200px;margin:0 auto 30px;padding:0 20px}}
    .insights h2{{margin-bottom:12px;color:#1B5E20}}
    .insights ul{{background:#fff;border-radius:12px;padding:20px 20px 20px 36px;box-shadow:0 2px 10px rgba(0,0,0,.07);line-height:1.8}}
    .footer{{text-align:center;padding:20px;color:#666;font-size:.85rem;border-top:1px solid #C8E6C9}}
    .loader{{text-align:center;padding:40px;color:#2E7D32;font-weight:600}}
    .plotly-graph-div{{min-height:{CHART_HEIGHT}px !important}}
  </style>
</head>
<body>
  <div class="hero">
    <h1>🌾 PUNJAB AGRO CENTRE</h1>
    <p>Agricultural Equipment Sales Analytics | Gopalganj, Bihar</p>
    <p style="font-size:.9rem">Rotavator • Cultivator • Harvester • Zero Till • Threshing Machine • Tawa</p>
    <div class="badge">✅ Live Project — 24/7 Running</div>
  </div>

  <div class="filters">
    <div><label>District</label><select id="fDistrict"><option value="all">All Districts</option>{"".join(f'<option>{d}</option>' for d in districts)}</select></div>
    <div><label>Equipment</label><select id="fEquip"><option value="all">All Equipment</option>{"".join(f'<option>{e}</option>' for e in equipment)}</select></div>
    <div><label>Customer Type</label><select id="fType"><option value="all">All Types</option><option>Farmer</option><option>Dealer</option><option>Cooperative</option></select></div>
    <div><label>Payment Mode</label><select id="fPay"><option value="all">All Modes</option><option>Cash</option><option>UPI</option><option>Bank Transfer</option><option>EMI/Finance</option></select></div>
  </div>

  <div class="kpis" id="kpis">
    <div class="kpi"><div class="val" id="kRev">₹{kpis['revenue']:,.0f}</div><div class="lbl">Total Revenue</div></div>
    <div class="kpi"><div class="val" id="kOrd">{kpis['orders']:,}</div><div class="lbl">Total Orders</div></div>
    <div class="kpi"><div class="val" id="kUnit">{kpis['units']:,}</div><div class="lbl">Units Sold</div></div>
    <div class="kpi"><div class="val" id="kCust">{kpis['customers']:,}</div><div class="lbl">Customers</div></div>
    <div class="kpi"><div class="val" id="kAvg">₹{kpis['avg_order']:,.0f}</div><div class="lbl">Avg Order Value</div></div>
    <div class="kpi"><div class="val" id="kGop">{kpis['gopalganj']:.1f}%</div><div class="lbl">Gopalganj Share</div></div>
  </div>

  <div class="charts" id="charts">
    {"".join(charts)}
  </div>

  <div class="insights">
    <h2>📋 Business Insights</h2>
    <ul>
      <li><b>Gopalganj</b> home district hai — 28% revenue yahan se aata hai</li>
      <li><b>Harvester</b> sabse zyada revenue generate karta hai (premium segment)</li>
      <li><b>Chapra, Samastipur, Muzaffarpur</b> — top outstation districts</li>
      <li><b>EMI/Finance</b> sirf 13.5% sales — high-value equipment ke liye opportunity</li>
      <li>Bihar ke <b>17 districts</b> se customers aate hain — wide reach</li>
    </ul>
  </div>

  <div class="footer">
    Fresher Data Analyst Portfolio | Punjab Agro Centre, Gopalganj, Bihar<br/>
    Python • Pandas • SQL • Plotly • Streamlit | Repo: github.com/Prabhashsingh17/punjab-agro-analytics
  </div>

  <script>
    const RAW = {data_json};
    const fmt = n => '₹' + Math.round(n).toLocaleString('en-IN');
    const els = ['fDistrict','fEquip','fType','fPay'].map(id => document.getElementById(id));

    function filterData() {{
      const [d, e, t, p] = els.map(el => el.value);
      return RAW.filter(r =>
        (d === 'all' || r.district === d) &&
        (e === 'all' || r.equipment === e) &&
        (t === 'all' || r.customer_type === t) &&
        (p === 'all' || r.payment_mode === p)
      );
    }}

    function updateKPIs(data) {{
      const rev = data.reduce((s,r) => s + r.net_revenue, 0);
      const units = data.reduce((s,r) => s + r.quantity, 0);
      const cust = new Set(data.map(r => r.district + r.customer_type)).size;
      const gop = data.filter(r => r.district === 'Gopalganj').reduce((s,r) => s + r.net_revenue, 0);
      document.getElementById('kRev').textContent = fmt(rev);
      document.getElementById('kOrd').textContent = data.length.toLocaleString('en-IN');
      document.getElementById('kUnit').textContent = units.toLocaleString('en-IN');
      document.getElementById('kCust').textContent = cust.toLocaleString('en-IN');
      document.getElementById('kAvg').textContent = data.length ? fmt(rev / data.length) : '₹0';
      document.getElementById('kGop').textContent = rev ? (gop / rev * 100).toFixed(1) + '%' : '0%';
    }}

    els.forEach(el => el.addEventListener('change', () => updateKPIs(filterData())));
    window.addEventListener('load', () => {{
      if (typeof Plotly !== 'undefined') {{
        document.querySelectorAll('.plotly-graph-div').forEach(div => Plotly.Plots.resize(div));
      }}
    }});
  </script>
</body>
</html>"""

    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Built: {OUT / 'index.html'}")


if __name__ == "__main__":
    build()
