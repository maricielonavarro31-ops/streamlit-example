import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Product Sales and Profit Analysis')

# Replace 'ruta/a/tu/archivo.xlsx' with the actual path to your file
# When running in Streamlit, the file should be accessible from the environment
excel_file_path = 'Ordenes Final.xlsx' # Update this path as needed

try:
    df_excel = pd.read_excel(excel_file_path)

    # Add filters to the sidebar
    st.sidebar.header("Filter by Region and State")

    # Use columns for side-by-side filters
    col1, col2 = st.sidebar.columns(2)

    # Region filter
    regions = ['Todas'] + df_excel['Region'].unique().tolist()
    selected_region = col1.selectbox('Select a Region', regions)

    # Filter data by region
    if selected_region == 'Todas':
        filtered_df_region = df_excel
    else:
        filtered_df_region = df_excel[df_excel['Region'] == selected_region]

    # State filter (dependent on selected region)
    if selected_region == 'Todas':
        states = ['Todos'] + filtered_df_region['State'].unique().tolist()
    else:
        states = ['Todos'] + filtered_df_region['State'].unique().tolist()

    selected_state = col2.selectbox('Select a State', states)

    # Filter data by state
    if selected_state == 'Todos':
        filtered_df = filtered_df_region
    else:
        filtered_df = filtered_df_region[filtered_df_region['State'] == selected_state]


    # Process data for top selling products
    product_sales = filtered_df.groupby('Product Name')['Sales'].sum().reset_index()
    product_sales = product_sales.sort_values(by='Sales', ascending=False)
    top_n_products = product_sales.head(5)

    # Create bar chart for top selling products using Plotly Express and Streamlit
    fig_sales = px.bar(top_n_products, x='Product Name', y='Sales', title=f'Top 5 Selling Products in {selected_state}, {selected_region}')
    fig_sales.update_layout(
        xaxis_tickangle=-45,
        xaxis=dict(
            tickmode="array",
            ticktext=[text.replace(' ', '<br>') for text in top_n_products['Product Name']],
            tickvals=top_n_products['Product Name']
        )
    )
    st.plotly_chart(fig_sales)

    # Process data for top profitable products
    product_profit = filtered_df.groupby('Product Name')['Profit'].sum().reset_index()
    product_profit = product_profit.sort_values(by='Profit', ascending=False)
    top_n_profitable_products = product_profit.head(5)

    # Create bar chart for top profitable products using Plotly Express and Streamlit
    fig_profit = px.bar(top_n_profitable_products, x='Product Name', y='Profit', title=f'Top 5 Most Profitable Products in {selected_state}, {selected_region}')
    fig_profit.update_layout(
        xaxis_tickangle=-45,
        xaxis=dict(
            tickmode="array",
            ticktext=[text.replace(' ', '<br>') for text in top_n_profitable_products['Product Name']],
            tickvals=top_n_profitable_products['Product Name']
        )
    )
    st.plotly_chart(fig_profit)

except FileNotFoundError:
    st.error(f"Error: The file was not found at the path: {excel_file_path}")
except Exception as e:
    st.error(f"An error occurred while reading the Excel file: {e}")
