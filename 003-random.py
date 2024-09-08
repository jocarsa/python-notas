import numpy as np
import sounddevice as sd
import random

# Existing functions
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

# New functions
def generate_scale(starting_note: str, scale_type: str = "major") -> list:
    major_intervals = [2, 2, 1, 2, 2, 2, 1]
    minor_intervals = [2, 1, 2, 2, 1, 2, 2]
    
    if scale_type.lower() == "major":
        intervals = major_intervals
    elif scale_type.lower() == "minor":
        intervals = minor_intervals
    else:
        raise ValueError("Unsupported scale type. Use 'major' or 'minor'.")

    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    starting_note_name = starting_note[:-1]
    octave = int(starting_note[-1])

    if starting_note_name not in note_names:
        raise ValueError("Invalid starting note.")

    scale = [starting_note]
    index = note_names.index(starting_note_name)

    for interval in intervals:
        index = (index + interval) % len(note_names)
        if index < note_names.index(scale[-1][:-1]):
            octave += 1
        scale.append(note_names[index] + str(octave))

    return scale

def select_random_note_in_scale(scale: list, octave_range: int, starting_note: str):
    starting_octave = int(starting_note[-1])
    possible_notes = []

    for octave_shift in range(-octave_range, octave_range + 1):
        for note in scale:
            note_name = note[:-1]
            note_octave = starting_octave + octave_shift
            possible_notes.append(note_name + str(note_octave))

    return random.choice(possible_notes)

def play_random_notes(starting_note: str, scale_type: str = "major", octave_range: int = 1, tempo: int = 120, num_notes: int = 10):
    scale = generate_scale(starting_note, scale_type)
    quarter_note_duration = 60 / tempo  # Duration of a quarter note in seconds
    note_durations = [quarter_note_duration * 4,  # Whole note
                      quarter_note_duration * 2,  # Half note
                      quarter_note_duration,      # Quarter note
                      quarter_note_duration / 2,  # Eighth note
                      quarter_note_duration / 4]  # Sixteenth note

    for _ in range(num_notes):
        selected_note = select_random_note_in_scale(scale, octave_range, starting_note)
        frequency = calculate_note_frequency(selected_note)
        duration = random.choice(note_durations)
        print(f"Playing {selected_note} at {frequency} Hz for {duration} seconds")
        play_note_frequency(frequency, duration)

# Example usage
starting_note = "C5"
play_random_notes(starting_note, scale_type="major", octave_range=0.2, tempo=120, num_notes=50)
