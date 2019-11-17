import midi

import manager

file = "Final_Fantasy_Jona.mid"
#pattern = midi.read_midifile(file)
pa_manager = manager.Manager(file)
pa_manager.setup()
meta_data = ["format", "resolution", "tick_relative"]
for data in meta_data:
    print "{}: {}".format(data.capitalize(), pa_manager.__getattribute__(data))
print ("")
#resolution = pattern.resolution

#title = file.split(".mid")[0]
print "Title: {}".format(pa_manager.title.upper())
#signature = pattern[0][0]

signature_data = ["numerator", "denominator"]
for data in signature_data:
    print "{}: {}".format(data.capitalize(), pa_manager.__getattribute__(data))

#midi.ControlChangeEvent
notes = {}
melody = pa_manager.pattern[0]
for note in melody:
    if isinstance(note, midi.NoteOnEvent):
        if note.get_velocity() is not 0:
            notes[note.pitch] = note.tick
        else:
            print "Note: {}, Beggining: {} End: {}".format(note.pitch,notes[note.pitch],note.tick)
            notes.pop(note.pitch)
    elif isinstance(note, midi.NoteOffEvent):
        print "Note: {}, Beggining: {} End: {}".format(note.pitch, notes[note.pitch], note.tick)
        notes.pop(note.pitch)

print melody
