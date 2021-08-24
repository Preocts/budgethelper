"""Testing for sqlite_io.py"""
import sqlite3
from typing import Generator

import pytest

from budgethelper.dbconnection import DBConnection


@pytest.fixture(scope="function", name="dbconn")
def fixture_dbconn() -> Generator[DBConnection, None, None]:
    """Create fixture class"""

    dbconn = DBConnection(":memory:")
    dbconn.cursor.execute("CREATE TABLE test01 (id INTEGER PRIMARY KEY )")
    dbconn.cursor.execute("CREATE TABLE test02 (id INTEGER PRIMARY KEY )")
    dbconn.cursor.execute("CREATE TABLE test03 (id INTEGER PRIMARY KEY )")

    yield dbconn

    del dbconn


def test_opens_database(dbconn: DBConnection) -> None:
    """Ensure we open database on initialization"""

    assert dbconn.database_name == ":memory:"
    assert isinstance(dbconn.conn, sqlite3.Connection)
    assert isinstance(dbconn.cursor, sqlite3.Cursor)


def test_table_creation(dbconn: DBConnection) -> None:
    """Check for correctly created tables"""

    tables = dbconn.get_tables()
    expected = ["test01", "test02", "test03"]

    assert tables == expected
