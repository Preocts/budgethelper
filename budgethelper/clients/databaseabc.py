"""
Abstract Base Class
"""
from abc import ABC
from abc import abstractmethod
from sqlite3 import Connection
from typing import Any
from typing import List


class DatabaseABC(ABC):
    conn: Connection

    @property
    def changes(self) -> int:
        """Return the # of changes pending"""

        return self.conn.total_changes

    def close(self) -> None:
        """Close connection, must reinitialize to open again"""

        self.conn.close()

    @staticmethod
    def listtables(conn: Connection) -> List[str]:
        """return a list of tables in the database"""

        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
            results = cursor.fetchall()
        finally:
            cursor.close()

        return [t[1] for t in results]

    @abstractmethod
    def listcolumns(self) -> List[str]:
        ...

    @abstractmethod
    def create(self, row_object: Any) -> None:
        ...

    @abstractmethod
    def read(self, uid: int) -> Any:
        ...

    @abstractmethod
    def update(self, row_object: Any) -> None:
        ...

    @abstractmethod
    def delete(self, uid: int) -> None:
        ...
