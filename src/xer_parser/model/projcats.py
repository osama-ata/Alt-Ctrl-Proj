from xer_parser.model.classes.projcat import ProjCat

__all__ = ["ProjCats"]


class ProjCats:
    def __init__(self) -> None:
        self.index = 0
        self._ProjCats = []

    def add(self, params):
        self._ProjCats.append(ProjCat(params))

    def get_tsv(self):
        tsv = []
        if len(self._ProjCats) > 0:
            tsv.append(["%T", "PROJPCAT"])
            tsv.append(["%F", "proj_id", "proj_catg_type_id", "proj_catg_id"])
            for pcatval in self._ProjCats:
                tsv.append(pcatval.get_tsv())
        return tsv

    # def find_by_id(self, id) -> ProjCat:
    #     obj = list(filter(lambda x: x.proj_catg_id == id, self._ProjCats))
    #     if len(obj) > 0:
    #         return obj[0]
    #     return obj

    @property
    def count(self):
        return len(self._ProjCats)

    def __len__(self) -> int:
        return len(self._ProjCats)

    def __iter__(self) -> "ProjCats":
        return self

    def __next__(self) -> ProjCat:
        if self.index >= len(self._ProjCats):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._ProjCats[idx]
