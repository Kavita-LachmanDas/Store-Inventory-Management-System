import streamlit as st
import pandas as pd
from database.products import add_product, get_all_products, delete_product
from database.users import get_all_users
from utils.notifications import get_notifications
import os

def admin_dashboard():
    st.title("🛠️ Admin Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "👥 Users", "🧾 Purchase Reports", "🔔 Notifications"])

    # ------------------- Tab 1: Products -------------------
    with tab1:
        st.subheader("➕ Add New Product")

        # Input fields
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0)
        quantity = st.number_input("Quantity", min_value=0)

        if st.button("Add Product"):
            if name and price >= 0 and quantity >= 0:
                add_product(name, price, quantity)
                st.success("✅ Product added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill all fields properly.")

        st.markdown("---")
        st.subheader("📋 Current Products")

        try:
            products = get_all_products()
            if not products.empty:
                st.dataframe(products, use_container_width=True, height=300)
            else:
                st.info("No products found.")
        except Exception as e:
            st.error(f"Error loading products: {e}")

        st.markdown("### 🗑️ Delete a Product")
        delete_id = st.text_input("Enter Product ID to Delete")
        if st.button("Delete Product"):
            if delete_id:
                delete_product(delete_id)
                st.success("🗑️ Product deleted!")
                st.rerun()
            else:
                st.warning("Enter a valid Product ID")

    # ------------------- Tab 2: Users -------------------
    with tab2:
        st.subheader("👥 Registered Users")
        try:
            users = get_all_users()
            if not users.empty:
                st.dataframe(users, use_container_width=True, height=300)
            else:
                st.info("No users registered yet.")
        except Exception as e:
            st.error(f"Error loading users: {e}")

    # ------------------- Tab 3: Purchase Reports -------------------
    with tab3:
        st.subheader("📈 Purchase Reports")
        report_path = "database/purchase_report.csv"
        try:
            if os.path.exists(report_path):
                report = pd.read_csv(
                    report_path,
                    names=["email", "product_id", "product_name", "price", "quantity", "total"],
                    header=None,
                    on_bad_lines="skip"
                )
                st.dataframe(report, use_container_width=True, height=300)
            else:
                st.info("No purchase report available.")
        except Exception as e:
            st.error(f"Error reading purchase report: {e}")

    # ------------------- Tab 4: Notifications -------------------
    with tab4:
        st.subheader("🔔 User Notifications")
        notes = get_notifications()
        if notes:
            for note in notes:
                st.info(note)
        else:
            st.info("No notifications.")
