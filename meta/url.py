from meta import DirtField


class UrlField(DirtField):
    name = "url"
    description = "url related with incident"

    @classmethod
    def add(cls, incident, args):
        raise NotImplementedError()

    @classmethod
    def show(cls, incident):
        raise NotImplementedError()
