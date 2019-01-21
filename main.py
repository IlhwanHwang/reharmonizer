from note import chord
from singable import MultiKey, Key, Enumerate, Parallel, AtChannel, Transpose, Amplify
from note import Note, Interval


song = Parallel()([
    AtChannel(0)(
        Enumerate()([
            Key(length=1, note=Note('G4')),
            Key(length=1, note=Note('G4')),
            Key(length=1/2, note=Note('E4')),
            Key(length=1/2, note=Note('F4')),
            Key(length=1, note=Note('G4')),
            Key(length=1, note=Note('A4')),
            Key(length=1, note=Note('A4')),
            Key(length=2, note=Note('G4')),
            Key(length=1, note=Note('G4')),
            Key(length=1, note=Note('C5')),
            Key(length=1, note=Note('E5')),
            Key(length=1/2, note=Note('D5')),
            Key(length=1/2, note=Note('C5')),
            Key(length=3, note=Note('D5')),
            Key(length=1, note=None),
            Key(length=1, note=Note('E5')),
            Key(length=1, note=Note('E5')),
            Key(length=1, note=Note('D5')),
            Key(length=1, note=Note('D5')),
            Key(length=1, note=Note('C5')),
            Key(length=1/2, note=Note('D5')),
            Key(length=1/2, note=Note('C5')),
            Key(length=1, note=Note('A4')),
            Key(length=1, note=Note('A4')),
            Key(length=1, note=Note('G4')),
            Key(length=1, note=Note('G4')),
            Key(length=1, note=Note('G4')),
            Key(length=1/2, note=Note('E4')),
            Key(length=1/2, note=Note('D4')),
            Key(length=3, note=Note('C4')),
            Key(length=1, note=None),
        ])
    ),
    AtChannel(1)(
        Amplify(0.75)(
            Transpose(-Interval('P8'))(
                Enumerate()([
                    # MultiKey(length=4, notes=chord('C')),
                    # MultiKey(length=2, notes=chord('F')),
                    # MultiKey(length=2, notes=chord('C')),
                    # MultiKey(length=4, notes=chord('C')),
                    # MultiKey(length=4, notes=chord('G')),
                    # MultiKey(length=2, notes=chord('C')),
                    # MultiKey(length=2, notes=chord('G7')),
                    # MultiKey(length=2, notes=chord('C')),
                    # MultiKey(length=2, notes=chord('D7')),
                    # MultiKey(length=3, notes=chord('C')),
                    # MultiKey(length=1, notes=chord('G')),
                    # MultiKey(length=4, notes=chord('C')),
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
            )
        )
    ),
])

from instruments.ensemble import string_ensemble_1
from instruments.piano import acoustic_grand_piano
from instruments.bass import synth_bass_1
from instruments.drum_kits import standard_drum_kit

from singable import to_lilypond

s = to_lilypond(song)
with open('untitled.ly', 'w') as f:
    f.write(s)

import os
os.system('lilypond untitled.ly')

# mid = to_midi(song, instruments={ 
#     0: acoustic_grand_piano,
#     1: string_ensemble_1,
#     2: synth_bass_1,
#     9: standard_drum_kit
# })
# mid.save('new_song.mid')

# import os
# import subprocess
# FNULL = open(os.devnull, 'w')
# subprocess.call(['timidity', 'new_song.mid'], stdout=FNULL, stderr=subprocess.STDOUT)

# import mido

# port = mido.open_output()
# for msg in mid.play():
#     port.send(msg)