# from PIL import Image, ImageDraw, ImageFont

# def text_to_png(text, output_file="output.png"):
#     img_width = len(text) * 50
#     img_height = 100
#     background_color = "white"

#     image = Image.new('RGB', (img_width, img_height), background_color)
#     draw = ImageDraw.Draw(image)

#     text_color = "black"

#     try:
#         font = ImageFont.truetype("font/braille.ttf", 22)
#     except:
#         print("Error converting to Braille")

#     text_bbox = draw.textbbox((0, 0), text, font=font)
#     x = (img_width - text_bbox[2]) // 2
#     y = (img_height - text_bbox[3]) // 2

#     draw.text((x, y), text, fill=text_color, font=font)

#     image.save(output_file)
#     return output_file

# if __name__ == "__main__":
#     sample_text = "Hello World!"
#     output = text_to_png(sample_text)
#     print(f"Image saved as {output}")

from PIL import Image, ImageDraw, ImageFont

def text_to_png(text, output_file="output.png"):
    # Get text size first
    temp_img = Image.new('RGB', (1, 1), "white")
    temp_draw = ImageDraw.Draw(temp_img)
    base_font_size = 22
    font = ImageFont.truetype("font/braille.ttf", base_font_size)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    
    # Scale up for better resolution
    scale = 4 
    img_width = (text_bbox[2] + 12) * scale
    img_height = (text_bbox[3] + 12) * scale
    
    image = Image.new('RGB', (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)
    
    text_color = "black"
    
    # Scale the font to match
    font = ImageFont.truetype("font/braille.ttf", base_font_size * scale)
    x = 6 * scale
    y = 6 * scale
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    image.save(output_file)
    return output_file

if __name__ == "__main__":
    sample_text = "Hello World!"
    output = text_to_png(sample_text)
    print(f"Image saved as {output}")

