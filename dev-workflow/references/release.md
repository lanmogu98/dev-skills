# Release Management

> **When to use:** After merging PRs, when ready to publish a new version.

## Why Version Management Matters

| Benefit | What it enables |
|---------|-----------------|
| User support | "Which version are you on?" — reproducible bug reports |
| Controlled upgrades | Users know what changed and if breaking |
| Easy distribution | GitHub Release + package manager = no git/build required |
| Rollback capability | Can point users to previous stable version |

---

## Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

| Component | When to bump | Examples |
|-----------|--------------|----------|
| **MAJOR** | Breaking changes | Config format change, removed API, behavior change requiring user action |
| **MINOR** | Backward-compatible features | New option, new command, new provider |
| **PATCH** | Backward-compatible fixes | Bug fix, performance fix, typo fix |

### Pre-1.0 Versioning

- Start with `v0.1.0` if "experimental, API may change"
- `0.x.y` signals: "not production-stable yet"
- Move to `v1.0.0` when API/behavior is stable

---

## Version File Sync

**Rule:** All version declarations must match.

| Project Type | Version Files |
|--------------|---------------|
| Node.js | `package.json` |
| Python | `pyproject.toml`, `setup.py`, `__version__` |
| Browser extension | `manifest.json` |
| Go | git tag (no version file) |
| Rust | `Cargo.toml` |
| Multi-platform | All applicable files |

**Check before release:**
```bash
# Grep all version declarations
grep -r "version" package.json manifest.json pyproject.toml 2>/dev/null
```

---

## CHANGELOG Release Flow

### Before Release (ongoing)

Keep changes under `## [Unreleased]`:

```markdown
## [Unreleased]

### Added
- New feature X

### Fixed
- Bug Y
```

### At Release Time

1. Replace `[Unreleased]` with version and date
2. Add new empty `[Unreleased]` section above

```markdown
## [Unreleased]

## [1.2.0] - 2025-01-15

### Added
- New feature X

### Fixed
- Bug Y
```

---

## Release Checklist

```
[ ] All tests pass
[ ] Version bumped in all version files
[ ] CHANGELOG.md: [Unreleased] → [x.y.z] - date
[ ] No secrets in codebase (grep for API keys, tokens)
[ ] README updated if CLI/config changed
[ ] Migration notes added (if breaking changes)
```

---

## Release Process (GitHub)

### Step 1: Prepare

```bash
# Ensure clean state
git status  # should be clean
git pull origin main

# Bump version in files
# Update CHANGELOG.md
git add -A
git commit -m "chore: bump version to x.y.z"
git push
```

### Step 2: Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

### Step 3: Create GitHub Release

- Go to Releases → Draft new release
- Select tag: `vX.Y.Z`
- Title: `vX.Y.Z`
- Body: Copy from CHANGELOG (this version's section)
- Add migration notes if breaking

### Step 4: Attach Build Artifacts (if applicable)

| Project Type | Artifact |
|--------------|----------|
| Browser extension | `extension-vX.Y.Z.zip` (manifest + src, no node_modules) |
| CLI tool | Pre-built binaries |
| Library | Usually none (users install via package manager) |

---

## Build Artifacts Guidelines

### What to Include

- Source code needed at runtime
- Assets (icons, styles, etc.)
- Dependency lockfile (for reproducibility)

### What to Exclude

```
node_modules/
__pycache__/
.env*
*.log
.git/
tests/
docs/
*.test.*
```

### Example: Browser Extension Zip

```bash
# Create release zip
zip -r extension-v1.2.0.zip \
  manifest.json \
  src/ \
  icons/ \
  -x "*.test.*" -x "*.spec.*"
```

---

## Migration Notes

**Required when:**
- Config key renamed/removed
- Default behavior changed
- Cache/storage format changed
- Required user action (re-auth, clear cache, etc.)

**Format in release notes:**

```markdown
## Upgrade Notes

**Breaking:** Config key `oldName` renamed to `newName`.
- Action required: Update your config file.

**Behavior change:** Default timeout changed from 30s to 60s.
- No action required unless you rely on the previous default.
```

---

## Hotfix Process

For critical bugs in released versions:

```bash
# Branch from release tag
git checkout -b hotfix/critical-bug vX.Y.Z

# Fix, test, commit
git commit -m "fix: critical bug description"

# Tag as patch version
git tag -a vX.Y.(Z+1) -m "Hotfix: critical bug"
git push origin hotfix/critical-bug --tags

# Create PR to merge back to main
```

---

## Automation (Optional)

Consider automating with:

| Tool | What it does |
|------|--------------|
| `semantic-release` | Auto version bump + changelog + release |
| `standard-version` | Changelog generation from commits |
| `release-please` | GitHub Action for release PRs |
| GitHub Actions | Build artifacts on tag push |

**Note:** Start manual, automate when release frequency justifies it.

---

**→ Back to:** SKILL.md (main workflow)
