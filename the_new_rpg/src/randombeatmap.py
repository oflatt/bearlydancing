from Beatmap import Beatmap
from Note import  Note

def random_beatmaps():
    return [Beatmap(1000, [Note(1, 1, 1), Note(2, 2, 1), Note(8, 2, 3), Note(6, 3, 0.5)]),
            Beatmap(1000, [Note(1, 1, 1), Note(2, 2, 1), Note(8, 2, 3), Note(6, 5, 0.5)])]
