import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

# Set page config
st.set_page_config(page_title="🚚 E-Waste Route Optimizer", layout="wide")
st.title("🚚 E-Waste Pickup Route Optimizer")

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Load data from .txt file
@st.cache_data
def load_data():
    try:
        return pd.read_csv(r"C:\Users\visha\OneDrive\Desktop\STJOSPEH HACK\map\data\pickups.txt")
    except FileNotFoundError:
        # Create default sample data if file doesn't exist
        df = pd.DataFrame({
            "name": ["Factory", "User1", "User2", "User3"],
            "lat": [22.5726, 19.0760, 28.7041, 12.9716],
            "lon": [88.3639, 72.8777, 77.1025, 77.5946]
        })
        df.to_csv(r"C:\Users\visha\OneDrive\Desktop\STJOSPEH HACK\map\data\pickups.txt", index=False)
        return df

df = load_data()

# Input form
st.markdown("### ➕ Add New Pickup Location")
with st.form("add_location"):
    name = st.text_input("Name")
    lat = st.number_input("Latitude", format="%.6f", value=19.0760)
    lon = st.number_input("Longitude", format="%.6f", value=72.8777)
    submitted = st.form_submit_button("Add Location")

if submitted and name:
    new_row = pd.DataFrame({"name": [name], "lat": [lat], "lon": [lon]})
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to .txt file
    df.to_csv(r"C:\Users\visha\OneDrive\Desktop\STJOSPEH HACK\map\data\pickups.txt", index=False)
    
    st.success(f"📍 Added {name} to the list.")
    st.experimental_rerun()

# Show current data
st.markdown("### 📋 Current Locations")
st.dataframe(df)

# Map visualization
st.markdown("### 🌍 Interactive Map with Routes")

# Build map center
if not df.empty:
    avg_lat = df['lat'].mean()
    avg_lon = df['lon'].mean()
else:
    avg_lat, avg_lon = 20.0, 75.0

# Create Folium map
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

# Split into users and factory
factory = df[df['name'] == 'Factory'].iloc[0]
pickups = df[df['name'] != 'Factory']

# Combine all locations
locations = [[factory.lat, factory.lon]] + pickups[['lat', 'lon']].values.tolist()
names = ['Factory'] + pickups['name'].tolist()

# Draw markers
for idx, coord in enumerate(locations):
    color = "red" if names[idx] == "Factory" else "blue"
    folium.Marker(
        location=coord,
        popup=names[idx],
        icon=folium.Icon(color=color, icon="pushpin")
    ).add_to(m)

# Simple TSP route optimization (greedy nearest neighbor)
def tsp_greedy(matrix):
    n = len(matrix)
    order = [0]  # Start at factory
    unvisited = set(range(1, n))
    while unvisited:
        last = order[-1]
        next_node = min(unvisited, key=lambda x: matrix[last][x])
        order.append(next_node)
        unvisited.remove(next_node)
    return order

# Compute straight-line distance matrix
def compute_distance_matrix(points):
    size = len(points)
    matrix = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            matrix[i][j] = (dx**2 + dy**2) ** 0.5
    return matrix

# Build distance matrix
distance_matrix = compute_distance_matrix(locations)

# Get optimized path using greedy TSP
try:
    optimized_order = tsp_greedy(distance_matrix)
except Exception as e:
    st.error("❌ Could not optimize route.")
    optimized_order = list(range(len(locations)))

# Build route lines
original_coords = locations
optimized_coords = [locations[i] for i in optimized_order]

# Add current route (straight line)
folium.PolyLine(original_coords, color="blue", weight=2, dash_array='10', tooltip="Current Route").add_to(m)
# Add optimized route
folium.PolyLine(optimized_coords, color="green", weight=3, tooltip="Optimized Route").add_to(m)

# Display map
st.markdown("### 🗺️ Route Visualization")
folium_static(m)

# Optional: Show legend
st.markdown("""
<style>
.legend {
    background-color: #fff;
    padding: 10px;
    border: 1px solid #ccc;
    font-size: 14px;
}
</style>
<div class="legend">
    🔴 Factory &nbsp;&nbsp;🔵 User Pickup &nbsp;&nbsp;🟦 Current Route &nbsp;&nbsp;🟩 Optimized Route
</div>
""", unsafe_allow_html=True)