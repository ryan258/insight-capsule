#!/usr/bin/env python
"""
Insight Capsule - System Tray Application
A persistent tray icon for voice-first thought capture.
"""

import pystray
from pystray import MenuItem as Item
from PIL import Image, ImageDraw
import subprocess
import sys
from pathlib import Path
from pynput import keyboard

from pipeline.orchestrator import InsightPipeline
from config.settings import LOGS_DIR
from core.logger import setup_logger
from utils.startup import StartupManager
from agents.drafter import DrafterAgent
from agents.searcher import SearcherAgent
from core.local_generation import HybridGenerator

logger = setup_logger(__name__)


class InsightCapsuleTrayApp:
    """System tray application for Insight Capsule."""

    def __init__(self):
        self.pipeline = InsightPipeline(use_local=True, enable_vector_search=True)
        self.startup_manager = StartupManager("InsightCapsule")

        # Create drafter agent using the same generator as the pipeline
        self.drafter = DrafterAgent(self.pipeline.generator)

        # Create searcher agent if vector store is available
        self.searcher = None
        if self.pipeline.vector_store:
            self.searcher = SearcherAgent(
                vector_store=self.pipeline.vector_store,
                generator=self.pipeline.generator
            )
            logger.info("Searcher agent initialized")

        self.icon = None

        # Track the latest insight for Actions menu
        self.latest_results = None

        # Set up pipeline callbacks
        self.pipeline.on_recording_start = self._on_recording_start
        self.pipeline.on_recording_stop = self._on_recording_stop
        self.pipeline.on_processing_start = self._on_processing_start
        self.pipeline.on_processing_complete = self._on_processing_complete
        self.pipeline.on_error = self._on_error

        # Set up global hotkey listener
        self.hotkey_listener = None
        self._setup_hotkey_listener()

    def _create_icon_image(self, color="blue"):
        """Create a simple icon image for the tray."""
        # Create a 64x64 image with a brain/lightbulb representation
        size = 64
        image = Image.new('RGB', (size, size), color='white')
        dc = ImageDraw.Draw(image)

        # Draw a simple brain/thought bubble icon
        if color == "blue":
            fill_color = (33, 150, 243)  # Blue - idle
        elif color == "red":
            fill_color = (244, 67, 54)  # Red - recording
        elif color == "orange":
            fill_color = (255, 152, 0)  # Orange - processing
        else:
            fill_color = (76, 175, 80)  # Green - success

        # Draw outer circle (thought bubble)
        margin = 8
        dc.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=fill_color,
            outline='black',
            width=2
        )

        # Draw inner "IC" letters for Insight Capsule
        center = size // 2
        # Draw simple geometric pattern instead of text
        # Draw a lightbulb-like shape
        bulb_center_x = center
        bulb_center_y = center - 5
        bulb_radius = 12

        # Bulb (circle)
        dc.ellipse(
            [
                bulb_center_x - bulb_radius,
                bulb_center_y - bulb_radius,
                bulb_center_x + bulb_radius,
                bulb_center_y + bulb_radius
            ],
            fill='white',
            outline='black',
            width=2
        )

        # Base of bulb (rectangle)
        base_width = 8
        base_height = 6
        dc.rectangle(
            [
                bulb_center_x - base_width // 2,
                bulb_center_y + bulb_radius,
                bulb_center_x + base_width // 2,
                bulb_center_y + bulb_radius + base_height
            ],
            fill='white',
            outline='black',
            width=1
        )

        return image

    def _on_recording_start(self):
        """Callback when recording starts."""
        logger.info("Tray: Recording started")
        if self.icon:
            self.icon.icon = self._create_icon_image("red")
            self.icon.title = "Insight Capsule - Recording..."

    def _on_recording_stop(self):
        """Callback when recording stops."""
        logger.info("Tray: Recording stopped")

    def _on_processing_start(self):
        """Callback when processing starts."""
        logger.info("Tray: Processing started")
        if self.icon:
            self.icon.icon = self._create_icon_image("orange")
            self.icon.title = "Insight Capsule - Processing..."

    def _on_processing_complete(self, results):
        """Callback when processing completes."""
        logger.info("Tray: Processing complete")

        # Store the latest results for Actions menu
        self.latest_results = results

        if self.icon:
            self.icon.icon = self._create_icon_image("green")
            self.icon.title = "Insight Capsule - Ready"
            # Return to blue after 2 seconds
            import threading
            threading.Timer(2.0, self._reset_icon).start()

    def _on_error(self, error_msg):
        """Callback when an error occurs."""
        logger.error(f"Tray: Error occurred - {error_msg}")
        if self.icon:
            self.icon.icon = self._create_icon_image("orange")
            self.icon.title = f"Insight Capsule - Error: {error_msg[:30]}"
            # Return to blue after 3 seconds
            import threading
            threading.Timer(3.0, self._reset_icon).start()

    def _reset_icon(self):
        """Reset icon to default state."""
        if self.icon:
            self.icon.icon = self._create_icon_image("blue")
            self.icon.title = "Insight Capsule - Ready"

    def _setup_hotkey_listener(self):
        """Set up the global hotkey listener (Ctrl+Shift+Space)."""
        try:
            # Define the hotkey combination
            hotkey_combination = {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.Key.space}
            currently_pressed = set()

            def on_press(key):
                """Handle key press events."""
                # Add the pressed key to our set
                currently_pressed.add(key)

                # Check if all keys in the hotkey combination are pressed
                if hotkey_combination.issubset(currently_pressed):
                    self._handle_hotkey()

            def on_release(key):
                """Handle key release events."""
                # Remove the released key from our set
                if key in currently_pressed:
                    currently_pressed.remove(key)

            # Start the listener
            self.hotkey_listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release
            )
            self.hotkey_listener.start()
            logger.info("Global hotkey listener started (Ctrl+Shift+Space)")

        except Exception as e:
            logger.error(f"Failed to set up hotkey listener: {e}", exc_info=True)

    def _handle_hotkey(self):
        """Handle the global hotkey press (toggle recording)."""
        try:
            if self.pipeline.is_recording:
                # Stop recording
                logger.info("Hotkey pressed: Stopping recording")
                success = self.pipeline.stop_recording_async()
                if not success:
                    logger.warning("Failed to stop recording via hotkey")
            elif not self.pipeline.is_processing:
                # Start recording (only if not processing)
                logger.info("Hotkey pressed: Starting recording")
                success = self.pipeline.start_recording_async()
                if not success:
                    logger.warning("Failed to start recording via hotkey")
            else:
                logger.info("Hotkey pressed but pipeline is busy processing")

        except Exception as e:
            logger.error(f"Error handling hotkey: {e}", exc_info=True)

    def _start_recording(self, icon, item):
        """Menu action: Start recording."""
        if self.pipeline.is_busy:
            logger.warning("Cannot start recording: pipeline is busy")
            return

        success = self.pipeline.start_recording_async()
        if success:
            logger.info("Recording started from tray menu")
        else:
            logger.error("Failed to start recording from tray menu")

    def _stop_recording(self, icon, item):
        """Menu action: Stop recording."""
        if not self.pipeline.is_recording:
            logger.warning("Cannot stop recording: not currently recording")
            return

        success = self.pipeline.stop_recording_async()
        if success:
            logger.info("Recording stopped from tray menu")
        else:
            logger.error("Failed to stop recording from tray menu")

    def _open_logs(self, icon, item):
        """Menu action: Open logs folder."""
        try:
            logs_path = LOGS_DIR
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', str(logs_path)])
            elif sys.platform == 'win32':  # Windows
                subprocess.run(['explorer', str(logs_path)])
            else:  # Linux
                subprocess.run(['xdg-open', str(logs_path)])
            logger.info(f"Opened logs folder: {logs_path}")
        except Exception as e:
            logger.error(f"Failed to open logs folder: {e}")

    def _toggle_startup(self, icon, item):
        """Menu action: Toggle launch on startup."""
        try:
            if self.startup_manager.is_enabled():
                if self.startup_manager.disable():
                    logger.info("Disabled launch on startup")
                else:
                    logger.error("Failed to disable launch on startup")
            else:
                if self.startup_manager.enable():
                    logger.info("Enabled launch on startup")
                else:
                    logger.error("Failed to enable launch on startup")
        except Exception as e:
            logger.error(f"Error toggling startup: {e}")

    def _generate_blog_outline(self, icon, item):
        """Menu action: Generate blog outline from latest insight."""
        if not self.latest_results or not self.latest_results.get("success"):
            logger.warning("No recent insight available for drafting")
            return

        try:
            capsule = self.latest_results.get("capsule")
            transcript = self.latest_results.get("transcript")

            if not capsule:
                logger.error("No capsule found in latest results")
                return

            logger.info("Generating blog outline...")
            self.tts.speak("Generating blog outline")

            outline = self.drafter.generate_blog_outline(
                capsule=capsule,
                transcript=transcript
            )

            # Save the outline to the same log file
            log_path = self.latest_results.get("log_path")
            if log_path:
                self._append_to_log(log_path, "Blog Outline", outline)
                logger.info(f"Blog outline saved to {log_path}")

            self.tts.speak("Blog outline generated and saved")

        except Exception as e:
            logger.error(f"Error generating blog outline: {e}", exc_info=True)
            self.tts.speak("Error generating blog outline")

    def _generate_first_draft(self, icon, item):
        """Menu action: Generate first draft from latest insight."""
        if not self.latest_results or not self.latest_results.get("success"):
            logger.warning("No recent insight available for drafting")
            return

        try:
            capsule = self.latest_results.get("capsule")
            transcript = self.latest_results.get("transcript")

            if not capsule:
                logger.error("No capsule found in latest results")
                return

            logger.info("Generating first draft...")
            self.tts.speak("Generating first draft")

            draft = self.drafter.generate_first_draft(
                capsule=capsule,
                transcript=transcript
            )

            # Save the draft to the same log file
            log_path = self.latest_results.get("log_path")
            if log_path:
                self._append_to_log(log_path, "First Draft", draft)
                logger.info(f"First draft saved to {log_path}")

            self.tts.speak("First draft generated and saved")

        except Exception as e:
            logger.error(f"Error generating first draft: {e}", exc_info=True)
            self.tts.speak("Error generating first draft")

    def _generate_takeaways(self, icon, item):
        """Menu action: Generate key takeaways from latest insight."""
        if not self.latest_results or not self.latest_results.get("success"):
            logger.warning("No recent insight available for drafting")
            return

        try:
            capsule = self.latest_results.get("capsule")

            if not capsule:
                logger.error("No capsule found in latest results")
                return

            logger.info("Generating key takeaways...")
            self.tts.speak("Generating key takeaways")

            takeaways = self.drafter.generate_key_takeaways(capsule=capsule)

            # Save the takeaways to the same log file
            log_path = self.latest_results.get("log_path")
            if log_path:
                self._append_to_log(log_path, "Key Takeaways", takeaways)
                logger.info(f"Key takeaways saved to {log_path}")

            self.tts.speak("Key takeaways generated and saved")

        except Exception as e:
            logger.error(f"Error generating key takeaways: {e}", exc_info=True)
            self.tts.speak("Error generating key takeaways")

    def _append_to_log(self, log_path: str, section_title: str, content: str):
        """Append a new section to an existing log file."""
        try:
            with open(log_path, 'a') as f:
                f.write(f"\n\n---\n\n## {section_title}\n\n{content}\n")
            logger.info(f"Appended {section_title} to {log_path}")
        except Exception as e:
            logger.error(f"Failed to append to log: {e}")

    def _search_thoughts(self, icon, item):
        """Menu action: Search through past insights."""
        if not self.searcher:
            logger.warning("Search not available: vector store not initialized")
            self.tts.speak("Search is not available")
            return

        try:
            # Get stats
            stats = self.searcher.get_stats()
            total = stats.get("total_insights", 0)

            if total == 0:
                logger.info("No insights in library yet")
                self.tts.speak("You don't have any insights in your library yet")
                return

            # Prompt user for query (via console since we don't have a GUI dialog)
            print("\n" + "="*60)
            print("🔍 SEARCH YOUR INSIGHTS")
            print(f"You have {total} insights in your library")
            print("="*60)
            query = input("Enter your search query (or press Enter to cancel): ").strip()

            if not query:
                logger.info("Search cancelled by user")
                return

            logger.info(f"Searching for: {query}")
            self.tts.speak(f"Searching for {query}")

            # Perform search and synthesize answer
            answer = self.searcher.synthesize_answer(query, n_results=5)

            # Display answer
            print("\n" + "-"*60)
            print("ANSWER:")
            print("-"*60)
            print(answer)
            print("-"*60 + "\n")

            # Speak answer
            self.tts.speak("Here is what I found")
            # For TTS, read just the main answer without sources
            main_answer = answer.split("\n\nSources:")[0]
            self.tts.speak(main_answer)

            logger.info("Search completed successfully")

        except Exception as e:
            logger.error(f"Search error: {e}", exc_info=True)
            self.tts.speak("An error occurred during search")

    def _quit_app(self, icon, item):
        """Menu action: Quit application."""
        logger.info("Quitting Insight Capsule tray app")

        # Stop the hotkey listener
        if self.hotkey_listener and self.hotkey_listener.is_alive():
            self.hotkey_listener.stop()
            logger.info("Hotkey listener stopped")

        icon.stop()

    def _create_menu(self):
        """Create the tray menu."""
        return pystray.Menu(
            Item(
                'Start Recording',
                self._start_recording,
                enabled=lambda item: not self.pipeline.is_busy
            ),
            Item(
                'Stop Recording',
                self._stop_recording,
                enabled=lambda item: self.pipeline.is_recording
            ),
            pystray.Menu.SEPARATOR,
            Item(
                'Search My Thoughts...',
                self._search_thoughts,
                enabled=lambda item: self.searcher is not None
            ),
            pystray.Menu.SEPARATOR,
            Item(
                'Actions',
                pystray.Menu(
                    Item(
                        'Generate Blog Outline',
                        self._generate_blog_outline,
                        enabled=lambda item: self.latest_results is not None
                    ),
                    Item(
                        'Generate First Draft',
                        self._generate_first_draft,
                        enabled=lambda item: self.latest_results is not None
                    ),
                    Item(
                        'Generate Key Takeaways',
                        self._generate_takeaways,
                        enabled=lambda item: self.latest_results is not None
                    )
                )
            ),
            pystray.Menu.SEPARATOR,
            Item('Open Logs Folder', self._open_logs),
            Item(
                'Launch on Startup',
                self._toggle_startup,
                checked=lambda item: self.startup_manager.is_enabled()
            ),
            pystray.Menu.SEPARATOR,
            Item('Quit', self._quit_app)
        )

    def run(self):
        """Start the tray application."""
        logger.info("Starting Insight Capsule tray application")

        # Create the tray icon
        self.icon = pystray.Icon(
            "insight_capsule",
            self._create_icon_image("blue"),
            "Insight Capsule - Ready",
            self._create_menu()
        )

        # Run the icon (this blocks)
        self.icon.run()


def main():
    """Entry point for the tray application."""
    print("🧠 Insight Capsule - Tray Application")
    print("=" * 60)
    print("Starting system tray app...")
    print("Look for the brain icon in your system tray/menu bar.")
    print("=" * 60)

    app = InsightCapsuleTrayApp()

    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Tray app interrupted by user")
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Tray app error: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
