from PIL import Image
import sys

def remove_background(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        
        # Get pixels
        pixels = img.load()
        width, height = img.size
        
        # We'll do a simple flood fill from the corners
        # But PIL ImageDraw.floodfill replaces color. We can replace white with transparent.
        from PIL import ImageDraw
        
        # To avoid anti-aliasing artifacts, let's find all pixels connected to the corners 
        # that are close to white.
        # Actually, let's just make all nearly white pixels transparent, but 
        # let's check if there's an easier way with standard libraries.
        
        # Simple color replacement for now (with tolerance)
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                # If pixel is close to white (e.g., > 240)
                if r > 235 and g > 235 and b > 235:
                    pixels[x, y] = (255, 255, 255, 0)
        
        img.save(output_path, "PNG")
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

remove_background('images/logo_aipe.jpg.jpg', 'images/logo_aipe.png')
