from tools.text_to_png import text_to_png
from tools.png_to_stl import png_to_stl
import numpy as np
from PIL import Image
import os

def measure_dot_spacing(png_path):
    # Load and process image
    img = Image.open(png_path).convert('L')
    img_data = np.array(img)
    
    # Find dot centers using same method as png_to_stl
    threshold = 128
    from scipy import ndimage
    labeled_array, num_features = ndimage.label(img_data < threshold)
    
    dot_positions = []
    for feature_idx in range(1, num_features + 1):
        y, x = np.where(labeled_array == feature_idx)
        if len(x) > 0 and len(y) > 0:
            center_x = np.mean(x)
            center_y = np.mean(y)
            dot_positions.append((center_x, center_y))
    
    # Sort dots by x position to measure horizontal spacing
    dot_positions.sort(key=lambda x: x[0])
    
    # Calculate average spacing between adjacent dots
    spacings = []
    for i in range(len(dot_positions)-1):
        x1, y1 = dot_positions[i]
        x2, y2 = dot_positions[i+1]
        spacing = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        spacings.append(spacing)
    
    return np.mean(spacings) if spacings else 0

def run_calibration():
    test_text = "⠿⠿"  # Two full braille cells
    test_sizes = range(20, 36, 2)  # Test font sizes from 20 to 34
    
    if not os.path.exists('calibration'):
        os.makedirs('calibration')
    
    print("Starting calibration...")
    print("Target spacing: 2.5mm")
    print("\nFont Size | Measured Spacing (mm)")
    print("-" * 30)
    
    for size in test_sizes:
        png_path = f"calibration/test_{size}.png"
        stl_path = f"calibration/test_{size}.stl"
        
        # Generate test pattern
        text_to_png(test_text, png_path, font_size=size)
        png_to_stl(png_path, stl_path, size_scale=1.0)
        
        # Measure spacing
        spacing = measure_dot_spacing(png_path) * 1.0  # Convert to mm
        print(f"{size:^9} | {spacing:.2f}mm")

if __name__ == "__main__":
    run_calibration()
