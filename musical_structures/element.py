import mido

from musical_structures.note import *


class Element(object):
    def __init__(self,
                 tie_in_front=None,
                 duration=None,
                 notes=[]):
        self.tie_in_front = tie_in_front
        self.duration = duration
        self.notes = notes

    def get_notes(self):
        pass

    def get_note(self, note):
        pass
