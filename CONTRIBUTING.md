# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork>`
3. Create feature branch: `git checkout -b feature/your-feature`
4. Make changes
5. Commit: `git commit -m "feat: description"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

## Code Standards

### Python Style
- PEP 8 (enforced with Black)
- Line length: 100 characters
- Type hints required
- Docstrings for public APIs

### Commits
- Use conventional commits:
  - `feat:` New feature
  - `fix:` Bug fix
  - `docs:` Documentation
  - `test:` Tests
  - `chore:` Maintenance
  - `refactor:` Code refactoring
  - `perf:` Performance improvements

### Testing
- Minimum 80% code coverage
- Unit tests for new features
- Integration tests for APIs
- Fixtures for common setups

### Documentation
- Update README.md for new APIs
- Add docstrings to all functions
- Include examples for new features
- Update architecture docs if needed

## Review Process

1. **Automated Checks**
   - Code style (Black, isort)
   - Type checking (mypy)
   - Linting (flake8)
   - Tests (pytest)
   - Coverage (>80%)

2. **Code Review**
   - At least 2 approvals required
   - Security review for auth/threat detection
   - Documentation review
   - Performance review

3. **Approval**
   - Squash and merge commits
   - Delete feature branch
   - Update CHANGELOG.md

## Security Considerations

- ✓ No hardcoded secrets
- ✓ Input validation always
- ✓ SQL injection prevention
- ✓ No sensitive data in logs
- ✓ OWASP compliance
- ✓ Audit logging for sensitive operations

## Performance Guidelines

- Async/await for I/O operations
- Query optimization and indexing
- Connection pooling configured
- Caching where appropriate
- Monitoring and profiling

## Architecture Guidelines

- Keep modules independent
- Use dependency injection
- Implement repository pattern
- Separate concerns
- Document complex algorithms

## Issues

Report security issues to security@example.com privately.

For other issues:
1. Check existing issues
2. Provide reproduction steps
3. Include environment info
4. Add minimal example

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions auto-publishes

## Questions?

- Check documentation
- Review existing issues
- Open discussion issue
- Contact maintainers

Thank you for contributing!
