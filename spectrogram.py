import numpy as np
import matplotlib.pyplot as plt

sample_rate = 2e6
x = np.arange(1024*1000)/sample_rate
fft_size = 1024
num_rows = len(x) // fft_size
spectrogram = np.zeros((num_rows, fft_size))
for i in range(num_rows):
	spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)

plt.imshow(spectrogram, aspect='auto', extent = [sample_rate/-2/2e6, sample_rate/2/2e6, len(x)/sample_rate, 0])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [s]")

