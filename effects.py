import numpy as np
from scipy.signal import butter, filtfilt

def normalize(wave):
    max_val = np.max(np.abs(wave))
    if max_val > 0:
        return wave / max_val * 0.99
    return wave

def lowpass_filter(wave, cutoff, sample_rate):
    cutoff = min(cutoff, sample_rate/2-1)
    b,a = butter(2, cutoff/(sample_rate/2), 'low')
    return filtfilt(b,a,wave)

def distortion(wave, amount):
    return np.tanh(wave * (1 + 5*amount/100))

def multitap_reverb(wave, taps, amount, sample_rate):
    reverb_wave = np.zeros_like(wave)
    for i, tap in enumerate(taps):
        delay = int(sample_rate*tap)
        if delay < len(wave):
            temp = np.zeros_like(wave)
            temp[delay:] = wave[:-delay]
            decay = 0.5 ** i
            reverb_wave += decay * temp
    reverb_wave /= len(taps)
    return normalize((1-amount/100)*wave + (amount/100)*reverb_wave)
