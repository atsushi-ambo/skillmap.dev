# Contributing to Skillmap.dev

Thank you for your interest in contributing to Skillmap.dev! We're excited to have you on board. This document outlines the process for contributing to our project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your changes
4. Make your changes
5. Test your changes
6. Commit and push to your fork
7. Open a pull request

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (for local development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/skillmap.dev.git
   cd skillmap.dev
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Security Guidelines

### ⚠️ Secrets in Code

**Never commit sensitive information** such as:
- API keys
- Authentication tokens
- Database credentials
- Private keys
- Any other sensitive data

### Secure Development Practices

1. **Environment Variables**
   - Store configuration in environment variables
   - Use `.env` files for local development (they are in `.gitignore`)
   - Never commit `.env` files

2. **Dependencies**
   - Keep dependencies up to date
   - Audit dependencies for known vulnerabilities
   - Use `npm audit` and `pip-audit` regularly

3. **Code Review**
   - All code must be reviewed before merging
   - Pay special attention to security-sensitive areas
   - Use static analysis tools to identify potential issues

## Testing

Run the test suite:

```bash
pytest
```

## Submitting Changes

1. Ensure all tests pass
2. Update documentation as needed
3. Commit your changes with a descriptive message
4. Push to your fork and create a pull request

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [mypy](http://mypy-lang.org/) for static type checking

## Reporting Issues

When reporting issues, please include:
- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
