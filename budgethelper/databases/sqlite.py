"""
Abstract class for SQLite3 Database connection
"""
import sqlite3
from typing import List

from budgethelper.databases.databaseabc import DatabaseABC
from budgethelper.models.database import Database


class SQlite(DatabaseABC):
    def __init__(self, database: Database) -> None:
        """Creates SQLite3 connection abstract"""
        self.database = database
        self.conn = sqlite3.connect(database=database.name)

    @property
    def changes(self) -> int:
        """Return the # of changes pending"""

        return self.conn.total_changes

    def listtables(self) -> List[str]:
        """return a list of tables in the database"""

        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
            results = cursor.fetchall()
        finally:
            cursor.close()

        return [t[1] for t in results]

    def close(self) -> None:
        """Close connection, must reinitialize to open again"""

        self.conn.close()

    def commit(self) -> None:
        """Commit pending changes to database (write to file)"""

        self.conn.commit()
