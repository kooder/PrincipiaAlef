class Note(object):
    def __init__(self,
                 note=None,
                 staccato=None,
                 tie_in_front=None):
        self.note = note
        self.staccato = staccato
        self.tie_in_front = tie_in_front
