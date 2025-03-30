import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from cats.entities.breed.models import Breed
from cats.entities.breed.value_objects import BreedName
from cats.infrastructure.persistence.models.base import mapper_registry

breeds_table = sa.Table(
    "breeds",
    mapper_registry.metadata,
    sa.Column("breed_id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("breed_name", sa.String(50), nullable=False, unique=True),
    sa.Column(
        "created_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        server_onupdate=sa.func.now(),
        nullable=True,
    ),
)
"""SQLAlchemy table definition for breed entities.

Defines the database schema for storing breed information with:

Columns:
    - breed_id: Primary key (auto-incrementing bigint)
    - breed_name: Unique breed name (max 50 chars, required)
    - created_at: Automatic timestamp for creation
    - updated_at: Automatic timestamp for updates

Constraints:
    - Primary key on breed_id
    - Unique constraint on breed_name
    - Not null on breed_name and created_at

Note:
    - Uses the shared mapper_registry metadata
    - Includes automatic timestamp management
    - Follows naming conventions from base metadata
"""


def map_breed_table() -> None:
    """Configures the ORM mapping between Breed entity and database table.

    Uses imperative mapping to connect the Breed domain
        model to the breeds_table,
    including value object composition and relationship configuration.

    Mapped properties:
        - oid: Maps to breed_id column as primary key
        - cats: One-to-many relationship with Cat entities
        - name: Composite property using BreedName value object

    Note:
        - Uses composite() for BreedName value object mapping
        - Sets up bidirectional relationship with Cat
        - Imperative mapping allows cleaner separation of concerns
        - Should be called during application startup
    """
    _ = mapper_registry.map_imperatively(
        Breed,
        breeds_table,
        properties={
            "oid": breeds_table.c.breed_id,
            "cats": relationship("Cat", back_populates="breed"),
            "name": composite(BreedName, breeds_table.c.breed_name),
        },
    )
