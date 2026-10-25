"""Data module storage: the assumption ledger schema (SQLite for V1).

    from sales_capacity_model.db import create
    con = create("engagement.db")      # schema + reference data
"""
from __future__ import annotations

import sqlite3
from importlib import resources


def schema_sql() -> str:
    return resources.files(__name__).joinpath("schema.sql").read_text(encoding="utf-8")


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
