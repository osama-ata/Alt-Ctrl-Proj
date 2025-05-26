from typing import Optional, Any
from pydantic import BaseModel, Field


class Account(BaseModel):
    acct_id: Optional[int] = None
    parent_acct_id: Optional[int] = None
    acct_seq_num: Optional[int] = None
    acct_name: Optional[str] = None
    acct_short_name: Optional[str] = None
    acct_descr: Optional[str] = None
    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            model_data.get("acct_id") if model_data.get("acct_id") is not None else "",
            model_data.get("parent_acct_id") if model_data.get("parent_acct_id") is not None else "",
            model_data.get("acct_seq_num") if model_data.get("acct_seq_num") is not None else "",
            model_data.get("acct_name") if model_data.get("acct_name") is not None else "",
            model_data.get("acct_short_name") if model_data.get("acct_short_name") is not None else "",
            model_data.get("acct_descr") if model_data.get("acct_descr") is not None else "",
        ]

    def __repr__(self):
        return self.acct_name if self.acct_name is not None else super().__repr__()
