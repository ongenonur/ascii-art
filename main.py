import os
import sys
from PIL import Image, ImageEnhance

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrftj1?-_+~<>i!lI;:,\"^`'. "


def scale_image(image, new_width=140):
    (original_width, original_height) = image.size
    # 0.52 factor precisely balances standard font character dimensions (2:1 height:width ratio)
    aspect_ratio = original_height / float(original_width) * 0.72
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def enhance_image(image, contrast_factor=1.2, brightness_factor=1.15):
    # Gentler enhancement so shadows and background details aren't crushed to pure black
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)
    return image


def convert_to_ascii_html(image_path, output_path, width=140):
    raw_img = Image.open(image_path).convert("RGB")
    enhanced_img = enhance_image(raw_img, contrast_factor=1.2, brightness_factor=1.15)
    img = scale_image(enhanced_img, new_width=width)

    pixels = img.getdata()
    num_chars = len(ASCII_CHARS) - 1

    html_content = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>ASCII Art</title>",
        "<style>",
        "  body {",
        "    background-color: #0d0d0d;",
        "    display: flex;",
        "    justify-content: center;",
        "    align-items: center;",
        "    min-height: 100vh;",
        "    margin: 0;",
        "    padding: 20px;",
        "  }",
        "  pre {",
        "    font-family: 'Courier New', Courier, monospace;",
        "    font-size: 8px;",
        "    line-height: 0.82;",     # Locks line spacing to character width
        "    letter-spacing: 0px;",
        "    white-space: pre;",
        "    font-weight: bold;",
        "  }",
        "</style>",
        "</head>",
        "<body>",
        "<pre>",
    ]

    current_line = []
    for i, pixel in enumerate(pixels):
        r, g, b = pixel
        
        # Perceptual luminance calculation
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        char_index = int(luminance * num_chars)
        char = ASCII_CHARS[min(char_index, num_chars)]

        current_line.append(f'<span style="color: rgb({r},{g},{b});">{char}</span>')

        if (i + 1) % img.width == 0:
            html_content.append("".join(current_line))
            current_line = []

    html_content.extend(["</pre>", "</body>", "</html>"])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

    print(f"\nSaved proportioned ASCII art to: {output_path}")


if __name__ == "__main__":
    user_file = input("Enter image filename (e.g., test or test2.jpg): ").strip()

    if not user_file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        user_file += ".jpg"

    output_html_path = f"{os.path.splitext(user_file)[0]}_ascii.html"

    if os.path.exists(user_file):
        convert_to_ascii_html(user_file, output_html_path, width=140)
    else:
        print(f"Error: Could not find '{user_file}' in {os.getcwd()}")