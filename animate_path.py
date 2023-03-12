import math
import bpy
import psycopg2
import json
import os
import argparse

# Load configuration from file or environment variables
with open('config.json', 'r') as f:
    config = json.load(f)
    
host = os.getenv('DB_HOST', config['db']['host'])
port = os.getenv('DB_PORT', config['db']['port'])
database = os.getenv('DB_NAME', config['db']['name'])
username = os.getenv('DB_USERNAME', config['db']['username'])
password = os.getenv('DB_PASSWORD', config['db']['password'])

# Connect to the database
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=username,
    password=password
)

# Create a cursor
cursor = conn.cursor()

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--texture', type=str, help='path to the texture map', default='images/ear0xuu2.jpg')
parser.add_argument('--start', type=str, help='starting coordinates as "lat,lon"')
parser.add_argument('--end', type=str, help='ending coordinates as "lat,lon"')
parser.add_argument('--interpolation-points', type=int, default=20, help='number of interpolation points to generate along the path')
args = parser.parse_args()

# Extract arguments
texture_path = args.texture
start_coords = tuple(map(float, args.start.split(',')))
end_coords = tuple(map(float, args.end.split(',')))
num_points = args.interpolation_points

# Define SQL query with parameters
sql = """
WITH great_circle_path AS (
  SELECT ST_MakeLine(
             ST_Transform(
                 ST_GeomFromText('POINT(%s %s)', 4326), 
                 3857), 
             ST_Transform(
                 ST_GeomFromText('POINT(%s %s)', 4326), 
                 3857)
         ) AS geom
)
SELECT ST_X(pt) AS lon, ST_Y(pt) AS lat, 0 AS alt
FROM great_circle_path, generate_series(1, %s) AS s(n), 
     LATERAL ST_LineInterpolatePoint(geom, (n + 0.5) / (SELECT COUNT(*) FROM generate_series(1, %s) AS s(n))) AS pt;
"""

# Execute SQL query with parameters and retrieve points along the path
cursor.execute(sql, (start_coords[1], start_coords[0], end_coords[1], end_coords[0], num_points, num_points))
points = cursor.fetchall()
cursor.close()
conn.close()

# Create new Blender scene
scene = bpy.context.scene

# Add globe mesh to scene
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=1)
globe = bpy.context.object
globe.name = "Globe"

# Apply texture map to globe mesh
texture = bpy.data.images.load(texture_path)
material = bpy.data.materials.new(name="GlobeMaterial")
material.use_nodes = True
material.node_tree.nodes.new("ShaderNodeTexImage")
material.node_tree.nodes["TexImage"].image = texture
material_output = material.node_tree.nodes["Material Output"]
material_output.location = (400, 0)
material_output.inputs["Surface"].default_value = material.node_tree.nodes["TexImage"].outputs["Color"]
globe.data.materials.append(material)

# Create new empty object to serve as parent of points
empty = bpy.data.objects.new("Points", None)
scene.collection.objects.link(empty)

# Create new sphere mesh for each point and position it on the globe
for i, point in enumerate(points):
    # Create new sphere mesh and add it to empty object
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.05)
    sphere = bpy.context.object
    sphere.name = f"Point{i}"
    empty.children.link(sphere)

    # Set sphere location on surface of globe
    lon, lat, alt = point
    sphere.location = (math.radians(lon), math.radians(lat), 1)

# Set up keyframes for globe rotation and point movement
globe = bpy.data.objects["Globe"]
globe.rotation_euler = (0, 0, 0)
globe.keyframe_insert(data_path="rotation_euler", frame=1)
globe.rotation_euler = (0, 0, math.radians(360))
globe.keyframe_insert(data_path="rotation_euler", frame=100)

empty = bpy.data.objects["Points"]
for i, sphere in enumerate(empty.children):
    point = points[i]
    sphere.location = (math.radians(point[0]), math.radians(point[1]), 1)
    sphere.keyframe_insert(data_path="location", frame=1)
    sphere.location = (math.radians(point[0]), math.radians(point[1]), point[2] + 1)
    sphere.keyframe_insert(data_path="location", frame=100)
bpy.ops.render.render(animation=True)