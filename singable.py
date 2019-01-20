from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from math import floor
from note import Note


class Singable:
    def messages(self):
        raise NotImplementedError


class Key(Singable):
    def __init__(self, start=0, length=0, note=None, channel=0, velocity=0.75):
        self.start = start
        self.length = length
        self.note = note
        self.channel = channel
        self.velocity = velocity

    def replace(self, start=None, length=None, note=None, channel=None, velocity=None):
        return Key(
            start=self.start if start is None else start, 
            length=self.length if length is None else length, 
            channel=self.channel if channel is None else channel, 
            note=self.note if note is None else note, 
            velocity=self.velocity if velocity is None else velocity, 
        )

    def sing(self):
        yield self


def MultiKey(start=0, length=0, notes=None, channel=0, velocity=0.75):
    return [Key(start=start, length=length, note=note, channel=channel, velocity=velocity) for note in notes]


def parameter_graphmaker(cls):
    def _graphmaker(*arg, **kwargs):
        def _singablemaker(x):
            return cls(x, *arg, **kwargs)
        return _singablemaker
    return _graphmaker


class _Parallel(Singable):
    def __init__(self, children):
        self.children = children

    def sing(self):
        for c in self.children:
            for mm in c.sing():
                yield mm


class _Enumerate(Singable):
    def __init__(self, children, interval=None):
        self.children = children
        self.interval = interval

    def sing(self):
        time = 0
        for cl in self.children:
            time_max = 0
            if not isinstance(cl, (list, tuple)):
                cl = [cl]
            for c in cl:
                for mm in ShiftTime(time)(c).sing():
                    time_max = max(mm.start + mm.length, time_max)
                    yield mm
            if self.interval:
                time += self.interval
            else:
                time = time_max


class _Repeat(Singable):
    def __init__(self, child, repeat_num, interval=None):
        self.child = child
        self.repeat_num = repeat_num
        self.interval = interval

    def sing(self):
        time = 0
        time_max = 0
        for _ in range(self.repeat_num):
            for key in ShiftTime(time)(self.child).sing():
                time_max = max(key.start + key.length, time_max)
                yield key
            if self.interval:
                time += self.interval
            else:
                time = time_max



class _SelectTime(Singable):
    def __init__(self, child, start, length, func):
        self.child = child
        self.start = start
        self.length = length
        self.func = func

    def sing(self):
        for key in self.child.sing():
            if key.start >= self.start and key.start < self.start + self.length:
                for k in self.func(key).sing():
                    yield k
            else:
                yield key


class _SelectInterval(Singable):
    def __init__(self, child, interval, funcs, outliers='loop'):
        self.child = child
        self.interval = interval
        self.funcs = funcs
        self.outliers = outliers

    def sing(self):
        for key in self.child.sing():
            ind = key.start // self.interval
            if ind < 0 or ind >= len(self.funcs):
                if self.outliers == 'loop':
                    ind = ind - floor(ind / len(self.funcs)) * len(self.funcs)
                elif self.outliers == 'clip':
                    ind = min(len(self.funcs) - 1, max(0, ind))
                elif self.outliers == 'none' or self.outliers is None:
                    continue
            for k in self.funcs[ind](key).sing():
                yield k


class _SelectIndex(Singable):
    def __init__(self, child, istart, ilength, func):
        self.child = child
        self.istart = istart
        self.ilength = ilength
        self.func = func

    def sing(self):
        for i, key in enumerate(self.child.sing()):
            if i >= self.istart and i < self.istart + self.ilength:
                for k in self.func(key).sing():
                    yield k
            else:
                yield key


class _ShiftTime(Singable):
    def __init__(self, child, time):
        self.child = child
        self.time = time

    def sing(self):
        for key in self.child.sing():
            yield key.replace(start=key.start + self.time)


class _Lengthen(Singable):
    def __init__(self, child, scale):
        self.child = child
        self.scale = scale

    def sing(self):
        for key in self.child.sing():
            yield key.replace(start=max(0, key.length * self.scale))


class _Longify(Singable):
    def __init__(self, child, time):
        self.child = child
        self.time = time

    def sing(self):
        for key in self.child.sing():
            yield key.replace(start=max(0, key.length + self.time))


class _Amplify(Singable):
    def __init__(self, child, magnitude):
        self.child = child
        self.magnitude = magnitude

    def sing(self):
        for key in self.child.sing():
            yield key.replace(velocity=key.velocity * self.magnitude)


class _Transpose(Singable):
    def __init__(self, child, transpose):
        self.child = child
        self.transpose = transpose

    def sing(self):
        for key in self.child.sing():
            yield key.replace(note=key.note + self.transpose)


# class _CloseVoice(Singable):
#     def __init__(self, child, olow, ohigh):
#         self.child = child
#         self.ohigh = ohigh
#         self.olow = olow

#     def sing(self):
#         for key in self.child.sing():
#             octave = key.note.tone // 7
#             tdiff = 0
#             ointerval = self.ohigh - self.olow
#             while octave >= self.ohigh:
#                 octave -= ointerval
#                 tdiff -= 7 * ointerval
#             while octave < self.olow:
#                 octave += ointerval
#                 tdiff += 7 * ointerval
#             yield key.replace(note=key.note + tdiff)


