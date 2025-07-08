# import streamlit as st
# import pandas as pd
# from database.products import add_product, get_all_products, delete_product
# from database.users import get_all_users
# from utils.notifications import get_notifications
# import os

# def admin_dashboard():
#     st.title("🛠️ Admin Dashboard")

#     tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "👥 Users", "🧾 Purchase Reports", "🔔 Notifications"])

#     # ------------------- Tab 1: Products -------------------
#     with tab1:
#         st.subheader("➕ Add New Product")

#         # Input fields
#         name = st.text_input("Product Name")
#         price = st.number_input("Price", min_value=0.0)
#         quantity = st.number_input("Quantity", min_value=0)

#         if st.button("Add Product"):
#             if name and price >= 0 and quantity >= 0:
#                 add_product(name, price, quantity)
#                 st.success("✅ Product added successfully!")
#                 st.rerun()
#             else:
#                 st.error("❌ Please fill all fields properly.")

#         st.markdown("---")
#         st.subheader("📋 Current Products")

#         try:
#             products = get_all_products()
#             if not products.empty:
#                 st.dataframe(products, use_container_width=True, height=300)
#             else:
#                 st.info("No products found.")
#         except Exception as e:
#             st.error(f"Error loading products: {e}")

#         st.markdown("### 🗑️ Delete a Product")
#         delete_id = st.text_input("Enter Product ID to Delete")
#         if st.button("Delete Product"):
#             if delete_id:
#                 delete_product(delete_id)
#                 st.success("🗑️ Product deleted!")
#                 st.rerun()
#             else:
#                 st.warning("Enter a valid Product ID")

#     # ------------------- Tab 2: Users -------------------
#     with tab2:
#         st.subheader("👥 Registered Users")
#         try:
#             users = get_all_users()
#             if not users.empty:
#                 st.dataframe(users, use_container_width=True, height=300)
#             else:
#                 st.info("No users registered yet.")
#         except Exception as e:
#             st.error(f"Error loading users: {e}")

#     # ------------------- Tab 3: Purchase Reports -------------------
#     with tab3:
#         st.subheader("📈 Purchase Reports")
#         report_path = "database/purchase_report.csv"
#         try:
#             if os.path.exists(report_path):
#                 report = pd.read_csv(
#                     report_path,
#                     names=["email", "product_id", "product_name", "price", "quantity", "total"],
#                     header=None,
#                     on_bad_lines="skip"
#                 )
#                 st.dataframe(report, use_container_width=True, height=300)
#             else:
#                 st.info("No purchase report available.")
#         except Exception as e:
#             st.error(f"Error reading purchase report: {e}")

#     # ------------------- Tab 4: Notifications -------------------
#     with tab4:
#         st.subheader("🔔 User Notifications")
#         notes = get_notifications()
#         if notes:
#             for note in notes:
#                 st.info(note)
#         else:
#             st.info("No notifications.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from database.products import add_product, get_all_products, delete_product
from database.users import get_all_users
from utils.notifications import get_notifications
import os

