#!/usr/bin/env python3
"""
Validation script to check audio file naming convention
"""

import os
from pathlib import Path
from typing import Dict, List

def validate_filename(filename: str) -> Dict:
    """Validate a single filename against the naming convention"""
    name = Path(filename).stem.upper()
    
    if len(name) != 3:
        return {
            'valid': False,
            'error': f"Filename must be exactly 3 characters, got {len(name)}"
        }
    
    # Check each character
    language_code = name[0]
    speech_code = name[1]
    background_code = name[2]
    
    language_map = {'A': 'EN', 'B': 'EN_ACCENT', 'C': 'CN', 'D': 'SV'}
    speech_map = {'A': 'REGULAR', 'B': 'QUIET', 'C': 'WHISPER'}
    background_map = {'A': 'NIGHTCLUB', 'B': 'CAFE', 'C': 'SPEAKING'}
    
    errors = []
    
    if language_code not in language_map:
        errors.append(f"Invalid language code '{language_code}'. Must be A, B, C, or D")
    
    if speech_code not in speech_map:
        errors.append(f"Invalid speech code '{speech_code}'. Must be A, B, or C")
    
    if background_code not in background_map:
        errors.append(f"Invalid background code '{background_code}'. Must be A, B, or C")
    
    if errors:
        return {
            'valid': False,
            'error': '; '.join(errors)
        }
    
    return {
        'valid': True,
        'language': language_map[language_code],
        'speech_type': speech_map[speech_code],
        'background': background_map[background_code]
    }

def check_directory(directory: Path) -> Dict:
    """Check all audio files in a directory"""
    if not directory.exists():
        return {
            'exists': False,
            'error': f"Directory {directory} does not exist"
        }
    
    audio_extensions = ['.wav', '.mp3', '.m4a', '.flac']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(directory.glob(f"*{ext}"))
    
    results = {
        'exists': True,
        'total_files': len(audio_files),
        'valid_files': 0,
        'invalid_files': [],
        'valid_files_details': []
    }
    
    for audio_file in audio_files:
        validation = validate_filename(audio_file.name)
        if validation['valid']:
            results['valid_files'] += 1
            results['valid_files_details'].append({
                'filename': audio_file.name,
                'language': validation['language'],
                'speech_type': validation['speech_type'],
                'background': validation['background']
            })
        else:
            results['invalid_files'].append({
                'filename': audio_file.name,
                'error': validation['error']
            })
    
    return results

def main():
    """Main validation function"""
    print("Audio File Validation")
    print("====================")
    print()
    
    data_dir = Path("data")
    
    for system in ['skywalk', 'nothing']:
        system_dir = data_dir / system
        print(f"Checking {system.upper()} directory...")
        
        results = check_directory(system_dir)
        
        if not results['exists']:
            print(f"  ❌ {results['error']}")
            print()
            continue
        
        print(f"  📁 Directory: {system_dir}")
        print(f"  📊 Total files: {results['total_files']}")
        print(f"  ✅ Valid files: {results['valid_files']}")
        print(f"  ❌ Invalid files: {len(results['invalid_files'])}")
        
        if results['valid_files'] > 0:
            print("\n  Valid files:")
            for file_info in results['valid_files_details']:
                print(f"    ✅ {file_info['filename']} ({file_info['language']} {file_info['speech_type']} {file_info['background']})")
        
        if results['invalid_files']:
            print("\n  Invalid files:")
            for file_info in results['invalid_files']:
                print(f"    ❌ {file_info['filename']}: {file_info['error']}")
        
        print()
    
    # Summary
    print("Naming Convention Reference:")
    print("===========================")
    print("Format: ABC.wav where:")
    print("  A = Language: A=EN, B=EN_ACCENT, C=CN, D=SV")
    print("  B = Speech: A=REGULAR, B=QUIET, C=WHISPER")
    print("  C = Background: A=NIGHTCLUB, B=CAFE, C=SPEAKING")
    print()
    print("Examples:")
    print("  ACB.wav = English whisper with cafe background")
    print("  BAA.wav = English accent regular speech with nightclub background")
    print("  CCB.wav = Chinese quiet speech with cafe background")

if __name__ == "__main__":
    main() 