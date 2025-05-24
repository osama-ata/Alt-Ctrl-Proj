class TaskProc:
    def __init__(self, params):
        self.complete_flag = (
            params.get("complete_flag").strip() if params.get("complete_flag") else None
        )
        self.complete_pct = (
            params.get("complete_pct").strip() if params.get("complete_pct") else None
        )
        self.proc_descr = (
            params.get("proc_descr").strip() if params.get("proc_descr") else None
        )
        self.proc_id = params.get("proc_id").strip() if params.get("proc_id") else None
        self.proc_name = (
            params.get("proc_name").strip() if params.get("proc_name") else None
        )
        self.proc_wt = params.get("proc_wt").strip() if params.get("proc_wt") else None
        self.proj_id = params.get("proj_id").strip() if params.get("proj_id") else None
        self.seq_num = params.get("seq_num").strip() if params.get("seq_num") else None
        self.task_id = params.get("task_id").strip() if params.get("task_id") else None

    def get_id(self):
        return self.proc_id

    def get_tsv(self):
        tsv = [
            "%R",
            self.proc_id,
            self.task_id,
            self.proj_id,
            self.seq_num,
            self.proc_name,
            self.complete_flag,
            self.proc_wt,
            self.complete_pct,
            self.proc_descr,
        ]
        return tsv

    def __repr__(self):
        return self.proc_id + "->" + self.task_id
