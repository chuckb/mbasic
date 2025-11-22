#!/bin/bash
# Build documentation for local nginx deployment at https://mbasic.awohl.com/docs/

cd /home/mbasic/cl/mbasic

LOCAL_URL="https://mbasic.awohl.com/docs"
GITHUB_URL="https://avwohl.github.io/mbasic"

# Build all docs with local URL
mkdocs build --strict -f mkdocs-local.yml

# Replace all GitHub URLs with local URLs across entire site
echo "Replacing GitHub URLs with local URLs..."
find site/ -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" -o -name "*.js" -o -name "*.json" \) \
    -exec sed -i "s|${GITHUB_URL}|${LOCAL_URL}|g" {} +

# Count replacements for verification
COUNT=$(grep -r "${LOCAL_URL}" site/ 2>/dev/null | wc -l)
echo "✓ Replaced URLs in $COUNT locations"

# Copy sitemap to sitemap1.xml
cp site/sitemap.xml site/sitemap1.xml

echo "✓ Local documentation built for $LOCAL_URL"
