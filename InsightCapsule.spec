# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Insight Capsule
Builds a macOS .app bundle with all dependencies
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect data files from various packages
datas = []
datas += collect_data_files('sentence_transformers', include_py_files=True)
datas += collect_data_files('transformers', include_py_files=True)
datas += collect_data_files('tiktoken')
datas += collect_data_files('chromadb')

# Add our .env.example file
datas += [('.example.env', '.')]

# Collect all submodules that might be dynamically imported
hiddenimports = []
hiddenimports += collect_submodules('sentence_transformers')
hiddenimports += collect_submodules('transformers')
hiddenimports += collect_submodules('tiktoken')
hiddenimports += collect_submodules('chromadb')
hiddenimports += collect_submodules('onnxruntime')
hiddenimports += collect_submodules('sklearn')
hiddenimports += collect_submodules('scipy')
hiddenimports += ['pynput.keyboard._darwin', 'pynput.mouse._darwin']

# Additional imports that PyInstaller might miss
hiddenimports += [
    'pkg_resources.py2_warn',
    'PIL._tkinter_finder',
    'sklearn.utils._typedefs',
    'sklearn.utils._heap',
    'sklearn.utils._sorting',
    'sklearn.utils._vector_sentinel',
    'sklearn.neighbors._partition_nodes',
]

a = Analysis(
    ['tray_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_tkinter', 'tkinter', 'matplotlib', 'notebook', 'jupyter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='InsightCapsule',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: Add an .icns file later
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InsightCapsule',
)

app = BUNDLE(
    coll,
    name='InsightCapsule.app',
    icon=None,  # TODO: Add an .icns file later
    bundle_identifier='com.ryanleej.insightcapsule',
    version='1.0.0',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025 Ryan Lee Johnson',
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,  # Show in Dock
        'NSMicrophoneUsageDescription': 'Insight Capsule needs microphone access to record your voice insights.',
        'NSAppleEventsUsageDescription': 'Insight Capsule needs accessibility access for global hotkeys.',
    },
)
