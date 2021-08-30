"""Testing for transctions.py"""
import datetime
import random
from typing import Generator

import pytest

from budgethelper.models.transaction import Transaction
from budgethelper.transactions import DBTransactions


@pytest.fixture(scope="function", name="dbconn")
def fixture_dbconn() -> Generator[DBTransactions, None, None]:
    """Create fixture"""
    trans = DBTransactions(":memory:")

    yield trans

    del trans


def test_01_save_row(dbconn: DBTransactions) -> None:
    """Add a row to given table, follow schema"""
    row = Transaction(
        source=0,
        amount=10.99,
        description="Happy go lucky now",
        date=datetime.datetime.now(),
    )
    change_count: int = dbconn.changes
    dbconn.create(row)
    assert dbconn.changes == change_count + 1


def test_02_get_row(dbconn: DBTransactions) -> None:
    """Get a row from a given table, force schema"""
    row = Transaction(
        source=99,
        amount=99.99,
        description="Nine Nine Nine",
        date=datetime.datetime.now(),
    )
    dbconn.create(row)
    dbconn.commit()
    results = dbconn.get(1)
    assert isinstance(results, Transaction)

    assert results.uid == 1
    assert results.source == 99
    assert results.amount == 99.99
    assert results.description == "Nine Nine Nine"


def test_03_update_row(dbconn: DBTransactions) -> None:
    """Test updating with valid data"""
    row = Transaction(
        source=99,
        amount=99.99,
        description="Nine Nine Nine",
        date=datetime.datetime.now(),
    )
    dbconn.create(row)
    dbconn.commit()

    row = Transaction(
        uid=1,
        source=10,
        amount=99.99,
        description="Updated",
        date=datetime.datetime.now(),
    )

    dbconn.update(row)
    results = dbconn.get(1)
    assert results.description == "Updated"


def test_04_list_rows(dbconn: DBTransactions) -> None:
    """Test listing transactions from a start/end date"""
    random.seed()
    dates = date_gen("2021-01-01")
    for _ in range(100):
        row = Transaction(
            source=random.randint(0, 99),  # nosec
            amount=round(random.random(), 2),  # nosec
            description="Lots of entries",
            date=next(dates),
        )
        dbconn.create(row)
    since = datetime.date.fromisoformat("2020-12-01")
    results = dbconn.getlist(since)
    assert len(results) == 30

    since = datetime.date.fromisoformat("1995-12-01")
    results = dbconn.getlist(since)
    assert len(results) == 0

    since = datetime.date.fromisoformat("2020-12-01")
    until = datetime.date.fromisoformat("2020-12-10")
    results = dbconn.getlist(since, until)
    assert len(results) == 10


def date_gen(startdate: str) -> Generator[datetime.date, None, None]:
    """Generate dates counting backward from the given start"""
    idx = 0
    base = datetime.date.fromisoformat(startdate)
    while True:
        idx += 1
        yield base - datetime.timedelta(days=idx)
