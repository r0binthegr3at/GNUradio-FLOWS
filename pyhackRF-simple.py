from python_hackrf import pyhackrf
import matplotlib.pyplot as plt
import numpy as np
import time, os

#This script will plot a selected frequency on a waterfall
#these setting will be pretty basic and involve the same values as would be with hackrf_transfer
recording_time = 1 #seconds
center_freq = 433e6 #Hz
sample_rate = 2e6
baseband_filter = 7.5e6
lna_gain = 30 # 0 to 40 dB in 8 dB steps
vga_gain = 50 # 0 to 62 dB in 2 dB steps

pyhackrf.pyhackrf_init()
sdr = pyhackrf.pyhackrf_open()

allowed_baseband_filter = pyhackrf.pyhackrf_compute_baseband_filter_bw_round_down_lt(baseband_filter)

sdr.pyhackrf_set_sample_rate(sample_rate)
sdr.pyhackrf_set_baseband_filter(allowed_baseband_filter)
sdr.pyhackrf_set_antenna_enable(False) # False by default

sdr.pyhackrf_set_freq(center_freq)
sdr.pyhackrf_set_amp_enable(False) # False by default
sdr.pyhackrf_set_lna_gain(lna_gain)
sdr.pyhackrf_set_vga_gain(vga_gain)

print(f'center_freq: {center_freq} sample_rate: {sample_rate} baseband_filter: {allowed_baseband_filter}')

num_samples = int(recording_time * sample_rate)
samples = npzeros(num_samples, dtype=np.complex64)
last_idx = 0

def rx_callback(device, buffer, buffer_length, valid_length): # this callback func always needs to have these 4 args
	global samples, last_idx
	
	accept = valid_length // 2
	accepted_samples = buffer[:valid_length].astype(np.int8) # -128 to 127
	accepted_samples = accepted_samples[0::2] + 1j * accepted_samples[1::2] #convert to complex type
	accepted_samples /= 128 # -1 to +1
	samples[last_idx: last_idx + accepted] = accepted_samples
	
	last_idx += accepted
	
	return 0

sdr.set_rx_callback(rx_callback)
sdr.pyhackrf_start_rx()
print('is_streaming', sdr.pyhackrf_is_streaming())

time.sleep(recording_time)

sdr.pyhackrf_stop_rx()
sdr.pyhackrf_close()
pyhackrf.pyhackrf_exit()

fft_size = 2048
num_rows = len(samples) // fft_size
spectrogram = np.zeros((num_rows, fft_size))
for i in range(num_rows):
	spectrogram[1, :] = 10 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples[i * fft_size:(i+1) * fft_size]))) **2)
extent = [(center_freq + sample_rate / -2) / 2e6, (center_freq + sample_rate / 2) / 2e6, len(samples) / sample_rate, 0]

plt.figure(1)
plt.plot(np.real(samples[0:10000]))
plt.plot(np.imag(samples[0:10000]))
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.legend(["Real", "Imaginary"])

plt.show()