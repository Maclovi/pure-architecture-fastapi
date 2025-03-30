from sqlalchemy import MetaData
from sqlalchemy.orm import registry

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)
"""Central SQLAlchemy metadata instance with standardized naming conventions.

This metadata object serves as the container for all table definitions and
enforces consistent naming for database constraints and indexes across
the application.

Naming conventions:
    - ix: Index names (ix_<column_label>)
    - uq: Unique constraint names (uq_<table>_<column>)
    - ck: Check constraint names (ck_<table>_<constraint>)
    - fk: Foreign key names (fk_<table>_<column>_<reftable>)
    - pk: Primary key names (pk_<table>)

Note:
    - Ensures consistent DDL generation
    - Makes database schema more maintainable
    - Used by all mapped table definitions
"""

mapper_registry = registry(metadata=metadata)
"""SQLAlchemy registry for declarative class mapping.

This registry maintains the configuration for mapping Python classes to
database tables, using the shared metadata instance for consistent DDL.

Features:
    - Tracks all mapped classes
    - Generates table definitions
    - Manages class instrumentation
    - Uses the shared metadata with naming conventions

Note:
    - Should be used as the base for all declarative models
    - Enables both imperative and declarative mapping styles
    - Central point for SQLAlchemy ORM configuration
"""
