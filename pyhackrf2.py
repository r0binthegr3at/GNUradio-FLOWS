from pyhackrf2 import HackRF
hackrf = HackRF()
hackrf.sample_rate = 2.4e6
hackrf.center_freq = 314.96e6
hackrf.baseband_filter = 5e6
samples = hackrf.read_samples(2e6)

