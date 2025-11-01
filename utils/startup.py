"""
Utility functions for managing application launch on system startup.
"""

import sys
import os
import subprocess
from pathlib import Path
from core.logger import setup_logger

logger = setup_logger(__name__)


class StartupManager:
    """Manages launch-on-startup functionality across platforms."""

    def __init__(self, app_name="InsightCapsule"):
        self.app_name = app_name
        self.platform = sys.platform

    def is_enabled(self) -> bool:
        """Check if launch on startup is currently enabled."""
        if self.platform == "darwin":  # macOS
            return self._is_enabled_macos()
        elif self.platform == "win32":  # Windows
            return self._is_enabled_windows()
        elif self.platform.startswith("linux"):  # Linux
            return self._is_enabled_linux()
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
            return False

    def enable(self) -> bool:
        """Enable launch on startup."""
        if self.platform == "darwin":
            return self._enable_macos()
        elif self.platform == "win32":
            return self._enable_windows()
        elif self.platform.startswith("linux"):
            return self._enable_linux()
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
            return False

    def disable(self) -> bool:
        """Disable launch on startup."""
        if self.platform == "darwin":
            return self._disable_macos()
        elif self.platform == "win32":
            return self._disable_windows()
        elif self.platform.startswith("linux"):
            return self._disable_linux()
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
            return False

    # === macOS Implementation ===

    def _get_macos_plist_path(self) -> Path:
        """Get the path to the LaunchAgent plist file."""
        home = Path.home()
        launch_agents_dir = home / "Library" / "LaunchAgents"
        return launch_agents_dir / f"com.{self.app_name.lower()}.plist"

    def _is_enabled_macos(self) -> bool:
        """Check if launch agent exists on macOS."""
        return self._get_macos_plist_path().exists()

    def _enable_macos(self) -> bool:
        """Enable launch on startup for macOS using LaunchAgent."""
        try:
            plist_path = self._get_macos_plist_path()
            plist_path.parent.mkdir(parents=True, exist_ok=True)

            # Get the path to the tray_app.py script
            project_root = Path(__file__).parent.parent
            script_path = project_root / "tray_app.py"
            python_path = sys.executable

            # Create the plist content
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{self.app_name.lower()}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>{project_root}/data/logs/startup.log</string>
    <key>StandardErrorPath</key>
    <string>{project_root}/data/logs/startup_error.log</string>
</dict>
</plist>
"""

            # Write the plist file
            with open(plist_path, 'w') as f:
                f.write(plist_content)

            logger.info(f"Created LaunchAgent plist at: {plist_path}")

            # Load the launch agent
            subprocess.run(['launchctl', 'load', str(plist_path)], check=True)
            logger.info("Launch agent loaded successfully")

            return True

        except Exception as e:
            logger.error(f"Failed to enable launch on startup (macOS): {e}", exc_info=True)
            return False

    def _disable_macos(self) -> bool:
        """Disable launch on startup for macOS."""
        try:
            plist_path = self._get_macos_plist_path()

            if not plist_path.exists():
                logger.info("Launch agent not found, nothing to disable")
                return True

            # Unload the launch agent
            try:
                subprocess.run(['launchctl', 'unload', str(plist_path)], check=True)
                logger.info("Launch agent unloaded successfully")
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to unload launch agent: {e}")

            # Remove the plist file
            plist_path.unlink()
            logger.info(f"Removed LaunchAgent plist: {plist_path}")

            return True

        except Exception as e:
            logger.error(f"Failed to disable launch on startup (macOS): {e}", exc_info=True)
            return False

    # === Windows Implementation ===

    def _is_enabled_windows(self) -> bool:
        """Check if startup entry exists in Windows registry."""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, self.app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            logger.error(f"Failed to check Windows registry: {e}")
            return False

    def _enable_windows(self) -> bool:
        """Enable launch on startup for Windows using registry."""
        try:
            import winreg
            project_root = Path(__file__).parent.parent
            script_path = project_root / "tray_app.py"
            python_path = sys.executable

            # Command to run
            command = f'"{python_path}" "{script_path}"'

            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )

            # Set value
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)

            logger.info(f"Added Windows startup entry: {command}")
            return True

        except Exception as e:
            logger.error(f"Failed to enable launch on startup (Windows): {e}", exc_info=True)
            return False

    def _disable_windows(self) -> bool:
        """Disable launch on startup for Windows."""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )

            try:
                winreg.DeleteValue(key, self.app_name)
                logger.info("Removed Windows startup entry")
            except FileNotFoundError:
                logger.info("Startup entry not found, nothing to disable")

            winreg.CloseKey(key)
            return True

        except Exception as e:
            logger.error(f"Failed to disable launch on startup (Windows): {e}", exc_info=True)
            return False

    # === Linux Implementation ===

    def _get_linux_autostart_path(self) -> Path:
        """Get the path to the .desktop file for autostart."""
        config_home = os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))
        autostart_dir = Path(config_home) / 'autostart'
        return autostart_dir / f'{self.app_name.lower()}.desktop'

    def _is_enabled_linux(self) -> bool:
        """Check if autostart file exists on Linux."""
        return self._get_linux_autostart_path().exists()

    def _enable_linux(self) -> bool:
        """Enable launch on startup for Linux using .desktop file."""
        try:
            desktop_path = self._get_linux_autostart_path()
            desktop_path.parent.mkdir(parents=True, exist_ok=True)

            project_root = Path(__file__).parent.parent
            script_path = project_root / "tray_app.py"
            python_path = sys.executable

            # Create .desktop file content
            desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.app_name}
Exec={python_path} {script_path}
Terminal=false
X-GNOME-Autostart-enabled=true
"""

            with open(desktop_path, 'w') as f:
                f.write(desktop_content)

            # Make it executable
            desktop_path.chmod(0o755)

            logger.info(f"Created autostart entry at: {desktop_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to enable launch on startup (Linux): {e}", exc_info=True)
            return False

    def _disable_linux(self) -> bool:
        """Disable launch on startup for Linux."""
        try:
            desktop_path = self._get_linux_autostart_path()

            if not desktop_path.exists():
                logger.info("Autostart entry not found, nothing to disable")
                return True

            desktop_path.unlink()
            logger.info(f"Removed autostart entry: {desktop_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to disable launch on startup (Linux): {e}", exc_info=True)
            return False
