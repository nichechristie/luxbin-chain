#!/usr/bin/env python3
"""
Jesus Loves Me sheet music data
"""

# Simplified melody representation
# Each note: (pitch, duration, lyric_syllable)

jesus_loves_me_melody = [
    # Verse 1
    ("C4", 1, "Je"),
    ("E4", 1, "sus"),
    ("G4", 1, "loves"),
    ("C4", 1, "me"),
    ("E4", 1, "this"),
    ("G4", 1, "I"),
    ("C4", 1, "know"),
    ("E4", 1, "For"),
    ("G4", 1, "the"),
    ("G4", 1, "Bi"),
    ("F4", 1, "ble"),
    ("E4", 1, "tells"),
    ("D4", 1, "me"),
    ("C4", 1, "so"),
    ("E4", 1, "Lit"),
    ("G4", 1, "tle"),
    ("C4", 1, "ones"),
    ("E4", 1, "to"),
    ("G4", 1, "Him"),
    ("C5", 1, "be"),
    ("G4", 1, "long"),
    ("E4", 1, "They"),
    ("G4", 1, "are"),
    ("F4", 1, "weak"),
    ("E4", 1, "but"),
    ("D4", 1, "He"),
    ("C4", 1, "is"),
    ("E4", 1, "strong"),
    ("G4", 1, "Yes"),
    ("C4", 1, "Je"),
    ("E4", 1, "sus"),
    ("G4", 1, "loves"),
    ("C5", 1, "me"),
    ("G4", 1, "Yes"),
    ("C4", 1, "Je"),
    ("E4", 1, "sus"),
    ("G4", 1, "loves"),
    ("C5", 1, "me"),
    ("G4", 1, "Yes"),
    ("C4", 1, "Je"),
    ("E4", 1, "sus"),
    ("G4", 1, "loves"),
    ("C5", 1, "me"),
    ("G4", 1, "The"),
    ("F4", 1, "Bi"),
    ("E4", 1, "ble"),
    ("D4", 1, "tells"),
    ("C4", 1, "me"),
    ("E4", 1, "so"),
    ("G4", 1, ""),
]

def melody_to_text(melody):
    """Convert melody to natural language text description"""
    text = ""
    for pitch, duration, lyric in melody:
        if lyric:
            text += f"{lyric} on {pitch} for {duration} beat(s), "
    return text

if __name__ == "__main__":
    text = melody_to_text(jesus_loves_me_melody)
    print("Sheet music as text:")
    print(text)