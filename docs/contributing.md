# Contributing

Contributions to the Cats API are welcome! This guide outlines how to contribute.

## Getting Started

1. **Fork the Repository**:
   Fork [Maclovi/pure-architecture-fastapi](https://github.com/Maclovi/pure-architecture-fastapi).

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/<your-username>/pure-architecture-fastapi
   cd pure-architecture-fastapi
   ```

3. **Set Up Development**:

   ```bash
   just bootstrap
   ```

## Making Changes

1. **Create a Branch**:

   ```bash
   git checkout -b feature/your-feature
   ```

2. **Follow Coding Standards**:

   - Use Ruff for linting (just lint).
   - Run static analysis (just static).
   - Write tests (just test).

3. **Commit Messages**: Use conventional commits (enforced by conventional-pre-commit):

   - **Example**: `feat: add new cat endpoint`
   - **Types**: `feat`, `fix`, `docs`, `chore`, `style`, `refactor`, `test`, `build`.

4. **Run Pre-Commit Hooks**:

   ```bash
   pre-commit run --all-files
   ```

## Submitting Changes

1. **Push Changes**:

   ```bash
   git push origin feature/your-feature
   ```

2. **Create a Pull Request**:

   - Target the develop branch.
   - Describe the changes and reference any issues.

3. **CI Checks**: The PR will trigger pr-tests.yaml to run tests and linters. Ensure all checks pass.

## Code Review

- Respond to feedback promptly.
- Make necessary changes and push updates to the same branch.

## Issues

Report bugs or suggest features via GitHub Issues.

## Contact

- **Author**: Sergey Yavorsky ([GitHub](https://github.com/Maclovi))
- **Email**: maclovi.dev@gmail.com

Thank you for contributing!
