
class PCatVal:
    def __init__(self, params):
        # %F	proj_catg_id	proj_catg_type_id	seq_num	proj_catg_short_name	parent_proj_catg_id	proj_catg_name
        self.proj_catg_id = (
            params.get("proj_catg_id").strip() if params.get("proj_catg_id") else None
        )
        self.proj_catg_type_id = (
            params.get("proj_catg_type_id").strip()
            if params.get("proj_catg_type_id")
            else None
        )
        self.seq_num = params.get("seq_num").strip() if params.get("seq_num") else None
        self.proj_catg_short_name = (
            params.get("proj_catg_short_name").strip()
            if params.get("proj_catg_short_name")
            else None
        )
        self.parent_proj_catg_id = (
            params.get("parent_proj_catg_id").strip()
            if params.get("parent_proj_catg_id")
            else None
        )
        self.proj_catg_name = (
            params.get("proj_catg_name").strip()
            if params.get("proj_catg_name")
            else None
        )

    def get_id(self):
        return self.proj_catg_id

    def get_tsv(self):
        tsv = [
            "%R",
            self.proj_catg_id,
            self.proj_catg_type_id,
            self.seq_num,
            self.proj_catg_short_name,
            self.parent_proj_catg_id,
            self.proj_catg_name,
        ]
        return tsv

    def __repr__(self):
        return self.proj_catg_name
