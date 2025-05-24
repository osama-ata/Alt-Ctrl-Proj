from xer_parser.model.classes.nonwork import NonWork

__all__ = ["NonWorks"]

class NonWorks:
    def __init__(self):
        self.index = 0
        self._NonWorks = []

    def add(self, params):
        self._NonWorks.append(NonWork(params))

    def get_tsv(self):
        if len(self._NonWorks) > 0:
            tsv = []
            tsv.append(["%T", "NONWORK"])
            tsv.append(
                ["%F", "nonwork_type_id", "seq_num", "nonwork_code", "nonwork_type"]
            )
            for nw in self._NonWorks:
                tsv.append(nw.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> NonWork:
        obj = list(filter(lambda x: x.fintmpl_id == id, self._NonWorks))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._NonWorks)

    def __len__(self):
        return len(self._NonWorks)

    def __iter__(self):
        return self

    def __next__(self) -> NonWork:
        if self.index >= len(self._NonWorks):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._NonWorks[idx]
