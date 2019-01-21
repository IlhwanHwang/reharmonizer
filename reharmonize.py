from note import Note, Interval, Scale

def _get_melody_weight(melody):
    return [key.length for key in melody]


from collections import defaultdict
from math import floor

def _song_to_chord(song, scale, granularity=2):
    keys = list(song.sing())
    time_max = max([x.start + x.length for x in keys])
    melodies = defaultdict(list)
    for key in keys:
        time = floor(key.start / granularity) * granularity
        melodies[time].append(key)

    numbers = [1, 4, 5]
    transitions = {
        1: [1, 4, 5],
        4: [1, 4, 5],
        5: [1, 4, 5],
        None: [1]
    }

    current_number = None
    chords = []

    for time in range(0, time_max, granularity):
        melody = melodies[time]
        if not melody:
            next_number = current_number
        else:
            valid_numbers = transitions[current_number]
            weight = _get_melody_weight(melody)
            scores = [scale.score_melody(melody, n, weight=weight) for n in valid_numbers]
            next_number = max(zip(valid_numbers, scores), key=lambda x: x[1])[0]
        chords.append(next_number)

        
        
    


def reharmonize(song, scale):