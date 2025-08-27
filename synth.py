import numpy as np
from scipy.signal import square, sawtooth
from effects import normalize, lowpass_filter, distortion, multitap_reverb, bitcrusher
from layer import Layer

SAMPLE_RATE = 44100

def apply_adsr(length, adsr):
    attack = int(SAMPLE_RATE*adsr.get("Attack",0)/1000)
    decay = int(SAMPLE_RATE*adsr.get("Decay",0)/1000)
    sustain_level = adsr.get("Sustain",100)/100
    release = int(SAMPLE_RATE*adsr.get("Release",0)/1000)
    sustain_length = max(length-(attack+decay+release),0)
    env = np.zeros(length)
    if attack>0: env[:attack] = np.linspace(0,1,attack,endpoint=False)
    if decay>0: env[attack:attack+decay] = np.linspace(1,sustain_level,decay,endpoint=False)
    if sustain_length>0: env[attack+decay:attack+decay+sustain_length] = sustain_level
    if release>0: env[-release:] = np.linspace(sustain_level,0,release,endpoint=True)
    return env

def generate_layer_wave(layer: Layer) -> np.ndarray:
    length = int(SAMPLE_RATE*layer.dur)
    t = np.linspace(0, layer.dur, length, endpoint=False)

    # Base frequency + frequency slide
    freq = np.linspace(layer.freq, layer.freq_end, length)
    
    # Apply multiple LFOs
    mod = np.zeros(length)
    for lfo in layer.lfos:
        mod += lfo.get("depth",0)*np.sin(2*np.pi*lfo.get("freq",0)*t)

    # Add randomness
    mod += layer.randomness * np.random.uniform(-1,1,length)
    phase = np.cumsum(2*np.pi*(freq + mod)/SAMPLE_RATE)

    # Waveform
    wave_map = {
        "Sine": np.sin,
        "Square": square,
        "Triangle": lambda p: sawtooth(p,0.5),
        "Sawtooth": sawtooth,
        "Noise": lambda p: np.random.uniform(-1,1,len(p))
    }
    wave = wave_map.get(layer.waveform, lambda p: np.zeros_like(p))(phase)

    # ADSR envelope
    wave *= apply_adsr(length, layer.adsr)

    # Effects: Filter → Distortion → Bitcrusher → Reverb
    if layer.filter_freq>0: wave = lowpass_filter(wave, layer.filter_freq, SAMPLE_RATE)
    if layer.distortion>0: wave = distortion(wave, layer.distortion)
    if layer.bitcrusher>0: wave = bitcrusher(wave, layer.bitcrusher)
    if layer.reverb>0: wave = multitap_reverb(wave, [0.01,0.03,0.05], layer.reverb, SAMPLE_RATE)

    # Apply volume and stereo panning
    wave *= layer.volume
    left = wave * np.sqrt(1-layer.pan)
    right = wave * np.sqrt(layer.pan)
    return np.column_stack([left,right])

def generate_final_wave(layers: list[Layer]) -> np.ndarray:
    if not layers: return np.zeros((1,2))
    max_len = int(SAMPLE_RATE*max(layer.dur for layer in layers))
    final_wave = np.zeros((max_len,2))
    for layer in layers:
        wave = generate_layer_wave(layer)
        if len(wave) < max_len:
            padded = np.zeros((max_len,2))
            padded[:len(wave)] = wave
            wave = padded
        final_wave += wave
    return normalize(final_wave)
