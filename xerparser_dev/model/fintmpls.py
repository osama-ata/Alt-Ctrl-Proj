from xerparser_dev.model.classes.fintmpl import FinTmpl

__all__ = ["FinTmpls"]

class FinTmpls:
    def __init__(self):
        self.index = 0
        self._FinTmpls = []

    def add(self, params):
        self._FinTmpls.append(FinTmpl(params))

    def get_tsv(self):
        if len(self._FinTmpls) > 0:
            tsv = []
            tsv.append(["%T", "FINTMPL"])
            tsv.append(["%F", "fintmpl_id", "fintmpl_name", "default_flag"])
            for fin in self._FinTmpls:
                tsv.append(fin.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> FinTmpl:
        obj = list(filter(lambda x: x.fintmpl_id == id, self._FinTmpls))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._FinTmpls)

    def __len__(self):
        return len(self._FinTmpls)

    def __iter__(self):
        return self

    def __next__(self) -> FinTmpl:
        if self.index >= len(self._FinTmpls):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._FinTmpls[idx]
