import json
from layer import Layer

DEFAULT_PRESETS = {
    "Explosion": [
        {"waveform": "Noise", "freq": 200, "freq_end": 3000, "dur": 0.8,
         "adsr": {"Attack": 0, "Decay": 200, "Sustain": 30, "Release": 300},
         "lfo_freq": 5, "lfo_depth": 50, "distortion": 70, "reverb": 40, "filter_freq": 5000,
         "volume": 1.0, "pan": 0.5}
    ],
    "Laser": [
        {"waveform": "Sine", "freq": 800, "freq_end": 200, "dur": 0.3,
         "adsr": {"Attack": 5, "Decay": 50, "Sustain": 20, "Release": 50},
         "lfo_freq": 10, "lfo_depth": 20, "distortion": 40, "reverb": 20, "filter_freq": 8000,
         "volume": 1.0, "pan": 0.5}
    ],
    "Riser": [
        {"waveform": "Sawtooth", "freq": 100, "freq_end": 2000, "dur": 1.5,
         "adsr": {"Attack": 10, "Decay": 200, "Sustain": 50, "Release": 200},
         "lfo_freq": 5, "lfo_depth": 30, "distortion": 30, "reverb": 40, "filter_freq": 6000,
         "volume": 1.0, "pan": 0.5}
    ]
}

class PresetManager:
    @staticmethod
    def load_preset(path: str):
        with open(path, "r") as f:
            data = json.load(f)
        return [Layer.from_dict(d) for d in data.get("layers", [])]

    @staticmethod
    def save_preset(path: str, layers: list):
        data = {"layers": [layer.to_dict() for layer in layers]}
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def generate_layer_from_preset(preset_name):
        preset_data = DEFAULT_PRESETS.get(preset_name, [])
        layers = []
        for layer_dict in preset_data:
            layers.append(Layer.from_dict(layer_dict))
        return layers
