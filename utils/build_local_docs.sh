#!/bin/bash
# Build documentation for local nginx deployment at https://mbasic.awohl.com/docs/
# Uses mkdocs-local.yml which overrides site_url for structural URLs.
# Post-processes content URLs since mkdocs-macros has a bug with None page titles.

cd /home/mbasic/cl/mbasic

LOCAL_URL="https://mbasic.awohl.com/docs"
GITHUB_URL="https://avwohl.github.io/mbasic"

# Build docs with local URL (mkdocs-local.yml inherits and overrides site_url)
mkdocs build --strict -f mkdocs-local.yml

# Replace GitHub URLs in content with local URLs
find site/ -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" -o -name "*.js" -o -name "*.json" \) \
    -exec sed -i "s|${GITHUB_URL}|${LOCAL_URL}|g" {} +

# Copy sitemap to sitemap1.xml
cp site/sitemap.xml site/sitemap1.xml

echo "✓ Local documentation built for $LOCAL_URL"
