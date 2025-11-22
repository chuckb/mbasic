#!/bin/bash
# Build and deploy local documentation to /local/site for nginx
# Replaces GitHub URLs with local URLs for mbasic.awohl.com/docs

cd /home/mbasic/cl/mbasic

LOCAL_URL="https://mbasic.awohl.com/docs"
GITHUB_URL="https://avwohl.github.io/mbasic"

# Build with local URL config
mkdocs build --strict -f mkdocs-local.yml > /dev/null 2>&1

# Replace GitHub URLs in content with local URLs
find site/ -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" -o -name "*.js" -o -name "*.json" \) \
    -exec sed -i "s|${GITHUB_URL}|${LOCAL_URL}|g" {} +

# Deploy atomically using symlink swap
# /local/site is a symlink to /local/site-a or /local/site-b
TIMESTAMP=$(date +%s)
NEW_DIR="/local/site-${TIMESTAMP}"
cp -r site "$NEW_DIR"

# Atomic symlink update (ln -sfn atomically replaces symlink target)
ln -sfn "$NEW_DIR" /local/site

# Clean up old versions (keep only current)
for old in /local/site-*; do
    [ "$old" != "$NEW_DIR" ] && rm -rf "$old"
done

echo "✓ Local docs deployed to /local/site -> $NEW_DIR"
