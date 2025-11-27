import streamlit as st
import pandas as pd
import plotly.express as px

# Load the modified Excel file
file_path = 'Coffee Shop Sales_Modified.xlsx'
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"Error: The file '{file_path}' was not found. Please ensure it's in the correct location.")
    st.stop()

st.title("Coffee Shop Sales Dashboard")

# Ensure 'store_name' column exists as per previous steps (if not already renamed in the loaded file)
if 'store_location' in df.columns and 'store_name' not in df.columns:
    df.rename(columns={'store_location': 'store_name'}, inplace=True)

# Extract unique product details and store names for filter options
unique_products = df['product_detail'].unique().tolist()
unique_stores = df['store_name'].unique().tolist()

st.sidebar.header("Filter Data")

# Create Streamlit multiselect widgets for 'product_detail' and 'store_name'
selected_products = st.sidebar.multiselect(
    'Select Products:',
    options=unique_products,
    default=unique_products
)

selected_stores = st.sidebar.multiselect(
    'Select Stores:',
    options=unique_stores,
    default=unique_stores
)

# Apply filters to the DataFrame
if selected_products and selected_stores:
    filtered_df = df[
        df['product_detail'].isin(selected_products) &
        df['store_name'].isin(selected_stores)
    ]
else:
    filtered_df = pd.DataFrame() # Empty DataFrame if no filters selected

# Aggregate the filtered data to find the most sold products
top_products_filtered = filtered_df.groupby('product_detail')['transaction_qty'].sum().nlargest(10).reset_index()
top_products_filtered.rename(columns={'transaction_qty': 'total_quantity_sold'}, inplace=True)

st.header("Top 10 Most Sold Products (Filtered)")

if not top_products_filtered.empty:
    # Create the bar chart using Plotly Express
    fig = px.bar(
        top_products_filtered,
        x='product_detail',
        y='total_quantity_sold',
        title='Top 10 Most Sold Products by Quantity',
        labels={'product_detail': 'Product', 'total_quantity_sold': 'Total Quantity Sold'}
    )
    fig.update_layout(xaxis_title_standoff=25)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, width='stretch') # Changed use_container_width=True to width='stretch'
else:
    st.warning("No data available for the selected filters to display a chart.")

st.subheader("How to run this Streamlit app:")
st.markdown("1. Save the code above as a Python file (e.g., `app.py`).")
st.markdown("2. Open your terminal or command prompt.")
st.markdown("3. Navigate to the directory where you saved `app.py`.")
st.markdown("4. Run the command: `streamlit run app.py`")
