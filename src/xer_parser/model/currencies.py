from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.currency import Currency

__all__ = ["Currencies"]


class Currencies:
    _currencies: List[Currency]

    def __init__(self, data_context: Optional[Any] = None) -> None: # Added optional data_context
        self.index: int = 0
        self._currencies: List[Currency] = []
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a Currency to the collection.
        The params dictionary is validated into a Currency Pydantic model.
        """
        currency_instance = Currency.model_validate(params)
        if self.data_context: # Pass the main Data object to the instance if available and needed
            currency_instance.data = self.data_context
        self._currencies.append(currency_instance)

    def find_by_id(self, curr_id: int) -> Optional[Currency]:
        """Finds a currency by its curr_id."""
        return next((cur for cur in self._currencies if cur.curr_id == curr_id), None)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._currencies:
            return []
            
        tsv_data: list[list[str]] = [["%T", "CURRTYPE"]]
        header = [
            "%F",
            "curr_id", "decimal_digit_cnt", "curr_symbol", "decimal_symbol",
            "digit_group_symbol", "pos_curr_fmt_type", "neg_curr_fmt_type",
            "curr_type", "curr_short_name", "group_digit_cnt", "base_exch_rate",
        ]
        tsv_data.append(header)
        for cur in self._currencies:
            tsv_data.append(cur.get_tsv())
        return tsv_data

    @property
    def count(self) -> int: # Added as a property for consistency with other collections
        return len(self._currencies)

    def __len__(self) -> int:
        return len(self._currencies)

    def __iter__(self) -> Iterator[Currency]:
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> Currency:
        if self.index < len(self._currencies):
            result = self._currencies[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
