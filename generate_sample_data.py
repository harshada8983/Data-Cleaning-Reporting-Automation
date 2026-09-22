"""
generate_sample_data.py
------------------------
Creates a messy/dirty sample dataset (sales records) so you can test the
cleaning + reporting pipeline immediately, without needing your own data.

Run:
    python generate_sample_data.py

Output:
    data/raw_sales_data.csv
"""

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

n = 300

regions = ["North", "South", "East", "West", "north", "SOUTH", " East ", None]
products = ["Laptop", "Mobile", "Tablet", "Monitor", "laptop", "MOBILE", None]
reps = ["Aman", "Priya", "Rahul", "Sneha", "Aman ", " Priya", "Rahul", None]

rows = []
for i in range(n):
    order_id = f"ORD{1000 + i}"
    region = random.choice(regions)
    product = random.choice(products)
    rep = random.choice(reps)
    qty = random.choice([1, 2, 3, 5, 10, -1, None, 1000])  # includes bad values
    price = random.choice([500, 1200, 300, 15000, 25000, None, -500])
    date = pd.Timestamp("2024-01-01") + pd.Timedelta(days=random.randint(0, 400))

    rows.append({
        "OrderID": order_id,
        "Region": region,
        "Product": product,
        "SalesRep": rep,
        "Quantity": qty,
        "UnitPrice": price,
        "OrderDate": date.strftime("%Y-%m-%d") if random.random() > 0.05 else None,
    })

df = pd.DataFrame(rows)

# Inject duplicate rows on purpose
dupes = df.sample(15, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1, random_state=2).reset_index(drop=True)

df.to_csv("data/raw_sales_data.csv", index=False)
print(f"Sample dirty dataset created: data/raw_sales_data.csv ({len(df)} rows)")
