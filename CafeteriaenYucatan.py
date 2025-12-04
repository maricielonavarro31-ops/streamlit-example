import streamlit as st
import pandas as pd
import pydeck as pdk

# Define the file path (re-load for self-contained script)
file_path = '/content/drive/MyDrive/Herramientas Datos/Coffee Shop Sales_Modified.xlsx'

# Load the Excel file into a pandas DataFrame
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"Error: The file '{file_path}' was not found. Please ensure it's in the correct location.")
    st.stop()

st.title("Coffee Shop Location Dashboard")

# Ensure 'store_name' column exists and 'state store location' was added
if 'store_location' in df.columns and 'store_name' not in df.columns:
    df.rename(columns={'store_location': 'store_name'}, inplace=True)

# Create a dictionary for state store location to lat/lon mapping
# Approximate coordinates for the specified locations in Yucatán, Mexico
location_coordinates = {
    'MOTUL': {'lat': 21.1667, 'lon': -89.2667},
    'TICUL': {'lat': 20.5833, 'lon': -89.5333},
    'MERIDA': {'lat': 20.9670, 'lon': -89.6247}
}

# Add 'latitude' and 'longitude' columns to the DataFrame
if 'state store location' in df.columns:
    # Ensure state store location column values are clean and in line with dictionary keys
    df['state store location'] = df['state store location'].str.upper().str.strip()
    df['latitude'] = df['state store location'].map(lambda x: location_coordinates.get(x, {}).get('lat'))
    df['longitude'] = df['state store location'].map(lambda x: location_coordinates.get(x, {}).get('lon'))
else:
    st.warning("Column 'state store location' not found. Cannot map store locations.")
    df['latitude'] = None
    df['longitude'] = None

# Drop rows where latitude or longitude could not be determined
df.dropna(subset=['latitude', 'longitude'], inplace=True)

# Extract unique store names for filter options
unique_store_names = df['store_name'].unique().tolist() if 'store_name' in df.columns else []

# Extract unique product types for filter options
unique_product_types = df['product_type'].unique().tolist() if 'product_type' in df.columns else []

st.sidebar.header("Filter Data")

# Create a Streamlit multiselect widget in the sidebar for 'store_name'
selected_store_names = st.sidebar.multiselect(
    'Select Stores:',
    options=unique_store_names,
    default=unique_store_names
)

# Create a Streamlit multiselect widget in the sidebar for 'product_type'
selected_product_types = st.sidebar.multiselect(
    'Select Product Types:',
    options=unique_product_types,
    default=unique_product_types
)

# Apply filters to the DataFrame
filtered_df = df[
    df['store_name'].isin(selected_store_names) &
    df['product_type'].isin(selected_product_types)
]

st.subheader("Store Locations on Map")

if not filtered_df.empty:
    # Aggregate data to get unique store locations and their details (if needed for tooltip)
    # For simplicity, we'll just plot distinct store locations available in the filtered_df
    store_locations_for_map = filtered_df[['store_name', 'state store location', 'latitude', 'longitude']].drop_duplicates()

    # Set the initial view state for the map, centered around the average coordinates
    view_state = pdk.ViewState(
        latitude=store_locations_for_map['latitude'].mean(),
        longitude=store_locations_for_map['longitude'].mean(),
        zoom=9,
        pitch=45
    )

    # Create a PyDeck Layer for the Scatterplot
    layer = pdk.Layer(
        'ScatterplotLayer',
        store_locations_for_map,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=500,  # Radius in meters
        pickable=True,
        tooltip={
            "text": "Store: {store_name}\nLocation: {state store location}\nLat: {latitude}\nLon: {longitude}"
        }
    )

    # Create a Deck object
    r = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={
            "html": "<b>Store:</b> {store_name}<br/><b>Location:</b> {state store location}"
        }
    )

    # Render the map
    st.pydeck_chart(r)
else:
    st.warning("No store locations to display based on current filters.")

st.subheader("Filtered Data Table")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No data available for the selected filters.")

st.subheader("How to run this Streamlit app:")
st.markdown("1. Save the code above as a Python file (e.g., `app.py`).")
st.markdown("2. Open your terminal or command prompt.")
st.markdown("3. Navigate to the directory where you saved `app.py`.")
st.markdown("4. Run the command: `streamlit run app.py`")
