import numpy as np
from scipy.signal import butter, lfilter

def normalize(wave: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    max_val = np.max(np.abs(wave))
    return wave / (max_val + eps) if max_val > 0 else wave

def lowpass_filter(wave: np.ndarray, cutoff: float, sample_rate: int) -> np.ndarray:
    cutoff = min(cutoff, sample_rate / 2 - 1)
    b, a = butter(2, cutoff / (sample_rate / 2), 'low')
    if wave.ndim == 1:
        return lfilter(b, a, wave)
    return np.column_stack([lfilter(b, a, wave[:, i]) for i in range(wave.shape[1])])

def distortion(wave: np.ndarray, amount: float) -> np.ndarray:
    amount = np.clip(amount, 0, 100)
    return np.tanh(wave * (1 + 5 * amount / 100))

def bitcrusher(wave: np.ndarray, reduction: float) -> np.ndarray:
    reduction = np.clip(reduction, 0, 100)
    steps = max(int(256 - 2.56 * reduction), 2)
    wave_scaled = (wave + 1) / 2
    wave_quant = np.floor(wave_scaled * steps) / steps
    return wave_quant * 2 - 1

def multitap_reverb(wave: np.ndarray, taps: list[float], amount: float, sample_rate: int) -> np.ndarray:
    amount = np.clip(amount, 0, 100)
    reverb_wave = np.zeros_like(wave)
    for tap in taps:
        delay = int(sample_rate * tap)
        if delay >= len(wave):
            continue
        if wave.ndim == 1:
            temp = np.pad(wave[:-delay], (delay, 0), 'constant')
        else:
            temp = np.pad(wave[:-delay, :], ((delay, 0), (0, 0)), 'constant')
        reverb_wave += temp
    reverb_wave /= max(len(taps), 1)
    return (1 - amount / 100) * wave + (amount / 100) * reverb_wave
