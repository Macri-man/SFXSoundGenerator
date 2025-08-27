import json
import random
from layer import Layer

DEFAULT_PRESETS = {
    "Explosion": [
        {"waveform":"Noise", "freq":200, "freq_end":3000, "dur":0.8, "adsr":{"Attack":0,"Decay":200,"Sustain":30,"Release":300},
         "lfo_freq":5,"lfo_depth":50,"distortion":70,"reverb":40,"filter_freq":5000,"volume":1.0,"pan":0.5}
    ],
    "Laser": [
        {"waveform":"Sine","freq":800,"freq_end":200,"dur":0.3,"adsr":{"Attack":5,"Decay":50,"Sustain":20,"Release":50},
         "lfo_freq":10,"lfo_depth":20,"distortion":40,"reverb":20,"filter_freq":8000,"volume":1.0,"pan":0.5}
    ],
    "Riser": [
        {"waveform":"Sawtooth","freq":100,"freq_end":2000,"dur":1.5,"adsr":{"Attack":10,"Decay":200,"Sustain":50,"Release":200},
         "lfo_freq":5,"lfo_depth":30,"distortion":30,"reverb":40,"filter_freq":6000,"volume":1.0,"pan":0.5}
    ],
    "Impact": [
        {"waveform":"Square","freq":300,"freq_end":150,"dur":0.2,"adsr":{"Attack":0,"Decay":50,"Sustain":50,"Release":100},
         "lfo_freq":0,"lfo_depth":0,"distortion":50,"reverb":20,"filter_freq":5000,"volume":1.0,"pan":0.5}
    ],
    "Hit": [
        {"waveform":"Triangle","freq":400,"freq_end":400,"dur":0.15,"adsr":{"Attack":0,"Decay":20,"Sustain":60,"Release":50},
         "lfo_freq":0,"lfo_depth":0,"distortion":30,"reverb":10,"filter_freq":4000,"volume":1.0,"pan":0.5}
    ]
}

class PresetManager:
    """Load, save, and apply SFX presets from JSON files"""

    @staticmethod
    def load_preset(path: str):
        with open(path, "r") as f:
            data = json.load(f)
        layers = []
        for layer_data in data.get("layers", []):
            layer = Layer()
            for key, val in layer_data.items():
                setattr(layer, key, val)
            layers.append(layer)
        return layers

    @staticmethod
    def save_preset(path: str, layers: list):
        data = {"layers":[{k:getattr(layer,k) for k in vars(layer)} for layer in layers]}
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
