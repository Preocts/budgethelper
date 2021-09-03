"""
Abstract Base Class
"""
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class DatabaseABC(ABC):
    conn: Any

    @property
    @abstractmethod
    def changes(self) -> int:
        ...

    @abstractmethod
    def listtables(self) -> List[str]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def create(self, row_object: Any) -> bool:
        ...

    @abstractmethod
    def read(self, uid: int) -> Any:
        ...

    @abstractmethod
    def getlist(self, params: Optional[Dict[str, Any]]) -> List[Any]:
        ...

    @abstractmethod
    def update(self, row_object: Any) -> bool:
        ...

    @abstractmethod
    def delete(self, uid: int) -> bool:
        ...
