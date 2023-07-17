from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd


class GenericTransformer(ABC):
    """Generic Transformer class."""

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def apply(self, data: pd.DataFrame, missingness_column: Optional[pd.Series]) -> None:
        """Apply the transformer to the data."""
        pass

    @abstractmethod
    def revert(self, data: pd.DataFrame, missingness_column: Optional[pd.Series], missing_value: Optional[Any]) -> None:
        """Revert data to pre-transformer state."""
        pass


class TransformerWrapper(ABC):
    """Transformer Wrapper class."""

    def __init__(self, wrapped_transformer: GenericTransformer) -> None:
        super().__init__()
        self._wrapped_transformer = wrapped_transformer

    def apply(self, data: pd.Series, *args, **kwargs) -> pd.DataFrame:
        return self._wrapped_transformer.apply(data, *args, **kwargs)

    def revert(self, data: pd.Series, *args, **kwargs) -> pd.DataFrame:
        return self._wrapped_transformer.revert(data, *args, **kwargs)
