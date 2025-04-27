from typing import list

from xerparser_dev.model.classes.wbs import WBS

__all__ = ["WBSs"]

class WBSs:
    def __init__(self, data=None):
        self.index = 0
        self._wbss = []
        self.data = data

    def add(self, params, data):
        wbs = WBS(params, data)
        self._wbss.append(wbs)

    def get_tsv(self):
        tsv = []
        if len(self._wbss) > 0:
            tsv.append(["%T", "PROJWBS"])
            tsv.append(
                [
                    "%F",
                    "wbs_id",
                    "proj_id",
                    "obs_id",
                    "seq_num",
                    "est_wt",
                    "proj_node_flag",
                    "sum_data_flag",
                    "status_code",
                    "wbs_short_name",
                    "wbs_name",
                    "phase_id",
                    "parent_wbs_id",
                    "ev_user_pct",
                    "ev_etc_user_value",
                    "orig_cost",
                    "indep_remain_total_cost",
                    "ann_dscnt_rate_pct",
                    "dscnt_period_type",
                    "indep_remain_work_qty",
                    "anticip_start_date",
                    "anticip_end_date",
                    "ev_compute_type",
                    "ev_etc_compute_type",
                    "guid",
                    "tmpl_guid",
                    "plan_open_state",
                ]
            )
            for wb in self._wbss:
                tsv.append(wb.get_tsv())
        return tsv

    def get_by_project(self, id) -> list[WBS]:
        return list(filter(lambda x: x.proj_id == id, self._wbss))

    def __iter__(self):
        return self

    def __next__(self) -> WBS:
        if self.index >= len(self._wbss):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._wbss[idx]
