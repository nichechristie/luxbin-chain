#!/usr/bin/env python3
"""
Translate a video to Luxbin light language
Video → Frames → Binary → Luxbin → Light Wavelengths
"""

import sys
import numpy as np
from PIL import Image
import cv2
sys.path.append('luxbin-light-language')

from luxbin_light_converter import LuxbinLightConverter

def load_video_frames(video_path, max_frames=10):
    """Load video and extract frames"""
    cap = cv2.VideoCapture(video_path)
    video_frames = []
    frame_count = 0

    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        video_frames.append(img)
        frame_count += 1

    cap.release()
    return video_frames

def video_to_binary(video_frames):
    """Convert video frames to binary data"""
    binary_data = b""
    for frame in video_frames:
        binary_data += frame.tobytes()
    return binary_data

def binary_to_luxbin(binary_data):
    """Convert binary to Luxbin characters"""
    converter = LuxbinLightConverter(enable_quantum=True)
    luxbin_chars = converter.binary_to_luxbin_chars(binary_data)
    return luxbin_chars

def luxbin_to_wavelengths(luxbin_chars):
    """Convert Luxbin to light wavelengths"""
    converter = LuxbinLightConverter()
    wavelengths = []

    for char in luxbin_chars[:200]:  # Limit for demo
        hsl = converter.char_to_hsl(char)
        # Convert hue to wavelength approximation
        wavelength = 400 + (hsl[0] / 360) * 300
        wavelengths.append(int(wavelength))

    return wavelengths

def main(video_path="/Users/nicholechristie/Downloads/grok-video-a901a7b7-6fad-441a-861d-7433f8fc036c-2.mp4"):
    # Load video frames
    video_frames = load_video_frames(video_path, max_frames=10)
    print(f"Loaded video with {len(video_frames)} frames")

    # Convert to binary
    binary_data = video_to_binary(video_frames)
    print(f"Binary data size: {len(binary_data)} bytes")

    # Convert to Luxbin
    luxbin_chars = binary_to_luxbin(binary_data)
    print(f"Luxbin characters: {luxbin_chars[:50]}...")

    # Convert to wavelengths
    wavelengths = luxbin_to_wavelengths(luxbin_chars)
    print(f"Light wavelengths: {wavelengths[:20]}...")

    return video_frames, binary_data, luxbin_chars, wavelengths

if __name__ == "__main__":
    main()