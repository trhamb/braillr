from tools.text_to_png import text_to_png
from tools.png_to_stl import png_to_stl

# Convert text to braille PNG
png_file = text_to_png("Hello World!")

# Convert PNG to STL
stl_file = png_to_stl(png_file, "braille_output.stl", height_scale=5.0)
