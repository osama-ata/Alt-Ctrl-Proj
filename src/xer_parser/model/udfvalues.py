from xer_parser.model.classes.udfvalue import UDFValue

__all__ = ["UDFValues"]

class UDFValues:
    def __init__(self):
        self.index = 0
        self._udfvalues = []

    def add(self, params):
        self._udfvalues.append(UDFValue(params))

    def get_tsv(self):
        if len(self._udfvalues) > 0:
            tsv = []
            tsv.append(["%T", "UDFVALUE"])
            tsv.append(
                [
                    "%F",
                    "udf_type_id",
                    "fk_id",
                    "proj_id",
                    "udf_date",
                    "udf_number",
                    "udf_text",
                    "udf_code_id",
                ]
            )
            for udfval in self._udfvalues:
                tsv.append(udfval.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> UDFValue:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._udfvalues))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._udfvalues)

    def __len__(self):
        return len(self._udfvalues)

    def __iter__(self):
        return self

    def __next__(self) -> UDFValue:
        if self.index >= len(self._udfvalues):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._udfvalues[idx]
