#!/usr/bin/env python3
"""
Translate a photo to Luxbin light language
Image → Binary → Luxbin → Light Wavelengths
"""

import sys
import numpy as np
from PIL import Image
sys.path.append('luxbin-light-language')

from luxbin_light_converter import LuxbinLightConverter

def load_image(image_path):
    """Load image from file"""
    img = Image.open(image_path)
    return img

def image_to_binary(img):
    """Convert image to binary data"""
    return img.tobytes()

def binary_to_luxbin(binary_data):
    """Convert binary to Luxbin characters"""
    converter = LuxbinLightConverter(enable_quantum=True)
    luxbin_chars = converter.binary_to_luxbin_chars(binary_data)
    return luxbin_chars

def luxbin_to_wavelengths(luxbin_chars):
    """Convert Luxbin to light wavelengths"""
    converter = LuxbinLightConverter()
    wavelengths = []

    for char in luxbin_chars[:100]:  # Limit for demo
        hsl = converter.char_to_hsl(char)
        # Convert hue to wavelength approximation
        wavelength = 400 + (hsl[0] / 360) * 300
        wavelengths.append(int(wavelength))

    return wavelengths

def main(image_path="/Users/nicholechristie/Downloads/a901a7b7-6fad-441a-861d-7433f8fc036c.jpg"):
    # Load photo
    img = load_image(image_path)
    print(f"Loaded image: {img.size} pixels")

    # Convert to binary
    binary_data = image_to_binary(img)
    print(f"Binary data size: {len(binary_data)} bytes")

    # Convert to Luxbin
    luxbin_chars = binary_to_luxbin(binary_data)
    print(f"Luxbin characters: {luxbin_chars[:50]}...")

    # Convert to wavelengths
    wavelengths = luxbin_to_wavelengths(luxbin_chars)
    print(f"Light wavelengths: {wavelengths[:20]}...")

    return img, binary_data, luxbin_chars, wavelengths

if __name__ == "__main__":
    main()