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

# Deploy atomically to nginx serving directory
rm -rf /local/site.new
cp -r site /local/site.new
rm -rf /local/site.old
mv /local/site /local/site.old 2>/dev/null || true
mv /local/site.new /local/site
rm -rf /local/site.old

echo "✓ Local docs deployed to /local/site"
