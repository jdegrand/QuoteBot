class Entry:
    def __init__(self, key, occurances, quote):
        self.occurances = int(occurances)
        self.quote = quote
        self.key = key

    def get_key(self):
        return self.key

    def get_quote(self):
        return self.quote

    def get_occurances(self):
        return self.occurances

    def increment_occurances(self):
        self.occurances += 1
        return self.occurances

    def change_key(self, key):
        self.key = key
        return self.key

