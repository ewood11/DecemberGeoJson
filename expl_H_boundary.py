# expl_H_boundary.py   EW241227
# below geojson file can be obtained by download from
# https://opendata.hawaii.gov/gl/dataset/flood-zones/resource/40b0add8-b29f-4968-94a9-8f60411e57c7?inner_span=True

import geopandas as gpd
import folium
from shapely.geometry import Point, Polygon
from folium import plugins

# Load geolocation dataset (example: GeoJSON or shapefile)
# Here, we assume the dataset contains points (e.g., disaster locations) in GeoJSON format.
# You can replace this with your actual dataset.

# Example: load disaster locations (GeoJSON format)
data_path = '~/Downloads/Hydrography_-8190465070377318917.geojson'
# data_path = "disaster_locations.geojson"  # Replace with actual file path
gdf = gpd.read_file(data_path)
print(f'debug 020 finish read geojson\n First few records = {gdf.head()}')

# Step 1: Define Hawaii's bounding box as the area of interest
hawaii_bbox = Polygon([
    (-156.0, 18.5),  # South West
    (-154.5, 18.5),  # South East
    (-154.5, 20.5),  # North East
    (-156.0, 20.5),  # North West
])

# Step 2: Filter the dataset to include only points within Hawaii's bounding box
hawaii_gdf = gdf[gdf.geometry.within(hawaii_bbox)]

# Step 3: Create a disaster relief boundary (buffer around the points of interest)
# Here, we generate a buffer of 10 km around each disaster location point.
buffered_points = hawaii_gdf.copy()
buffered_points['geometry'] = buffered_points.geometry.buffer(10000)  # Buffer in meters
print(f'debug 030 finished buf pts')
# Step 4: Generate the disaster relief boundary as a convex hull (optional)
# This will combine all the points into one continuous boundary.
relief_boundary = buffered_points.geometry.unary_union.convex_hull
print(f'debug050 finished relief B')
# Step 5: Create a map centered on Hawaii
m = folium.Map(location=[20.5, -156.0], zoom_start=8)

# Step 6: Add disaster relief boundary as a polygon
folium.GeoJson(relief_boundary).add_to(m)
print(f'debug 080 finish folium')
# Step 7: Add disaster locations (points) to the map
for _, row in hawaii_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f"Disaster Site: {row['name']}").add_to(m)
print(f'debug 100 finish folium loop')
# Step 8: Save the map to an HTML file
m.save("hawaii_disaster_relief_map.html")
print(f'debug 110 finish save map')
# Print message to indicate successful map generation
print("Map generated and saved as 'hawaii_disaster_relief_map.html'")
print(f'debug 150 pgm finish')
