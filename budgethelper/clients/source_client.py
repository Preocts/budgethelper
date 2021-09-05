"""
Provider class for database sources table
"""
import logging
from typing import List

from budgethelper.clients.databaseabc import DatabaseABC
from budgethelper.constants import SOURCES_TABLE_SCHEMA
from budgethelper.exceptions import SourceTableError
from budgethelper.models.database import Database
from budgethelper.models.source import Source


class SourceClient(DatabaseABC):
    TABLE_NAME = "sources"

    def __init__(self, database: Database) -> None:
        """Provisions SQL client to database for sources table"""
        super().__init__(database)
        self.log = logging.getLogger(__name__)

        if self.TABLE_NAME not in self.listtables(self.conn):
            raise SourceTableError(f"Table missing '{self.TABLE_NAME}'")

        for column in SOURCES_TABLE_SCHEMA["required_cols"]:
            if column not in self.listcolumns():
                raise SourceTableError(f"Missing column from table: {column}")

    def listcolumns(self) -> List[str]:
        """Return column names from table"""

        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT * from sources where uid = 0")
            return [c[0] for c in cursor.description]

        finally:
            cursor.close()

    def create(self, sourcerow: Source) -> None:
        """Creates a source row in the database"""

        sql = "INSERT INTO sources (name, created_on, updated_on) VALUES (?, ?, ?)"
        values = (sourcerow.name, sourcerow.created_on, sourcerow.updated_on)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

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

    def getlist(self) -> List[Source]:
        """Get all sources from database"""

        sql = "SELECT name, created_on, updated_on, uid FROM sources"

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

        finally:
            cursor.close()

        return [Source(*row) for row in results]

    def update(self, source: Source) -> None:
        """Update a source in the database"""

        sql = "UPDATE sources SET name = ?, updated_on = ? WHERE uid = ?"
        values = (source.name, source.updated_on, source.uid)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

    def delete(self, uid: int) -> None:
        """Delete a row out of the database, may have downstream impact"""

        sql = "DELETE from sources WHERE uid = ?"
        values = (uid,)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()
