"""Testing for transctions.py"""
import datetime
import random
from typing import Generator

import pytest

from budgethelper.transactions import DBTransactions
from budgethelper.transactions import TransRow


@pytest.fixture(scope="function", name="dbconn")
def fixture_dbconn() -> Generator[DBTransactions, None, None]:
    """Create fixture"""
    trans = DBTransactions(":memory:")

    yield trans

    del trans


def test_01_save_row(dbconn: DBTransactions) -> None:
    """Add a row to given table, follow schema"""
    row: TransRow = {
        "source": 0,
        "amount": 10.99,
        "description": "Happy go lucky now",
        "date": datetime.datetime.now(),
    }
    change_count: int = dbconn.changes
    dbconn.save_row(row)
    assert dbconn.changes == change_count + 1


def test_02_get_row(dbconn: DBTransactions) -> None:
    """Get a row from a given table, force schema"""
    row: TransRow = {
        "source": 99,
        "amount": 99.99,
        "description": "Nine Nine Nine",
        "date": datetime.datetime.now(),
    }
    dbconn.save_row(row)
    dbconn.commit()
    results = dbconn.get_trans(1)
    assert isinstance(results, dict)

    assert results["uid"] == 1
    assert results["source"] == 99
    assert results["amount"] == 99.99
    assert results["description"] == "Nine Nine Nine"


def test_03_update_row(dbconn: DBTransactions) -> None:
    """Test updating with valid and invalid data"""
    row: TransRow = {
        "source": 99,
        "amount": 99.99,
        "description": "Nine Nine Nine",
        "date": datetime.datetime.now(),
    }
    dbconn.save_row(row)
    dbconn.commit()
    row["uid"] = 1
    row["source"] = 10
    row["description"] = "Updated"
    dbconn.update_trans(row)
    results = dbconn.get_trans(1)
    assert results["description"] == "Updated"

    del row["description"]
    with pytest.raises(Exception):
        dbconn.update_trans(row)


def test_04_list_rows(dbconn: DBTransactions) -> None:
    """Test listing transactions from a start/end date"""
    random.seed()
    dates = date_gen("2021-01-01")
    for _ in range(100):
        row: TransRow = {
            "source": random.randint(0, 99),  # nosec
            "amount": round(random.random(), 2),  # nosec
            "description": "Lots of entries",
            "date": next(dates),
        }
        dbconn.save_row(row)
    since = datetime.date.fromisoformat("2020-12-01")
    results = dbconn.list_trans(since)
    assert len(results) == 30

    since = datetime.date.fromisoformat("1995-12-01")
    results = dbconn.list_trans(since)
    assert len(results) == 0

    since = datetime.date.fromisoformat("2020-12-01")
    until = datetime.date.fromisoformat("2020-12-10")
    results = dbconn.list_trans(since, until)
    assert len(results) == 10


def date_gen(startdate: str) -> Generator[datetime.date, None, None]:
    """Generate dates counting backward from the given start"""
    idx = 0
    base = datetime.date.fromisoformat(startdate)
    while True:
        idx += 1
        yield base - datetime.timedelta(days=idx)
