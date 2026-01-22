#!/usr/bin/env python3
"""
Translate Jesus Loves Me from sound (sheet music) to Luxbin light wavelengths
Sound → Natural Language → Luxbin → Morse Light → Wavelengths
"""

import sys
import numpy as np
sys.path.append('luxbin-light-language')
sys.path.append('luxbin-quantum-internet')

from jesus_loves_me_sheet_music import melody_to_text, jesus_loves_me_melody
from luxbin_light_converter import LuxbinLightConverter
from luxbin_morse_light import LuxbinMorseLight, LUXBIN_TO_MORSE

def text_to_morse_luxbin(text):
    """Convert text to Luxbin Morse encoding"""
    converter = LuxbinLightConverter(enable_quantum=True)
    morse_encoder = LuxbinMorseLight()

    # Convert to Luxbin
    binary_data = text.encode('utf-8')
    luxbin_chars = converter.binary_to_luxbin_chars(binary_data)

    # Convert to Morse
    morse_sequence = ""
    for char in luxbin_chars.upper():
        if char in LUXBIN_TO_MORSE:
            morse_sequence += LUXBIN_TO_MORSE[char] + " "
        else:
            morse_sequence += " "  # Space for unknown

    return luxbin_chars, morse_sequence

def morse_to_wavelengths(morse_sequence):
    """Convert Morse sequence to light wavelengths with timing"""
    wavelengths = []
    times = []

    current_time = 0
    for char in morse_sequence:
        if char == '.':
            # Dot: short pulse at specific wavelength
            wavelengths.append(450)  # Blue for dot
            times.append((current_time, current_time + 5))
            current_time += 5 + 5  # dot + gap
        elif char == '-':
            # Dash: long pulse
            wavelengths.append(650)  # Red for dash
            times.append((current_time, current_time + 15))
            current_time += 15 + 5  # dash + gap
        elif char == ' ':
            # Character gap
            current_time += 15
        elif char == '/':
            # Word gap
            current_time += 35

    return wavelengths, times

def main():
    # Get text from sheet music
    text = melody_to_text(jesus_loves_me_melody)
    print("Natural Language from Sound:")
    print(text[:200] + "...\n")

    # Convert to Luxbin Morse
    luxbin_chars, morse = text_to_morse_luxbin(text)
    print("Luxbin Characters:")
    print(luxbin_chars[:100] + "...\n")
    print("Morse Sequence:")
    print(morse[:200] + "...\n")

    # Convert Morse to wavelengths
    wavelengths, times = morse_to_wavelengths(morse.replace(" ", "/"))  # Use / for word gaps
    print("Light Wavelengths (nm) with timing:")
    for i, wl in enumerate(wavelengths[:20]):
        start, end = times[i]
        print(f"  {start}-{end}ms: {wl}nm")
    print("...\n")

    print(f"Total pulses: {len(wavelengths)}")
    print("Error correction: Morse timing provides redundancy")

    return text, luxbin_chars, morse, wavelengths, times

if __name__ == "__main__":
    main()