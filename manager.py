import mido
import patter_policy as PATPOL


class Manager(object):

    def __init__(self,
                 path=None,
                 pattern=None):
        if path:
            self.pattern = mido.MidiFile(path)
        elif pattern:
            self.pattern = pattern
        else:
            raise Exception("Path nor Pattern were provided.")

    def setup(self):
        """ Get metadata from the self pattern

        The data that is saved is:
            Title
            Tick_relative
            Metronome
            First Numerator with it's Denominator
        """

        self.length = self.pattern.length
        self.tick_relative = self.pattern.ticks_per_beat

        self.numerator = None
        self.denominator = None
        self.metronome = None
        self.title = None

        #self.title = self.pattern
        breaker = False
        for track in self.pattern.tracks:
            if breaker:
                break
            for event in track:
                if event.is_meta:
                    if event.type == PATPOL.TIME_SIGNATURE:
                        self.numerator = event.numerator
                        self.denominator = event.denominator
                        self.metronome = event.notated_32nd_notes_per_beat
                        # Stop looking for the metadata
                        breaker = True
                        break
        # Not all the data was found
        if not breaker:
            data_requested = [PATPOL.NUMERATOR, PATPOL.DENOMINATOR, PATPOL.METRONOME, PATPOL.TITLE]
            error_msg = "Data that was not found:\n"
            for lost_variable in data_requested:
                if self.__getattribute__(lost_variable) is None:
                    error_msg += "\t%s\n" % lost_variable
            raise Exception(error_msg)
