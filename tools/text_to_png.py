from PIL import Image, ImageDraw, ImageFont

def text_to_png(text, output_file="output.png", font_size=22):
    # Get text size first
    temp_img = Image.new('RGB', (1, 1), "white")
    temp_draw = ImageDraw.Draw(temp_img)
    font = ImageFont.truetype("font/braillr.ttf", font_size)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    
    # Scale up for better resolution
    scale = 1 
    img_width = (text_bbox[2] + 6) * scale
    img_height = (text_bbox[3] + 6) * scale
    
    image = Image.new('RGB', (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)
    
    text_color = "black"
    
    # Scale the font to match
    font = ImageFont.truetype("font/braillr.ttf", font_size * scale)
    x = 3 * scale
    y = 3 * scale
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    image.save(output_file)
    return output_file


if __name__ == "__main__":
    sample_text = "Hello World!"
    output = text_to_png(sample_text)
    print(f"Image saved as {output}")

