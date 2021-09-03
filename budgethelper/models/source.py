import dataclasses
import datetime
from typing import Optional


@dataclasses.dataclass(frozen=True)
class Source:
    """Model of Source Table row"""

    name: str
    created_on: datetime.datetime = datetime.datetime.now()
    updated_on: datetime.datetime = datetime.datetime.now()
    uid: Optional[int] = None
