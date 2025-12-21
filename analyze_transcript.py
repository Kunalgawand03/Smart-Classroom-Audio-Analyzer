import whisper
import re
from transformers import pipeline


def student_focus_score(text):
    focus_words = ['you', 'everyone', 'class', 'students', 'doubt', 'question', 'ask']
    words = re.findall(r'\w+', text.lower())
    count = sum(1 for w in words if w in focus_words)
    return count

def load_and_transcribe(audio_path='lecture.wav', model_size='small'):
    print("Loading Whisper model... this may take time...")
    model = whisper.load_model(model_size)
    print("Transcribing audio...")
    res = model.transcribe(audio_path)
    return res

def words_per_minute(segments):
    total_words = 0
    total_time = 0.0
    for seg in segments:
        text = seg['text'].strip()
        words = len(re.findall(r'\w+', text))
        duration = seg['end'] - seg['start']
        total_words += words
        total_time += duration
    if total_time == 0:
        return 0
    wpm = (total_words / total_time) * 60.0
    return round(wpm, 1)

def question_count(full_text):
    q_marks = full_text.count('?')
    question_words = [
        'what', 'when', 'where', 'why', 'who', 'how',
        'do', 'did', 'does', 'is', 'are',
        'can', 'could', 'would', 'should'
    ]
    words = re.findall(r'\w+', full_text.lower())
    qword_count = sum(1 for w in words if w in question_words)
    return q_marks, qword_count

def sentiment_analysis(text):
    print("Running sentiment analysis...")
    nlp = pipeline("sentiment-analysis")
    chunk = text[:500]   # limit speed
    out = nlp(chunk)[0]
    return out

if __name__ == "__main__":
    # IMPORTANT: Change file name here if needed
    res = load_and_transcribe('test.wav', 'small')
    full_text = res['text']

    wpm = words_per_minute(res['segments'])
    q_marks, qword_count = question_count(full_text)
    sentiment = sentiment_analysis(full_text)

    report = {
        "wpm": wpm,
        "question_marks": q_marks,
        "question_word_mentions": qword_count,
        "sentiment": sentiment,
        "transcript_preview": full_text[:2000]
    }

    import json
    print(json.dumps(report, indent=2))
