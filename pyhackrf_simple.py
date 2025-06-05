from python_hackrf import pyhackrf
pyhackrf.pyhackrf_init()
sdr = pyhackrf.pyhackrf_open()
sdr.pyhackrf_set_sample_rate(2e6)
sdr.pyhackrf_set_antenna_enable(False)
sdr.pyhackrf_set_freq(314.65e6)
sdr.pyhackrf_set_amp_enable(False)
sdr.pyhackrf_set_lna_gain(30)
sdr.pyhackrf_set_vga_gain(50)

