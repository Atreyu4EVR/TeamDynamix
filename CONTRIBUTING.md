# Version Control Cheatsheet

## Semantic Commit Messages

Format: `<type>(<scope>): <subject>`

## Quick Reference

```bash
# Most common commands
git add .                                    # Stage all changes
git commit -m "feat: new feature"           # Commit with semantic message
git push origin main                        # Push to main branch
```

### Types

- `feat`: New feature (minor version bump)
- `fix`: Bug fix (patch version bump)
- `docs`: Documentation only
- `style`: Formatting, missing semi colons, etc
- `refactor`: Code restructuring
- `test`: Adding missing tests
- `chore`: Maintenance tasks

### Scopes (Optional)

Examples:

- `feat(auth): add JWT support`
- `fix(api): correct header format`
- `docs(readme): update installation steps`

### Version Bumping

- Patch (0.0.X): Bug fixes and minor changes

  ```bash
  git commit -m "fix: resolve timeout issue"
  ```

- Minor (0.X.0): New features (non-breaking)

  ```bash
  git commit -m "feat: add rate limiting"
  ```

- Major (X.0.0): Breaking changes

  ```bash
  git commit -m "feat!: redesign API interface"
  # or
  git commit -m "feat: redesign API interface

  BREAKING CHANGE: New API is not backward compatible"
  ```

### Common Workflows

1. **Making Changes**

   ```bash
   git add .
   git commit -m "type: description"
   git push origin main
   ```

2. **Multiple Changes in One Commit**

   ```bash
   git commit -m "feat: add new endpoint
   fix: resolve timeout issue
   docs: update API documentation"
   ```

3. **Checking Status**

   ```bash
   git status  # Check changed files
   git log     # View commit history
   ```

### Examples by Task

#### Adding Features

```bash
git commit -m "feat: add JWT authentication"
git commit -m "feat: implement rate limiting"
git commit -m "feat: add new API endpoint"

```

#### Fixing Bugs

```bash
git commit -m "fix: correct header format"
git commit -m "fix: resolve connection timeout"
git commit -m "fix: handle null response"
```

#### Documentation

```bash
git commit -m "docs: update API documentation"
git commit -m "docs: add usage examples"
git commit -m "docs: update README"
git commit -m "docs: add API examples"
git commit -m "docs: fix typos"
```

#### Breaking Changes

```bash
git commit -m "feat!: remove deprecated endpoint"
git commit -m "feat!: change API response format"
git commit -m "fix!: remove deprecated methods"

# or with breaking change message
git commit -m "feat: remove deprecated endpoint

BREAKING CHANGE: Endpoint removed, use new endpoint instead"
```

### Version Numbers Explained

- Given a version number **MAJOR.MINOR.PATCH**:
  - **MAJOR** version when you make incompatible API changes
  - **MINOR** version when you add functionality in a backwards compatible manner
  - **PATCH** version when you make backwards compatible bug fixes

### GitHub Actions

- Pushes to `main` branch automatically:
  1. Run tests
  2. Update version based on commits
  3. Create GitHub release
  4. Publish to TestPyPI

### Checking Versions

- Current version is in:
  - `pyproject.toml`
  - `src/teamdynamix/__init__.py`

### Notifications

- Push notifications are sent via NTFY after each successful build
- You'll receive notifications for:
  - Build success/failure
  - Test results
  - Version updates
