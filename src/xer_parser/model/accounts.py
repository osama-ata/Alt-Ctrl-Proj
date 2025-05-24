from xer_parser.model.classes.account import Account

__all__ = ["Accounts"]


class Accounts:
    def __init__(self) -> None:
        self._accounts = []
        self.index = 0

    def add(self, params) -> None:  # TODO: Add type annotation for params
        self._accounts.append(Account(params))

    def get_tsv(self) -> list:
        tsv = []
        if len(self._accounts) > 0:
            tsv.append(["%T", "ACCOUNT"])
            tsv.append(
                [
                    "%F",
                    "acct_id",
                    "parent_acct_id",
                    "acct_seq_num",
                    "acct_name",
                    "acct_short_name",
                    "acct_descr",
                ]
            )
            for account in self._accounts:
                tsv.append(account.get_tsv())
            return tsv
        return []

    def count(self) -> int:
        return len(self._accounts)

    def __iter__(self) -> "Accounts":
        return self

    def __next__(self) -> Account:
        if self.index >= len(self._accounts):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._accounts[idx]
