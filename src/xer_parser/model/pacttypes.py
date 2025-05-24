from xer_parser.model.classes.pcattype import PCatType

__all__ = ["PCatTypes"]

class PCatTypes:
    def __init__(self):
        self.index = 0
        self._pcattypes = []

    def add(self, params):
        self._pcattypes.append(PCatType(params))

    def find_by_id(self, id) -> PCatType:
        obj = list(filter(lambda x: x.proj_catg_type_id == id, self._pcattypes))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        if len(self._pcattypes) > 0:
            tsv = []
            tsv.append(["%T", "PCATTYPE"])
            tsv.append(
                [
                    "%F",
                    "proj_catg_type_id",
                    "seq_num",
                    "proj_catg_short_len",
                    "proj_catg_type",
                    "export_flag",
                ]
            )
            for acttyp in self._pcattypes:
                tsv.append(acttyp.get_tsv())
            return tsv
        return []

    def count(self):
        return len(self._pcattypes)

    def __len__(self):
        return len(self._pcattypes)

    def __iter__(self):
        return self

    def __next__(self) -> PCatType:
        if self.index >= len(self._pcattypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._pcattypes[idx]
