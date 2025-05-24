from xer_parser.model.classes.taskproc import TaskProc

__all__ = ["TaskProcs"]


class TaskProcs:
    def __init__(self) -> None:
        self.index = 0
        self._TaskProcs = []

    def add(self, params):
        self._TaskProcs.append(TaskProc(params))

    def get_tsv(self):
        if len(self._TaskProcs) > 0:
            tsv = []
            tsv.append(["%T", "TASKPROC"])
            tsv.append(
                [
                    "%F",
                    "proc_id",
                    "task_id",
                    "proj_id",
                    "seq_num",
                    "proc_name",
                    "complete_flag",
                    "proc_wt",
                    "complete_pct",
                    "proc_descr",
                ]
            )
            for taskproc in self._TaskProcs:
                tsv.append(taskproc.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> TaskProc:
        obj = list(filter(lambda x: x.proc_id == id, self._TaskProcs))
        if len(obj) > 0:
            return obj[0]
        return obj

    def find_by_activity_id(self, id):
        objs = list(filter(lambda x: x.task_id == id, self._TaskProcs))
        return objs

    @property
    def count(self):
        return len(self._TaskProcs)

    def __len__(self) -> int:
        return len(self._TaskProcs)

    def __iter__(self) -> "TaskProcs":
        return self

    def __next__(self) -> TaskProc:
        if self.index >= len(self._TaskProcs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._TaskProcs[idx]