class _Harmonize(Singable):
    def __init__(self, child, transpose):
        self.child = child
        self.transpose = transpose

    def sing(self):
        for key1, key2 in zip(self.child.sing(), Transpose(self.transpose)(self.child).sing()):
            yield key1
            yield key2


class _Swing(Singable):
    def __init__(self, child, interval, rate):
        self.child = child
        self.interval = interval
        self.rate = rate

    def sing(self):
        for key in self.child.sing():
            def _swing_time(time):
                index = floor(time / self.interval)
                frac = (time / self.interval - index)
                if frac < 0.5:
                    frac = frac / 0.5 * self.rate
                else:
                    frac = 1 - ((1 - frac) / 0.5 * (1 - self.rate))
                return (index + frac) * self.interval
            time_start = _swing_time(key.start)
            time_end = _swing_time(key.start + key.length)
            yield key.replace(start=time_start, length=(time_end - time_start))


class _AtChannel(Singable):
    def __init__(self, child, channel):
        self.child = child
        self.channel = channel

    def sing(self):
        for key in self.child.sing():
            yield key.replace(channel=self.channel)


class _AtNote(Singable):
    def __init__(self, child, note):
        self.child = child
        self.note = note

    def sing(self):
        for key in self.child.sing():
            yield key.replace(note=self.note)


# class _Arpeggio(Singable):
#     # outliers can be 'loop', 'octave', 'clip'
#     def __init__(self, chord_and_pattern, outliers='loop'):
#         self.chord, self.pattern = chord_and_pattern
#         self.outliers = outliers

#     def sing(self):
#         key_chord = list(self.chord.sing())
#         for arp_key in self.pattern.sing():
#             time = arp_key.start
#             keys_at_time = [key for key in key_chord if key.start <= time and key.start + key.length > time]
            
#             if self.outliers == 'loop':
#                 ind = arp_key.note.tone
#                 ind = int(ind - floor(ind / len(keys_at_time)) * len(keys_at_time))
#                 target_key = keys_at_time[ind]
            
#             elif self.outliers == 'octave':
#                 ind = arp_key.note.tone
#                 octave = floor(ind / len(keys_at_time))
#                 target_key = keys_at_time[ind]
#                 target_key = target_key.replace(note=target_key.note.add_octave(octave))

#             elif self.outliers == 'clip':
#                 ind = max(0, min(len(keys_at_time), arp_key.note.tone))
#                 target_key = keys_at_time[ind]

#             yield target_key.replace(
#                 velocity=(target_key.velocity * arp_key.velocity), 
#                 start=arp_key.start,
#                 length=arp_key.length,
#                 channel=arp_key.channel
#             )

Parallel = parameter_graphmaker(_Parallel)
Enumerate = parameter_graphmaker(_Enumerate)
Repeat = parameter_graphmaker(_Repeat)
SelectTime = parameter_graphmaker(_SelectTime)
SelectInterval = parameter_graphmaker(_SelectInterval)
SelectIndex = parameter_graphmaker(_SelectIndex)
ShiftTime = parameter_graphmaker(_ShiftTime)
Lengthen = parameter_graphmaker(_Lengthen)
Longify = parameter_graphmaker(_Longify)
Amplify = parameter_graphmaker(_Amplify)
Transpose = parameter_graphmaker(_Transpose)
# Bound = parameter_graphmaker(_Bound)
Harmonize = parameter_graphmaker(_Harmonize)
Swing = parameter_graphmaker(_Swing)
AtChannel = parameter_graphmaker(_AtChannel)
AtNote = parameter_graphmaker(_AtNote)
# Arpeggio = parameter_graphmaker(_Arpeggio)


# def BoundOffset(olow, ohigh, toffset):
#     def _BoundOffset(child):
#         return Transpose(-toffset)(
#             Bound(olow, ohigh)(
#                 Transpose(toffset)(child)
#             )
#         )
#     return _BoundOffset


def to_midi(
    singable, velocity_max=127, tick_per_beat=480, instruments=None,
    initial_bpm=144
    ):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    messages = []
    for key in singable.sing():
        channel = key.channel

        velocity = int(key.velocity * velocity_max)
        time_start = int(key.start * tick_per_beat)
        time_end = int((key.start + key.length) * tick_per_beat)
        
        messages.append(Message('note_on', note=key.note.midi_number(), velocity=velocity, time=time_start, channel=channel))
        messages.append(Message('note_off', note=key.note.midi_number(), velocity=velocity, time=time_end, channel=channel))
    
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(initial_bpm)))

    for channel, program in instruments.items():
        track.append(Message('program_change', channel=channel, program=program))

    time_prev = 0
    messages = sorted(messages, key=lambda x: x.time)
    for msg in messages:
        msg_timed = msg.copy(time=msg.time - time_prev)
        time_prev = msg.time
        track.append(msg_timed)
    
    return mid

