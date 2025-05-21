# test_tts.py (Enhanced Diagnostics Version)
import pyttsx3 # This should import the installed library

def run_tts_diagnostics():
    print("--- Starting TTS Diagnostics ---")
    
    engine = None
    initialized_driver_name = "None"

    # 1. Initialization Phase
    print("\nPHASE 1: TTS Engine Initialization")
    try:
        print("Attempting to initialize TTS engine (default driver)...")
        # We are calling pyttsx3.init() here, relying on the global import
        engine = pyttsx3.init() 
        initialized_driver_name = engine.getProperty('driverName') if hasattr(engine, 'getProperty') else "default (unknown specific)"
        print(f"SUCCESS: TTS Engine initialized with driver: {initialized_driver_name}")
    except Exception as e_default:
        print(f"ERROR (Default Driver): Failed to initialize - {e_default}")
        print("Attempting to initialize with SAPI5 explicitly...")
        try:
            # We are calling pyttsx3.init() here, relying on the global import
            engine = pyttsx3.init(driverName='sapi5')
            initialized_driver_name = "sapi5"
            print(f"SUCCESS: TTS Engine initialized explicitly with driver: {initialized_driver_name}")
        except Exception as e_sapi:
            print(f"ERROR (SAPI5 Driver): Failed to initialize - {e_sapi}")
            print("CRITICAL: No TTS engine could be initialized. Cannot proceed with further tests.")
            return # Exit if no engine

    if not engine:
        print("CRITICAL: Engine object is None after initialization attempts. Cannot proceed.")
        return

    # 2. Engine Properties Phase
    print(f"\nPHASE 2: Fetching Engine Properties (Driver: {initialized_driver_name})")
    try:
        print("Attempting to get 'rate' property...")
        rate = engine.getProperty('rate')
        print(f"  SUCCESS: Default Rate = {rate}")
    except Exception as e:
        print(f"  ERROR: Could not get 'rate' property - {e}")

    try:
        print("Attempting to get 'volume' property...")
        volume = engine.getProperty('volume')
        print(f"  SUCCESS: Default Volume = {volume}")
    except Exception as e:
        print(f"  ERROR: Could not get 'volume' property - {e}")
    
    try:
        print("Attempting to get 'voice' (current voice ID) property...")
        voice_id = engine.getProperty('voice')
        print(f"  SUCCESS: Default Voice ID = {voice_id}")
    except Exception as e:
        print(f"  ERROR: Could not get 'voice' property - {e}")

    # 3. Voices Listing Phase
    print("\nPHASE 3: Listing Available Voices")
    voices = [] # Initialize to empty list
    try:
        print("Attempting to get 'voices' property...")
        voices = engine.getProperty('voices')
        if voices:
            print(f"  SUCCESS: Found {len(voices)} voice(s).")
            for i, voice_obj in enumerate(voices): # renamed 'voice' to 'voice_obj' to avoid any confusion
                print(f"  Voice {i}:")
                try:
                    print(f"    ID: {voice_obj.id}")
                except Exception as e_vid:
                    print(f"    ERROR fetching ID: {e_vid}")
                try:
                    print(f"    Name: {voice_obj.name}")
                except Exception as e_vname:
                    print(f"    ERROR fetching Name: {e_vname}")
                try:
                    print(f"    Languages: {voice_obj.languages}")
                except AttributeError: 
                    print(f"    Languages: Not available via this attribute")
                except Exception as e_vlang:
                    print(f"    ERROR fetching Languages: {e_vlang}")
                try:
                    print(f"    Gender: {voice_obj.gender}")
                except AttributeError:
                    print(f"    Gender: Not available via this attribute")
                except Exception as e_vgender:
                    print(f"    ERROR fetching Gender: {e_vgender}")
        else:
            print("  INFO: No voices found or returned by the engine.")
    except Exception as e:
        print(f"  ERROR: Could not get 'voices' property - {e}")

    # 4. Speaking Test Phase
    print("\nPHASE 4: Speaking Test")
    print("---------------------------------------------------------------------")
    print("IMPORTANT PRE-TEST CHECKS:")
    print("  1. Ensure your speakers (or Bluetooth speaker) are ON and CONNECTED.")
    print("  2. Verify it's set as the DEFAULT audio output device in Windows Sound Settings.")
    print("  3. Test sound from another application (e.g., YouTube) RIGHT NOW to confirm general audio output.")
    print("---------------------------------------------------------------------")
    input("Press [Enter] once you've checked the above points to start the speaking test...")
    
    text_to_say = "Hello, this is a detailed pyttsx3 voice test. Can you hear this message?"
    print(f"Attempting to speak: '{text_to_say}'")
    
    if voices:
        try:
            print(f"Attempting to set voice to the first available: {voices[0].id}")
            engine.setProperty('voice', voices[0].id)
            print("  SUCCESS: Set voice.")
        except Exception as e_setvoice:
            print(f"  WARNING: Could not set voice to {voices[0].id} - {e_setvoice}. Using default.")

    try:
        print("Calling engine.say()...")
        engine.say(text_to_say)
        print("  SUCCESS: engine.say() called.")
    except Exception as e_say:
        print(f"  ERROR: engine.say() failed - {e_say}")
        print("Speaking test cannot continue if say() failed.")
        # Do not return here, proceed to runAndWait if say didn't hard error
        # return # Commented out return to allow runAndWait to be attempted unless say truly bails

    try:
        print("Calling engine.runAndWait() - This is where it might hang or fail silently...")
        engine.runAndWait()
        print("  SUCCESS: engine.runAndWait() completed.")
        print("  IMPORTANT: Did you hear any audio? Please verify.")
    except RuntimeError as re_run:
        print(f"  ERROR (RuntimeError): engine.runAndWait() failed - {re_run}")
    except Exception as e_run:
        print(f"  ERROR (Exception): engine.runAndWait() failed - {e_run}")

    # 5. Driver Info Phase (Informational)
    print("\nPHASE 5: Listing Available pyttsx3 Driver Modules (Informational)")
    try:
        # This 'import pyttsx3.drivers' accesses a submodule of the globally imported 'pyttsx3'
        # It does not redefine or shadow the global 'pyttsx3' module itself.
        import pyttsx3.drivers 
        print(f"  Available driver modules listed in pyttsx3.drivers: {pyttsx3.drivers.__all__}")
    except ImportError:
        print("  INFO: Could not import pyttsx3.drivers module.")
    except AttributeError:
        print("  INFO: pyttsx3.drivers module does not have an __all__ attribute (or similar for listing).")
    except Exception as e_drivers:
        print(f"  ERROR trying to list drivers: {e_drivers}")

    print("\n--- TTS Diagnostics Finished ---")

if __name__ == '__main__':
    run_tts_diagnostics()
    input("Diagnostics complete. Press Enter to exit.")