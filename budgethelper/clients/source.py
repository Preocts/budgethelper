"""
Abstract class for SQLite3 Database connection
"""
import logging
import sqlite3
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from budgethelper.clients.databaseabc import DatabaseABC
from budgethelper.exceptions import SourceTableError
from budgethelper.models.database import Database
from budgethelper.models.source import Source


class SQlite(DatabaseABC):
    def __init__(self, database: Database) -> None:
        """Creates SQLite3 connection abstract"""
        self.log = logging.getLogger(__name__)
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

    def create(self, sourcerow: Source) -> bool:
        """Creates a source row in the database"""

        sql = "INSERT INTO sources (name, created_on, updated_on) VALUES (?, ?, ?)"
        values = (sourcerow.name, sourcerow.created_on, sourcerow.updated_on)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

        return True

    def read(self, uid: int) -> Source:
        """Return source by uid"""

        sql = "SELECT name, created_on, updated_on, uid FROM sources WHERE uid = ?"
        values = (uid,)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            result = cursor.fetchone()

        finally:
            cursor.close()

        if not result:
            msg = f"Unable to read, UID not found: {uid}"
            self.log.error(msg)
            raise SourceTableError(msg)

        return Source(*result)

    def getlist(self, _params: Optional[Dict[str, Any]] = None) -> List[Source]:
        """Get all sources from database"""

        sql = "SELECT name, created_on, updated_on, uid FROM sources"

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

        finally:
            cursor.close()

        return [Source(*row) for row in results]

    def update(self, source: Source) -> bool:
        """Update a source in the database"""

        sql = "UPDATE sources SET name = ?, updated_on = ? WHERE uid = ?"
        values = (source.name, source.updated_on, source.uid)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

        return True

    def delete(self, uid: int) -> bool:
        """Delete a row out of the database, may have downstream impact"""

        sql = "DELETE from sources WHERE uid = ?"
        values = (uid,)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

        return True
