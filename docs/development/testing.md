# Testing

The Cats API includes comprehensive unit and integration tests to ensure reliability and maintainability.

## Test Structure

### Unit Tests: `tests/unit/`

- Test business logic and entities (e.g., `test_add_cat.py`, `test_value_objects.py`).
- Use mocking to isolate dependencies (see `tests/unit/application/conftest.py`).

### Integration Tests: `tests/integrations/`

- Test HTTP endpoints (e.g., `test_cat_api.py`, `test_healthcheck.py`).
- Use a test database (PostgreSQL via Docker).

## Running Tests

1. **Start Infrastructure**:

   ```bash
   just infra
   ```

2. **Run Tests**:

   ```bash
   just test
   ```

3. **Run with Coverage**:

   ```bash
   just cov
   ```

Generates a coverage report, excluding adapters and migrations (see pyproject.toml).

## Tools

- **Pytest**: Test framework with async support (pytest-asyncio).
- **Coverage**: Measures test coverage (coverage[toml]).
- **Mocking**: Uses unittest.mock for dependency isolation.

## Example Test

From `tests/integrations/http/v1/test_cat_api.py`:

```python
async def test_scenarios_cat(client: AsyncClient) -> None:
    payload = {
        "age": 1,
        "color": "red",
        "description": "biba blyt",
        "breed_name": "plain",
    }
    response = await client.post("/v1/cats/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.read() == b"1"
```

## Configuration

Test settings are defined in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
xfail_strict = true
testpaths = ["tests"]
asyncio_mode = "auto"
```
