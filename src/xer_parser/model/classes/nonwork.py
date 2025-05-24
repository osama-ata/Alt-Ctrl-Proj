class NonWork:
    def __init__(self, params):
        self.nonwork_type_id = (
            params.get("nonwork_type_id").strip()
            if params.get("nonwork_type_id")
            else None
        )
        self.seq_num = params.get("seq_num").strip() if params.get("seq_num") else None
        self.nonwork_code = (
            params.get("nonwork_code").strip() if params.get("nonwork_code") else None
        )
        self.nonwork_type = (
            params.get("nonwork_type").strip() if params.get("nonwork_type") else None
        )

    def get_id(self):
        return self.nonwork_type_id

    def get_tsv(self):
        tsv = [
            "%R",
            self.nonwork_type_id,
            self.seq_num,
            self.nonwork_code,
            self.nonwork_type,
        ]
        return tsv

    def __repr__(self):
        return self.nonwork_type_id + "->" + self.nonwork_type
