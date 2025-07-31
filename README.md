# Skywalk vs Nothing ENC Performance Test

This repository contains a test script to compare the performance of Skywalk's ENC solution against the native ENC on Elekid (referred to as "Nothing") in terms of Word Error Rate (WER) and Character Error Rate (CER).

## Overview

The test evaluates audio recordings across multiple variables:
- **Languages**: English, English (heavy accent), Chinese, Swedish
- **Speech Types**: Regular indoor speaking, quiet speech, whisper
- **Background Noise**: Nightclub scene, cafe scene, someone else speaking

## File Structure

```
data/
├── skywalk/     # Audio files recorded with Skywalk ENC
└── nothing/     # Audio files recorded with native ENC
```

## Audio File Naming Convention

Audio files should be named using a 3-character code format: `ABC.wav`

Where:
- **A** = Language (A=EN, B=EN_ACCENT, C=CN, D=SV)
- **B** = Speech Type (A=REGULAR, B=QUIET, C=WHISPER)
- **C** = Background (A=NIGHTCLUB, B=CAFE, C=SPEAKING)

### Examples:
- `ACB.wav` = English whisper with cafe background
- `BAA.wav` = English accent regular speech with nightclub background
- `CCB.wav` = Chinese quiet speech with cafe background

## Setup

1. **Install Dependencies**:
   ```bash
   # Option 1: Use the automated setup script
   ./setup.sh
   
   # Option 2: Manual installation
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Prepare Audio Files**:
   - Place Skywalk recordings in `data/skywalk/`
   - Place Nothing recordings in `data/nothing/`
   - Ensure files follow the naming convention above

## Running the Test

```bash
# Activate virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the test
python test_script.py
```

## Quick Usage

```bash
# 1. Setup (if not done already)
./setup.sh

# 2. Activate environment
source venv/bin/activate

# 3. Validate your audio files
python validate_files.py

# 4. Run the test
python test_script.py

# 5. Check results
cat enc_test_report.txt
```

## Output Files

The script generates two output files:

1. **`enc_test_report.txt`**: Human-readable report with:
   - Summary statistics for each system
   - Detailed comparison by test condition
   - Performance breakdown by language
   - Improvement metrics

2. **`enc_test_results.json`**: Detailed JSON results containing:
   - Original reference text
   - Transcribed text
   - WER and CER scores
   - Test conditions for each file

## Test Phrases

The script uses the following reference phrases for each language:

### English
"Hey, just thinking out loud here. I had an idea during my walk—what if we made the intro flow more dynamic? Maybe animations or voice cues? Could be good for first-time users. Also, Marcus still hasn't sent the revised mockups. Need to chase that. Oh, and budget—Jill flagged an inconsistency. Gotta double-check the numbers. Anyway, I'm recording this now so I don't forget later. Testing, testing—how's the clarity? Hopefully background noise is cleaner with the new update. Alright, that's it for now. Saving this and moving on. Add this recording to the work collection."

### Chinese
"刚刚路上突然想到一个点子，录一下以防忘了。那个新手引导是不是可以做得更有互动感一点？比如加点动画或者语音提示，可能对第一次用的用户更友好。然后，马克那边的新版图还没发我，得催一下。还有预算那块，吉尔说有个地方对不上，我回头再核对一下。顺便测试下这个录音效果，新功能应该能降点噪吧？听得清吗？把这份录音添加到工作收藏夹里面。"

### Swedish
"Fick en idé på vägen hem, tänkte spela in innan jag glömmer. Kanske borde vi göra introduktionen lite mer interaktiv? Typ lägga till animationer eller röststöd—kan hjälpa nya användare att fatta snabbare. Förresten, Marcus har fortfarande inte skickat de uppdaterade mockupsen, måste påminna honom. Och budgeten—Jill nämnde att nåt inte stämmer där, jag kollar det sen. Testar ljudet nu också—hörs det klart? Bakgrundsljudet borde vara mindre med nya funktionen. Okej, det var allt för nu. Lägg till det här i arbetskollektionen."

## ASR Model

The test script uses **Whisper V3 Turbo Large** as the universal ASR model for all transcriptions. This ensures:
- Consistent transcription quality across all test conditions
- High accuracy for multiple languages (English, Chinese, Swedish)
- Robust performance with various speech types and background noise
- Fair comparison between Skywalk and Nothing systems

## Metrics Explained

- **WER (Word Error Rate)**: Measures the proportion of words that were incorrectly transcribed
- **CER (Character Error Rate)**: Measures the proportion of characters that were incorrectly transcribed

Lower values indicate better performance.

## Troubleshooting

1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **No Audio Files Found**: Ensure files are in the correct directories and follow naming convention
3. **Transcription Errors**: Check that audio files are valid and not corrupted
4. **Memory Issues**: The script uses Whisper V3 Turbo Large which requires significant memory (8GB+ recommended)
5. **Whisper Model Download**: The first run will download the large-v3 model (~3GB). Ensure stable internet connection

## Example Report Output

```
================================================================================
SKYWALK vs NOTHING ENC PERFORMANCE COMPARISON
================================================================================
Generated: 2024-01-15 14:30:25

SKYWALK SYSTEM:
  Total files processed: 36
  Average WER: 0.1234
  Average CER: 0.0567

NOTHING SYSTEM:
  Total files processed: 36
  Average WER: 0.2345
  Average CER: 0.1234

DETAILED COMPARISON BY TEST CONDITION:
------------------------------------------------------------

Test Condition: EN_REGULAR_NIGHTCLUB
  Skywalk - WER: 0.1000, CER: 0.0500
  Nothing - WER: 0.2000, CER: 0.1000
  Improvement - WER: +0.1000, CER: +0.0500
``` 