# API Endpoints

The Cats API provides a RESTful interface for managing cat and breed data. All endpoints are versioned under `/v1`.

## Base URL

- **Development**: `http://localhost:8080/api`
- **Staging/Production**: `http://<host>/api`

## Endpoints

### **Healthcheck**

#### `GET /v1/healthcheck/`

- **Description**: Checks the API’s health.

- **Response**:

  ```json
  { "message": "ok", "status": "success" }
  ```

- **Status**: 200 OK

### **Index**

#### `GET /v1/`

- **Description**: Returns a welcome message.
- **Response**:

  ```json
  { "message": "Hello there! Welcome to cats API" }
  ```

- **Status**: 200 OK

### Cats

#### `GET /v1/cats/`

- **Description**: Retrieves a paginated list of cats, filterable by breed or color.

- **Query Parameters**:

  - `breed` _(optional)_: Filter by breed name.
  - `color` _(optional)_: Filter by color.
  - `limit` _(optional)_: Number of results (default: 10).
  - `offset` _(optional)_: Pagination offset (default: 0).

- **Response**:

  ```json
  {
    "total": 0,
    "cats": []
  }
  ```

**Status**: 200 OK

#### `GET /v1/cats/{cat_id}`

- **Description**: Retrieves a cat by ID.
- **Path Parameters**:
  - `cat_id`: Cat identifier (integer).
- **Response**:

  ```json
  {
    "cat": {
      "cat_id": 1,
      "breed": "plain",
      "age": 1,
      "color": "red",
      "description": "biba blyt"
    }
  }
  ```

- **Status**: 200 OK, 404 Not Found

#### `POST /v1/cats/`

- **Description**: Creates a new cat.
- **Request Body**:
  ```json
  {
    "age": 1,
    "color": "red",
    "description": "biba blyt",
    "breed_name": "plain"
  }
  ```
- **Response**: Cat ID (e.g., 1)
- **Status**: 201 Created

#### `PATCH /v1/cats/{cat_id}`

- **Description**: Updates a cat’s attributes.
- **Path Parameters**:
  - `cat_id`: Cat identifier.
- **Request Body**:
  ```json
  {
    "description": "nixya ne biba"
  }
  ```
- **Response**: None
- **Status**: 204 No Content, 404 Not Found

#### `DELETE /v1/cats/{cat_id}`

- **Description**: Deletes a cat by ID.
- **Path Parameters**:
  - `cat_id`: Cat identifier.
- **Response**: None
- **Status**: 204 No Content, 404 Not Found

### **Breeds**

- **GET /v1/breeds/**

  - **Description**: Retrieves a paginated list of breeds.
  - **Query Parameters**:

    - `limit` (optional): Number of results.
    - `offset` (optional): Pagination offset.

  - **Response**:
    ```json
    {
      "total": 0,
      "breeds": []
    }
    ```
  - **Status**: 200 OK

## Swagger UI

Interactive documentation is available at:

- http://localhost:8080/docs

See for details on request/response schemas.
