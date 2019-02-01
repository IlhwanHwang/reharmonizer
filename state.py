
class Node:
    def __init__(self):
        self.selected = False
        self.children = []
        self.identifier = None


class SingableNode(Node):
    def __init__(self, func, *args, **kwargs):
        super(SingableNode, self).__init__()
        self.descendant = None
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def apply(self):
        if isinstance(self.descendant, (list, tuple)):
            applied = [d.apply() for d in self.descendant]
        else:
            applied = self.descendant.apply()
        return self.func(*self.args, **self.kwargs)(applied)


from singable import Parallel

class PianoRollNode(SingableNode):
    def __init__(self):
        super(PianoRollNode, self).__init__(None)
        self.keys = []

    def apply(self):
        return Parallel()(self.keys)


class KeyNode(Node):
    def __init__(self, key):
        super(KeyNode, self).__init__()
        self.key = key


class state:
    singables = []


from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.Qt import QPainter

class QSingableNode(QLabel):
    def __init__(self, singable, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setStyleSheet('background-color: orange')
        self.setText(singable.identifier)
        self.setGeometry(0, 0, 100, 80)


class Form(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setFixedSize(640, 480)
        self.drawfuncs = []
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        for func in self.drawfuncs:
            func(painter)
        painter.end()


def find_node(state, identifier):
    try:
        return next((s for s in state.singables if s.identifier == identifier))
    except StopIteration:
        return None


from math import pi, cos, sin
from PyQt5.QtCore import QPoint

def draw(form, state):
    form.drawfuncs = []
    
    def group_sort(nodes):
        connections = {}
        for n in nodes:
            descendant = n.descendant
            if descendant is None:
                descendant = []
            elif isinstance(descendant, tuple):
                descendant = list(descendant)
            elif not isinstance(descendant, list):
                descendant = [descendant]
            connections[n] = descendant
        def _group_sort():
            while connections:
                out = [n for n in connections.keys() if not connections[n]]
                yield out[:]
                for n in connections.keys():
                    for m in out:
                        if m in connections[n]:
                            connections[n].remove(m)
                while out:
                    m = out.pop()
                    del connections[m]
        return list(reversed(list(_group_sort())))

    ordering = group_sort(state.singables)

    widgets = {}

    dx = 100
    for group in ordering:
        dy = 100
        for s in group:
            w = QSingableNode(s, parent=form)
            w.move(dx, dy)
            widgets[s] = w
            dy += 100
        dx += 120

    def draw_node_lines(painter):
        for s in state.singables:
            descendants = s.descendant
            if not descendants:
                continue
            if not isinstance(descendants, (list, tuple)):
                descendants = [descendants]
            for d in descendants:
                w1 = widgets[s]
                w2 = widgets[d]
                painter.drawLine(w1.pos() + QPoint(w1.width(), w1.height() / 2), w2.pos() + QPoint(0, w2.height() / 2))
    
    form.drawfuncs.append(draw_node_lines)
    form.show()

def play(target):
    from instruments.piano import acoustic_grand_piano
    from instruments.bass import synth_bass_1
    from instruments.drum_kits import standard_drum_kit
    from singable import to_midi

    song = target.apply()
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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = Form()

    from songs import crepas_song, crepas_scale
    s = PianoRollNode()
    s.keys = list(crepas_song.sing())
    s.identifier = 'melody'
    state.singables.append(s)
    
    from singable import Reharmonize
    s = SingableNode(Reharmonize, crepas_scale)
    s.identifier = 'reharmonize'
    state.singables.append(s)

    from riffs import riff1
    s = PianoRollNode()
    s.keys = list(riff1.sing())
    s.identifier = 'base riff'
    state.singables.append(s)

    from singable import Arpeggio
    s = SingableNode(Arpeggio)
    s.identifier = 'arp'
    state.singables.append(s)

    from singable import Repeat
    s = SingableNode(Repeat, 16)
    s.identifier = 'repeat'
    state.singables.append(s)

    from singable import Transpose
    from note import Interval
    s = SingableNode(Transpose, Interval('-P8'))
    s.identifier = 'transpose'
    state.singables.append(s)

    from singable import Parallel
    s = SingableNode(Parallel)
    s.identifier = 'parallel'
    state.singables.append(s)

    find_node(state, 'reharmonize').descendant = find_node(state, 'melody')
    find_node(state, 'repeat').descendant = find_node(state, 'base riff')
    find_node(state, 'arp').descendant = (find_node(state, 'reharmonize'), find_node(state, 'repeat'))
    find_node(state, 'transpose').descendant = find_node(state, 'arp')
    find_node(state, 'parallel').descendant = [find_node(state, 'melody'), find_node(state, 'transpose')]

    draw(form, state)
    # play(find_node(state, 'parallel'))

    exit(app.exec_())
