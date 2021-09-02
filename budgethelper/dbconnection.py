"""
Class object for handling IO of a sqlite database

Author: Preocts
"""
from typing import List

from budgethelper.databases.databaseabc import DatabaseABC
from budgethelper.databases.sqlite import SQlite
from budgethelper.models.database import Database
from budgethelper.protocols.sqlcursor import SQLCursor


class DBConnection(DatabaseABC):
    """Abstraction for SQLite3 database level functions"""

    def __init__(self, database: Database) -> None:
        """
        Initilize class

        Args:
            database: path and name of the database file to open
        """
        self.client: DatabaseABC
        self.database = database

        if self.database.type == "sqlite3":
            self.client = SQlite(self.database)
        else:
            raise ValueError(f"Unexpected database type '{database.type}'")

    def __del__(self) -> None:
        """Destroy connection, does not commit"""

        self.close()

    def cursor(self) -> SQLCursor:
        return self.client.conn.cursor()

    @property
    def changes(self) -> int:
        """Return the # of changes pending"""

        return self.client.changes()  # type: ignore

    def listtables(self) -> List[str]:
        """return a list of tables in the database"""

        return self.client.listtables()

    def close(self) -> None:
        """Close connection, must reinitialize to open again"""

        self.client.close()

    def commit(self) -> None:
        """Commit pending changes to database (write to file)"""

        self.client.commit()
