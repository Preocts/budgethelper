"""
Class object for handling sources

Author: Preocts
"""
import logging
from typing import List

from budgethelper.dbconnection import DBConnection
from budgethelper.exceptions import SourceTableError
from budgethelper.models.database import Database
from budgethelper.models.source import SourceRow


class DBSources(DBConnection):
    """Abstraction of SQL CRUD methods for sources table"""

    log = logging.getLogger(__name__)

    def __init__(self, database: Database) -> None:
        """
        Creates a sources table object for CRUD operations

        Args:
            database: Database config object for connection

        Raises:
            SourceTableError (Exception) - Message will detail error
        """
        super().__init__(database)

    def create(self, sourcerow: SourceRow) -> None:
        """Creates a source row in the database"""

        sql = "INSERT INTO sources (name, created_on, updated_on) VALUES (?, ?, ?)"
        values = (sourcerow.name, sourcerow.created_on, sourcerow.updated_on)

        cursor = self.cursor()

        try:
            cursor.execute(sql, values)
            self.commit()

        finally:
            cursor.close()

    def read(self, uid: int) -> SourceRow:
        """Return source by uid"""

        sql = "SELECT name, created_on, updated_on, uid FROM sources WHERE uid = ?"
        values = (uid,)

        cursor = self.cursor()

        try:
            cursor.execute(sql, values)
            result = cursor.fetchone()

        finally:
            cursor.close()

        if not result:
            msg = f"Unable to read, UID not found: {uid}"
            self.log.error(msg)
            raise SourceTableError(msg)

        return SourceRow(*result)

    def getlist(self) -> List[SourceRow]:
        """Get all sources from database"""

        sql = "SELECT name, created_on, updated_on, uid FROM sources"

        cursor = self.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

        finally:
            cursor.close()

        return [SourceRow(*row) for row in results]

    def update(self, source: SourceRow) -> None:
        """Update a source in the database"""

        sql = "UPDATE sources SET name = ?, updated_on = ? WHERE uid = ?"
        values = (source.name, source.updated_on, source.uid)

        cursor = self.cursor()

        try:
            cursor.execute(sql, values)
            self.commit()

        finally:
            cursor.close()

    def delete(self, uid: int) -> None:
        """Delete a row out of the database, may have downstream impact"""

        sql = "DELETE from sources WHERE uid = ?"
        values = (uid,)

        cursor = self.cursor()

        try:
            cursor.execute(sql, values)
            self.commit()

        finally:
            cursor.close()
