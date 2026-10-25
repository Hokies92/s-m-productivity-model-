"""Storage (SQLite for V1): two schemas that never share a foreign key (docs/MODEL.md section 4).

    from sales_capacity_model.db import create, create_modeller
    reg = create("register.db")        # state assumptions: the register, with reference data
    mod = create_modeller("modeller.db")  # method versions and scenarios
"""
from __future__ import annotations

import sqlite3
from importlib import resources


def schema_sql() -> str:
    return resources.files(__name__).joinpath("schema.sql").read_text(encoding="utf-8")


def modeller_sql() -> str:
    return resources.files(__name__).joinpath("modeller.sql").read_text(encoding="utf-8")


def seed_sql() -> str:
    return resources.files(__name__).joinpath("seed.sql").read_text(encoding="utf-8")


def create(path: str = ":memory:", seed: bool = True) -> sqlite3.Connection:
    """Create (or open) a database with the schema and, by default, the reference data."""
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(schema_sql())
    if seed:
        con.executescript(seed_sql())
    return con


def create_modeller(path: str = ":memory:") -> sqlite3.Connection:
    """Create (or open) the modeller database: levers, method versions, scenarios, runs."""
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(modeller_sql())
    return con
