class Movie:
    def __init__(self, id, url, title, eq=0):
        self.id = id
        self.eq = eq
        self.url = url
        self.title = title

    def __repr__(self):
        return '[{eq}]: {title}'.format(eq=self.eq, title=self.title)
