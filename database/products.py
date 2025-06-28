# import pandas as pd
# import uuid
# import os

# FILE = "database/products.csv"

# def add_product(name, price, quantity):
#     # Create new product row as a DataFrame
#     product_df = pd.DataFrame([{
#         "id": str(uuid.uuid4())[:8],
#         "name": name,
#         "price": price,
#         "quantity": quantity
#     }])

#     # Load existing data or create empty DataFrame
#     if os.path.exists(FILE):
#         df = pd.read_csv(FILE)
#     else:
#         df = pd.DataFrame(columns=["id", "name", "price", "quantity"])

#     # ✅ Use concat instead of deprecated append
#     df = pd.concat([df, product_df], ignore_index=True)

#     # Save updated file
#     df.to_csv(FILE, index=False)

# def get_all_products():
#     return pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["id", "name", "price", "quantity"])

# def delete_product(pid):
#     df = pd.read_csv(FILE)
#     df = df[df["id"] != pid]
#     df.to_csv(FILE, index=False)

# def update_quantity(pid, qty):
#     df = pd.read_csv(FILE)
#     df.loc[df["id"] == pid, "quantity"] = df.loc[df["id"] == pid, "quantity"] - qty
#     df.to_csv(FILE, index=False)

import pandas as pd
import uuid
import os

FILE = "database/products.csv"

def add_product(name, price, quantity):
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame(columns=["id", "name", "price", "quantity"])

    if name in df["name"].values:
        df.loc[df["name"] == name, ["price", "quantity"]] = [price, quantity]
    else:
        new_product = pd.DataFrame([{
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "price": price,
            "quantity": quantity
        }])
        df = pd.concat([df, new_product], ignore_index=True)

    df.to_csv(FILE, index=False)

def get_all_products():
    return pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["id", "name", "price", "quantity"])

def delete_product(pid):
    df = pd.read_csv(FILE)
    if pid in df["id"].values:
        df = df[df["id"] != pid]
        df.to_csv(FILE, index=False)
        return True
    return False

def update_quantity(pid, qty):
    df = pd.read_csv(FILE)
    df.loc[df["id"] == pid, "quantity"] = df.loc[df["id"] == pid, "quantity"] - qty
    df.to_csv(FILE, index=False)
