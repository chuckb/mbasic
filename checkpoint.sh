#!/bin/bash
# Checkpoint script: Increment version, commit, and push
# Usage: ./checkpoint.sh "commit message"

if [ -z "$1" ]; then
    echo "Error: Commit message required"
    echo "Usage: ./checkpoint.sh \"commit message\""
    exit 1
fi

COMMIT_MSG="$1"
VERSION_FILE="src/version.py"

# Read current version
CURRENT_VERSION=$(grep 'VERSION = ' $VERSION_FILE | cut -d'"' -f2)
echo "Current version: $CURRENT_VERSION"

# Increment patch version (X.Y.Z -> X.Y.Z+1)
IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
NEW_PATCH=$((patch + 1))
NEW_VERSION="$major.$minor.$NEW_PATCH"

echo "New version: $NEW_VERSION"

# Update version file
sed -i "s/VERSION = \"$CURRENT_VERSION\"/VERSION = \"$NEW_VERSION\"/" $VERSION_FILE

# Check if help documentation was modified
HELP_CHANGED=$(git diff --name-only docs/help/ 2>/dev/null || echo "")

if [ -n "$HELP_CHANGED" ]; then
    echo "Help documentation changed - rebuilding indexes..."
    python3 utils/build_help_indexes.py
    if [ $? -eq 0 ]; then
        echo "✓ Help indexes rebuilt successfully"
    else
        echo "⚠ Warning: Help index build failed"
    fi
fi

# Check if docs were modified - validate mkdocs build
DOCS_CHANGED=$(git diff --name-only docs/ mkdocs.yml 2>/dev/null || echo "")

if [ -n "$DOCS_CHANGED" ]; then
    echo "Documentation changed - validating mkdocs build..."
    if command -v mkdocs &> /dev/null; then
        # Run mkdocs build in strict mode and capture output
        BUILD_OUTPUT=$(mkdocs build --strict 2>&1)

        # Check for warnings or errors
        if echo "$BUILD_OUTPUT" | grep -q "WARNING\|ERROR"; then
            echo "❌ ERROR: mkdocs build has warnings or errors in strict mode!"
            echo ""
            echo "$BUILD_OUTPUT" | grep "WARNING\|ERROR"
            echo ""
            echo "Run 'mkdocs build --strict' to see full details"
            exit 1
        else
            echo "✓ mkdocs build validation passed (no warnings or errors)"
        fi
    else
        echo "⚠ Warning: mkdocs not installed, skipping build validation"
    fi
fi

# Git add, commit, push
git add -A
git commit -m "$COMMIT_MSG

Version: $NEW_VERSION

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push

echo "✓ Checkpoint complete: Version $NEW_VERSION committed and pushed"
