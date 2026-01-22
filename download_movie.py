#!/usr/bin/env python3
"""
Download a public domain movie for Luxbin streaming
"""

import requests
import os

def download_movie(url, filename):
    """Download movie from URL"""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded {filename}")

if __name__ == "__main__":
    # Sunrise: A Song of Two Humans (1927) - Public domain romantic drama
    movie_url = "https://archive.org/download/Sunrise_201509/Sunrise_512kb.mp4"
    movie_file = "sunrise_1927.mp4"

    if not os.path.exists(movie_file):
        try:
            download_movie(movie_url, movie_file)
        except:
            print("Download failed, using existing demo video")
            movie_file = "/Users/nicholechristie/Downloads/grok-video-a901a7b7-6fad-441a-861d-7433f8fc036c-2.mp4"
    else:
        print(f"Movie already exists: {movie_file}")

    print(f"Movie ready for Luxbin streaming: {movie_file}")