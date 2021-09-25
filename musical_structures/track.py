import mido

from musical_structures.section import *


class Track(object):
    def __init__(self,
                 index=None,
                 instrument=None,
                 tie=None,
                 instrument_name=None,
                 order=None,
                 sections=[]):
        self.index = index
        self.instrument = instrument
        self.tie = tie
        self.instrument_name = instrument_name
        self.order = order
        self.sections = sections

    def build_sections_from_raw(self, pattern):
        """Get a midi.pattern and converts it to data structure"""
        tempo_changes = []
        # Each change of tempo will create a new section
        for i, event in enumerate(pattern):
            if isinstance(event, midi.TimeSignatureEvent):
                tempo_changes.append((i, event))

        tempo_changes.append((len(pattern), None))

        for i, change in enumerate(tempo_changes[:-1]):
            start = change[0]
            end = tempo_changes[i + 1]
            event = change[1]
            section = Section(index=len(self.sections),
                              name=None,
                              tempo=event.metronome,
                              numerator=event.numerator,
                              denominator=event.denominator,
                              compasses=[])
            if section.build_compasses_from_raw(pattern[start:end]):
                self.sections.append(section)
        # if any section was created, return a false
        if len(self.sections) == 0:
            return False

        return True

    def get_sections(self):
        pass

    def get_section(self, index):
        pass
