"""
PUNJAB AGRO CENTRE - Interactive Sales Analytics Dashboard
Agricultural Equipment Sales | Gopalganj, Bihar
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="Punjab Agro Centre Analytics",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#1B5E20",
    "secondary": "#2E7D32",
    "accent": "#66BB6A",
    "bg": "#F1F8E9",
}


@st.cache_data
def load_data():
    sales = pd.read_csv(DATA_DIR / "sales_clean.csv")
    customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
    inventory = pd.read_csv(BASE_DIR / "data" / "raw" / "inventory.csv")
    sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    return sales, customers, inventory


def format_inr(value):
    if value >= 1_00_00_000:
        return f"₹{value / 1_00_00_000:.2f} Cr"
    if value >= 1_00_000:
        return f"₹{value / 1_00_000:.2f} L"
    return f"₹{value:,.0f}"


def apply_filters(sales, customers):
    st.sidebar.header("🔍 Filters")

    min_date = sales["sale_date"].min().date()
    max_date = sales["sale_date"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    districts = sorted(sales["district"].unique())
    selected_districts = st.sidebar.multiselect(
        "District", districts, default=districts
    )

    equipment_list = sorted(sales["equipment"].unique())
    selected_equipment = st.sidebar.multiselect(
        "Equipment", equipment_list, default=equipment_list
    )

    customer_types = sorted(sales["customer_type"].unique())
    selected_types = st.sidebar.multiselect(
        "Customer Type", customer_types, default=customer_types
    )

    if len(date_range) == 2:
        start, end = date_range
        mask = (
            (sales["sale_date"].dt.date >= start)
            & (sales["sale_date"].dt.date <= end)
            & (sales["district"].isin(selected_districts))
            & (sales["equipment"].isin(selected_equipment))
            & (sales["customer_type"].isin(selected_types))
        )
        filtered_sales = sales[mask].copy()
    else:
        filtered_sales = sales.copy()

    return filtered_sales


def render_header():
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1B5E20, #43A047);
                    padding: 24px; border-radius: 12px; color: white; margin-bottom: 20px;'>
            <h1 style='margin:0; font-size: 2rem;'>🌾 PUNJAB AGRO CENTRE</h1>
            <p style='margin:8px 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                Agricultural Equipment Sales Analytics | Gopalganj, Bihar
            </p>
            <p style='margin:4px 0 0 0; opacity: 0.75; font-size: 0.9rem;'>
                Rotavator • Cultivator • Harvester • Zero Till • Threshing Machine • Tawa
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(df):
    total_revenue = df["net_revenue"].sum()
    total_orders = len(df)
    total_units = df["quantity"].sum()
    unique_customers = df["customer_id"].nunique()
    avg_order = df["net_revenue"].mean()
    gopalganj_pct = (
        df[df["district"] == "Gopalganj"]["net_revenue"].sum() / total_revenue * 100
        if total_revenue > 0
        else 0
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Revenue", format_inr(total_revenue))
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Units Sold", f"{total_units:,}")
    c4.metric("Unique Customers", f"{unique_customers:,}")
    c5.metric("Avg Order Value", format_inr(avg_order))
    c6.metric("Gopalganj Share", f"{gopalganj_pct:.1f}%")


def render_charts(df):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📈 Revenue Trend", "🚜 Equipment", "🗺️ Districts", "📅 Seasonality", "💳 Payments"]
    )

    with tab1:
        monthly = (
            df.groupby(df["sale_date"].dt.to_period("M"))
            .agg(revenue=("net_revenue", "sum"), orders=("sale_id", "count"))
            .reset_index()
        )
        monthly["sale_date"] = monthly["sale_date"].astype(str)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=monthly["sale_date"],
                y=monthly["revenue"],
                mode="lines+markers",
                name="Revenue",
                line=dict(color="#2E7D32", width=3),
                fill="tozeroy",
                fillcolor="rgba(46,125,50,0.15)",
            )
        )
        fig.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Month",
            yaxis_title="Revenue (INR)",
            height=400,
            plot_bgcolor="white",
        )
        st.plotly_chart(fig, use_container_width=True)

        yearly = df.groupby("year")["net_revenue"].sum().reset_index()
        fig2 = px.bar(
            yearly,
            x="year",
            y="net_revenue",
            title="Yearly Revenue Comparison",
            color_discrete_sequence=["#43A047"],
            text_auto=",.0f",
        )
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        equip_rev = (
            df.groupby("equipment")["net_revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        with col1:
            fig = px.bar(
                equip_rev,
                x="equipment",
                y="net_revenue",
                title="Revenue by Equipment",
                color="net_revenue",
                color_continuous_scale="Greens",
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        equip_qty = (
            df.groupby("equipment")["quantity"]
            .sum()
            .reset_index()
        )
        with col2:
            fig = px.pie(
                equip_qty,
                names="equipment",
                values="quantity",
                title="Units Sold by Equipment",
                color_discrete_sequence=px.colors.sequential.Greens_r,
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        district_data = (
            df.groupby("district")
            .agg(
                revenue=("net_revenue", "sum"),
                customers=("customer_id", "nunique"),
                orders=("sale_id", "count"),
            )
            .reset_index()
            .sort_values("revenue", ascending=False)
        )

        fig = px.bar(
            district_data.head(12),
            x="district",
            y="revenue",
            color="customers",
            title="District-wise Revenue (Top 12 Bihar Districts)",
            labels={"revenue": "Revenue (INR)", "customers": "Customers"},
            color_continuous_scale="Greens",
            text_auto=",.0f",
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "💡 **Insight:** Gopalganj ke alawa Siwan, Chapra, Muzaffarpur aur Patna se "
            "sabse zyada customers aate hain — in districts me targeted marketing se sales badh sakti hai."
        )

    with tab4:
        col1, col2 = st.columns(2)
        season_rev = df.groupby("season")["net_revenue"].sum().reset_index()
        with col1:
            fig = px.pie(
                season_rev,
                names="season",
                values="net_revenue",
                title="Revenue by Agricultural Season",
                color_discrete_sequence=px.colors.sequential.Greens,
            )
            st.plotly_chart(fig, use_container_width=True)

        heatmap_data = (
            df.groupby(["season", "equipment"])["quantity"]
            .sum()
            .reset_index()
        )
        pivot = heatmap_data.pivot(index="equipment", columns="season", values="quantity").fillna(0)
        with col2:
            fig = px.imshow(
                pivot,
                title="Season × Equipment Demand Heatmap",
                color_continuous_scale="Greens",
                aspect="auto",
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        col1, col2 = st.columns(2)
        payment = df.groupby("payment_mode").agg(
            count=("sale_id", "count"),
            revenue=("net_revenue", "sum"),
        ).reset_index()
        with col1:
            fig = px.pie(
                payment,
                names="payment_mode",
                values="count",
                title="Payment Mode Distribution",
                color_discrete_sequence=px.colors.sequential.Greens_r,
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cust_type = df.groupby("customer_type")["net_revenue"].sum().reset_index()
            fig = px.bar(
                cust_type,
                x="customer_type",
                y="net_revenue",
                title="Revenue by Customer Type",
                color="customer_type",
                color_discrete_sequence=["#1B5E20", "#43A047", "#66BB6A"],
            )
            st.plotly_chart(fig, use_container_width=True)


def render_insights(df):
    st.subheader("📋 Business Insights & Recommendations")

    top_district = df.groupby("district")["net_revenue"].sum().idxmax()
    top_equip = df.groupby("equipment")["net_revenue"].sum().idxmax()
    peak_season = df.groupby("season")["net_revenue"].sum().idxmax()
    emi_pct = (df["payment_mode"] == "EMI/Finance").mean() * 100

    insights = [
        f"**Top District:** {top_district} sabse zyada revenue generate karta hai. "
        "Door ke districts ke liye delivery aur service camp arrange karein.",
        f"**Best Equipment:** {top_equip} highest revenue driver hai. "
        "Stock level aur service team is product par focus karein.",
        f"**Peak Season:** {peak_season} me demand sabse zyada hoti hai. "
        "Is season se 2 mahine pehle marketing campaign start karein.",
        f"**EMI Adoption:** {emi_pct:.1f}% sales EMI/Finance se hoti hain. "
        "Bank tie-ups se high-value equipment (Harvester) ki sales badh sakti hai.",
        "**Cross-District Opportunity:** Bihar ke 17 districts se customers aate hain. "
        "District-wise sales agent appoint karke reach badhayein.",
    ]

    for i, insight in enumerate(insights, 1):
        st.markdown(f"{i}. {insight}")


def render_data_table(df):
    st.subheader("📊 Filtered Sales Data")
    st.dataframe(
        df.sort_values("sale_date", ascending=False).head(100),
        use_container_width=True,
        hide_index=True,
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data (CSV)",
        csv,
        "punjab_agro_sales_filtered.csv",
        "text/csv",
    )


def main():
    sales, customers, inventory = load_data()
    render_header()

    filtered = apply_filters(sales, customers)
    render_kpis(filtered)
    st.divider()
    render_charts(filtered)
    st.divider()
    render_insights(filtered)
    st.divider()
    render_data_table(filtered)

    st.sidebar.divider()
    st.sidebar.markdown(
        """
        **About Project**
        
        Fresher Data Analyst portfolio project for
        **Punjab Agro Centre**, Gopalganj, Bihar.
        
        **Tools:** Python, Pandas, SQL, Plotly, Streamlit
        
        **Analyst:** Data Analytics Team
        """
    )


if __name__ == "__main__":
    main()
