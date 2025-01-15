import numpy as np
from stl import mesh
from PIL import Image

def png_to_stl(png_path, stl_path="output.stl", height_scale=5.0, baseplate=False):
    # Load the image and convert to grayscale
    img = Image.open(png_path).convert('L')
    img_data = np.array(img)
    
    rows, cols = img_data.shape
    vertices = []
    faces = []
    
    # Generate vertices
    for x in range(rows):
        for y in range(cols):
            z = -1 * (img_data[x, y] / 255.0 * height_scale)
            vertices.append([x, y, z])
            
    # Add baseplate vertices here
    if baseplate:
        base_height = 1.0  # 1mm thick baseplate
        for x in range(rows):
            for y in range(cols):
                vertices.append([x, y, base_height])
    
    vertices = np.array(vertices)
    
    # Generate faces with correct orientation
    for x in range(rows - 1):
        for y in range(cols - 1):
            v1 = x * cols + y
            v2 = v1 + 1
            v3 = (x + 1) * cols + y
            v4 = v3 + 1
            # Reversed triangle orientation
            faces.append([v1, v3, v2])
            faces.append([v2, v3, v4])
    
    faces = np.array(faces)
    
    # Create STL mesh
    my_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            my_mesh.vectors[i][j] = vertices[f[j], :]
    
    # Save the STL file
    my_mesh.save(stl_path)
    print(f"STL file saved to {stl_path}")
    return stl_path
