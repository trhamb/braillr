import numpy as np
from stl import mesh
from PIL import Image

def png_to_stl(png_path, stl_path="output.stl", height_scale=5.0, size_scale=0.5, baseplate=False):
    # Load the image and convert to grayscale
    img = Image.open(png_path).convert('L')
    img_data = np.array(img)
    
    rows, cols = img_data.shape
    vertices = []
    faces = []
    
    # Define heights
    base_thickness = 1.0 if baseplate else 0.0
    braille_offset = 1.5
    
    # Generate vertices with adjusted height for baseplate and scaled X/Y
    for x in range(rows):
        for y in range(cols):
            z = (-1 * (img_data[x, y] / 255.0 * height_scale)) + (braille_offset if baseplate else 0.0)
            vertices.append([x * size_scale, y * size_scale, z])
            
    # Add baseplate vertices
    if baseplate:
        for x in range(rows):
            for y in range(cols):
                vertices.append([x * size_scale, y * size_scale, -base_thickness])
    
    vertices = np.array(vertices)
    vertex_count = rows * cols
    
    # Generate faces with correct orientation
    for x in range(rows - 1):
        for y in range(cols - 1):
            v1 = x * cols + y
            v2 = v1 + 1
            v3 = (x + 1) * cols + y
            v4 = v3 + 1
            
            # Top surface triangles
            faces.append([v1, v3, v2])
            faces.append([v2, v3, v4])
            
            if baseplate:
                # Base surface triangles
                b1 = v1 + vertex_count
                b2 = v2 + vertex_count
                b3 = v3 + vertex_count
                b4 = v4 + vertex_count
                faces.append([b1, b2, b3])
                faces.append([b2, b4, b3])
                
                # Side walls
                faces.append([v1, v2, b1])
                faces.append([b1, v2, b2])
                faces.append([v2, v4, b2])
                faces.append([b2, v4, b4])
                faces.append([v3, v1, b3])
                faces.append([b3, v1, b1])
                faces.append([v4, v3, b4])
                faces.append([b4, v3, b3])
    
    faces = np.array(faces)
    
    # Create STL mesh
    my_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            my_mesh.vectors[i][j] = vertices[f[j], :]
    
    my_mesh.save(stl_path)
    return stl_path




