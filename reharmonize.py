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

    numbers = [1, 2, 3, 4, 5, 6]
    scores = []

    for time in range(0, time_max, granularity):
        melody = melodies[time]
        weight = _get_melody_weight(melody)
        scores.append({ number: scale.score_melody(melody, number, weight=weight) for number in numbers })
    
    transitions = {
        1: [1, 3, 6, 2, 4, 5],
        2: [2, 3, 5],
        3: [3, 6, 2, 4],
        4: [4, 1, 3, 2, 5],
        5: [5, 1, 3, 6],
        6: [6, 3, 2, 4]
    }
    inv_transitions = { number: [] for number in transitions.keys() }
    for src, dests in transitions.items():
        for dest in dests:
            inv_transitions[dest].append(src)
    
    dag = [{ 1: (0, None) }]
    for score in scores[1:]:
        prev = dag[-1]
        current = {}
        for number in inv_transitions.keys():
            target, (value, _) = max(filter(lambda x: x[0] in inv_transitions[number], prev.items()), key=lambda x: x[1][0])
            current[number] = (value + score[number], target)
        dag.append(current)
    
    chords = [max(dag[-1].items(), key=lambda x: x[1][0])[0]]
    for current in reversed(dag[1:]):
        prev = chords[0]
        chords.insert(0, current[prev][1])

    return chords


from singable import MultiKey, Enumerate


def reharmonize(song, scale, granularity=2):
    chords = _song_to_chord(song, scale, granularity=granularity)
    progression = []
    for number in chords:
        c = scale.diatonic(number)
        progression.append(MultiKey(notes=c, length=granularity))
    return Enumerate()(progression)
