class FinTmpl:
    def __init__(self, params):
        self.fintmpl_id = (
            params.get("fintmpl_id").strip() if params.get("fintmpl_id") else None
        )
        self.fintmpl_name = (
            params.get("fintmpl_name").strip() if params.get("fintmpl_name") else None
        )
        self.default_flag = (
            params.get("default_flag").strip() if params.get("default_flag") else None
        )

    def get_id(self):
        return self.fintmpl_id

    def get_tsv(self):
        tsv = ["%R", self.fintmpl_id, self.fintmpl_name, self.default_flag]
        return tsv

    def __repr__(self):
        return self.proc_id + "->" + self.task_id
