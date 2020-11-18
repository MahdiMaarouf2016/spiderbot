import datetime


class Domain:
    domain = ""
    last_update = datetime.datetime.today()
    state = 0

    def __init__(self, domain, last_update=datetime.datetime.today(), state: int = 0):
        self.domain = domain
        self.state = state
        self.last_update = last_update

    def _object(self):
        return {"state": self.state, "domain": self.domain, "last_update": self.last_update}

    def _fromobject(self, object):
        self.state, self.domain, self.last_update = object["state"], object["domain"], object["last_update"]

    def _array(self):
        return [self.domain, self.state, self.last_update]


class RssChannel:
    url = ""
    domain = ""
    last_update = datetime.datetime.today()

    def __init__(self, url, domain, last_update=datetime.datetime.today()):
        self.domain = domain
        self.url = url
        self.last_update = last_update

    def _object(self):
        return {"url": self.url, "domain": self.domain, "last_update": self.last_update}

    def _fromobject(self, object):
        self.url, self.domain, self.last_update = object["url"], object["domain"], object["last_update"]

    def _array(self):
        return [self.url, self.domain, self.last_update]
