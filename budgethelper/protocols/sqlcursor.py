"""Protocal for Cursor type"""
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Protocol


class SQLCursor(Protocol):
    def execute(self, sql: str, parameters: Iterable[Any]) -> "SQLCursor":
        ...

    def executemany(self, sql: str, paramters: Iterable[Any]) -> "SQLCursor":
        ...

    def close(self) -> None:
        ...

    def fetchone(self) -> List[Any]:
        ...

    def fetchall(self) -> List[Any]:
        ...

    def fetchmany(self, size: Optional[int] = None) -> List[Any]:
        ...
