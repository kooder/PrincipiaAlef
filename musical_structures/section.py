import mido

from musical_structures.compass import *


class Section(object):
    def __init__(self,
                 index=None,
                 name=None,
                 tempo=None,
                 numerator=None,
                 denominator=None,
                 compasses=[]):
        self.index = id
        self.name = name
        self.tempo = tempo
        self.numerator = numerator
        self.denominator = denominator
        self.compasses = compasses

    def build_compasses_from_raw(self, pattern):
        pass

    def get_compasses(self):
        pass

    def get_compass(self, index):
        pass
