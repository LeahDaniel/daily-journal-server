class Entry():
    """[summary]
    """
    # Class initializer. It has 4 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.

    def __init__(self, id, mood_id, date, concept, entry):
        self.id = id
        self.mood_id = mood_id
        self.date = date
        self.concept = concept
        self.entry = entry
