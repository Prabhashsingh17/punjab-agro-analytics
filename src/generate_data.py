"""
PUNJAB AGRO CENTRE - Synthetic Sales Data Generator
Generates realistic agricultural equipment sales data for Gopalganj, Bihar.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

EQUIPMENT = {
    "Rotavator": {"price_range": (85000, 145000), "weight": 22},
    "Cultivator": {"price_range": (35000, 75000), "weight": 18},
    "Harvester": {"price_range": (450000, 850000), "weight": 8},
    "Zero Till Seed Drill": {"price_range": (120000, 220000), "weight": 12},
    "Threshing Machine": {"price_range": (55000, 95000), "weight": 15},
    "Tawa (Plough)": {"price_range": (18000, 45000), "weight": 25},
}

BIHAR_DISTRICTS = [
    ("Gopalganj", 28),
    ("Siwan", 12),
    ("Chapra (Saran)", 10),
    ("Muzaffarpur", 9),
    ("Patna", 8),
    ("Darbhanga", 7),
    ("Samastipur", 6),
    ("Madhubani", 5),
    ("East Champaran", 5),
    ("West Champaran", 4),
    ("Sitamarhi", 4),
    ("Vaishali", 4),
    ("Begusarai", 3),
    ("Bhagalpur", 3),
    ("Purnia", 2),
    ("Katihar", 2),
    ("Araria", 1),
]

CUSTOMER_TYPES = ["Farmer", "Dealer", "Cooperative"]
PAYMENT_MODES = ["Cash", "UPI", "Bank Transfer", "EMI/Finance"]
SEASONS = {
    "Kharif Prep": (6, 7),
    "Kharif Peak": (8, 9),
    "Rabi Prep": (10, 11),
    "Rabi Peak": (12, 1),
    "Off-Season": (2, 5),
}


def weighted_choice(choices):
    items, weights = zip(*choices)
    return random.choices(items, weights=weights, k=1)[0]


def get_season(month):
    for season, (start, end) in SEASONS.items():
        if start <= end:
            if start <= month <= end:
                return season
        else:
            if month >= start or month <= end:
                return season
    return "Off-Season"


def generate_customers(n=350):
    records = []
    for i in range(1, n + 1):
        district = weighted_choice(BIHAR_DISTRICTS)
        records.append(
            {
                "customer_id": f"C{i:04d}",
                "customer_name": f"Customer {i}",
                "district": district,
                "customer_type": random.choices(
                    CUSTOMER_TYPES, weights=[72, 18, 10], k=1
                )[0],
                "phone": f"9{random.randint(100000000, 999999999)}",
                "registration_date": (
                    datetime(2022, 1, 1)
                    + timedelta(days=random.randint(0, 900))
                ).strftime("%Y-%m-%d"),
            }
        )
    return pd.DataFrame(records)


def generate_sales(customers_df, n=1200):
    records = []
    start_date = datetime(2023, 1, 1)
    equipment_names = list(EQUIPMENT.keys())
    equipment_weights = [EQUIPMENT[e]["weight"] for e in equipment_names]

    for i in range(1, n + 1):
        sale_date = start_date + timedelta(days=random.randint(0, 730))
        equipment = random.choices(equipment_names, weights=equipment_weights, k=1)[0]
        price_low, price_high = EQUIPMENT[equipment]["price_range"]
        unit_price = random.randint(price_low, price_high)
        qty = random.choices([1, 2, 3], weights=[88, 10, 2], k=1)[0]
        customer = customers_df.sample(1).iloc[0]
        discount_pct = random.choices(
            [0, 2, 5, 8, 10], weights=[55, 20, 15, 7, 3], k=1
        )[0]
        gross = unit_price * qty
        discount_amt = round(gross * discount_pct / 100, 2)
        net_revenue = gross - discount_amt

        records.append(
            {
                "sale_id": f"S{i:05d}",
                "sale_date": sale_date.strftime("%Y-%m-%d"),
                "year": sale_date.year,
                "month": sale_date.month,
                "quarter": f"Q{(sale_date.month - 1) // 3 + 1}",
                "season": get_season(sale_date.month),
                "customer_id": customer["customer_id"],
                "district": customer["district"],
                "customer_type": customer["customer_type"],
                "equipment": equipment,
                "quantity": qty,
                "unit_price": unit_price,
                "gross_amount": gross,
                "discount_pct": discount_pct,
                "discount_amount": discount_amt,
                "net_revenue": net_revenue,
                "payment_mode": random.choices(
                    PAYMENT_MODES, weights=[35, 30, 20, 15], k=1
                )[0],
                "delivery_status": random.choices(
                    ["Delivered", "Pending", "Cancelled"], weights=[94, 4, 2], k=1
                )[0],
            }
        )

    return pd.DataFrame(records)


def generate_inventory():
    records = []
    for idx, (equipment, meta) in enumerate(EQUIPMENT.items(), start=1):
        records.append(
            {
                "product_id": f"P{idx:03d}",
                "equipment": equipment,
                "brand": random.choice(
                    ["Mahindra", "Swaraj", "John Deere", "Sonalika", "Local Make"]
                ),
                "stock_quantity": random.randint(5, 45),
                "reorder_level": 10,
                "avg_unit_cost": int(meta["price_range"][0] * 0.72),
                "selling_price_min": meta["price_range"][0],
                "selling_price_max": meta["price_range"][1],
            }
        )
    return pd.DataFrame(records)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    customers = generate_customers()
    sales = generate_sales(customers)
    inventory = generate_inventory()

    sales = sales[sales["delivery_status"] != "Cancelled"].copy()

    customers.to_csv(RAW_DIR / "customers.csv", index=False)
    sales.to_csv(RAW_DIR / "sales.csv", index=False)
    inventory.to_csv(RAW_DIR / "inventory.csv", index=False)

    sales.to_csv(PROCESSED_DIR / "sales_clean.csv", index=False)
    customers.to_csv(PROCESSED_DIR / "customers_clean.csv", index=False)

    print(f"Generated {len(customers)} customers")
    print(f"Generated {len(sales)} sales records")
    print(f"Generated {len(inventory)} inventory items")
    print(f"Data saved to {DATA_DIR}")


if __name__ == "__main__":
    main()
