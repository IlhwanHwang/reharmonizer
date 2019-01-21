from note import Note, Interval, Scale

def _get_melody_weight(melody):
    return [key.length for key in melody]


from collections import defaultdict
from math import floor

def _song_to_chord(song, scale, granularity=2):
    keys = list(song.sing())
    time_max = int(max([x.start + x.length for x in keys]))
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
        current_number = next_number
        chords.append(current_number)

    return chords


from singable import MultiKey, Enumerate


def reharmonize(song, scale, granularity=2):
    chords = _song_to_chord(song, scale, granularity=granularity)
    progression = []
    for number in chords:
        c = scale.diatonic(number)
        progression.append(MultiKey(notes=c, length=granularity))
    return Enumerate()(progression)
