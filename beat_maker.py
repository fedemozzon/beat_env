from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
from pydub.playback import play
import time
import random
import os

def generate_kick():
    """Generate a kick drum sound"""
    duration = 100
    kick = Sine(60).to_audio_segment(duration=duration)
    return kick.fade_out(50) - 12

def generate_snare():
    """Generate a snare drum sound"""
    duration = 80
    snare = Sine(200).to_audio_segment(duration=duration)
    return snare.fade_out(40) - 12

def generate_hihat():
    """Generate a hihat sound"""
    duration = 50
    hihat = Sine(1000).to_audio_segment(duration=duration)
    return hihat.fade_out(30) - 20

def generate_cymbal():
    """Generate a cymbal sound"""
    duration = 150
    cymbal = Sine(1500).to_audio_segment(duration=duration)
    return cymbal.fade_out(100) - 25

def generate_tom():
    """Generate a tom drum sound"""
    duration = 100
    tom = Sine(150).to_audio_segment(duration=duration)
    return tom.fade_out(60) - 15

def generate_clap():
    """Generate a clap sound"""
    duration = 60
    clap = WhiteNoise().to_audio_segment(duration=duration)
    return clap.fade_out(30) - 25

def word_to_pattern(text):
    """Convert text to an extended drum pattern"""
    pattern = ""
    vowels = set('aeiouAEIOU')
    consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
    
    for char in text:
        if char.isspace():
            pattern += 'h'  # Hihat for spaces
        elif char in '.,!?':
            pattern += 'c'  # Cymbal for punctuation
        elif char in vowels:
            pattern += 's' if random.random() > 0.5 else 'p'  # Snare or Clap for vowels
        elif char in consonants:
            pattern += 'k' if random.random() > 0.5 else 't'  # Kick or Tom for consonants
    
    return pattern

def create_beat(pattern, bpm=120):
    """Create a beat with extended instrument set"""
    beat = AudioSegment.empty()
    beat_duration = int(60000 / bpm)
    
    for char in pattern.lower():
        if char == 'k':
            sound = generate_kick()
        elif char == 's':
            sound = generate_snare()
        elif char == 'h':
            sound = generate_hihat()
        elif char == 'c':
            sound = generate_cymbal()
        elif char == 't':
            sound = generate_tom()
        elif char == 'p':
            sound = generate_clap()
        else:
            continue
            
        beat += sound
        silence = AudioSegment.silent(duration=beat_duration - len(sound))
        beat += silence
    
    return beat

def main():
    try:
        text = input("Enter a sentence to create a beat: ")
        bpm = int(input("Enter BPM (60-180): "))
        if not 60 <= bpm <= 180:
            raise ValueError("BPM must be between 60 and 180")
            
        pattern = word_to_pattern(text)
        print(f"Generated pattern: {pattern}")
        beat = create_beat(pattern, bpm)
        play(beat)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
