import sys
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

# Fine-line character palette (Darkest to Lightest)
FINE_LINE_CHARS = [
    "M", "W", "$", "@", "B", "#", "H", "K", "X", "*", 
    "o", "a", "c", "v", "i", "l", "|", "/", "\\", "(", 
    ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", 
    "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", 
    "\"", "^", "`", "'", ".", " "
]

def prepare_image(image_path, target_width=200):
    try:
        img = Image.open(image_path).convert("L")
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

    # 1. Edge sharpening for fine outlines
    edges = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # 2. Autocontrast & contrast enhancement
    balanced = ImageOps.autocontrast(edges, cutoff=2)
    
    enhancer = ImageEnhance.Contrast(balanced)
    img = enhancer.enhance(1.3)

    # 3. Aspect Ratio Correction (~0.48 for terminal fonts)
    width, height = img.size
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio * 0.48)

    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

def image_to_ascii(image_path, target_width=200, light_theme=False):
    img = prepare_image(image_path, target_width)
    if not img:
        return None

    pixels = img.getdata()
    # Invert char order for dark editor background
    chars = FINE_LINE_CHARS if light_theme else FINE_LINE_CHARS[::-1]
    num_chars = len(chars)

    ascii_str = "".join([chars[pixel * (num_chars - 1) // 255] for pixel in pixels])
    lines = [ascii_str[i : i + target_width] for i in range(0, len(ascii_str), target_width)]
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to image: ").strip('"')

    art = image_to_ascii(image_path, target_width=200, light_theme=False)

    if art:
        with open("ascii_image.txt", "w") as f:
            f.write(art)
        print(f"\n[Success] Output for '{image_path}' saved to 'ascii_image.txt'")