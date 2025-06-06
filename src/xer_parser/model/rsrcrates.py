from xer_parser.model.classes.rsrcrate import ResourceRate

__all__ = ["ResourceRates"]


class ResourceRates:
    def __init__(self) -> None:
        self.index = 0
        self._rsrcrates = []

    def add(self, params):
        self._rsrcrates.append(ResourceRate(params))

    def find_by_id(self, id) -> ResourceRate:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rsrcrates))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        tsv = []
        if len(self._rsrcrates) > 0:
            tsv.append(["%T", "RSRCRATE"])
            tsv.append(
                [
                    "%F",
                    "rsrc_rate_id",
                    "rsrc_id",
                    "max_qty_per_hr",
                    "cost_per_qty",
                    "start_date",
                    "shift_period_id",
                    "cost_per_qty2",
                    "cost_per_qty3",
                    "cost_per_qty4",
                    "cost_per_qty5",
                ]
            )
            for rr in self._rsrcrates:
                tsv.append(rr.get_tsv())
        return tsv

    @property
    def count(self):
        return len(self._rsrcrates)

    def __len__(self) -> int:
        return len(self._rsrcrates)

    def __iter__(self) -> "ResourceRates":
        return self

    def __next__(self) -> ResourceRate:
        if self.index >= len(self._rsrcrates):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrcrates[idx]
