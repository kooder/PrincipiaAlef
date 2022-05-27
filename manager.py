import mido
import xmltodict
import patter_policy as PATPOL
from musical_structures import song


class Manager(object):

    def __init__(self,
                 path=None,
                 pattern=None):

        self.time = None
        self.numerator = None
        self.denominator = None
        self.metronome = None
        self.title = None
        self.song = None

        if path:
            file_format = path.split(".")[-1]
            if file_format in ["mid", "midi"]:
                self.pattern = mido.MidiFile(path)
            elif file_format == "xml":
                # TODO: Would it be necessary to look for different encodings?
                with open(path, 'r', encoding='utf-8') as file:
                    my_xml = file.read()
                self.pattern = xmltodict.parse(my_xml)
            else:
                raise Exception("Format of file {} unknown." % file_format)
        elif pattern:
            self.pattern = pattern
        else:
            raise Exception("Path nor Pattern were provided.")

    def setup(self):
        """ TODO: FUNCTION IRRELEVANT, MOVE THIS TO EACH SECTION
        Get metadata from the self pattern

        The data that is saved is:
            Title
            Tick_relative
            Metronome
            First Numerator with it's Denominator
        """

        #self.length = self.pattern.length
        self.tick_relative = self.pattern.ticks_per_beat

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

    def fill_song(self):
        self.song = song.Song(self.pattern, self.pattern.tracks)
        return True
