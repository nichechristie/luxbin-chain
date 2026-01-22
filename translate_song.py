#!/usr/bin/env python3
"""
Translate "Jesus Loves Me" song to Luxbin light language
"""

import sys
import os
sys.path.append('luxbin-light-language')

from luxbin_light_converter import LuxbinLightConverter

# Song lyrics
lyrics = """
Jesus loves me, this I know,
For the Bible tells me so;
Little ones to Him belong;
They are weak, but He is strong.

Yes, Jesus loves me,
Yes, Jesus loves me,
Yes, Jesus loves me,
The Bible tells me so.
"""

def main():
    converter = LuxbinLightConverter(enable_quantum=True)
    
    # Convert text to binary
    binary_data = lyrics.encode('utf-8')
    
    # Convert to Luxbin characters
    luxbin_chars = converter.binary_to_luxbin_chars(binary_data)
    print("Luxbin Characters:")
    print(luxbin_chars)
    
    # Analyze grammar (simple)
    grammar_analysis = converter.analyze_grammar(lyrics)
    
    # Convert to HSL colors
    colors = []
    for i, char in enumerate(luxbin_chars):
        if i < len(grammar_analysis):
            grammar_type = grammar_analysis[i][1]
        else:
            grammar_type = 'default'
        hsl = converter.char_to_hsl(char, grammar_type)
        colors.append(hsl)
    
    print("\nHSL Colors (Light Wavelengths):")
    for i, hsl in enumerate(colors):
        print(f"Char {luxbin_chars[i]}: Hue={hsl[0]}°, Sat={hsl[1]}%, Light={hsl[2]}%")
    
    # Convert HSL to approximate wavelengths (nm)
    wavelengths = []
    for hsl in colors:
        # Approximate wavelength from hue (rough mapping)
        wavelength = 400 + (hsl[0] / 360) * 300  # 400-700nm visible spectrum
        wavelengths.append(round(wavelength))
    
    print("\nApproximate Wavelengths (nm):")
    print(wavelengths)
    
    return luxbin_chars, colors, wavelengths

if __name__ == "__main__":
    main()