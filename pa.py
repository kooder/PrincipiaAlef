import mido
import sys
import manager
import patter_policy as PATPOL
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
meta_data = [PATPOL.METRONOME]
for data in meta_data:
    print("{}: {}".format(data.capitalize(), pa_manager.__getattribute__(data)))
print("")

#print("Title: {}").format(pa_manager.title.upper())

signature_data = [PATPOL.NUMERATOR, PATPOL.DENOMINATOR]
for data in signature_data:
    print("{}: {}".format(data.capitalize(), pa_manager.__getattribute__(data)))

notes = {}
melody = pa_manager.pattern.tracks[1]

# Try to build song
song_obj = Song()
#TODO: Recognize all tracks and being able to print a single track
current_time = 0
for note in melody:
    if note.type == PATPOL.NOTE_ON:
        if note.velocity is 0:
            print ("Note: {}, Beggining: {} End: {}".format(note.note % 12, notes[note.note], note.time))
            notes.pop(note.note)
            continue
        notes[note.note] = current_time
    elif note.type == PATPOL.NOTE_OFF:
        current_time += note.time
        print ("Note: {}, Beggining: {} End: {}".format(note.note % 12, notes[note.note], current_time))
        notes.pop(note.note)
print (melody)
if "--interactive" in sys.argv:
    code.interact(local=locals())
