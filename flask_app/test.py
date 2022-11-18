import librosa
import soundfile as sf
import time

ar, sr = librosa.load('abhishek.wav', sr=3840000)

tik = time.time()
sf.write('abhishek_2.wav', ar, 384000)
tok = time.time()

print(tok - tik)

# 0.0639503002166748
