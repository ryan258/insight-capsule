#!/bin/bash
# Build script for Insight Capsule macOS application

set -e  # Exit on error

echo "================================================"
echo "Building Insight Capsule v1.0.0"
echo "================================================"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This build script is optimized for macOS"
    echo "   The resulting app bundle will only work on macOS"
    echo ""
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist InsightCapsule.app
echo "✓ Cleaned"
echo ""

# Build with PyInstaller
echo "📦 Building application with PyInstaller..."
pyinstaller InsightCapsule.spec

echo ""
echo "✓ Build complete!"
echo ""

# Check if build was successful
if [ -d "dist/InsightCapsule.app" ]; then
    echo "================================================"
    echo "✅ SUCCESS!"
    echo "================================================"
    echo ""
    echo "Your app is ready at: dist/InsightCapsule.app"
    echo ""
    echo "📋 Next steps:"
    echo ""
    echo "1. Test the app:"
    echo "   open dist/InsightCapsule.app"
    echo ""
    echo "2. Install Ollama (if not already installed):"
    echo "   https://ollama.ai"
    echo ""
    echo "3. Pull the required model:"
    echo "   ollama pull llama3.2"
    echo ""
    echo "4. Move to Applications folder:"
    echo "   cp -r dist/InsightCapsule.app /Applications/"
    echo ""
    echo "================================================"
else
    echo "❌ Build failed - app bundle not found"
    exit 1
fi
