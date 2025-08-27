class Layer:
    def __init__(self, name="Layer 1"):
        self.name = name
        self.waveform = "Sine"       # "Sine", "Square", "Triangle", "Sawtooth", "Noise"
        self.freq = 440
        self.freq_end = 440           # For pitch slides
        self.dur = 0.5
        self.adsr = {"Attack":50,"Decay":50,"Sustain":70,"Release":50}  # ms & %
        self.lfo_freq = 0
        self.lfo_depth = 0
        self.distortion = 0
        self.reverb = 0
        self.filter_freq = 0
        self.volume = 1.0             # Layer gain
        self.pan = 0.5                # 0 = left, 1 = right, 0.5 = center
        self.id = None
