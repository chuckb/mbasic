#!/bin/bash
# Build documentation for local nginx deployment at https://mbasic.awohl.com/docs/

cd /home/mbasic/cl/mbasic

LOCAL_URL="https://mbasic.awohl.com/docs"

# Build all docs with local URL
mkdocs build --strict -f mkdocs-local.yml

# Copy sitemap to sitemap1.xml
cp site/sitemap.xml site/sitemap1.xml

echo "✓ Local documentation built for $LOCAL_URL"
