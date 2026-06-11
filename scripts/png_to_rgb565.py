#!/usr/bin/env python3
"""Convert PNG to RGB565 C header for ESP32 display."""

import sys
from PIL import Image
import os

def rgb888_to_rgb565(r, g, b):
    """Convert 8-bit RGB to 16-bit RGB565."""
    r5 = (r >> 3) & 0x1F
    g6 = (g >> 2) & 0x3F
    b5 = (b >> 3) & 0x1F
    return (r5 << 11) | (g6 << 5) | b5

def png_to_rgb565_header(png_path, output_header, var_name, max_width=120, max_height=120):
    """Convert PNG to RGB565 C header."""
    img = Image.open(png_path)
    
    # Convert to RGBA to handle transparency
    img = img.convert("RGBA")
    
    # Resize maintaining aspect ratio
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    width, height = img.size
    pixels = img.load()
    
    # Generate C header
    header_content = f"""#pragma once

// Logo: {os.path.basename(png_path)}
// Dimensions: {width}x{height}
// Format: RGB565 (16-bit color)

constexpr int LOGO_WIDTH = {width};
constexpr int LOGO_HEIGHT = {height};

const uint16_t {var_name}[{width * height}] = {{
"""
    
    # Convert pixels to RGB565
    data = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If transparent, use black
            if a < 128:
                rgb565 = 0x0000
            else:
                rgb565 = rgb888_to_rgb565(r, g, b)
            
            data.append(rgb565)
    
    # Write data as hex values (16 per line for readability)
    for i, val in enumerate(data):
        if i % 16 == 0:
            header_content += "    "
        header_content += f"0x{val:04X}"
        if i < len(data) - 1:
            header_content += ","
        if (i + 1) % 16 == 0:
            header_content += "\n"
    
    header_content += "\n};\n"
    
    with open(output_header, 'w') as f:
        f.write(header_content)
    
    print(f"Converted {png_path} ({width}x{height}) -> {output_header}")
    return width, height

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    png_file = os.path.join(project_root, "data", "logo.png")
    header_file = os.path.join(project_root, "include", "ui", "logo.h")
    
    if not os.path.exists(png_file):
        print(f"Error: {png_file} not found")
        sys.exit(1)
    
    width, height = png_to_rgb565_header(png_file, header_file, "LOGO_DATA", max_width=120, max_height=120)
    print(f"Success! Logo dimensions: {width}x{height}")
