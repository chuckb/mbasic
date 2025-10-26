# MBASIC Documentation

This directory contains all documentation for the MBASIC 5.21 interpreter project.

## Directory Structure

### `/help` - In-UI Help System
Documentation accessible from within the MBASIC user interfaces.

- **`/help/common/`** - General help content shared across all UI backends
  - Language reference
  - Statement documentation
  - Function reference
  - General usage

- **`/help/ui/cli/`** - CLI backend-specific help
- **`/help/ui/curses/`** - Curses (urwid) backend-specific help
- **`/help/ui/tk/`** - Tkinter GUI backend-specific help
- **`/help/ui/visual/`** - Visual backend-specific help

### `/dev` - Development Documentation
Current development notes, plans, and technical documentation.

- **`/dev/archive/`** - Completed development sessions and obsolete notes
- Active development documents
- Implementation guides
- Technical specifications

### `/history` - Historical Documentation
Archived development timeline, session logs, and progress reports.

- Session timelines
- Progress reports
- Analysis documents from development
- Historical design decisions

### `/user` - User-Facing Documentation
End-user guides and tutorials (external, not in-UI).

- Quick start guides
- Tutorials
- FAQ
- Installation instructions

### `/design` - Design Documents
Architecture, design patterns, and future plans.

- System architecture
- Component designs
- Future compiler plans
- Optimization strategies

### `/external` - External References
Documentation for external formats, protocols, and standards.

- File format specifications
- CP/M compatibility notes
- MBASIC 5.21 reference materials

## Web Deployment

Documentation is automatically deployed to GitHub Pages using MkDocs:

- **Live Site:** https://avwohl.github.io/mbasic
- **Configuration:** `../mkdocs.yml` (project root)
- **Workflow:** `../.github/workflows/docs.yml`

### Local Preview

```bash
# Install dependencies
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin

# Start development server
mkdocs serve

# Open http://127.0.0.1:8000
```

### Manual Deployment

```bash
# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Adding Documentation

1. Create markdown file in appropriate `help/` subdirectory
2. Add YAML front matter (title, type, category, keywords, description)
3. Rebuild search index: `python3 utils/frontmatter_utils.py docs/help/common/language -o docs/help/common/language/search_index.json`
4. Update `mkdocs.yml` navigation if needed
5. Test: `python3 utils/test_help_integration.py`

## Quick Links

- **[Web Documentation](https://avwohl.github.io/mbasic)** - Live documentation site
- [Quick Reference](user/QUICK_REFERENCE.md) - Fast command reference
- [Language Reference](help/common/language/index.md) - BASIC-80 language
- [MBASIC Documentation](help/mbasic/index.md) - Interpreter docs
- [Development Status](dev/STATUS.md) - Current project status
