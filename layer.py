class Layer:
    def __init__(self):
        # Waveform settings
        self.waveform = "Sine"  # "Sine", "Square", "Triangle", "Sawtooth", "Noise"
        self.freq = 440
        self.freq_end = 440
        self.dur = 1.0  # seconds

        # ADSR envelope
        self.adsr = {
            "Attack": 0,
            "Decay": 100,
            "Sustain": 50,
            "Release": 100
        }

        # LFO / Modulation
        self.lfo_freq = 0.0
        self.lfo_depth = 0.0

        # Effects
        self.distortion = 0
        self.reverb = 0
        self.filter_freq = 8000

        # Output
        self.volume = 1.0
        self.pan = 0.5  # 0 = left, 1 = right

    # ------------------- Serialization -------------------
    def to_dict(self):
        """
        Convert layer to JSON-serializable dictionary.
        """
        return {
            "waveform": self.waveform,
            "freq": self.freq,
            "freq_end": self.freq_end,
            "dur": self.dur,
            "adsr": self.adsr.copy(),
            "lfo_freq": self.lfo_freq,
            "lfo_depth": self.lfo_depth,
            "distortion": self.distortion,
            "reverb": self.reverb,
            "filter_freq": self.filter_freq,
            "volume": self.volume,
            "pan": self.pan
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Layer instance from a dictionary.
        """
        layer = cls()
        layer.waveform = data.get("waveform", "Sine")
        layer.freq = data.get("freq", 440)
        layer.freq_end = data.get("freq_end", layer.freq)
        layer.dur = data.get("dur", 1.0)
        layer.adsr = data.get("adsr", layer.adsr.copy())
        layer.lfo_freq = data.get("lfo_freq", 0.0)
        layer.lfo_depth = data.get("lfo_depth", 0.0)
        layer.distortion = data.get("distortion", 0)
        layer.reverb = data.get("reverb", 0)
        layer.filter_freq = data.get("filter_freq", 8000)
        layer.volume = data.get("volume", 1.0)
        layer.pan = data.get("pan", 0.5)
        return layer