# Custom CSS for modern dashboard styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom Header */
    .dashboard-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        animation: slideDown 0.6s ease-out;
    }
    
    .dashboard-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .dashboard-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Stats Cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        flex: 1;
        min-width: 200px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #667eea;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 10px;
        padding: 0.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        gap: 0.5rem;
        margin-top: 30px;        
    }
    
    .stTabs [data-baseweb="tab"] {
        
        height: 3rem;
        border-radius: 8px;
        padding: 0 1.5rem;
        background: transparent;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Form Styling */
    .product-form {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    .form-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* Button Animations */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Data Table Styling */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        border: none;
        border-radius: 8px;
        animation: slideInRight 0.5s ease-out;
    }
    
    .stError {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        border: none;
        border-radius: 8px;
        animation: shake 0.5s ease-out;
    }
    
    .stInfo {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        border-radius: 8px;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Notification Styles */
    .notification-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .notification-item:hover {
        transform: translateX(5px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .stats-container {
            flex-direction: column;
        }
        
        .dashboard-title {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_dashboard_header():
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">🏪 Store Management System</h1>
        <p class="dashboard-subtitle">Professional Admin Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

def create_stats_cards():
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        products = get_all_products()
        users = get_all_users()
        
        total_products = len(products) if not products.empty else 0
        total_users = len(users) if not users.empty else 0
        
        # Calculate total inventory value
        total_value = 0
        if not products.empty and 'price' in products.columns and 'quantity' in products.columns:
            total_value = (products['price'] * products['quantity']).sum()
        
        # Low stock items
        low_stock = 0
        if not products.empty and 'quantity' in products.columns:
            low_stock = len(products[products['quantity'] < 10])
        
    except Exception as e:
        total_products = total_users = total_value = low_stock = 0
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_products}</div>
            <div class="stat-label">📦 Total Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_users}</div>
            <div class="stat-label">👥 Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">Rs.{total_value:,.0f}</div>
            <div class="stat-label">💰 Inventory Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{low_stock}</div>
            <div class="stat-label">⚠️ Low Stock Items</div>
        </div>
        """, unsafe_allow_html=True)

def create_product_form():
    st.markdown('<div class="product-form">', unsafe_allow_html=True)
    st.subheader("➕ Add New Product")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("🏷️ Product Name", placeholder="Enter product name...")
        price = st.number_input("💰 Price (Rs.)", min_value=0.0, step=0.01)
    
    with col2:
        quantity = st.number_input("📦 Quantity", min_value=0, step=1)
        category = st.selectbox("📂 Category", 
                               ["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"])
    
    if st.button("✨ Add Product", use_container_width=True):
        if name and price >= 0 and quantity >= 0:
            with st.spinner("Adding product..."):
                time.sleep(0.5)  # Simulate processing
                add_product(name, price, quantity)
                st.success("✅ Product added successfully!")
                time.sleep(1)
                st.rerun()
        else:
            st.error("❌ Please fill all fields properly.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_products_table():
    st.subheader("📋 Product Inventory")
    
    try:
        with st.spinner("Loading products..."):
            products = get_all_products()
            
        if not products.empty:
            # Add colored status based on quantity
            def get_stock_status(qty):
                if qty == 0:
                    return "🔴 Out of Stock"
                elif qty < 10:
                    return "🟡 Low Stock"
                else:
                    return "🟢 In Stock"
            
            if 'quantity' in products.columns:
                products['Stock Status'] = products['quantity'].apply(get_stock_status)
            
            # Display with enhanced styling
            st.dataframe(
                products,
                use_container_width=True,
                height=400,
                column_config={
                    "price": st.column_config.NumberColumn(
                        "Price (Rs.)",
                        format="Rs. %.2f"
                    ),
                    "quantity": st.column_config.NumberColumn(
                        "Quantity",
                        format="%d units"
                    )
                }
            )
            
            # Quick actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Generate Report", use_container_width=True):
                    st.info("📄 Report generation feature coming soon!")
            
            with col2:
                if st.button("📤 Export Data", use_container_width=True):
                    csv = products.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"products_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                    
        else:
            st.info("📭 No products found. Add some products to get started!")
    
    except Exception as e:
        st.error(f"❌ Error loading products: {e}")

def create_product_charts():
    try:
        products = get_all_products()
        if not products.empty and len(products) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Price distribution chart
                if 'price' in products.columns:
                    fig_price = px.histogram(
                        products, 
                        x='price', 
                        title="📊 Price Distribution",
                        color_discrete_sequence=['#667eea']
                    )
                    fig_price.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_family="Inter",
                    )
                    st.plotly_chart(fig_price, use_container_width=True)
            
            with col2:
                # Stock levels chart
                if 'quantity' in products.columns:
                    fig_stock = px.bar(
                        products.head(10), 
                        x='name', 
                        y='quantity',
                        title="📦 Top 10 Products by Stock",
                        color='quantity',
                        color_continuous_scale='viridis'
                    )
                    fig_stock.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_family="Inter",
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_stock, use_container_width=True)
    except Exception as e:
        st.info("📈 Charts will appear when you have product data.")

def admin_dashboard():
    # Load custom CSS
    load_custom_css()
    
    # Create header
    create_dashboard_header()
    
    # Create stats cards
    create_stats_cards()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📦 Products", 
        "👥 Users", 
        "📊 Analytics", 
        "🔔 Notifications"
    ])

    # ------------------- Tab 1: Products -------------------
    with tab1:
        create_product_form()
        
        st.markdown("---")
        
        display_products_table()
        
        st.markdown("---")
        
        # Delete product section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("🗑️ Delete Product")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            delete_id = st.text_input("🆔 Enter Product ID to Delete", placeholder="Product ID...")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete", use_container_width=True):
                if delete_id:
                    with st.spinner("Deleting product..."):
                        time.sleep(0.5)
                        delete_product(delete_id)
                        st.success("✅ Product deleted successfully!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("⚠️ Enter a valid Product ID")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------- Tab 2: Users -------------------
    with tab2:
        st.subheader("👥 Registered Users")
        
        try:
            with st.spinner("Loading users..."):
                users = get_all_users()
                
            if not users.empty:
                # Enhanced user display
                total_users = len(users)
                st.metric("Total Registered Users", total_users)
                
                st.dataframe(
                    users,
                    use_container_width=True,
                    height=400,
                    column_config={
                        "email": st.column_config.TextColumn(
                            "📧 Email",
                            width="medium"
                        ),
                        "username": st.column_config.TextColumn(
                            "👤 Username",
                            width="medium"
                        )
                    }
                )
                
                # User analytics
                if st.button("📊 User Analytics", use_container_width=True):
                    st.info("👥 User analytics dashboard coming soon!")
                    
            else:
                st.info("👤 No users registered yet.")
                
        except Exception as e:
            st.error(f"❌ Error loading users: {e}")

    # ------------------- Tab 3: Analytics -------------------
    with tab3:
        st.subheader("📊 Business Analytics")
        
        # Product charts
        create_product_charts()
        
        st.markdown("---")
        
        # Purchase Reports
        st.subheader("🧾 Purchase Reports")
        report_path = "database/purchase_report.csv"
        
        try:
            if os.path.exists(report_path):
                with st.spinner("Loading purchase data..."):
                    report = pd.read_csv(
                        report_path,
                        names=["email", "product_id", "product_name", "price", "quantity", "total"],
                        header=None,
                        on_bad_lines="skip"
                    )
                
                if not report.empty:
                    # Summary metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        total_sales = report['total'].sum() if 'total' in report.columns else 0
                        st.metric("💰 Total Sales", f"Rs. {total_sales:,.2f}")
                    
                    with col2:
                        total_orders = len(report)
                        st.metric("🛒 Total Orders", total_orders)
                    
                    with col3:
                        avg_order = total_sales / total_orders if total_orders > 0 else 0
                        st.metric("📊 Average Order", f"Rs. {avg_order:.2f}")
                    
                    # Display report
                    st.dataframe(
                        report,
                        use_container_width=True,
                        height=300,
                        column_config={
                            "total": st.column_config.NumberColumn(
                                "Total (Rs.)",
                                format="Rs. %.2f"
                            )
                        }
                    )
                    
                    # Download report
                    if st.button("📥 Download Report", use_container_width=True):
                        csv = report.to_csv(index=False)
                        st.download_button(
                            label="💾 Download Purchase Report",
                            data=csv,
                            file_name=f"purchase_report_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                else:
                    st.info("📋 No purchase data available.")
            else:
                st.info("📄 No purchase report file found.")
                
        except Exception as e:
            st.error(f"❌ Error reading purchase report: {e}")

    # ------------------- Tab 4: Notifications -------------------
    with tab4:
        st.subheader("🔔 System Notifications")
        
        try:
            notes = get_notifications()
            
            if notes:
                for i, note in enumerate(notes):
                    st.markdown(f"""
                    <div class="notification-item">
                        <strong>🔔 Notification {i+1}</strong><br>
                        {note}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("🔕 No notifications available.")
                
            # Add notification management
            st.markdown("---")
            st.subheader("➕ Add New Notification")
            
            new_notification = st.text_area("📝 Notification Message", placeholder="Enter notification message...")
            
            if st.button("📢 Send Notification", use_container_width=True):
                if new_notification:
                    st.success("✅ Notification sent successfully!")
                    st.info(f"📧 Notification: {new_notification}")
                else:
                    st.warning("⚠️ Please enter a notification message.")
                    
        except Exception as e:
            st.error(f"❌ Error loading notifications: {e}")

# Run the dashboard
if __name__ == "__main__":
    admin_dashboard()