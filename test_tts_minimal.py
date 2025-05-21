# test_tts_minimal.py
print("--- Starting Minimal TTS Test ---")

print("STEP 1: Attempting to import pyttsx3...")
try:
    import pyttsx3
    print("  SUCCESS: pyttsx3 imported.")
except Exception as e_import:
    print(f"  CRITICAL ERROR: Failed to import pyttsx3 - {e_import}")
    print("  Cannot proceed. This indicates a problem with your Python environment or pyttsx3 installation.")
    input("Press Enter to exit.")
    exit()

print("\nSTEP 2: Attempting to initialize TTS engine directly at top level...")
engine = None
try:
    # This is called directly in the global scope, immediately after import.
    engine = pyttsx3.init() 
    
    if engine:
        print("  SUCCESS: pyttsx3.init() called and returned an engine object.")
        
        # Optional: Try getting a property
        try:
            rate = engine.getProperty('rate')
            print(f"    Engine rate: {rate}")
        except Exception as e_prop:
            print(f"    WARNING: Could not get engine property (e.g., rate) - {e_prop}")

        # Optional: Try a very simple speak operation
        print("\nSTEP 3: Attempting a simple speak operation...")
        print("  IMPORTANT: Please ensure your audio output (e.g., Bluetooth speaker) is connected,")
        print("  set as default in Windows, and tested with another sound source (like YouTube) NOW.")
        input("  Press [Enter] to attempt speaking...")
        
        text_to_say = "Minimal test."
        print(f"  Calling say() with: '{text_to_say}'")
        engine.say(text_to_say)
        
        print("  Calling runAndWait()... (If this hangs, you may need to manually stop the script)")
        engine.runAndWait()
        print("  SUCCESS: runAndWait() completed.")
        print("  QUESTION: Did you hear any audio?")
        
    else:
        print("  ERROR: pyttsx3.init() did not return an engine object (it returned None).")
        print("  This can happen if no suitable TTS drivers are found or if there's a configuration issue.")

except Exception as e_init_or_speak:
    print(f"  CRITICAL ERROR: An exception occurred during pyttsx3.init() or a subsequent operation - {e_init_or_speak}")
    print("  This suggests a problem with the TTS engine on your system, the pyttsx3 library's interaction with it, or system permissions.")

print("\n--- Minimal TTS Test Finished ---")
input("Press Enter to exit.")