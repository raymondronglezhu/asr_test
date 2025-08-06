#!/usr/bin/env python3
"""
Demo Simple ASR Script - Shows functionality without requiring audio files
This demonstrates the simplified ASR workflow for single file processing
"""

import sys
import argparse
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DemoSimpleASR:
    def __init__(self):
        # Reference texts for different languages
        self.reference_texts = {
            'EN': "Hey, just thinking out loud here. I had an idea during my walk—what if we made the intro flow more dynamic? Maybe animations or voice cues? Could be good for first-time users. Also, Marcus still hasn't sent the revised mockups. Need to chase that. Oh, and budget—Jill flagged an inconsistency. Gotta double-check the numbers. Anyway, I'm recording this now so I don't forget later. Testing, testing—how's the clarity? Hopefully background noise is cleaner with the new update. Alright, that's it for now. Saving this and moving on. Add this recording to the work collection.",
            'CN': "刚刚路上突然想到一个点子，录一下以防忘了。那个新手引导是不是可以做得更有互动感一点？比如加点动画或者语音提示，可能对第一次用的用户更友好。然后，马克那边的新版图还没发我，得催一下。还有预算那块，吉尔说有个地方对不上，我回头再核对一下。顺便测试下这个录音效果，新功能应该能降点噪吧？听得清吗？把这份录音添加到工作收藏夹里面。",
            'SV': "Fick en idé på vägen hem, tänkte spela in innan jag glömmer. Kanske borde vi göra introduktionen lite mer interaktiv? Typ lägga till animationer eller röststöd—kan hjälpa nya användare att fatta snabbare. Förresten, Marcus har fortfarande inte skickat de uppdaterade mockupsen, måste påminna honom. Och budgeten—Jill nämnde att nåt inte stämmer där, jag kollar det sen. Testar ljudet nu också—hörs det klart? Bakgrundsljudet borde vara mindre med nya funktionen. Okej, det var allt för nu. Lägg till det här i arbetskollektionen."
        }
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        try:
            import jiwer
            logger.info("All required dependencies are available")
            return True
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            logger.info("Please install required packages: pip install jiwer")
            return False
    
    def detect_language_from_filename(self, filename: str) -> str:
        """Detect language from filename (first character)"""
        name = Path(filename).stem.upper()
        if len(name) >= 1:
            language_code = name[0]
            language_map = {'A': 'EN', 'B': 'EN', 'C': 'CN', 'D': 'SV'}
            return language_map.get(language_code, 'EN')
        return 'EN'  # Default to English
    
    def compute_wer(self, reference: str, hypothesis: str) -> float:
        """Compute Word Error Rate"""
        try:
            import jiwer
            transformation = jiwer.Compose([
                jiwer.ToLowerCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.Strip(),
                jiwer.RemovePunctuation()
            ])
            
            reference_clean = transformation(reference)
            hypothesis_clean = transformation(hypothesis)
            
            if not reference_clean:
                return 1.0
            
            return jiwer.wer(reference_clean, hypothesis_clean)
        except Exception as e:
            logger.error(f"Error computing WER: {e}")
            return 1.0
    
    def compute_cer(self, reference: str, hypothesis: str) -> float:
        """Compute Character Error Rate"""
        try:
            import jiwer
            transformation = jiwer.Compose([
                jiwer.ToLowerCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.Strip(),
                jiwer.RemovePunctuation()
            ])
            
            reference_clean = transformation(reference)
            hypothesis_clean = transformation(hypothesis)
            
            if not reference_clean:
                return 1.0
            
            return jiwer.cer(reference_clean, hypothesis_clean)
        except Exception as e:
            logger.error(f"Error computing CER: {e}")
            return 1.0
    
    def process_audio_file(self, audio_path: str, reference_text: str = None, demo_mode: bool = True) -> dict:
        """Process a single audio file and return results"""
        audio_path = Path(audio_path)
        
        if not audio_path.exists() and not demo_mode:
            logger.error(f"Audio file not found: {audio_path}")
            return None
        
        # Detect language if reference text not provided
        if reference_text is None:
            language = self.detect_language_from_filename(audio_path.name)
            reference_text = self.reference_texts.get(language, self.reference_texts['EN'])
            logger.info(f"Detected language: {language}")
        
        if demo_mode:
            # Demo mode: simulate transcription based on filename
            logger.info(f"DEMO MODE: Simulating transcription for {audio_path.name}")
            
            # Generate a simulated transcription with some errors
            if 'A' in audio_path.name:  # English
                transcription = "Hey, just thinking out loud here. I had an idea during my walk—what if we made the intro flow more dynamic? Maybe animations or voice cues? Could be good for first-time users. Also, Marcus still hasn't sent the revised mockups. Need to chase that. Oh, and budget—Jill flagged an inconsistency. Gotta double-check the numbers. Anyway, I'm recording this now so I don't forget later. Testing, testing—how's the clarity? Hopefully background noise is cleaner with the new update. Alright, that's it for now. Saving this and moving on. Add this recording to the work collection."
            elif 'C' in audio_path.name:  # Chinese
                transcription = "刚刚路上突然想到一个点子，录一下以防忘了。那个新手引导是不是可以做得更有互动感一点？比如加点动画或者语音提示，可能对第一次用的用户更友好。然后，马克那边的新版图还没发我，得催一下。还有预算那块，吉尔说有个地方对不上，我回头再核对一下。顺便测试下这个录音效果，新功能应该能降点噪吧？听得清吗？把这份录音添加到工作收藏夹里面。"
            else:  # Swedish
                transcription = "Fick en idé på vägen hem, tänkte spela in innan jag glömmer. Kanske borde vi göra introduktionen lite mer interaktiv? Typ lägga till animationer eller röststöd—kan hjälpa nya användare att fatta snabbare. Förresten, Marcus har fortfarande inte skickat de uppdaterade mockupsen, måste påminna honom. Och budgeten—Jill nämnde att nåt inte stämmer där, jag kollar det sen. Testar ljudet nu också—hörs det klart? Bakgrundsljudet borde vara mindre med nya funktionen. Okej, det var allt för nu. Lägg till det här i arbetskollektionen."
        else:
            # Real mode: would use Whisper for transcription
            logger.info("Loading Whisper model...")
            logger.info(f"Transcribing: {audio_path}")
            # This would be the actual Whisper transcription
            transcription = "Demo transcription - replace with actual Whisper output"
        
        # Compute metrics
        wer = self.compute_wer(reference_text, transcription)
        cer = self.compute_cer(reference_text, transcription)
        
        return {
            'filename': audio_path.name,
            'reference_text': reference_text,
            'transcription': transcription,
            'wer': wer,
            'cer': cer,
            'demo_mode': demo_mode
        }

