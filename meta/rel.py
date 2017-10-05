from meta import DirtField


class RelationField(DirtField):
    name = "rel"
    description = "related incidents"

    @classmethod
    def add(cls, incident, args):
        raise NotImplementedError()

    @classmethod
    def show(cls, incident):
        raise NotImplementedError()
