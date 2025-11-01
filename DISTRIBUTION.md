# Distribution Guide - Insight Capsule

This guide explains how to build and distribute Insight Capsule as a standalone macOS application.

## **Prerequisites for Building**

Before building the distributable app, ensure you have:

1. **Python 3.11+** with UV package manager
2. **All dependencies installed** (`uv pip install -r requirements.txt`)
3. **macOS** (for building .app bundles)
4. **Ollama installed** on your system (for testing)

## **Building the macOS App**

### **Quick Build**

```bash
# Make the build script executable (first time only)
chmod +x build.sh

# Run the build
./build.sh
```

The script will:
- Clean previous builds
- Run PyInstaller with the spec file
- Create `dist/InsightCapsule.app`
- Provide next steps for installation

### **Manual Build**

If you prefer to build manually:

```bash
# Clean previous builds
rm -rf build dist

# Build with PyInstaller
pyinstaller InsightCapsule.spec

# Your app will be at: dist/InsightCapsule.app
```

## **Testing the Build**

### **1. Launch the App**

```bash
open dist/InsightCapsule.app
```

### **2. Check the System Tray**

Look for the Insight Capsule icon in your menu bar (top-right of screen).

### **3. Test Basic Functionality**

- **Menu Access**: Click the tray icon to see the menu
- **Recording**: Click "Start Recording" or press Ctrl+Shift+Space
- **Processing**: Stop recording and verify the insight is processed
- **Search**: Try "Search My Thoughts..." (after creating a few insights)

### **4. Check Logs**

If something doesn't work, check the logs:

```bash
# Logs are saved in the app's data directory
ls -la dist/InsightCapsule.app/Contents/MacOS/data/logs/
```

## **Installation for End Users**

### **Prerequisites for Users**

Users need:

1. **macOS 10.15+** (Catalina or later)
2. **Ollama** - Local LLM runtime
3. **Microphone access** permission

### **Installation Steps**

#### **Step 1: Install Ollama**

```bash
# Download from https://ollama.ai or use Homebrew
brew install ollama

# Start Ollama
ollama serve &

# Pull the required model
ollama pull llama3.2
```

#### **Step 2: Install Insight Capsule**

```bash
# Copy the app to Applications
cp -r InsightCapsule.app /Applications/

# Launch the app
open /Applications/InsightCapsule.app
```

#### **Step 3: Grant Permissions**

On first launch, macOS will ask for permissions:

1. **Microphone Access** - Click "Allow" to enable voice recording
2. **Accessibility** - Needed for global hotkeys (Ctrl+Shift+Space)
   - Go to System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Insight Capsule to the allowed apps

#### **Step 4: Configure (Optional)**

The app works out of the box, but you can customize:

```bash
# Navigate to the app's data directory
cd ~/Library/Application\ Support/InsightCapsule/

# Copy the example env file
cp .example.env .env

# Edit settings
nano .env
```

Available settings:
- `USE_LOCAL_LLM=true` - Use Ollama (default)
- `LOCAL_LLM_MODEL=llama3.2` - Model to use
- `SILENCE_DETECTION_ENABLED=false` - Auto-stop on silence
- `TTS_ENABLED=true` - Voice feedback

## **Distribution Options**

### **Option 1: Direct Distribution**

Simply zip the app bundle and share it:

```bash
# Create a distributable ZIP
cd dist
zip -r InsightCapsule-v1.0.0-macOS.zip InsightCapsule.app

# Share the ZIP file
```

**Pros**:
- Simple and fast
- Small file size (app uses system Python libs)

**Cons**:
- Users must install Ollama separately
- No automatic updates

### **Option 2: DMG Image** (Recommended)

Create a drag-and-drop installer:

```bash
# Install create-dmg (one time)
brew install create-dmg

# Create DMG
create-dmg \
  --volname "Insight Capsule" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "InsightCapsule.app" 175 120 \
  --hide-extension "InsightCapsule.app" \
  --app-drop-link 425 120 \
  "InsightCapsule-v1.0.0.dmg" \
  "dist/"
```

**Pros**:
- Professional appearance
- Familiar installation process for macOS users
- Can include README and instructions

### **Option 3: Homebrew Cask** (Advanced)

For wider distribution, create a Homebrew cask:

```ruby
# insight-capsule.rb
cask "insight-capsule" do
  version "1.0.0"
  sha256 "..."

  url "https://github.com/yourusername/insight-capsule/releases/download/v#{version}/InsightCapsule.dmg"
  name "Insight Capsule"
  desc "Voice-first thought capture and insight generation"
  homepage "https://github.com/yourusername/insight-capsule"

  depends_on formula: "ollama"

  app "InsightCapsule.app"
end
```

## **Code Signing** (For Distribution Outside the Mac App Store)

To avoid "unidentified developer" warnings:

### **1. Get a Developer ID**

Sign up for the Apple Developer Program ($99/year):
https://developer.apple.com/programs/

### **2. Sign the App**

```bash
# Sign the app bundle
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  dist/InsightCapsule.app

# Verify signature
codesign --verify --verbose=4 dist/InsightCapsule.app
spctl --assess --verbose=4 dist/InsightCapsule.app
```

### **3. Notarize with Apple**

```bash
# Create a ZIP for notarization
ditto -c -k --keepParent dist/InsightCapsule.app InsightCapsule.zip

# Submit for notarization
xcrun notarytool submit InsightCapsule.zip \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --password "app-specific-password"

# Staple the notarization ticket
xcrun stapler staple dist/InsightCapsule.app
```

## **Troubleshooting Distribution Issues**

### **"InsightCapsule.app is damaged and can't be opened"**

This happens if the app wasn't signed. Users can bypass with:

```bash
xattr -cr /Applications/InsightCapsule.app
```

### **App crashes on launch**

Check that all dependencies are bundled:

```bash
# List bundled frameworks
otool -L dist/InsightCapsule.app/Contents/MacOS/InsightCapsule
```

### **Microphone not working**

Ensure `NSMicrophoneUsageDescription` is in the Info.plist (already included in the spec file).

### **Global hotkey not working**

Users need to grant Accessibility permission manually:
- System Preferences → Security & Privacy → Privacy → Accessibility

## **File Size Optimization**

The built app can be large (~500MB+) due to ML models. To reduce size:

### **1. Use UPX Compression** (Already enabled in spec file)

```bash
# Install UPX
brew install upx

# Build with compression (already in spec)
pyinstaller InsightCapsule.spec
```

### **2. Exclude Unnecessary Files**

Edit `InsightCapsule.spec` to exclude more packages:

```python
excludes=['_tkinter', 'tkinter', 'matplotlib', 'notebook', 'jupyter', 'IPython']
```

### **3. Use Smaller Models**

Recommend users pull smaller Ollama models:
- `llama3.2:1b` (1.3GB) instead of `llama3.2` (2GB)
- `tinyllama` (637MB) for testing

## **Support & Documentation**

Include these files with your distribution:

- **README.md** - Quick start guide
- **DISTRIBUTION.md** (this file) - For developers
- **.example.env** - Configuration template
- **LICENSE** - Your chosen license

## **Changelog**

### **v1.0.0** (2025-11-01)
- Initial release
- System tray application with persistent menu
- Global hotkey (Ctrl+Shift+Space)
- Content drafting (blog outlines, first drafts, takeaways)
- Semantic search across insights
- Local-first with Ollama integration
- Cross-platform startup support
