import numpy as np
import sounddevice as sd

def calculate_note_frequency(note: str) -> float:
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    semitone_positions = np.array([-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2])  # A4 is the reference (0 semitones)
    A4_freq = 440.0
    note_part = note[:-1]
    octave = int(note[-1])
    if note_part not in note_names:
        raise ValueError("Invalid note name provided. Please provide a note like 'A4' or 'C#3'.")
    semitone_shift = semitone_positions[note_names.index(note_part)] + (octave - 4) * 12
    frequency = A4_freq * (2 ** (semitone_shift / 12.0))
    return round(frequency, 2)

def play_note_frequency(frequency, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, sample_rate)
    sd.wait()  # Wait until the sound has finished playing

example_note = "C4"
frequency = calculate_note_frequency(example_note)
print(f"The frequency of {example_note} is {frequency} Hz")
play_note_frequency(frequency)
