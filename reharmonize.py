from note import Note, Interval, Scale

def _get_melody_weight(melody):
    return [key.length for key in melody]


from collections import defaultdict
from math import floor

class ChordNode:
    def __init__(self, number, value, start, length):
        self.value = value
        self.total_value = None
        self.start = start
        self.length = length
        self.number = number
        self.prevs = []
        self.target = None
    
    def actual_value(self):
        return (self.length ** 1.1) * self.value


class ChordDag:
    def __init__(self):
        self.nodes = []

    def add_node(self, number, value, start, length):
        self.nodes.append(ChordNode(number, value, start, length))
    
    def _build_edge(self):
        for n in self.nodes:
            n.prev = []

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
        
        nodes_at_ending = defaultdict(list)
        for n in self.nodes:
            nodes_at_ending[n.start + n.length].append(n)
        
        for n in self.nodes:
            for m in nodes_at_ending[n.start]:
                if m.number in inv_transitions[n.number]:
                    n.prev.append(m)

    def solve(self):
        self._build_edge()
        topological_nodes = sorted(self.nodes, key=lambda n: n.start)

        for n in topological_nodes:
            if n.prev:
                m = max(n.prev, key=lambda m: m.total_value)
                n.total_value = m.total_value + n.actual_value()
                n.target = m
            else:
                n.total_value = 0
        
        timing_max = max([n.start + n.length for n in self.nodes])
        endnodes = [n for n in self.nodes if n.start + n.length == timing_max]
        endnode = max(endnodes, key=lambda n: n.total_value)
        result = []
        node = endnode
        while node:
            result.insert(0, node)
            node = node.target
        
        return result


def _song_to_chord(song, scale, granularity=(1, 2, 4), 
                   offset=0, cadence_at=16, cadence_score=1):

    melody = list(song.sing())

    def _slice_melody(melody, start, length):
        end = start + length
        for k in melody:
            k_end = k.start + k.length
            if k.start >= start and k_end <= end:
                yield k
            elif k.start >= start and k.start < end and k_end > end:
                yield k.replace(length=start + length - k.start)
            elif k.start < start and k_end > start and k_end <= end:
                yield k.replace(start=start, length=k.start + k.length - start)
            else:
                pass
    
    time_max = int(max([k.start + k.length for k in melody]))
    dag = ChordDag()
    numbers = scale.possible_numbers()

    for g in granularity:
        timing = offset
        while timing < time_max:
            part = list(_slice_melody(melody, timing, g))
            for k in part:
                if k.length > g:
                    print("?????")
            weight = _get_melody_weight(part)
            scores = []
            for number in numbers:
                score = scale.score_melody(part, number, weight)
                if (timing + g - offset) % cadence_at == 0:
                    if number not in scale.possible_cadences():
                        score -= cadence_score
                scores.append((number, score))
            for number, score in scores:
                dag.add_node(number, score, timing, g)
            timing += g
    
    return dag.solve()


from singable import MultiKey, Enumerate


def reharmonize(song, scale, granularity=(1, 2, 4)):
    nodes = _song_to_chord(song, scale, granularity=granularity)
    progression = []
    for n in nodes:
        c = scale.diatonic(n.number)
        progression.append(MultiKey(notes=c, length=n.length))
    return Enumerate()(progression)
