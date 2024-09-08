import numpy as np

def calculate_note_frequency(note: str) -> float:
    """
    Calculate the frequency of a given musical note.

    :param note: The musical note in the format "NoteOctave" (e.g., "A4", "C#3").
    :return: The frequency of the note in Hz.
    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    semitone_positions = np.array([-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2])  # A4 is the reference (0 semitones)
    A4_freq = 440.0

    # Extract the note and the octave from the input
    note_part = note[:-1]
    octave = int(note[-1])

    if note_part not in note_names:
        raise ValueError("Invalid note name provided. Please provide a note like 'A4' or 'C#3'.")

    # Calculate the semitone shift from A4
    semitone_shift = semitone_positions[note_names.index(note_part)] + (octave - 4) * 12
    
    # Calculate the frequency
    frequency = A4_freq * (2 ** (semitone_shift / 12.0))
    
    return round(frequency, 2)

# Example usage
example_note = "C4"
calculated_frequency = calculate_note_frequency(example_note)
print(calculated_frequency)  # Output: 261.63
