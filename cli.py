import argparse
import sys
from pathlib import Path
from pipeline.orchestrator import InsightPipeline
from utils.helpers import validate_environment

def main():
    parser = argparse.ArgumentParser(description="Insight Capsule - Voice to Insight Pipeline")
    parser.add_argument(
        "--audio", 
        type=str, 
        help="Path to pre-recorded audio file (skip recording step)"
    )
    parser.add_argument(
        "--no-tts", 
        action="store_true", 
        help="Disable text-to-speech output"
    )
    parser.add_argument(
        "--whisper-model",
        type=str,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size to use"
    )
    parser.add_argument(
        "--whisper-model",
        type=str,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size to use"
    )
    parser.add_argument(
        "--external-llm",
        action="store_true",
        help="Use external OpenAI models instead of local LLM"
    )
    args = parser.parse_args()
    
    # Validate environment
    issues = validate_environment()
    if issues:
        print("⚠️  Environment issues detected:")
        for issue in issues:
            print(f"   - {issue}")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Configure based on arguments
    if args.no_tts:
        from config import settings
        settings.TTS_ENABLED = False
    
    if args.whisper_model:
        from config import settings
        settings.WHISPER_MODEL = args.whisper_model
    
    # Run pipeline
    try:
        pipeline = InsightPipeline()
        
        audio_path = Path(args.audio) if args.audio else None
        if audio_path and not audio_path.exists():
            print(f"Error: Audio file not found: {audio_path}")
            return 1
        
        results = pipeline.run(audio_path)
        
        # Display results
        if results["success"]:
            print("\n📊 Pipeline Results:")
            print(f"  ✓ Transcript: {len(results['transcript'].split())} words")
            print(f"  ✓ Brief Title: {results['brief'].get('title', 'N/A')}")
            print(f"  ✓ Capsule: {len(results['capsule'].split())} words")
            print(f"  ✓ Log saved: {results['log_path']}")
            return 0
        else:
            print(f"\n❌ Pipeline failed: {results['error']}")
            return 1
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
