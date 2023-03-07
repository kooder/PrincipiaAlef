import xmltodict
import tkinter as tk
import tkinter.messagebox as msg
import xml.etree.ElementTree as ET
from xml.dom import minidom
from copy import deepcopy
from _collections import OrderedDict
import re
from tkinter.filedialog import askopenfilename

lyric = {#"@number": "1",
         "@default-x": "6.50",
         "@default-y": "-46.31",
         "@relative-y": "-30.00",
         "syllabic": "single",
         "text": None
         }
lyric_str = '<lyric default-x="6.50" default-y="-46.31" relative-y="-30.00">' \
            '<syllabic>single</syllabic><text>10</text></lyric>'
translate = {"C": 0,"D": 2,"E": 4,"F": 5,"G": 7,"A": 9,"B": 11}
#path = "D:/wamp64/www/PrincipiaAlef/Test_cases_v2/Chords_with_both_hands.musicxml"
path = ""

def load_UI(root):
    root.geometry("300x100")
    root.title("Account Overview")
    select_label = tk.Label(root, text="Select a musicxml file")
    load_button = tk.Button(root, text='Load', command=get_name)
    add_subt_button = tk.Button(root, text='Make Subtitled file', command=add_subtitles)
    select_label.grid(row=0, column=0)
    load_button.grid(row=1, column=0)
    add_subt_button.grid(row=1, column=1)


def get_name():
    global path
    path = askopenfilename()
    extension = path.split(".")[-1]
    if path == "":
        return
    if extension != "musicxml":
        msg.showerror(title="Wrong File extension", message="This program only accepts musicxml files.")

"""
def add_subtitles():
    if path == "":
        msg.showwarning(title="No file loaded", message="Please load a proper musicxml file.")
        return
    xml = None
    with open(path, 'r', encoding='utf-8') as file:
        xml = file.read()
    score = xmltodict.parse(xml, dict_constructor=OrderedDict)
    parts = score["score-partwise"]["part"]
    #measure_iterator = None
    #if type(measures) is dict:
    #    measure_iterator =
    #if type(measures) is list:
    #    measure_iterator = measures
    if type(parts) is not list:
        parts = [parts]
    for part in parts:
        for measure in part['measure']:
            last_note = None
            if type(measure['note']) is dict:
                notes_iterator = [measure['note']]
            else:
                notes_iterator = measure['note']
            for note in notes_iterator:
                if 'pitch' not in note.keys():
                    continue
                new_lyric = deepcopy(lyric)
                # if 'chord' not in note.keys():
                #    new_lyric['text'] = "({})=".format(note['pitch']['octave'])
                new_lyric['text'] = translate[note['pitch']['step']]
                if 'alter' in note['pitch'].keys():
                    new_lyric['text'] = str(new_lyric['text'] + int(note['pitch']['alter']))
                if 'chord' in note.keys():
                    previous_chord = last_note['lyric']['text']
                    del last_note['lyric']
                    new_lyric['text'] = "{}-{}".format(previous_chord, new_lyric['text'])
                note["lyric"] = new_lyric
                last_note = note
    final_xml = xmltodict.unparse(score, pretty=True, short_empty_elements=True)
    old_path = path.split(".")[:-1]
    old_path.append("_subtitled.musicxml")
    final_path = "".join(old_path)
    with open(final_path, 'w') as result_file:
        result_file.write(final_xml)
    msg.showinfo(title="Success!",message="Subtitles added correctly. Result file: {}".format(final_path))
"""

def add_subtitles():
    print("Path: {}".format(path))
    if path == "":
        msg.showwarning(title="No file loaded", message="Please load a proper musicxml file.")
        return
    xml = None
    with open(path, 'r', encoding='utf-8') as file:
        raw_xml = file.read()
        #flat_xml = raw_xml.replace("\n","")
        flat_xml = re.sub(" *\n *","", raw_xml)
        xml = minidom.parseString(flat_xml)
    parts = xml.getElementsByTagName("part")
    for part in parts:
        for measure in part.getElementsByTagName("measure"):
            last_note = None
            for note in measure.childNodes:
                if note.localName != "note":
                    continue
                pitch = note.getElementsByTagName("pitch")
                if not pitch:
                    continue
                new_lyric = minidom.parseString(lyric_str)
                text = new_lyric.getElementsByTagName("text")[0].firstChild
                pitch = pitch[0]
                step = pitch.getElementsByTagName("step")[0].firstChild.data
                text.data = translate[step]
                alter = pitch.getElementsByTagName("alter")
                if alter:
                    alter = alter[0].firstChild.data
                    text.data = text.data + int(alter)
                chord = note.getElementsByTagName("chord")
                if chord:
                    old_lyrics_tag = last_note.getElementsByTagName('lyric')[0]
                    previous_chord = old_lyrics_tag.getElementsByTagName('text')[0].firstChild.data
                    last_note.removeChild(old_lyrics_tag)
                    text.data = "{}-{}".format(previous_chord, text.data)
                note.appendChild(new_lyric.firstChild)
                last_note = note
    final_xml = xml.toprettyxml()
    old_path = path.split(".")[:-1]
    old_path.append("_subtitled.musicxml")
    final_path = "".join(old_path)
    with open(final_path, 'w') as result_file:
        result_file.write(final_xml)
    msg.showinfo(title="Success!", message="Subtitles added correctly. Result file: {}".format(final_path))

if __name__ == "__main__":
    #add_subtitles()
    root = tk.Tk()
    load_UI(root)
    root.mainloop()

#path = 'Chords_with_both_hands.musicxml'