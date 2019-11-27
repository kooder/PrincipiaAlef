import midi

from track import *


class Song(object):

    def __init__(self, pattern=None, tracks=[]):
        if pattern:
            self.build_tracks(pattern)
        else:
            self.tracks = tracks

    def build_tracks(self, pattern):
        for index, raw_track in enumerate(pattern):
            track = Track(index=index,
                          instrument=None,
                          tie=None,
                          instrument_name=None,
                          order=index)
            Track.build_sections(track)
        pass

    def _get_track_metadata(self, raw_track):
        metadata = {}
        breaker = [False, False]
        for event in raw_track:
            if isinstance(event, midi.TimeSignatureEvent):
                self.numerator = event.numerator
                self.denominator = event.denominator
                self.metronome = event.metronome
                breaker[0] = True
            if isinstance(event, midi.TrackNameEvent):
                self.title = event.text
                breaker[1] = True
            # Stop looking for the metadata
            if breaker == [True, True]:
                break
        # Not all the data was found
        if breaker != [True, True]:
            data_missed = ["numerator", "denominator", "metronome", "title"]
            error_msg = "Data that was not found:\n"
            for lost_variable in data_missed:
                if self.__getattribute__(lost_variable) is None:
                    error_msg += "\t%s\n" % lost_variable
            raise Exception(error_msg)

    def get_tracks(self):
        return self.tracks

    def get_track(self, id=None, name=None):
        pass
