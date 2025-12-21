from pydub import AudioSegment, silence
import noisereduce as nr
import numpy as np

# -------- STEP 1: LOAD AUDIO --------
audio_path = "test.wav"        # change to your file name
output_path = "test_clean.wav"

print("Loading audio...")
audio = AudioSegment.from_wav(audio_path)

# -------- STEP 2: TRIM LARGE SILENCES --------
print("Removing long silences...")
chunks = silence.split_on_silence(
    audio,
    min_silence_len=500,      # silence longer than 0.5 sec
    silence_thresh=-40        # consider <-40 dB as silence
)

clean_audio = AudioSegment.empty()
for c in chunks:
    clean_audio += c + AudioSegment.silent(duration=200)

# Convert to numpy for noise reduction
print("Applying noise reduction (soft mode)...")
samples = np.array(clean_audio.get_array_of_samples())

reduced_noise = nr.reduce_noise(
    y=samples.astype(float),
    sr=clean_audio.frame_rate
)

# Convert back to AudioSegment
final_audio = AudioSegment(
    reduced_noise.astype("int16").tobytes(),
    frame_rate=clean_audio.frame_rate,
    sample_width=clean_audio.sample_width,
    channels=clean_audio.channels
)

# -------- STEP 3: SAVE CLEANED AUDIO --------
final_audio.export(output_path, format="wav")

print("\n===== AUDIO CLEANING COMPLETE =====")
print(f"Saved cleaned audio as: {output_path}")
