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

import json 
import pandas as pd
import pydeck as pdk
import streamlit  as st

import pydeck as pdk

municipios_yucatan = "Yucatan.geojson"
with open(municipios_yucatan) as archivo:
    municipios_json = json.load(archivo)
dfMunicipios = pd.read_csv("municipiosDatos.csv")
dfMunicipios.drop('Unnamed: 0',axis=1,inplace=True)
st.dataframe(dfMunicipios)

# Create a copy of the GeoJSON data to modify it
enriched_municipios_json = json.loads(json.dumps(municipios_json))

# Merge RandomNumbers from dfMunicipios into the GeoJSON properties
for feature in enriched_municipios_json['features']:
    municipio_name = feature['properties']['NOMGEO']
    # Find the corresponding row in dfMunicipios
    matching_row = dfMunicipios[dfMunicipios['Municipio'] == municipio_name]
    if not matching_row.empty:
        # Convert numpy.int64 to a standard Python int
        random_number = int(matching_row['RandomNumbers'].iloc[0])
        feature['properties']['RandomNumbers'] = random_number
    else:
        feature['properties']['RandomNumbers'] = 0 # Default value if no match found
# Define the pydeck GeoJsonLayer
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    enriched_municipios_json,
    filled=True,
    get_fill_color=[
        "(properties.RandomNumbers / 1000) * 255", # Red component (scaled by value)
        "(properties.RandomNumbers / 1000) * 255", # Green component
        "255 - (properties.RandomNumbers / 1000) * 255", # Blue component (inverse scaled)
        200 # Alpha transparency
    ],
    get_line_color=[0, 0, 0, 200],
    get_line_width=1,
    stroked=True,
    opacity=0.8,
    extruded=False,
    auto_highlight=True,
    pickable=True # Make polygons pickable for interactivity
)

# Set the initial view state for Yucatan
view_state = pdk.ViewState(
    latitude=20.8,
    longitude=-89.0,
    zoom=7,
    pitch=0
)

# Create the pydeck Deck
r = pdk.Deck(
    layers=[geojson_layer],
    initial_view_state=view_state,
    tooltip={"text": "Municipio: {NOMGEO}\nRandomNumbers: {RandomNumbers}"}
)

# Render the deck

st.pydeck_chart(r)
