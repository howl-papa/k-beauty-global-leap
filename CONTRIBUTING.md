# Contributing to K-Beauty Global Leap

We love your input! We want to make contributing to K-Beauty Global Leap as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Workflow

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Request Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Branch Naming Convention

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation updates
- `refactor/refactoring-description` - Code refactoring

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvements
- `test`: Adding missing tests
- `chore`: Changes to the build process or auxiliary tools

**Example:**
```
feat(market-intelligence): add real-time trend analysis

Implemented social media listening pipeline for Instagram and TikTok
to analyze K-Beauty trends in target markets.

Closes #123
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use `black` for formatting: `black .`
- Use `isort` for imports: `isort .`
- Use `mypy` for type checking: `mypy .`

### TypeScript (Frontend)
- Follow the Airbnb JavaScript Style Guide
- Use Prettier for formatting: `npm run format`
- Use ESLint: `npm run lint`

## Testing

### Backend Tests
```bash
cd backend
pytest -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue or reach out to the maintainers:
- **Yongrak Park**: contact@yongrak.pro
