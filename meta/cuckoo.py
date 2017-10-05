from meta import DirtField


class CuckooField(DirtField):
    name = "cuckoo"
    description = "related cuckoo analysis in malwaredb"

    @classmethod
    def add(cls, incident, args):
        raise NotImplementedError()

    @classmethod
    def show(cls, incident):
        raise NotImplementedError()
