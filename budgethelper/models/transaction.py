import dataclasses
import datetime
from typing import Optional


@dataclasses.dataclass(frozen=True)
class Transaction:
    """Represents a Transaction table row"""

    source: int
    amount: float
    description: str
    date: datetime.date
    uid: Optional[int] = None
    created_on: datetime.datetime = datetime.datetime.now()
    updated_on: datetime.datetime = datetime.datetime.now()
