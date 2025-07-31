#!/usr/bin/env python3
"""
Demo script to show how the test script works
This creates sample data and runs a demonstration
"""

import os
import json
from pathlib import Path
from test_script import ENCTestEvaluator

def create_sample_data():
    """Create sample data structure for demonstration"""
    print("Creating sample data structure...")
    
    # Create directories
    data_dir = Path("data")
    skywalk_dir = data_dir / "skywalk"
    nothing_dir = data_dir / "nothing"
    
    skywalk_dir.mkdir(parents=True, exist_ok=True)
    nothing_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample files (empty files for demo)
    sample_files = [
        "AAA.wav",  # EN REGULAR NIGHTCLUB
        "AAB.wav",  # EN REGULAR CAFE
        "AAC.wav",  # EN REGULAR SPEAKING
        "ABA.wav",  # EN QUIET NIGHTCLUB
        "ABB.wav",  # EN QUIET CAFE
        "ABC.wav",  # EN WHISPER CAFE
        "CAA.wav",  # CN REGULAR NIGHTCLUB
        "CBB.wav",  # CN QUIET CAFE
        "DCC.wav",  # SV WHISPER SPEAKING
    ]
    
    for filename in sample_files:
        # Create empty files for demo
        (skywalk_dir / filename).touch()
        (nothing_dir / filename).touch()
    
    print(f"Created {len(sample_files)} sample files in each directory")
    print("Note: These are empty files for demonstration purposes")
    print("In real usage, these would be actual audio recordings")

def run_demo():
    """Run a demonstration of the test script"""
    print("=" * 60)
    print("SKYWALK vs NOTHING ENC TEST - DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Create sample data
    create_sample_data()
    print()
    
    # Initialize evaluator
    evaluator = ENCTestEvaluator()
    
    # Show what the script would do
    print("What the test script does:")
    print("1. Scans data/skywalk/ and data/nothing/ for audio files")
    print("2. Parses filenames to determine test conditions")
    print("3. Transcribes audio using Whisper V3 Turbo Large")
    print("4. Compares transcriptions with reference text")
    print("5. Calculates WER and CER metrics")
    print("6. Generates comparison report")
    print()
    
    # Show filename parsing
    print("Filename parsing example:")
    test_filename = "ACB.wav"
    conditions = evaluator.parse_filename(test_filename)
    print(f"  Filename: {test_filename}")
    print(f"  Language: {conditions['language']}")
    print(f"  Speech Type: {conditions['speech_type']}")
    print(f"  Background: {conditions['background']}")
    print()
    
    # Show reference text
    print("Reference texts available:")
    for lang, text in evaluator.test_phrases.items():
        print(f"  {lang}: {text[:50]}...")
    print()
    
    print("To run the actual test:")
    print("1. Replace empty files with real audio recordings")
    print("2. Run: python test_script.py")
    print("3. Check enc_test_report.txt for results")

if __name__ == "__main__":
    run_demo() 