import midi


class Manager(object):

    def __init__(self,
                 path=None,
                 pattern=None):
        if path:
            self.pattern = midi.read_midifile(path)
        elif pattern:
            self.pattern = pattern
        else:
            raise Exception("Path nor Pattern were provided.")

    def setup(self):
        """ Get metadata from the self pattern

        The data that is saved is:
            Title
            Format
            Resolution
            Tick_relative
            Metronome
            First Numerator with it's Denominator
        """

        self.format = self.pattern.format
        self.resolution = self.pattern.resolution
        self.tick_relative = self.pattern.tick_relative

        self.numerator = None
        self.denominator = None
        self.metronome = None
        self.title = None

        breaker = [False, False]
        for track in self.pattern:
            for event in track:
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
            raise  Exception(error_msg)

