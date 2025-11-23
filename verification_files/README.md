# Google Site Verification Files

This directory contains Google site verification files for each deployment target.

## Structure

```
verification_files/
├── local/           # For mbasic.awohl.com/docs
│   └── google*.html
└── github/          # For avwohl.github.io/mbasic
    └── google*.html
```

## How It Works

- **Local deployment** (`utils/deploy_local_docs.sh`): Copies files from `local/` to `site/`
- **GitHub deployment** (`.github/workflows/docs.yml`): Copies files from `github/` to `site/`

## Adding Verification Files

1. Get the verification file from Google Search Console
2. Place it in the appropriate subdirectory:
   - `local/` for mbasic.awohl.com
   - `github/` for avwohl.github.io
3. The deployment scripts will copy it to the built site
