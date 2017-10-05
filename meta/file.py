from meta import DirtField


class FileField(DirtField):
    name = "file"
    description = "information about files in incident directory"

    @classmethod
    def add(cls, incident, args):
        raise NotImplementedError()

    @classmethod
    def show(cls, incident):
        raise NotImplementedError()
