# Contributing

## Getting Started

1. Fork the repository
2. Clone your fork
3. Run `make dev` to install development dependencies
4. Run `make pre-commit` to install pre-commit hooks

## Development Workflow

1. Create a feature branch from `master`: `git checkout -b feature/my-feature`
2. Make your changes
3. Run `make lint` to check code style
4. Run `make typecheck` to verify types
5. Run `make test` to ensure tests pass
6. Commit with a descriptive message
7. Push and open a Pull Request

## Code Standards

- Follow existing code patterns and conventions
- Use Python type hints for all function signatures
- Write Pydantic models for data validation
- Include unit tests for all new functionality
- Update documentation for API changes
- No hardcoded secrets or sensitive data

## Pull Request Process

1. Ensure all CI checks pass
2. Update documentation if needed
3. Add tests for new functionality
4. Request review from maintainers
5. Squash commits before merge

## Commit Messages

Follow conventional commits format:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` testing
- `refactor:` code restructuring
- `security:` security fix
- `ci:` CI/CD changes

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
