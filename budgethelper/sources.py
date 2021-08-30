"""
Class object for handling sources

Author: Preocts
"""
import logging

from budgethelper.dbconnection import DBConnection
from budgethelper.models.database import Database


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
        database_name = Database.name
        super().__init__(database_name)
