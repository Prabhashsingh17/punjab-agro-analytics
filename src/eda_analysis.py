"""
PUNJAB AGRO CENTRE - Exploratory Data Analysis
Run: python src/eda_analysis.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="Greens_d")


def load_data():
    sales = pd.read_csv(DATA_DIR / "sales_clean.csv")
    customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
    sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    return sales, customers


def print_summary(sales, customers):
    print("=" * 60)
    print("PUNJAB AGRO CENTRE - EDA SUMMARY REPORT")
    print("Location: Gopalganj, Bihar")
    print("=" * 60)
    print(f"\nTotal Sales Records : {len(sales):,}")
    print(f"Total Customers     : {len(customers):,}")
    print(f"Date Range          : {sales['sale_date'].min().date()} to {sales['sale_date'].max().date()}")
    print(f"Total Revenue       : Rs. {sales['net_revenue'].sum():,.0f}")
    print(f"Total Units Sold    : {sales['quantity'].sum():,}")
    print(f"Avg Order Value     : Rs. {sales['net_revenue'].mean():,.0f}")

    print("\n--- Top 5 Districts by Revenue ---")
    district_rev = (
        sales.groupby("district")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    for district, rev in district_rev.items():
        print(f"  {district:20s} Rs. {rev:,.0f}")

    print("\n--- Top 5 Equipment by Revenue ---")
    equip_rev = (
        sales.groupby("equipment")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    for equip, rev in equip_rev.items():
        print(f"  {equip:25s} Rs. {rev:,.0f}")

    print("\n--- Seasonal Revenue ---")
    season_rev = sales.groupby("season")["net_revenue"].sum().sort_values(ascending=False)
    for season, rev in season_rev.items():
        print(f"  {season:15s} Rs. {rev:,.0f}")

    print("\n--- Key Business Insights ---")
    gopalganj_share = (
        sales[sales["district"] == "Gopalganj"]["net_revenue"].sum()
        / sales["net_revenue"].sum()
        * 100
    )
    print(f"1. Gopalganj contributes {gopalganj_share:.1f}% of total revenue (home district).")
    top_equip = equip_rev.index[0]
    print(f"2. Best-selling equipment: {top_equip}")
    peak_season = season_rev.index[0]
    print(f"3. Peak sales season: {peak_season}")
    emi_share = (sales["payment_mode"] == "EMI/Finance").mean() * 100
    print(f"4. EMI/Finance used in {emi_share:.1f}% of transactions — upsell opportunity.")
    print("=" * 60)


def create_charts(sales):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "PUNJAB AGRO CENTRE - Sales Analytics Dashboard",
        fontsize=14,
        fontweight="bold",
        color="#1B5E20",
    )

    monthly = (
        sales.groupby(["year", "month"])["net_revenue"]
        .sum()
        .reset_index()
    )
    monthly["period"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)
    axes[0, 0].plot(monthly["period"], monthly["net_revenue"], marker="o", color="#2E7D32")
    axes[0, 0].set_title("Monthly Revenue Trend")
    axes[0, 0].set_xlabel("Period")
    axes[0, 0].set_ylabel("Revenue (INR)")
    axes[0, 0].tick_params(axis="x", rotation=45)

    equip = sales.groupby("equipment")["net_revenue"].sum().sort_values(ascending=True)
    equip.plot(kind="barh", ax=axes[0, 1], color="#43A047")
    axes[0, 1].set_title("Revenue by Equipment")
    axes[0, 1].set_xlabel("Revenue (INR)")

    district = (
        sales.groupby("district")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
    )
    district.plot(kind="bar", ax=axes[1, 0], color="#66BB6A")
    axes[1, 0].set_title("Top 8 Districts by Revenue")
    axes[1, 0].set_ylabel("Revenue (INR)")
    axes[1, 0].tick_params(axis="x", rotation=45)

    season = sales.groupby("season")["quantity"].sum()
    axes[1, 1].pie(season, labels=season.index, autopct="%1.1f%%", startangle=90)
    axes[1, 1].set_title("Units Sold by Season")

    plt.tight_layout()
    chart_path = OUTPUT_DIR / "eda_dashboard.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nChart saved: {chart_path}")


def main():
    sales, customers = load_data()
    print_summary(sales, customers)
    create_charts(sales)


if __name__ == "__main__":
    main()
