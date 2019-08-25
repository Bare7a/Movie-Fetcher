class Server:
    def __init__(self, id, url, title):
        self.id = id
        self.url = url
        self.title = title

    def __repr__(self):
        return '{title}: {url}'.format(title=self.title, url=self.url)
