from scipy.io.wavfile import write
import numpy as np
from tkinter import filedialog
import wave 
import os

data = filedialog.askopenfilename()
data_name = os.path.basename(data)
data2wav = np.loadtxt(data)
samplerate = 44100; fs = 100
write("example.wav", samplerate, data2wav)

with wave.open("{}.wav".format(data_name), mode="wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(1)
    wav_file.setframerate(44100)
    wav_file.setnframes(data2wav.size)
    wav_file.writeframes(data2wav.tobytes())
