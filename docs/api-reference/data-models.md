# Data Models

The Cats API uses structured data models for requests and responses, defined in `src/cats/entities` and `src/cats/presentation/http/v1/common/schemes.py`.

## Entities

### Cat

- **Location**: `src/cats/entities/cat/models.py`
- **Fields**:
  - `cat_id` (int): Unique identifier.
  - `breed_id` (int, optional): Foreign key to Breed.
  - `age` (int): Cat’s age (0–99).
  - `color` (str): Color description (3–50 characters).
  - `description` (str): Optional description (≤1000 characters).

### Breed

- **Location**: `src/cats/entities/breed/models.py`
- **Fields**:
  - `breed_id` (int): Unique identifier.
  - `name` (str): Breed name (2–50 characters).

## Value Objects

Value objects enforce validation rules:

### CatAge (`src/cats/entities/cat/value_objects.py`):

- Range: 0–99.
- Errors: `CatAgeMinError`, `CatAgeMaxError`.

### CatColor

- Length: 3–50 characters.
- Errors: `CatColorMinLengthError`, `CatColorMaxLengthError`.

### CatDescription:

- Length: ≤1000 characters.
- Error: `CatDescriptionLengthError`.

### BreedName (`src/cats/entities/breed/value_objects.py`):

- Length: 2–50 characters.
- Errors: `BreedNameMinlengthError`, `BreedNameMaxlengthError`.

## API Schemas

### Create Cat Request

```json
{
  "age": 1,
  "color": "red",
  "description": "biba blyt",
  "breed_name": "plain"
}
```

### Cat Response

```json
{
  "cat_id": 1,
  "breed": "plain",
  "age": 1,
  "color": "red",
  "description": "biba blyt"
}
```

### Update Cat Request

```json
{
  "age": 2,
  "color": "white",
  "description": "new desc"
}
```

### Breeds Response

```json
{
  "total": 1,
  "breeds": [{ "breed_id": 1, "name": "plain" }]
}
```

See for usage examples.
