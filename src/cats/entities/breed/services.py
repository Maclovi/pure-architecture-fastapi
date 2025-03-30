from typing import cast

from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName


class BreedService:
    """Domain service for breed-related business logic.

    Provides operations that don't naturally fit within the
        Breed entity itself,
    particularly around creation and validation of breed objects.

    Note:
        - Contains stateless operations
        - Follows domain-driven design principles
        - Works with Breed entities and BreedName value objects
    """

    @staticmethod
    def create_breed(breed_name: BreedName) -> Breed:
        """Creates a new Breed entity with the given name.

        Args:
            breed_name: Validated breed name value object.

        Returns:
            Breed: A new Breed entity with:
                - A temporary None ID (to be assigned during persistence)
                - The provided breed name

        Note:
            - Uses cast for temporary None ID to satisfy type checker
            - The actual ID should be assigned during persistence
            - The breed_name is assumed to be already validated
            - Caller is responsible for proper persistence

        Example:
            >>> breed = BreedService.create_breed(BreedName("Siamese"))
            >>> # Persist the breed to get a real ID
        """
        return Breed(
            oid=cast("BreedID", cast("object", None)),
            name=breed_name,
        )
