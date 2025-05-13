from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
from pydub.playback import play
from pydub.effects import normalize
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def apply_hyperpop_effects(sound):
    """Apply hyperpop-style effects with safe sample rates"""
    sound = sound.apply_gain(8)
    sound = normalize(sound)
    # Use safer octave shifts
    octave_shift = random.choice([-1, 0, 1])
    new_rate = int(sound.frame_rate * (2.0 ** octave_shift))
    # Ensure sample rate stays within supported range (8000-48000 Hz)
    new_rate = max(8000, min(48000, new_rate))
    sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": new_rate
    })
    return sound

def generate_kick():
    """Generate a hyperpop kick drum"""
    duration = 80
    kick = Sine(80, sample_rate=44100).to_audio_segment(duration=duration)
    kick = kick.apply_gain(10)
    return apply_hyperpop_effects(kick.fade_out(40))

def generate_snare():
    """Generate a hyperpop snare"""
    duration = 60
    snare = WhiteNoise(sample_rate=44100).to_audio_segment(duration=duration)
    snare = snare.overlay(Sine(400, sample_rate=44100).to_audio_segment(duration=duration))
    return apply_hyperpop_effects(snare.fade_out(30))

def generate_hihat():
    """Generate a hyperpop hihat"""
    duration = 30
    hihat = WhiteNoise(sample_rate=44100).to_audio_segment(duration=duration)
    hihat = hihat.high_pass_filter(2000)
    return apply_hyperpop_effects(hihat.fade_out(20))

def generate_lead():
    """Generate a hyperpop lead synth"""
    duration = 100
    freq = random.choice([400, 600, 800, 1000])
    lead = Sine(freq, sample_rate=44100).to_audio_segment(duration=duration)
    return apply_hyperpop_effects(lead.fade_out(50))

def generate_sharp_synth():
    """Generate a sharp, piercing synth sound"""
    duration = 40  # Short duration for sharpness
    # High frequency for piercing sound
    freq = random.choice([2000, 3000, 4000])
    sharp = Sine(freq).to_audio_segment(duration=duration)
    
    # Add distortion
    sharp = sharp.apply_gain(15)
    
    # Rapid pitch modulation
    mod_freq = random.uniform(10, 20)
    sharp = sharp._spawn(sharp.raw_data, overrides={
        "frame_rate": int(sharp.frame_rate * mod_freq)
    })
    
    return apply_hyperpop_effects(sharp.fade_out(20))

def generate_random_instrument():
    """Generate a random instrument configuration"""
    instruments = [
        (generate_kick, "bass"),
        (generate_snare, "mid"),
        (generate_hihat, "high"),
        (generate_lead, "melody"),
        (generate_sharp_synth, "sharp")
    ]
    return random.choice(instruments)[0]()

def create_random_mapping():
    """Create random mapping for characters to instruments"""
    instruments = ['k', 's', 'h', 'l', 'x']
    random.shuffle(instruments)
    return {
        'space': instruments[0],
        'vowel': instruments[1],
        'consonant': instruments[2],
        'uppercase': instruments[3],
        'punctuation': instruments[4]
    }

def word_to_pattern(text, mapping):
    """Convert text to pattern using provided mapping"""
    pattern = ""
    vowels = set('aeiouAEIOU')
    
    for char in text:
        if char.isspace():
            pattern += mapping['space'] * random.randint(1, 2)
        elif char.isupper():
            pattern += mapping['uppercase']
        elif char.lower() in vowels:
            pattern += mapping['vowel'] * random.randint(1, 2)
        elif char in '.,!?':
            pattern += mapping['punctuation']
        else:
            pattern += mapping['consonant']
    return pattern

def analyze_sentiment(text):
    """Analyze the sentiment of text and return mood parameters"""
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    
    # Map sentiment to musical parameters
    if scores['compound'] > 0.5:  # Very positive
        return {
            'tempo_factor': 1.3,
            'pitch_shift': 2,
            'distortion': 0.3,
            'base_note': 'major'
        }
    elif scores['compound'] > 0:  # Slightly positive
        return {
            'tempo_factor': 1.1,
            'pitch_shift': 1,
            'distortion': 0.5,
            'base_note': 'major'
        }
    elif scores['compound'] < -0.5:  # Very negative
        return {
            'tempo_factor': 0.8,
            'pitch_shift': -2,
            'distortion': 0.8,
            'base_note': 'minor'
        }
    else:  # Neutral or slightly negative
        return {
            'tempo_factor': 1.0,
            'pitch_shift': 0,
            'distortion': 0.6,
            'base_note': 'minor'
        }

def apply_mood_effects(sound, mood):
    """Apply effects based on mood"""
    sound = sound.apply_gain(8 * mood['distortion'])
    new_rate = int(sound.frame_rate * (2.0 ** (mood['pitch_shift'] / 12.0)))
    new_rate = max(8000, min(48000, new_rate))
    sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_rate})
    return sound

def create_beat(pattern, text, bpm=180):
    """Create a mood-based beat"""
    mood = analyze_sentiment(text)
    beat = AudioSegment.empty()
    beat_duration = int(60000 / (bpm * mood['tempo_factor']))
    
    instrument_bank = {
        'k': generate_kick,
        's': generate_snare,
        'h': generate_hihat,
        'l': generate_lead,
        'x': generate_sharp_synth
    }
    
    for char in pattern.lower():
        if char in instrument_bank:
            sound = instrument_bank[char]()
            sound = apply_mood_effects(sound, mood)
            beat += sound
            silence = AudioSegment.silent(duration=max(0, beat_duration - len(sound)))
            beat += silence
    
    return beat

def main():
    try:
        text = input("Enter text for mood-based beat: ")
        bpm = int(input("Enter base BPM (120-300): "))
        mapping = create_random_mapping()
        pattern = word_to_pattern(text, mapping)
        beat = create_beat(pattern, text, bpm)
        play(beat)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
