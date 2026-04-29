# Development Tasks

Common tasks and commands:

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements.txt[dev]

# Create environment
cp .env.example .env

# Run migrations
python -m alembic upgrade head
```

## Running

```bash
# Development server (with reload)
python src/main.py

# Production server
gunicorn -w 4 -b 0.0.0.0:8000 src.main:app

# Docker
docker-compose up
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/iam_threat_detection

# Run specific test
pytest tests/test_auth.py -v

# Run with markers
pytest -m unit
pytest -m integration
```

## Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/

# Complex checks
pylint src/
```

## Database

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Revert migration
alembic downgrade -1

# View migration history
alembic history
```

## Documentation

```bash
# Build docs
mkdocs build

# Serve docs locally
mkdocs serve

# Deploy docs
mkdocs gh-deploy
```

