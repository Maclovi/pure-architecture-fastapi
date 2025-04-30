# Installation

This guide covers the prerequisites and installation steps for the Cats API.

## Prerequisites

- **Python**: >= 3.10
- **Docker**: For containerized deployment
- **Git**: For cloning the repository
- **Just**: Task runner (optional, install via `pip install just`)

## Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Maclovi/pure-architecture-fastapi
   cd pure-architecture-fastapi
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies: Use the provided just command to bootstrap the environment**:

   ```bash
   just bootstrap
   ```

   This copies .env.dist to .env, installs dependencies, and sets up pre-commit hooks.

4. **Docker Setup (Optional)**: To run the full stack with Docker:

   ```bash
   just up
   ```

   This starts all services defined in docker-compose.dev.yaml, including the API, database, and observability tools.
