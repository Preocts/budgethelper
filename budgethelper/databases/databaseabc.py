"""
Abstract Base Class
"""
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List


class DatabaseABC(ABC):
    conn: Any

    @property
    @abstractmethod
    def changes(self) -> int:
        ...

    def listtables(self) -> List[str]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...
