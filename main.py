from note import chord
from singable import MultiKey, Key, Enumerate, Parallel, AtChannel, Transpose, Amplify, Arpeggio, Repeat
from note import Note, Interval, Scale
from reharmonize import reharmonize


song = Enumerate()([
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

# song = Enumerate()([
#     Key(length=1, note=Note('C4')),
#     Key(length=1, note=Note('C4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=2, note=Note('G4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=2, note=Note('C4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=2, note=Note('D4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=2, note=Note('D4')),
#     Key(length=1, note=Note('C4')),
#     Key(length=1, note=Note('C4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=2, note=Note('G4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('F4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=2, note=Note('C4')),
# ])


# song = Enumerate()([
#     Key(length=1, note=Note('E4')),
#     Key(length=1/2, note=Note('C4')),
#     Key(length=1/2, note=Note('D4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=2, note=Note('D4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1/2, note=Note('C4')),
#     Key(length=1/2, note=Note('D4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=2, note=Note('A4')),
#     Key(length=2, note=Note('C5')),
#     Key(length=2, note=Note('B4')),
#     Key(length=2, note=Note('A4')),
#     Key(length=2, note=Note('G4')),
#     Key(length=2, note=Note('C5')),
#     Key(length=2, note=Note('B4')),
#     Key(length=2, note=Note('A4')),
#     Key(length=2, note=Note('G4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1/2, note=Note('C4')),
#     Key(length=1/2, note=Note('D4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=1, note=Note('D4')),
#     Key(length=2, note=Note('D4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1/2, note=Note('C4')),
#     Key(length=1/2, note=Note('D4')),
#     Key(length=1, note=Note('E4')),
#     Key(length=1, note=Note('G4')),
#     Key(length=1, note=Note('A4')),
#     Key(length=1, note=Note('B4')),
#     Key(length=2, note=Note('C5')),
# ])


progression = reharmonize(song, Scale(tonic=Note('C5'), quality='major'))

song = Parallel()([
    AtChannel(0)(song),
    AtChannel(1)(
        Arpeggio()(
            (
                Transpose(Interval('-P15'))(progression),
                Repeat(8)(
                    Enumerate()([
                        Key(length=1/2, note=Note('C4')),
                        Key(length=1/2, note=Note('C##4')),
                        Key(length=1/2, note=Note('C#4')),
                        Key(length=1/2, note=Note('C##4')),
                        Key(length=1/2, note=Note('C4')),
                        Key(length=1/2, note=Note('C##4')),
                        Key(length=1/2, note=Note('C#4')),
                        Key(length=1/2, note=Note('C##4')),
                    ])
                )
            )
        )
    )
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

from singable import to_midi

mid = to_midi(song, instruments={ 
    0: acoustic_grand_piano,
    1: acoustic_grand_piano,
    2: synth_bass_1,
    9: standard_drum_kit
})
mid.save('new_song.mid')

import os
import subprocess
FNULL = open(os.devnull, 'w')
subprocess.call(['timidity', 'new_song.mid'], stdout=FNULL, stderr=subprocess.STDOUT)

# import mido

# port = mido.open_output()
# for msg in mid.play():
#     port.send(msg)