import streamlit as st
import pandas as pd
import csv
from database.products import get_all_products, update_quantity
from utils.notifications import notify_admin

def client_dashboard(user):
    st.title("🛍️ Client Dashboard")

    # --- Load Products ---
    products = get_all_products()

    # Add "Out of Stock" label
    display_products = products.copy()
    display_products["name"] = display_products.apply(
        lambda row: f"{row['name']} (Out of Stock)" if row["quantity"] == 0 else row["name"],
        axis=1
    )

    # --- Display Products Table ---
    st.subheader("Available Products")
    st.dataframe(display_products, use_container_width=True, height=300)

    # --- Purchase Section ---
    st.markdown("### 🛒 Purchase Product")
    selected_id = st.text_input("Enter Product ID")
    buy_qty = st.number_input("Quantity", min_value=1, value=1)

    if selected_id:
        selected_product = products[products["id"] == selected_id]

        if selected_product.empty:
            st.warning("⚠️ Product not found.")
        else:
            product = selected_product.iloc[0]
            name = product["name"]
            price = float(product["price"])
            available_qty = int(product["quantity"])
            total_price = price * buy_qty

            if available_qty == 0:
                st.error(f"❌ {name} is Out of Stock.")
            else:
                st.info(f"🧾 {name} × {buy_qty} = Rs. {total_price}")

                if st.button("Confirm Purchase"):
                    if buy_qty > available_qty:
                        st.error(f"Only {available_qty} items left.")
                    else:
                        update_quantity(selected_id, buy_qty)
                        notify_admin(f"{user['email']} purchased {name} (Qty: {buy_qty})")

                        # ✅ Write purchase data with all fields
                        with open("database/purchase_report.csv", "a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                user['email'], selected_id, name, price, buy_qty, total_price
                            ])

                        st.success(f"✅ Purchase successful! Rs. {total_price} paid.")
                        st.rerun()

    # --- User Purchase History ---
    st.markdown("---")
    st.subheader("📜 Your Purchase History")

    try:
        df = pd.read_csv(
            "database/purchase_report.csv",
            names=["email", "product_id", "product_name", "price", "quantity", "total"],
            header=None,
            on_bad_lines="skip"
        )

        # Filter current user’s purchases (skip header row if already added)
        user_history = df[df["email"] == user["email"]]

        if user_history.empty:
            st.info("You haven’t purchased anything yet.")
        else:
            st.dataframe(user_history, use_container_width=True, height=300)
    except FileNotFoundError:
        st.warning("No purchase history found.")
