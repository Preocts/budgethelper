"""
Create a database object that holds what we need to connect
"""
import dataclasses
from typing import Literal
from typing import Optional


@dataclasses.dataclass(frozen=True)
class Database:
    """
    Connection configuration for the database

    Attributes:
        type: Type of database being connected to
        name: Name of the database to use
        uri: The location of the database
        port: Port to access database
        user: Username to access database
        password: Password to access database

    """

    type: Literal["sqlite"]
    name: str
    uri: str = "localhost"
    port: int = 3306
    user: Optional[str] = None
    password: Optional[str] = None
