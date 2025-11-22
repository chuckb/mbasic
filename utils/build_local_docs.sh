#!/bin/bash
# Build documentation for local nginx deployment

cd /home/mbasic/cl/mbasic

# Build with GitHub URL
mkdocs build --strict

# Replace URLs in sitemap for local deployment
sed -i 's|https://avwohl.github.io/mbasic|https://mbasic.awohl.com/docs|g' site/sitemap.xml

# Copy sitemap to sitemap1.xml
cp site/sitemap.xml site/sitemap1.xml

echo "✓ Local documentation built with updated sitemap URLs"
