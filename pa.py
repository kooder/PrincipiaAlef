import midi
import sys

import manager
from musical_structures.song import *

# For interactive debugging
import code
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
#code.interact(local=locals())


file = "Do-Do.mid"

pa_manager = manager.Manager(file)
pa_manager.setup()
meta_data = ["format", "resolution", "tick_relative"]
for data in meta_data:
    print "{}: {}".format(data.capitalize(), pa_manager.__getattribute__(data))
print ("")

print "Title: {}".format(pa_manager.title.upper())

signature_data = ["numerator", "denominator"]
for data in signature_data:
    print "{}: {}".format(data.capitalize(), pa_manager.__getattribute__(data))

notes = {}
melody = pa_manager.pattern[0]

# Try to build song
song_obj = Song()

for note in melody:
    if isinstance(note, midi.NoteOnEvent):
        if note.get_velocity() is not 0:
            notes[note.pitch] = note.tick
        else:
            print "Note: {}, Beggining: {} End: {}".format(note.pitch, notes[note.pitch], note.tick)
            notes.pop(note.pitch)
    elif isinstance(note, midi.NoteOffEvent):
        print "Note: {}, Beggining: {} End: {}".format(note.pitch, notes[note.pitch], note.tick)
        notes.pop(note.pitch)
print melody
if "--interactive" in sys.argv:
    code.interact(local=locals())
