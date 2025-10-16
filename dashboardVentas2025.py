import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Product Sales and Profit Analysis')

# Replace 'ruta/a/tu/archivo.xlsx' with the actual path to your file
# When running in Streamlit, the file should be accessible from the environment
excel_file_path = 'Ordenes Final.xlsx' # Update this path as needed

try:
    df_excel = pd.read_excel(excel_file_path)

    # Process data for top selling products
    product_sales = df_excel.groupby('Product Name')['Sales'].sum().reset_index()
    product_sales = product_sales.sort_values(by='Sales', ascending=False)
    top_n_products = product_sales.head(5)

    # Create bar chart for top selling products using Plotly Express and Streamlit
    fig_sales = px.bar(top_n_products, x='Product Name', y='Sales', title='Top 5 Selling Products')
    fig_sales.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sales)

    # Process data for top profitable products
    product_profit = df_excel.groupby('Product Name')['Profit'].sum().reset_index()
    product_profit = product_profit.sort_values(by='Profit', ascending=False)
    top_n_profitable_products = product_profit.head(5)

    # Create bar chart for top profitable products using Plotly Express and Streamlit
    fig_profit = px.bar(top_n_profitable_products, x='Product Name', y='Profit', title='Top 5 Most Profitable Products')
    fig_profit.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_profit)

except FileNotFoundError:
    st.error(f"Error: The file was not found at the path: {excel_file_path}")
except Exception as e:
    st.error(f"An error occurred while reading the Excel file: {e}")
