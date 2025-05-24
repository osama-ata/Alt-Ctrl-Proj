from xer_parser.model.classes.udftype import UDFType

__all__ = ["UDFTypes"]

class UDFTypes:
    def __init__(self):
        self.index = 0
        self._udftypes = []

    def add(self, params):
        self._udftypes.append(UDFType(params))

    def get_tsv(self):
        tsv = []
        if len(self._udftypes) > 0:
            tsv.append(["%T", "UDFTYPE"])
            tsv.append(
                [
                    "%F",
                    "udf_type_id",
                    "table_name",
                    "udf_type_name",
                    "udf_type_label",
                    "logical_data_type",
                    "super_flag",
                    "indicator_expression",
                    "summary_indicator_expression",
                    "export_flag",
                ]
            )
            for udf in self._udftypes:
                tsv.append(udf.get_tsv())
        return tsv

    def find_by_id(self, id) -> UDFType:
        obj = list(filter(lambda x: x.udf_type_id == id, self._udftypes))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._udftypes)

    def __len__(self):
        return len(self._udftypes)

    def __iter__(self):
        return self

    def __next__(self) -> UDFType:
        if self.index >= len(self._udftypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._udftypes[idx]
