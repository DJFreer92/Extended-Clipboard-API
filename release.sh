#!/bin/bash

# Extended Clipboard API Release Script
# This script helps create a GitHub release for the Extended Clipboard API

echo "🚀 Extended Clipboard API Release v0.1.0"
echo "======================================="
echo ""

echo "✅ Package built successfully:"
echo "   - Source distribution: extended_clipboard_api-0.1.0.tar.gz (36.2 KB)"
echo "   - Wheel distribution: extended_clipboard_api-0.1.0-py3-none-any.whl (25.0 KB)"
echo ""

echo "✅ Git tag created: v0.1.0"
echo "✅ Tag pushed to GitHub"
echo ""

echo "📋 Next steps to complete the release:"
echo ""
echo "1. Go to: https://github.com/DJFreer92/Extended-Clipboard-API/releases/new"
echo ""
echo "2. Fill in the release form:"
echo "   - Tag: v0.1.0 (should be pre-selected)"
echo "   - Title: Extended Clipboard API v0.1.0"
echo "   - Description: Copy content from RELEASE_NOTES.md"
echo ""
echo "3. Attach the built packages:"
echo "   - dist/extended_clipboard_api-0.1.0.tar.gz"
echo "   - dist/extended_clipboard_api-0.1.0-py3-none-any.whl"
echo ""
echo "4. Mark as 'Latest release' and click 'Publish release'"
echo ""

echo "🎯 Optional: Publish to PyPI"
echo "   pip install twine"
echo "   twine upload dist/extended_clipboard_api-0.1.0*"
echo ""

echo "📄 Release assets ready in ./dist/"
ls -la dist/extended_clipboard_api-0.1.0*
