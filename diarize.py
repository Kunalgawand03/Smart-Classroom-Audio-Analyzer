from pyannote.audio import Pipeline
import torchaudio

def diarize_audio(audio_path):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=True
    )

    diarization = pipeline(audio_path)

    speakers = {}

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        duration = turn.end - turn.start
        speakers[speaker] = speakers.get(speaker, 0) + duration

    return diarization, speakers
