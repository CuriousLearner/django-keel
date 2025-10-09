# Contributing to Documentation

Help improve Django Keel documentation!

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── getting-started/            # Getting started guides
│   ├── quickstart.md
│   ├── installation.md
│   └── first-project.md
├── features/                   # Feature documentation
│   ├── overview.md
│   ├── api-options.md
│   ├── authentication.md
│   └── ...
├── deployment/                 # Deployment guides
│   ├── kubernetes.md
│   ├── aws-ec2.md
│   └── docker.md
└── contributing/              # Contributing guides
    ├── development.md
    ├── testing.md
    └── documentation.md
```

## Building Documentation Locally

### Install Dependencies

```bash
pip install -r docs/requirements.txt
```

### Serve Locally

```bash
mkdocs serve
```

Visit [http://localhost:8000](http://localhost:8000)

### Build Static Site

```bash
mkdocs build
```

Output in `site/` directory.

## Writing Documentation

### Markdown Style

- Use ATX-style headers (`#`, `##`, `###`)
- Code blocks with language identifiers
- Use admonitions for notes/warnings

Example:

```markdown
## Section Title

Some text with **bold** and *italic*.

### Code Example

\`\`\`python
def example():
    return "Hello"
\`\`\`

!!! note
    This is an important note.

!!! warning
    This is a warning.
```

### Navigation

Update `mkdocs.yml` when adding new pages:

```yaml
nav:
  - Home: index.md
  - Getting Started:
      - Quick Start: getting-started/quickstart.md
      - New Page: getting-started/new-page.md  # Add here
```

## Read the Docs

Documentation is automatically built and deployed to Read the Docs on:

- Pushes to main branch
- New releases/tags

Configuration: `.readthedocs.yaml`

## Review Process

1. Create a branch
2. Make documentation changes
3. Test locally with `mkdocs serve`
4. Create pull request
5. Maintainer reviews and merges

## Style Guidelines

- Use clear, concise language
- Provide code examples
- Include expected output
- Add screenshots when helpful
- Link to related documentation
- Keep examples up to date

Thank you for contributing to Django Keel documentation! 📚
