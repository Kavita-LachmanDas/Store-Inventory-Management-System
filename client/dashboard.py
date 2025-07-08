import streamlit as st
import pandas as pd
import csv
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from database.products import get_all_products, update_quantity
from utils.notifications import notify_admin

# Configure page
st.set_page_config(
    page_title="Premium Store Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern client dashboard with sidebar
def load_client_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    .css-1544g2n {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
        padding: 1rem;
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        padding: 1rem 0;
    }
    
    .nav-item {
        display: block;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #e2e8f0;
        text-decoration: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 500;
        border: 2px solid transparent;
    }
    
    .nav-item:hover {
        background: rgba(102, 126, 234, 0.2);
        color: white;
        transform: translateX(5px);
        border-color: #667eea;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Custom Header */
    .client-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }
    
    .client-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    .client-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        z-index: 1;
        position: relative;
    }
    
    .client-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        z-index: 1;
        position: relative;
    }
    
    .welcome-message {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        color: white;
        font-weight: 500;
    }
    
    /* Page Container */
    .page-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Product Cards Grid */
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    .product-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .product-card:hover::before {
        left: 100%;
    }
    
    .product-name {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .product-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .product-stock {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .stock-available {
        background: #d1fae5;
        color: #065f46;
    }
    
    .stock-low {
        background: #fef3c7;
        color: #92400e;
    }
    
    .stock-out {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Purchase Section */
    .purchase-section {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        margin: 2rem 0;
        animation: slideInUp 0.6s ease-out;
    }
    
    .purchase-form {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .purchase-form:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);
    }
    
    .purchase-summary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    /* Stats Cards */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        flex: 1;
        min-width: 200px;
        text-align: center;
        transition: transform 0.3s ease;
        border-top: 4px solid #667eea;
        animation: bounceIn 0.6s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
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
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
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
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.1);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        border: none;
        border-radius: 10px;
        animation: slideInRight 0.5s ease-out;
    }
    
    .stError {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        border: none;
        border-radius: 10px;
        animation: shake 0.5s ease-out;
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
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .product-grid {
            grid-template-columns: 1fr;
        }
        
        .client-title {
            font-size: 2rem;
        }
        
        .stats-row {
            flex-direction: column;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_sidebar_navigation():
    """Create sidebar navigation"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #334155; margin-bottom: 1rem;">
        <h2 style="color: rgba(125,25,355,0.9); margin: 0; font-size: 1.5rem;">🛍️ Store Menu</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation options
    pages = {
        "🏠 Dashboard": "dashboard",
        "🛍️ Products": "products", 
        "🛒 Purchase": "purchase",
        "📜 Order History": "history",
        "📊 Analytics": "analytics",
        "👤 Profile": "profile"
    }
    
    # Create navigation
    selected_page = st.sidebar.selectbox(
        "Navigate to:",
        options=list(pages.keys()),
        key="navigation"
    )
    
    # Add user info in sidebar
    st.sidebar.markdown("---")
    if 'user' in st.session_state:
        user = st.session_state.user
        st.sidebar.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <div style="color: #e2e8f0; text-align: center;">
                <h4 style="margin: 0; color: black;">👤 Welcome</h4>
                <p style="margin: 0.5rem 0; font-weight: 500; color: black;">{user.get('username', user.get('email', 'Customer'))}</p>
                <small style="color: black;">Online since {datetime.now().strftime('%H:%M')}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #e2e8f0;">
        <h4 style="color: white; margin-bottom: 1rem;">⚡ Quick Stats</h4>
    </div>
    """, unsafe_allow_html=True)
    
    return pages[selected_page]

def create_client_header(user):
    current_time = datetime.now().strftime("%B %d, %Y")
    
    st.markdown(f"""
    <div class="client-header">
        <h1 class="client-title">🛍️ Premium Store</h1>
        <p class="client-subtitle">Your Ultimate Shopping Experience</p>
        <div class="welcome-message">
            👋 Hello <strong>{user.get('username', user.get('email', 'Customer'))}</strong>! 
            Ready to explore? | 📅 {current_time}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_user_stats(user):
    try:
        # Get user's purchase history
        df = pd.read_csv(
            "database/purchase_report.csv",
            names=["email", "product_id", "product_name", "price", "quantity", "total"],
            header=None,
            on_bad_lines="skip"
        )
        user_history = df[df["email"] == user["email"]]
        
        total_purchases = len(user_history)
        total_spent = user_history["total"].sum() if not user_history.empty else 0
        avg_order = total_spent / total_purchases if total_purchases > 0 else 0
        
    except (FileNotFoundError, KeyError):
        total_purchases = total_spent = avg_order = 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_purchases}</div>
            <div class="stat-label">🛒 Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">Rs.{total_spent:,.0f}</div>
            <div class="stat-label">💰 Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">Rs.{avg_order:,.0f}</div>
            <div class="stat-label">📊 Avg Order</div>
        </div>
        """, unsafe_allow_html=True)

def dashboard_page(user):
    """Dashboard overview page"""
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    # User stats
    create_user_stats(user)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🎉 Welcome to your dashboard! Navigate using the sidebar to explore products, make purchases, and view your order history.")
    
    with col2:
        st.success("✅ All systems are running smoothly. Happy shopping!")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     if st.button("🛍️ Browse Products", use_container_width=True):
    #         st.experimental_set_query_params(navigation="🛍️ Products")
    #         st.rerun()

    
    # with col2:
    #     if st.button("🛒 Make Purchase", use_container_width=True):
    #         st.session_state.navigation = "🛒 Purchase"
    #         st.rerun()
    
    # with col3:
    #     if st.button("📜 View History", use_container_width=True):
    #         st.session_state.navigation = "📜 Order History"
    #         st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def products_page():
    """Products catalog page"""
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    st.subheader("🛍️ Product Catalog")
    
    # Load products
    with st.spinner("🔄 Loading products..."):
        try:
            products = get_all_products()
        except Exception as e:
            st.error(f"❌ Error loading products: {e}")
            products = pd.DataFrame()
    
    if products.empty:
        st.info("🏪 No products available at the moment. Please check back later!")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search products...", placeholder="Enter product name or ID")
    
    with col2:
        sort_by = st.selectbox("📊 Sort by", ["Name", "Price (Low to High)", "Price (High to Low)", "Stock"])
    
    # Filter products based on search
    if search_term:
        products = products[products['name'].str.contains(search_term, case=False, na=False)]
    
    # Sort products
    if sort_by == "Name":
        products = products.sort_values('name')
    elif sort_by == "Price (Low to High)":
        products = products.sort_values('price')
    elif sort_by == "Price (High to Low)":
        products = products.sort_values('price', ascending=False)
    elif sort_by == "Stock":
        products = products.sort_values('quantity', ascending=False)
    
    # Display products in grid
    if not products.empty:
        st.markdown('<div class="product-grid">', unsafe_allow_html=True)
        
        cols = st.columns(3)
        
        for idx, (_, product) in enumerate(products.iterrows()):
            col = cols[idx % 3]
            
            with col:
                # Determine stock status
                stock_qty = int(product['quantity'])
                if stock_qty == 0:
                    stock_class = "stock-out"
                    stock_text = "❌ Out of Stock"
                elif stock_qty < 10:
                    stock_class = "stock-low"
                    stock_text = f"⚠️ Low Stock ({stock_qty})"
                else:
                    stock_class = "stock-available"
                    stock_text = f"✅ In Stock ({stock_qty})"
                
                # Create product card
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-name">
                        🏷️ {product['name']}
                    </div>
                    <div class="product-price">
                        Rs. {float(product['price']):,.2f}
                    </div>
                    <div class="product-stock {stock_class}">
                        {stock_text}
                    </div>
                    <div style="color: #64748b; font-size: 0.9rem;">
                        ID: {product['id']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("🔍 No products found matching your search criteria.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def purchase_page(user):
    """Purchase page"""
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    st.subheader("🛒 Make a Purchase")
    
    # Load products
    with st.spinner("🔄 Loading products..."):
        try:
            products = get_all_products()
        except Exception as e:
            st.error(f"❌ Error loading products: {e}")
            products = pd.DataFrame()
    
    if products.empty:
        st.warning("No products available for purchase.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Create purchase form
    st.markdown('<div class="purchase-section">', unsafe_allow_html=True)
    st.markdown('<div class="purchase-form">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Product selection dropdown
        product_options = [(f"{row['name']} (ID: {row['id']}) - Rs.{row['price']}", row['id']) 
                          for _, row in products.iterrows() if row['quantity'] > 0]
        
        if product_options:
            selected_product_display = st.selectbox(
                "🏷️ Select Product",
                options=[option[0] for option in product_options],
                help="Choose a product from available inventory"
            )
            
            # Get selected product ID
            selected_id = next(option[1] for option in product_options if option[0] == selected_product_display)
        else:
            st.error("❌ No products available for purchase!")
            st.markdown('</div></div></div>', unsafe_allow_html=True)
            return
    
    with col2:
        buy_qty = st.number_input(
            "📦 Quantity", 
            min_value=1, 
            value=1,
            help="Enter quantity to purchase"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process selected product
    if selected_id:
        selected_product = products[products["id"] == selected_id]
        
        if not selected_product.empty:
            product = selected_product.iloc[0]
            name = product["name"]
            price = float(product["price"])
            available_qty = int(product["quantity"])
            total_price = price * buy_qty
            
            # Purchase summary
            if available_qty > 0:
                st.markdown(f"""
                <div class="purchase-summary">
                    <h3>🧾 Purchase Summary</h3>
                    <p><strong>{name}</strong></p>
                    <p>Quantity: {buy_qty} × Rs.{price:,.2f} = <strong>Rs.{total_price:,.2f}</strong></p>
                    <p>Available Stock: {available_qty} units</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Purchase button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🛒 Confirm Purchase", use_container_width=True):
                        if buy_qty > available_qty:
                            st.error(f"❌ Only {available_qty} items available!")
                        else:
                            # Process purchase with loading animation
                            with st.spinner("🔄 Processing your purchase..."):
                                time.sleep(1)  # Simulate processing time
                                
                                # Update quantity
                                update_quantity(selected_id, buy_qty)
                                notify_admin(f"{user['email']} purchased {name} (Qty: {buy_qty})")
                                
                                # Write purchase data
                                with open("database/purchase_report.csv", "a", newline="") as f:
                                    writer = csv.writer(f)
                                    writer.writerow([
                                        user['email'], selected_id, name, price, buy_qty, total_price
                                    ])
                                
                                st.success("✅ Purchase successful! Thank you for shopping with us! 🎉")
                                st.balloons()
                                # st.snow()
                                time.sleep(2)
                              
                                # try:
                                #     st.balloons()
                                #     time.sleep(3)  # Give time to see the balloons
                                # except Exception as e:
                                #     st.snow()  # Fallback effect
                                #     print(f"Balloon animation failed: {e}")
                                st.rerun()
            # else:
            #     st.error(f"❌ {name} is currently out of stock!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def history_page(user):
    """Order history page"""
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    st.subheader("📜 Your Purchase History")
    
    try:
        with st.spinner("Loading your purchase history..."):
            df = pd.read_csv(
                "database/purchase_report.csv",
                names=["email", "product_id", "product_name", "price", "quantity", "total"],
                header=None,
                on_bad_lines="skip"
            )
        
        # Filter current user's purchases
        user_history = df[df["email"] == user["email"]]
        
        if user_history.empty:
            st.info("🛍️ You haven't made any purchases yet. Start shopping to see your history!")
        else:
            # Display enhanced history
            st.dataframe(
                user_history,
                use_container_width=True,
                height=400,
                column_config={
                    "email": st.column_config.TextColumn("📧 Email", width="medium"),
                    "product_id": st.column_config.TextColumn("🆔 Product ID", width="small"),
                    "product_name": st.column_config.TextColumn("🏷️ Product", width="medium"),
                    "price": st.column_config.NumberColumn("💰 Price", format="Rs. %.2f"),
                    "quantity": st.column_config.NumberColumn("📦 Qty", format="%d"),
                    "total": st.column_config.NumberColumn("💵 Total", format="Rs. %.2f"),
                }
            )
            
            # Download history option
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Download Purchase History", use_container_width=True):
                    csv_data = user_history.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"purchase_history_{user['email']}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🔄 Refresh History", use_container_width=True):
                    st.rerun()
    
    except FileNotFoundError:
        st.warning("📂 No purchase history found.")
    except Exception as e:
        st.error(f"❌ Error loading purchase history: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def analytics_page(user):
    """Analytics page"""
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    st.subheader("📊 Your Shopping Analytics")
    
    try:
        df = pd.read_csv(
            "database/purchase_report.csv",
            names=["email", "product_id", "product_name", "price", "quantity", "total"],
            header=None,
            on_bad_lines="skip"
        )
        
        # Filter current user's purchases
        user_history = df[df["email"] == user["email"]]
        
        if user_history.empty:
            st.info("🛍️ No purchase data available for analytics. Make some purchases first!")
        else:
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_orders = len(user_history)
                st.metric("📦 Total Orders", total_orders)
            
            with col2:
                total_spent = user_history["total"].sum()
                st.metric("💰 Total Spent", f"Rs.{total_spent:,.2f}")
            
            with col3:
                avg_order = total_spent / total_orders if total_orders > 0 else 0
                st.metric("📊 Avg Order Value", f"Rs.{avg_order:,.2f}")
            
            with col4:
                total_items = user_history["quantity"].sum()
                st.metric("🛍️ Total Items", int(total_items))
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Spending by product
                if len(user_history) > 0:
                    fig1 = px.pie(
                        user_history, 
                        values='total', 
                        names='product_name',
                        title="💰 Spending by Product",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig1.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_family="Poppins"
                    )
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Quantity by product
                if len(user_history) > 0:
                    fig2 = px.bar(
                        user_history.groupby('product_name')['quantity'].sum().reset_index(),
                        x='quantity',
                        y='product_name',
                        title="📦 Quantity by Product",
                        orientation='h',
                        color='quantity',
                        color_continuous_scale='viridis'
                    )
                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_family="Poppins"
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            
            # Most purchased products
            st.subheader("🏆 Your Top Products")
            top_products = user_history.groupby('product_name').agg({
                'quantity': 'sum',
                'total': 'sum'
            }).sort_values('total', ascending=False).head(5)
            
            if not top_products.empty:
                st.dataframe(
                    top_products,
                    use_container_width=True,
                    column_config={
                        "quantity": st.column_config.NumberColumn("📦 Total Qty", format="%d"),
                        "total": st.column_config.NumberColumn("💰 Total Spent", format="Rs. %.2f"),
                    }
                )
    
    except FileNotFoundError:
        st.warning("📂 No purchase data found for analytics.")
    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def profile_page(user):
    """User profile page"""
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    st.subheader("👤 User Profile")
    
    # User information
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👤</div>
            <h3 style="margin: 0; color: white;">User Profile</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📝 Account Information")
        
        # Display user info
        st.text_input("📧 Email", value=user.get('email', ''), disabled=True)
        st.text_input("👤 Username", value=user.get('username', ''), disabled=True)
        
        # Account stats
        try:
            df = pd.read_csv(
                "database/purchase_report.csv",
                names=["email", "product_id", "product_name", "price", "quantity", "total"],
                header=None,
                on_bad_lines="skip"
            )
            user_history = df[df["email"] == user["email"]]
            
            if not user_history.empty:
                first_purchase = "Recent"  # Placeholder since we don't have dates
                last_purchase = "Recent"   # Placeholder since we don't have dates
            else:
                first_purchase = "No purchases yet"
                last_purchase = "No purchases yet"
                
        except FileNotFoundError:
            first_purchase = "No purchases yet"
            last_purchase = "No purchases yet"
        
        st.text_input("🗓️ Member Since", value="2024", disabled=True)
        st.text_input("🛒 First Purchase", value=first_purchase, disabled=True)
        st.text_input("🕒 Last Purchase", value=last_purchase, disabled=True)
    
    st.markdown("---")
    
    # Account actions
    st.subheader("⚙️ Account Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Profile", use_container_width=True):
            st.success("✅ Profile refreshed!")
            st.rerun()
    
    with col2:
        if st.button("📥 Export Data", use_container_width=True):
            try:
                df = pd.read_csv(
                    "database/purchase_report.csv",
                    names=["email", "product_id", "product_name", "price", "quantity", "total"],
                    header=None,
                    on_bad_lines="skip"
                )
                user_data = df[df["email"] == user["email"]]
                
                if not user_data.empty:
                    csv_data = user_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download My Data",
                        data=csv_data,
                        file_name=f"my_data_{user['email']}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No data to export.")
            except:
                st.error("Error exporting data.")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.warning("Logout functionality would redirect to login page.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def client_dashboard(user):
    # Load custom CSS
    load_client_css()
    
    # Initialize session state for user
    if 'user' not in st.session_state:
        st.session_state.user = user
    
    # Create sidebar navigation
    current_page = create_sidebar_navigation()
    
    # Create header
    create_client_header(user)
    
    # Route to appropriate page
    if current_page == "dashboard":
        dashboard_page(user)
    elif current_page == "products":
        products_page()
    elif current_page == "purchase":
        purchase_page(user)
    elif current_page == "history":
        history_page(user)
    elif current_page == "analytics":
        analytics_page(user)
    elif current_page == "profile":
        profile_page(user)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 2rem;">
        <p>🛍️ Thank you for choosing our store! Happy Shopping! 🎉</p>
        <p style="font-size: 0.9rem;">Need help? Contact our support team anytime.</p>
    </div>
    """, unsafe_allow_html=True)

# Run the client dashboard
if __name__ == "__main__":
    # Example user for testing
    test_user = {"email": "test@example.com", "username": "TestUser"}
    client_dashboard(test_user)