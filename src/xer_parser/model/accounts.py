from typing import List, Iterator, Any, Dict
from xer_parser.model.classes.account import Account

__all__ = ["Accounts"]


class Accounts:
    _accounts: List[Account]

    def __init__(self) -> None:
        self._accounts: List[Account] = []
        self.index: int = 0

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds an Account to the collection.
        The params dictionary is validated into an Account Pydantic model.
        """
        account_instance = Account.model_validate(params)
        self._accounts.append(account_instance)

    def get_tsv(self) -> list:
        tsv_data = []
        if not self._accounts:
            return tsv_data

        tsv_data.append(["%T", "ACCOUNT"])
        header = [
            "%F",
            "acct_id",
            "parent_acct_id",
            "acct_seq_num",
            "acct_name",
            "acct_short_name",
            "acct_descr",
        ]
        tsv_data.append(header)

        for account in self._accounts:
            tsv_data.append(account.get_tsv())
        
        return tsv_data

    def count(self) -> int:
        return len(self._accounts)

    def __iter__(self) -> Iterator[Account]:
        self.index = 0 # Reset index for each iteration
        return self

    def __next__(self) -> Account:
        if self.index < len(self._accounts):
            result = self._accounts[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
            
    # Example finder method (assuming it might be needed, can be removed if not)
    def find_by_id(self, account_id: int) -> Optional[Account]:
        for account in self._accounts:
            if account.acct_id == account_id:
                return account
        return None
