class ProjCat:
    def __init__(self, params):
        # %F	proj_id	proj_catg_type_id	proj_catg_id
        self.proj_id = params.get("proj_id").strip() if params.get("proj_id") else None
        self.proj_catg_type_id = (
            params.get("proj_catg_type_id").strip()
            if params.get("proj_catg_type_id")
            else None
        )
        self.proj_catg_id = (
            params.get("proj_catg_id").strip() if params.get("proj_catg_id") else None
        )

    def get_id(self):
        return self.proj_id

    def get_tsv(self):
        tsv = ["%R", self.proj_id, self.proj_catg_type_id, self.proj_catg_id]
        return tsv

    def __repr__(self):
        return self.proj_catg_name
