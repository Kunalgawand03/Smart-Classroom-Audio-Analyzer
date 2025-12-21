# analyze_confidence_tone.py

import whisper
import re
from transformers import pipeline

def load_transcript(audio_path='lecture.wav', model_size='small'):
    print("Loading Whisper model...")
    model = whisper.load_model(model_size)

    print("Transcribing audio...")
    result = model.transcribe(audio_path)

    return result


# -------------------------------
#  CONFIDENCE ESTIMATION (simple)
# -------------------------------

def estimate_confidence(segments):
    """
    Whisper local does NOT provide true confidence.
    So we approximate it using two simple heuristics:
    
    1. Words per second (too many words too fast = low clarity)
    2. Presence of [ ] unclear tokens (rare but useful)

    Output: confidence score 0–100 (rough estimate)
    """

    total_words = 0
    total_time = 0
    unclear_tokens = 0

    for seg in segments:
        text = seg['text']
        
        # Count words
        words = len(re.findall(r'\w+', text))
        
        # Count unclear tokens like [inaudible]
        unclear_tokens += text.count('[')

        # Time duration
        duration = seg['end'] - seg['start']

        total_words += words
        total_time += duration

    if total_time == 0:
        return 0

    words_per_second = total_words / total_time

    # Heuristic scoring:
    # Ideal speaking speed: 2–3 words per second
    # Faster = lower confidence

    if words_per_second < 1.5:
        speed_score = 85
    elif words_per_second < 2.5:
        speed_score = 95
    elif words_per_second < 3.5:
        speed_score = 80
    else:
        speed_score = 60

    # Penalize for unclear tokens
    unclear_penalty = unclear_tokens * 5

    confidence = max(0, min(100, speed_score - unclear_penalty))

    return confidence


# -------------------------
#  TONE / SENTIMENT
# -------------------------

def analyze_tone(text):
    print("Running sentiment analysis...")
    nlp = pipeline("sentiment-analysis")

    # Analyze first 500 chars for faster processing
    chunk = text[:500]

    result = nlp(chunk)[0]
    return result


# -------------------------
# MAIN PROGRAM
# -------------------------

if __name__ == "__main__":
    res = load_transcript('test.wav', 'small')

    full_text = res['text']
    segments = res['segments']

    confidence_score = estimate_confidence(segments)
    tone_result = analyze_tone(full_text)

    print("\n===== FINAL REPORT =====")
    print(f"Approx. Confidence Score: {confidence_score}/100")
    print(f"Tone Label: {tone_result['label']}")
    print(f"Tone Score: {tone_result['score']:.2f}")
    print("\nTranscript Preview:")
    print(full_text[:500])
