# Contributing

Thanks for your interest in contributing to the Multi-Cloud SOC Dashboard! This guide covers the development setup, workflow, and standards.

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker and Docker Compose
- Git

### Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd multi-cloud-soc-dashboard
   ```

2. **Start infrastructure services**

   ```bash
   docker compose up -d postgres redis
   ```

3. **Backend**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Frontend**

   ```bash
   cd frontend
   npm install
   npx vite --host 0.0.0.0 --port 5173
   ```

5. **Seed data (optional)**

   ```bash
   make seed
   ```

## Development Workflow

### Branch Strategy

- `main` — stable, production-ready code
- `develop` — integration branch for features
- `feature/<name>` — feature branches (branch from `develop`)
- `fix/<name>` — bug fix branches
- `docs/<name>` — documentation changes

### Commits

Write clear, concise commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add MITRE ATT&CK heatmap to dashboard
fix: correct false positive rate calculation
docs: update API reference for playbook endpoints
test: add integration tests for alert ingestion
refactor: extract detection engine into separate module
```

### Pull Requests

1. Create a feature branch from `develop`
2. Make your changes with tests
3. Ensure all checks pass (see below)
4. Open a PR against `develop`
5. Request review from at least one maintainer

## Code Style

### Python (Backend)

- **Linter**: [Ruff](https://docs.astral.sh/ruff/) — fast Python linter and formatter
- Run: `cd backend && ruff check app/ tests/`
- Auto-fix: `cd backend && ruff check --fix app/ tests/`
- Format: `cd backend && ruff format app/ tests/`
- Config is in `pyproject.toml` (if present) or uses Ruff defaults

### TypeScript (Frontend)

- **Linter**: ESLint
- Run: `cd frontend && npm run lint`
- Follow the project's ESLint configuration

### General

- Keep functions small and focused
- Prefer descriptive names over comments
- Type-annotate all Python function signatures
- Use TypeScript strict mode

## Testing

### Backend Tests

```bash
# Run all tests
cd backend && PYTHONPATH=. pytest -v

# Via Docker
make test

# With coverage
cd backend && PYTHONPATH=. pytest --cov=app -v
```

### Frontend Tests

```bash
cd frontend && npm test
```

### Requirements

- All new API endpoints must have at least one test
- Bug fixes must include a regression test
- Detection rules must be tested via the `/api/detections/test` endpoint
- Maintain or improve existing test coverage

## PR Checklist

Before submitting a pull request, verify:

- [ ] Code compiles/runs without errors
- [ ] All existing tests pass (`make test` or `pytest`)
- [ ] New tests added for new functionality
- [ ] Linting passes (`ruff check` for Python, `npm run lint` for TypeScript)
- [ ] Documentation updated if API or behavior changed
- [ ] Commit messages follow Conventional Commits format
- [ ] No secrets or credentials committed
- [ ] Docker build succeeds (`docker compose build`)

## Architecture

See [docs/architecture.md](docs/architecture.md) for a detailed overview of the system architecture, data flow, and component responsibilities.

## Questions?

Open a GitHub issue with the `question` label for any questions about contributing.