def main():
    parser = argparse.ArgumentParser(description='Demo Simple ASR with WER/CER calculation')
    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('--reference', '-r', help='Reference text (optional, will auto-detect from filename)')
    parser.add_argument('--output', '-o', help='Output file for results (optional)')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (simulate transcription)')
    
    args = parser.parse_args()
    
    # Initialize ASR
    asr = DemoSimpleASR()
    
    # Check dependencies
    if not asr.check_dependencies():
        sys.exit(1)
    
    # Process audio file
    logger.info(f"Processing: {args.audio_file}")
    results = asr.process_audio_file(args.audio_file, args.reference, args.demo)
    
    if results is None:
        logger.error("Failed to process audio file")
        sys.exit(1)
    
    # Print results
    print("\n" + "="*60)
    print("ASR RESULTS")
    print("="*60)
    print(f"File: {results['filename']}")
    print(f"WER: {results['wer']:.4f}")
    print(f"CER: {results['cer']:.4f}")
    if results.get('demo_mode'):
        print("(DEMO MODE - Simulated transcription)")
    print("\nReference Text:")
    print(f"{results['reference_text']}")
    print("\nTranscription:")
    print(f"{results['transcription']}")
    print("="*60)
    
    # Save to file if requested
    if args.output:
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {args.output}")

if __name__ == "__main__":
    main() 