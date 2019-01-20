from note import chord
from singable import MultiKey, Key, Enumerate, Parallel, AtChannel, Transpose, to_midi
from note import Note, Interval


song = Parallel()([
    AtChannel(0)(
        Enumerate()([
            Key(length=1, note=Note('G5')),
            Key(length=1, note=Note('G5')),
            Key(length=1/2, note=Note('E5')),
            Key(length=1/2, note=Note('F5')),
            Key(length=1, note=Note('G5')),
            Key(length=1, note=Note('A5')),
            Key(length=1, note=Note('A5')),
            Key(length=2, note=Note('G5')),
        ])
    ),
    AtChannel(1)(
        Transpose(Interval())
        Enumerate()([
            MultiKey(length=2, notes=chord('CM7')),
            MultiKey(length=2, notes=chord('Dm7')),
            MultiKey(length=2, notes=chord('G7')),
            MultiKey(length=2, notes=chord('CM7')),
            MultiKey(length=2, notes=chord('FM7')),
            MultiKey(length=2, notes=chord('D7')),
            MultiKey(length=4, notes=chord('G7')),
            MultiKey(length=2, notes=chord('Am7')),
            MultiKey(length=2, notes=chord('C7')),
            MultiKey(length=2, notes=chord('FM7')),
            MultiKey(length=2, notes=chord('A7')),
            MultiKey(length=2, notes=chord('Dm7')),
            MultiKey(length=2, notes=chord('G7')),
            MultiKey(length=4, notes=chord('C')),
        ])
    ),
])

from instruments.ensemble import string_ensemble_1
from instruments.piano import acoustic_grand_piano
from instruments.bass import synth_bass_1
from instruments.drum_kits import standard_drum_kit

mid = to_midi(song, instruments={ 
    0: acoustic_grand_piano,
    1: string_ensemble_1,
    2: synth_bass_1,
    9: standard_drum_kit
})
mid.save('new_song.mid')

import mido

port = mido.open_output()
for msg in mid.play():
    port.send(msg)