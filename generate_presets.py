import json
import os

PRESETS_DIR = "presets"
os.makedirs(PRESETS_DIR, exist_ok=True)

# ------------------- Preset Definitions -------------------
presets = {
    "explosion": [
        {
            "name": "Explosion Noise",
            "waveform": "Noise",
            "freq": 100,
            "freq_end": 2000,
            "dur": 1.0,
            "adsr": {"Attack": 0, "Decay": 200, "Sustain": 10, "Release": 500},
            "lfo_freq": 0,
            "lfo_depth": 0,
            "distortion": 60,
            "reverb": 50,
            "filter_freq": 8000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "laser": [
        {
            "name": "Laser Beam",
            "waveform": "Sine",
            "freq": 1000,
            "freq_end": 4000,
            "dur": 0.25,
            "adsr": {"Attack": 0, "Decay": 50, "Sustain": 20, "Release": 50},
            "lfo_freq": 10,
            "lfo_depth": 100,
            "distortion": 30,
            "reverb": 10,
            "filter_freq": 10000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "riser": [
        {
            "name": "Riser",
            "waveform": "Sawtooth",
            "freq": 100,
            "freq_end": 5000,
            "dur": 1.5,
            "adsr": {"Attack": 0, "Decay": 300, "Sustain": 10, "Release": 200},
            "lfo_freq": 0,
            "lfo_depth": 0,
            "distortion": 10,
            "reverb": 20,
            "filter_freq": 12000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "impact": [
        {
            "name": "Impact Hit",
            "waveform": "Square",
            "freq": 200,
            "freq_end": 0,
            "dur": 0.2,
            "adsr": {"Attack": 0, "Decay": 50, "Sustain": 20, "Release": 50},
            "lfo_freq": 0,
            "lfo_depth": 0,
            "distortion": 50,
            "reverb": 40,
            "filter_freq": 6000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "hit": [
        {
            "name": "Punch Hit",
            "waveform": "Triangle",
            "freq": 300,
            "freq_end": 0,
            "dur": 0.15,
            "adsr": {"Attack": 0, "Decay": 30, "Sustain": 10, "Release": 40},
            "lfo_freq": 0,
            "lfo_depth": 0,
            "distortion": 40,
            "reverb": 20,
            "filter_freq": 4000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "powerup": [
        {
            "name": "Power-Up Tone",
            "waveform": "Sine",
            "freq": 400,
            "freq_end": 2000,
            "dur": 0.5,
            "adsr": {"Attack": 0, "Decay": 100, "Sustain": 40, "Release": 200},
            "lfo_freq": 5,
            "lfo_depth": 50,
            "distortion": 0,
            "reverb": 30,
            "filter_freq": 10000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "punch": [
        {
            "name": "Deep Punch",
            "waveform": "Square",
            "freq": 100,
            "freq_end": 0,
            "dur": 0.2,
            "adsr": {"Attack": 0, "Decay": 50, "Sustain": 10, "Release": 50},
            "lfo_freq": 0,
            "lfo_depth": 0,
            "distortion": 60,
            "reverb": 20,
            "filter_freq": 3000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "zap": [
        {
            "name": "Zap High",
            "waveform": "Sine",
            "freq": 2000,
            "freq_end": 5000,
            "dur": 0.15,
            "adsr": {"Attack": 0, "Decay": 50, "Sustain": 20, "Release": 50},
            "lfo_freq": 10,
            "lfo_depth": 50,
            "distortion": 70,
            "reverb": 10,
            "filter_freq": 8000,
            "volume": 1.0,
            "pan": 0.5
        },
        {
            "name": "Zap Noise",
            "waveform": "Noise",
            "freq": 1000,
            "freq_end": 2000,
            "dur": 0.12,
            "adsr": {"Attack": 0, "Decay": 30, "Sustain": 10, "Release": 30},
            "lfo_freq": 5,
            "lfo_depth": 20,
            "distortion": 50,
            "reverb": 20,
            "filter_freq": 5000,
            "volume": 0.7,
            "pan": 0.3
        }
    ],
    "whip": [
        {
            "name": "Whoosh Noise",
            "waveform": "Noise",
            "freq": 100,
            "freq_end": 5000,
            "dur": 0.6,
            "adsr": {"Attack": 5, "Decay": 200, "Sustain": 10, "Release": 300},
            "lfo_freq": 0,
            "lfo_depth": 0,
            "distortion": 20,
            "reverb": 40,
            "filter_freq": 8000,
            "volume": 1.0,
            "pan": 0.5
        }
    ],
    "sparkle": [
        {
            "name": "Sparkle",
            "waveform": "Triangle",
            "freq": 3000,
            "freq_end": 6000,
            "dur": 0.25,
            "adsr": {"Attack": 0, "Decay": 50, "Sustain": 10, "Release": 100},
            "lfo_freq": 15,
            "lfo_depth": 30,
            "distortion": 10,
            "reverb": 40,
            "filter_freq": 12000,
            "volume": 1.0,
            "pan": 0.5
        }
    ]
}

# ------------------- Generate JSON Files -------------------
for preset_name, layers in presets.items():
    path = os.path.join(PRESETS_DIR, f"{preset_name}.json")
    with open(path, "w") as f:
        json.dump({"layers": layers}, f, indent=4)
    print(f"Saved preset: {path}")

print("All presets generated successfully!")
