import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Executive Overview", layout="wide")

# Custom CSS
st.markdown("""
<style>
    div.block-container { padding-top: 2rem; }
    [data-testid="stSidebar"] {
        background-color: #11151c !important; 
    }
</style>
""", unsafe_allow_html=True)

# 2. Resilient Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("superstore.csv", encoding="ISO-8859-1")
        date_col = next((col for col in df.columns if 'Order.Dat' in col), None)
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df['Month_Year'] = df[date_col].dt.to_period('M').astype(str)
        return df, date_col
    except FileNotFoundError:
        st.error("Fatal Error: 'superstore.csv' missing. Rectify your file path immediately.")
        st.stop()

df, date_col = load_data()

st.markdown("## Global Sales & Profitability Engine")

# 3. Dynamic Sidebar Filtering Engine
st.sidebar.header("Global Filters")

target_filters = ['Region', 'Category', 'Segment', 'State', 'Sub.Categ', 'Ship.Mode']
active_filters = {}

for col in target_filters:
    if col in df.columns:
        unique_vals = sorted(df[col].dropna().unique().tolist())
        selected = st.sidebar.multiselect(f"{col}", unique_vals)
        if selected:
            active_filters[col] = selected

filtered_df = df.copy()
for col, selected_values in active_filters.items():
    filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

if filtered_df.empty:
    st.warning("Your filter combination resulted in zero records. Clear some filters.")
    st.stop()

# --- HELPER FUNCTION FOR KPI NUMBERS ---
def format_metric(value):
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${value:,.0f}"

# 4. Top-Line KPI Cards
if 'Sales' in filtered_df.columns and 'Profit' in filtered_df.columns:
    st.markdown("### Top-Line Metrics")
    
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    total_qty = filtered_df['Quantity'].sum() if 'Quantity' in filtered_df.columns else 0

    formatted_sales = format_metric(total_sales)
    formatted_profit = format_metric(total_profit)
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Revenue", formatted_sales)
    col2.metric("Net Profit", formatted_profit)
    col3.metric("Profit Margin", f"{margin:.1f}%")
    
    if total_qty >= 1_000_000:
        col4.metric("Units Moved", f"{total_qty / 1_000_000:.2f}M")
    elif total_qty >= 1_000:
        col4.metric("Units Moved", f"{total_qty / 1_000:.1f}K")
    else:
        col4.metric("Units Moved", f"{total_qty:,.0f}")
    
    st.divider()

# ==========================================
# 5. VERTICAL SCROLLING LAYOUT (5 CHARTS STACKED)
# ==========================================

# Chart 1: Line Chart
st.markdown("### 1. Revenue Velocity (Sales over Time)")
if date_col and 'Sales' in filtered_df.columns:
    trend_df = filtered_df.groupby('Month_Year', as_index=False)['Sales'].sum().sort_values('Month_Year')
    fig_line = px.line(trend_df, x='Month_Year', y='Sales', markers=True, template="plotly_dark")
    fig_line.update_layout(height=600) 
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("Cannot render chart: Missing temporal or Sales data.")

st.divider()

# Chart 2: Horizontal Bar Chart
st.markdown("### 2. Category Dominance (Sales by Sub-Category)")
sub_cat_col = next((col for col in df.columns if 'Sub.Categ' in col), None)
if sub_cat_col and 'Sales' in filtered_df.columns:
    cat_df = filtered_df.groupby(sub_cat_col, as_index=False)['Sales'].sum().nlargest(15, 'Sales')
    fig_bar = px.bar(cat_df, x='Sales', y=sub_cat_col, orientation='h', template="plotly_dark")
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=600)
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Cannot render chart: Missing Category or Sales data.")

st.divider()

# Chart 3: Pie Chart
st.markdown("### 3. Geographic Sales Distribution")
if 'Region' in filtered_df.columns and 'Sales' in filtered_df.columns:
    pie_df = filtered_df.groupby('Region', as_index=False)['Sales'].sum()
    fig_pie = px.pie(pie_df, names='Region', values='Sales', template="plotly_dark", hole=0.3)
    fig_pie.update_layout(height=600)
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("Cannot render chart: Missing Region or Sales data.")

st.divider()

# Chart 4: Segment vs Shipping Mode Profitability Matrix (NEW)
st.markdown("### 4. Operational Profit Matrix (Segment vs. Shipping Mode)")
if 'Segment' in filtered_df.columns and 'Ship.Mode' in filtered_df.columns and 'Profit' in filtered_df.columns:
    matrix_df = filtered_df.groupby(['Segment', 'Ship.Mode'], as_index=False)['Profit'].sum()
    
    # Using a density heatmap configuration to expose operational sweet spots and leakage
    fig_matrix = px.density_heatmap(
        matrix_df, 
        x="Ship.Mode", 
        y="Segment", 
        z="Profit", 
        text_auto='.2s',
        template="plotly_dark",
        color_continuous_scale="Viridis"
    )
    fig_matrix.update_layout(height=600)
    st.plotly_chart(fig_matrix, use_container_width=True)
else:
    st.warning("Cannot render matrix: Missing Segment, Ship Mode, or Profit columns.")

st.divider()

# Chart 5: Quantity Distribution Histogram (NEW)
st.markdown("### 5. Transaction Volume Density (Unit Distribution Per Order)")
if 'Quantity' in filtered_df.columns:
    fig_hist = px.histogram(
        filtered_df, 
        x="Quantity", 
        nbins=20, 
        template="plotly_dark",
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(
        height=600,
        xaxis_title="Units Ordered Per Transaction",
        yaxis_title="Frequency Count",
        bargap=0.1
    )
    st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("Cannot render distribution: Missing Quantity data column.")