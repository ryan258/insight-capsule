#!/usr/bin/env python
"""
Insight Capsule - Local AI-Powered Thought Pipeline
Simple entry point for the default pipeline.
"""

from pipeline.orchestrator import InsightPipeline

def main():
    print("🧠 Insight Capsule - Voice to Insight Pipeline")
    print("=" * 50)
    
    pipeline = InsightPipeline()
    pipeline.run()

if __name__ == "__main__":
    main()