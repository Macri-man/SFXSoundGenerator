class Layer:
    def __init__(self, name="Layer"):
        self.name = name  # Added to fix layer selector display

        # Waveform settings
        self.waveform = "Sine"
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
        self.lfos = []  # Optional multiple LFOs for advanced synth

        # Effects
        self.distortion = 0
        self.reverb = 0
        self.filter_freq = 8000
        self.bitcrusher = 0  # Make sure bitcrusher is also present

        # Randomness
        self.randomness = 0.0  # Added to fix generate_layer_wave

        # Output
        self.volume = 1.0
        self.pan = 0.5  # 0 = left, 1 = right

    # ------------------- Serialization -------------------
    def to_dict(self):
        return {
            "name": self.name,
            "waveform": self.waveform,
            "freq": self.freq,
            "freq_end": self.freq_end,
            "dur": self.dur,
            "adsr": self.adsr.copy(),
            "lfo_freq": self.lfo_freq,
            "lfo_depth": self.lfo_depth,
            "lfos": self.lfos.copy(),
            "distortion": self.distortion,
            "reverb": self.reverb,
            "filter_freq": self.filter_freq,
            "bitcrusher": self.bitcrusher,
            "randomness": self.randomness,
            "volume": self.volume,
            "pan": self.pan
        }

    @classmethod
    def from_dict(cls, data):
        layer = cls(data.get("name", "Layer"))
        layer.waveform = data.get("waveform", "Sine")
        layer.freq = data.get("freq", 440)
        layer.freq_end = data.get("freq_end", layer.freq)
        layer.dur = data.get("dur", 1.0)
        layer.adsr = data.get("adsr", layer.adsr.copy())
        layer.lfo_freq = data.get("lfo_freq", 0.0)
        layer.lfo_depth = data.get("lfo_depth", 0.0)
        layer.lfos = data.get("lfos", [])
        layer.distortion = data.get("distortion", 0)
        layer.reverb = data.get("reverb", 0)
        layer.filter_freq = data.get("filter_freq", 8000)
        layer.bitcrusher = data.get("bitcrusher", 0)
        layer.randomness = data.get("randomness", 0.0)
        layer.volume = data.get("volume", 1.0)
        layer.pan = data.get("pan", 0.5)
        return layer
