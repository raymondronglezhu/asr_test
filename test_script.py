#!/usr/bin/env python3
"""
Test Script for Skywalk vs Nothing ENC Performance Comparison
Computes WER (Word Error Rate) and CER (Character Error Rate) metrics

Uses Whisper V3 Turbo Large as the universal ASR model for consistent,
high-quality transcription across all test conditions.
"""

import os
import json
import subprocess
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ENCTestEvaluator:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.skywalk_dir = self.data_dir / "skywalk"
        self.nothing_dir = self.data_dir / "nothing"
        
        # Test phrases in different languages
        self.test_phrases = {
            'EN': "Hey, just thinking out loud here. I had an idea during my walk—what if we made the intro flow more dynamic? Maybe animations or voice cues? Could be good for first-time users. Also, Marcus still hasn't sent the revised mockups. Need to chase that. Oh, and budget—Jill flagged an inconsistency. Gotta double-check the numbers. Anyway, I'm recording this now so I don't forget later. Testing, testing—how's the clarity? Hopefully background noise is cleaner with the new update. Alright, that's it for now. Saving this and moving on. Add this recording to the work collection.",
            'CN': "刚刚路上突然想到一个点子，录一下以防忘了。那个新手引导是不是可以做得更有互动感一点？比如加点动画或者语音提示，可能对第一次用的用户更友好。然后，马克那边的新版图还没发我，得催一下。还有预算那块，吉尔说有个地方对不上，我回头再核对一下。顺便测试下这个录音效果，新功能应该能降点噪吧？听得清吗？把这份录音添加到工作收藏夹里面。",
            'SV': "Fick en idé på vägen hem, tänkte spela in innan jag glömmer. Kanske borde vi göra introduktionen lite mer interaktiv? Typ lägga till animationer eller röststöd—kan hjälpa nya användare att fatta snabbare. Förresten, Marcus har fortfarande inte skickat de uppdaterade mockupsen, måste påminna honom. Och budgeten—Jill nämnde att nåt inte stämmer där, jag kollar det sen. Testar ljudet nu också—hörs det klart? Bakgrundsljudet borde vara mindre med nya funktionen. Okej, det var allt för nu. Lägg till det här i arbetskollektionen."
        }
        
        # Test conditions mapping
        self.languages = ['EN', 'EN_ACCENT', 'CN', 'SV']
        self.speech_types = ['REGULAR', 'QUIET', 'WHISPER']
        self.backgrounds = ['NIGHTCLUB', 'CAFE', 'SPEAKING']
        
        self.results = {
            'skywalk': {},
            'nothing': {}
        }
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        try:
            # Check for speech recognition libraries
            import speech_recognition
            import jiwer
            import whisper
            logger.info("All required dependencies are available")
            return True
        except ImportError as e:
            logger.error(f"Missing dependency: {e}")
            logger.info("Please install required packages: pip install SpeechRecognition jiwer openai-whisper")
            return False
    
    def get_audio_files(self, system: str) -> List[Path]:
        """Get all audio files from the specified system directory"""
        system_dir = self.data_dir / system
        if not system_dir.exists():
            logger.warning(f"Directory {system_dir} does not exist")
            return []
        
        audio_files = []
        for ext in ['*.wav', '*.mp3', '*.m4a', '*.flac']:
            audio_files.extend(system_dir.glob(ext))
        
        logger.info(f"Found {len(audio_files)} audio files in {system}")
        return audio_files
    
    def parse_filename(self, filename: str) -> Dict[str, str]:
        """Parse filename to extract test conditions (e.g., ACB.wav -> A=EN, C=QUIET, B=CAFE)"""
        # Remove extension
        name = Path(filename).stem.upper()
        
        if len(name) != 3:
            logger.warning(f"Invalid filename format: {filename}")
            return {}
        
        # Parse the three-character code
        language_code = name[0]
        speech_code = name[1]
        background_code = name[2]
        
        # Map codes to conditions
        language_map = {'A': 'EN', 'B': 'EN_ACCENT', 'C': 'CN', 'D': 'SV'}
        speech_map = {'A': 'REGULAR', 'B': 'QUIET', 'C': 'WHISPER'}
        background_map = {'A': 'NIGHTCLUB', 'B': 'CAFE', 'C': 'SPEAKING'}
        
        return {
            'language': language_map.get(language_code, 'UNKNOWN'),
            'speech_type': speech_map.get(speech_code, 'UNKNOWN'),
            'background': background_map.get(background_code, 'UNKNOWN'),
            'filename': filename
        }
    
    def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio file using Whisper V3 Turbo Large"""
        try:
            import whisper
            # Use Whisper V3 Turbo Large for consistent high-quality transcription
            model = whisper.load_model("large-v3")
            result = model.transcribe(str(audio_path))
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Error transcribing {audio_path}: {e}")
            return ""
    
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
    
    def evaluate_system(self, system: str) -> Dict:
        """Evaluate all audio files for a given system"""
        logger.info(f"Evaluating system: {system}")
        
        audio_files = self.get_audio_files(system)
        system_results = {}
        
        for audio_file in audio_files:
            logger.info(f"Processing: {audio_file.name}")
            
            # Parse filename to get test conditions
            conditions = self.parse_filename(audio_file.name)
            if not conditions:
                continue
            
            # Get reference text based on language
            language = conditions['language']
            if language == 'EN_ACCENT':
                language = 'EN'  # Use same reference text for accent
            
            reference_text = self.test_phrases.get(language, "")
            if not reference_text:
                logger.warning(f"No reference text for language: {language}")
                continue
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_file)
            if not transcription:
                logger.warning(f"Failed to transcribe: {audio_file.name}")
                continue
            
            # Compute metrics
            wer = self.compute_wer(reference_text, transcription)
            cer = self.compute_cer(reference_text, transcription)
            
            # Store results
            test_key = f"{conditions['language']}_{conditions['speech_type']}_{conditions['background']}"
            system_results[test_key] = {
                'filename': audio_file.name,
                'reference': reference_text,
                'transcription': transcription,
                'wer': wer,
                'cer': cer,
                'conditions': conditions
            }
            
            logger.info(f"WER: {wer:.4f}, CER: {cer:.4f} for {audio_file.name}")
        
        return system_results
    
    def generate_report(self) -> str:
        """Generate comprehensive comparison report"""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("SKYWALK vs NOTHING ENC PERFORMANCE COMPARISON")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary statistics
        for system in ['skywalk', 'nothing']:
            if system in self.results and self.results[system]:
                total_files = len(self.results[system])
                avg_wer = sum(r['wer'] for r in self.results[system].values()) / total_files
                avg_cer = sum(r['cer'] for r in self.results[system].values()) / total_files
                
                report_lines.append(f"{system.upper()} SYSTEM:")
                report_lines.append(f"  Total files processed: {total_files}")
                report_lines.append(f"  Average WER: {avg_wer:.4f}")
                report_lines.append(f"  Average CER: {avg_cer:.4f}")
                report_lines.append("")
        
        # Detailed comparison by test condition
        report_lines.append("DETAILED COMPARISON BY TEST CONDITION:")
        report_lines.append("-" * 60)
        
        # Get all unique test conditions
        all_conditions = set()
        for system_results in self.results.values():
            all_conditions.update(system_results.keys())
        
        for condition in sorted(all_conditions):
            report_lines.append(f"\nTest Condition: {condition}")
            
            skywalk_result = self.results.get('skywalk', {}).get(condition)
            nothing_result = self.results.get('nothing', {}).get(condition)
            
            if skywalk_result:
                report_lines.append(f"  Skywalk - WER: {skywalk_result['wer']:.4f}, CER: {skywalk_result['cer']:.4f}")
            else:
                report_lines.append("  Skywalk - No data")
            
            if nothing_result:
                report_lines.append(f"  Nothing - WER: {nothing_result['wer']:.4f}, CER: {nothing_result['cer']:.4f}")
            else:
                report_lines.append("  Nothing - No data")
            
            # Calculate improvement
            if skywalk_result and nothing_result:
                wer_improvement = nothing_result['wer'] - skywalk_result['wer']
                cer_improvement = nothing_result['cer'] - skywalk_result['cer']
                
                report_lines.append(f"  Improvement - WER: {wer_improvement:+.4f}, CER: {cer_improvement:+.4f}")
        
        # Performance by language
        report_lines.append("\n" + "=" * 60)
        report_lines.append("PERFORMANCE BY LANGUAGE:")
        report_lines.append("-" * 60)
        
        for language in ['EN', 'EN_ACCENT', 'CN', 'SV']:
            skywalk_lang_results = [r for r in self.results.get('skywalk', {}).values() 
                                  if r['conditions']['language'] == language]
            nothing_lang_results = [r for r in self.results.get('nothing', {}).values() 
                                  if r['conditions']['language'] == language]
            
            if skywalk_lang_results:
                skywalk_avg_wer = sum(r['wer'] for r in skywalk_lang_results) / len(skywalk_lang_results)
                skywalk_avg_cer = sum(r['cer'] for r in skywalk_lang_results) / len(skywalk_lang_results)
            else:
                skywalk_avg_wer = skywalk_avg_cer = None
            
            if nothing_lang_results:
                nothing_avg_wer = sum(r['wer'] for r in nothing_lang_results) / len(nothing_lang_results)
                nothing_avg_cer = sum(r['cer'] for r in nothing_lang_results) / len(nothing_lang_results)
            else:
                nothing_avg_wer = nothing_avg_cer = None
            
            report_lines.append(f"\n{language}:")
            if skywalk_avg_wer is not None:
                report_lines.append(f"  Skywalk - Avg WER: {skywalk_avg_wer:.4f}, Avg CER: {skywalk_avg_cer:.4f}")
            if nothing_avg_wer is not None:
                report_lines.append(f"  Nothing - Avg WER: {nothing_avg_wer:.4f}, Avg CER: {nothing_avg_cer:.4f}")
        
        return "\n".join(report_lines)
    
    def save_results(self, output_file: str = "enc_test_results.json"):
        """Save detailed results to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {output_file}")
    
    def run_evaluation(self) -> Dict:
        """Run the complete evaluation"""
        logger.info("Starting ENC performance evaluation")
        
        if not self.check_dependencies():
            return {}
        
        # Evaluate both systems
        for system in ['skywalk', 'nothing']:
            logger.info(f"Evaluating {system} system...")
            self.results[system] = self.evaluate_system(system)
        
        # Generate and save report
        report = self.generate_report()
        with open("enc_test_report.txt", 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save detailed results
        self.save_results()
        
        logger.info("Evaluation completed. Check enc_test_report.txt for results.")
        return self.results

def main():
    """Main function to run the evaluation"""
    evaluator = ENCTestEvaluator()
    results = evaluator.run_evaluation()
    
    if results:
        print("\nEvaluation completed successfully!")
        print("Check the following files for results:")
        print("- enc_test_report.txt: Human-readable report")
        print("- enc_test_results.json: Detailed JSON results")
    else:
        print("Evaluation failed. Check the logs for details.")

if __name__ == "__main__":
    main() 