import numpy as np

class Layer:
    """
    Represents a single SFX layer with advanced modulation and effects.
    """

    def __init__(
        self, waveform="Sine", freq=440.0, freq_end=None, dur=1.0,
        volume=1.0, pan=0.5, lfos=None, adsr=None,
        filter_freq=0.0, distortion=0.0, reverb=0.0, bitcrusher=0.0, randomness=0.0
    ):
        self.waveform = waveform
        self.freq = freq
        self.freq_end = freq_end if freq_end is not None else freq
        self.dur = dur
        self.volume = volume
        self.pan = np.clip(pan, 0, 1)  # 0=left, 1=right
        self.lfos = lfos if lfos is not None else []  # list of dicts: [{"freq":..., "depth":...}]
        self.adsr = adsr if adsr else {"Attack":10,"Decay":50,"Sustain":80,"Release":50}
        self.filter_freq = filter_freq
        self.distortion = distortion
        self.reverb = reverb
        self.bitcrusher = bitcrusher
        self.randomness = randomness  # adds subtle variation to pitch or amplitude
