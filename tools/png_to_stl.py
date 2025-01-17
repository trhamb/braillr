import numpy as np
from PIL import Image
import cadquery as cq

def png_to_stl(png_path, stl_path="output.stl", height_scale=5.0, size_scale=0.5, baseplate=False):
    print("Starting STL generation...")
    
    # Load and process image
    img = Image.open(png_path).convert('L')
    img_data = np.array(img)
    rows, cols = img_data.shape
    
    # Find actual dot centers
    dot_positions = []
    threshold = 128
    
    # Use connected components to find dot centers
    from scipy import ndimage
    labeled_array, num_features = ndimage.label(img_data < threshold)
    
    for feature_idx in range(1, num_features + 1):
        y, x = np.where(labeled_array == feature_idx)
        if len(x) > 0 and len(y) > 0:
            # Swap x and y here
            center_x = np.mean(y) * size_scale
            center_y = np.mean(x) * size_scale
            dot_positions.append((center_x, center_y))
    
    print(f"Found {len(dot_positions)} braille dots")
    
    # Create base workplane
    result = cq.Workplane("XY")
    
    # Add baseplate if requested
    if baseplate:
        print("Adding baseplate...")
        plate_width = rows * size_scale
        plate_length = cols * size_scale
        plate_height = 1.0  # Keep 1mm thick
        result = result.box(plate_width, plate_length, plate_height, centered=False)
    
    # Add dots at detected positions with larger size
    dot_height = 0.6 
    dot_radius = 0.75
    base_z = 0 if not baseplate else 0.2  # Changed to start at 2.0

    
    print("Creating braille dots...")
    for x, y in dot_positions:
        dot = (cq.Workplane("XY")
              .transformed(offset=(x, y, base_z))
              .cylinder(dot_height, dot_radius))
        result = result.union(dot)
    
    print(f"Exporting to {stl_path}")
    cq.exporters.export(result, stl_path)
    
    print("STL generation complete!")
    return stl_path
