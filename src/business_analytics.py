"""
PUNJAB AGRO CENTRE - Business Analytics Report
Descriptive + Diagnostic + Prescriptive Analytics
Run: python src/business_analytics.py
"""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
SALES = BASE / "data" / "processed" / "sales_clean.csv"
CUSTOMERS = BASE / "data" / "processed" / "customers_clean.csv"
INVENTORY = BASE / "data" / "raw" / "inventory.csv"


def load():
    sales = pd.read_csv(SALES, parse_dates=["sale_date"])
    customers = pd.read_csv(CUSTOMERS)
    inventory = pd.read_csv(INVENTORY)
    return sales, customers, inventory


def customer_segmentation(sales):
    clv = (
        sales.groupby("customer_id")
        .agg(orders=("sale_id", "count"), revenue=("net_revenue", "sum"))
        .reset_index()
    )
    clv["segment"] = pd.cut(
        clv["revenue"],
        bins=[0, 100000, 300000, float("inf")],
        labels=["Low Value", "Medium Value", "High Value"],
    )
    return clv


def profit_analysis(sales, inventory):
    merged = sales.merge(inventory[["equipment", "avg_unit_cost"]], on="equipment", how="left")
    merged["estimated_profit"] = (merged["unit_price"] - merged["avg_unit_cost"]) * merged["quantity"]
    merged["margin_pct"] = (merged["estimated_profit"] / merged["net_revenue"] * 100).round(1)
    return merged.groupby("equipment").agg(
        revenue=("net_revenue", "sum"),
        profit=("estimated_profit", "sum"),
        avg_margin=("margin_pct", "mean"),
    ).sort_values("profit", ascending=False)


def inventory_health(sales, inventory):
    sold = sales.groupby("equipment")["quantity"].sum().reset_index(name="units_sold")
    inv = inventory.merge(sold, on="equipment", how="left")
    inv["turnover_ratio"] = (inv["units_sold"] / inv["stock_quantity"]).round(2)
    inv["stock_status"] = inv.apply(
        lambda r: "Low Stock" if r["stock_quantity"] <= r["reorder_level"] else "Healthy", axis=1
    )
    return inv


def yoy_growth(sales):
    return (
        sales.groupby(["year", "equipment"])["net_revenue"]
        .sum()
        .unstack(fill_value=0)
        .pct_change()
        .iloc[-1]
        .sort_values(ascending=False)
        * 100
    )


def main():
    sales, customers, inventory = load()

    print("=" * 65)
    print("PUNJAB AGRO CENTRE — DATA & BUSINESS ANALYTICS REPORT")
    print("Gopalganj, Bihar | Agricultural Equipment")
    print("=" * 65)

    print("\n[1] DESCRIPTIVE ANALYTICS — What happened?")
    print(f"  Total Revenue     : Rs. {sales['net_revenue'].sum():,.0f}")
    print(f"  Total Orders      : {len(sales):,}")
    print(f"  Active Customers  : {sales['customer_id'].nunique():,}")
    print(f"  Avg Order Value   : Rs. {sales['net_revenue'].mean():,.0f}")
    print(f"  Districts Covered : {sales['district'].nunique()}")

    print("\n[2] DIAGNOSTIC ANALYTICS — Why did it happen?")
    seg = customer_segmentation(sales)
    print("  Customer Segmentation (by lifetime value):")
    for segment, grp in seg.groupby("segment", observed=True):
        print(f"    {segment:14s} : {len(grp):4d} customers | Avg spend Rs. {grp['revenue'].mean():,.0f}")

    profit = profit_analysis(sales, inventory)
    print("\n  Profitability by Equipment:")
    for equip, row in profit.head(4).iterrows():
        print(f"    {equip:25s} Margin {row['avg_margin']:.1f}% | Profit Rs. {row['profit']:,.0f}")

    inv = inventory_health(sales, inventory)
    low = inv[inv["stock_status"] == "Low Stock"]
    if len(low):
        print(f"\n  Inventory Alert: {len(low)} products at/below reorder level")

    growth = yoy_growth(sales)
    top_grower = growth.idxmax()
    print(f"\n  Fastest Growing Product (YoY): {top_grower} ({growth[top_grower]:.1f}%)")

    print("\n[3] PRESCRIPTIVE ANALYTICS — What should we do?")
    print("  1. Focus EMI schemes on Harvester — highest revenue + margin product")
    print("  2. Deploy sales agents in Chapra, Samastipur, Muzaffarpur (top outstation)")
    print("  3. Stock up Rotavator + Tawa before Kharif season (Jun-Jul)")
    print("  4. Target High Value customers with loyalty discounts")
    print("  5. Expand dealer network — dealers give bulk orders")
    print("=" * 65)


if __name__ == "__main__":
    main()
