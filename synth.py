import numpy as np
from scipy.signal import sawtooth, square
from effects import normalize, lowpass_filter, distortion, multitap_reverb

SAMPLE_RATE = 44100

def apply_adsr(length, adsr):
    attack = int(SAMPLE_RATE*adsr["Attack"]/1000)
    decay = int(SAMPLE_RATE*adsr["Decay"]/1000)
    sustain_level = adsr["Sustain"]/100
    release = int(SAMPLE_RATE*adsr["Release"]/1000)
    sustain_length = max(length-(attack+decay+release),0)

    env = np.zeros(length)
    if attack>0:
        env[:attack] = np.linspace(0,1,attack,endpoint=False)
    if decay>0:
        env[attack:attack+decay] = np.linspace(1,sustain_level,decay,endpoint=False)
    if sustain_length>0:
        env[attack+decay:attack+decay+sustain_length] = sustain_level
    if release>0:
        env[-release:] = np.linspace(sustain_level,0,release,endpoint=True)
    return env

def generate_layer_wave(layer):
    length = int(SAMPLE_RATE*layer.dur)
    t = np.linspace(0, layer.dur, length, endpoint=False)

    # Frequency slide
    freq = np.linspace(layer.freq, getattr(layer, "freq_end", layer.freq), length)
    phase = np.cumsum(2*np.pi*(freq + layer.lfo_depth*np.sin(2*np.pi*layer.lfo_freq*t))/SAMPLE_RATE)

    # Waveform
    if layer.waveform=="Sine":
        wave = np.sin(phase)
    elif layer.waveform=="Square":
        wave = square(phase)
    elif layer.waveform=="Triangle":
        wave = sawtooth(phase, 0.5)
    elif layer.waveform=="Sawtooth":
        wave = sawtooth(phase)
    elif layer.waveform=="Noise":
        wave = np.random.uniform(-1,1,len(t))
    else:
        wave = np.zeros_like(t)

    # Apply ADSR
    wave *= apply_adsr(len(wave), layer.adsr)
    # Filter → Distortion → Reverb
    if layer.filter_freq>0:
        wave = lowpass_filter(wave, layer.filter_freq, SAMPLE_RATE)
    if layer.distortion>0:
        wave = distortion(wave, layer.distortion)
    if layer.reverb>0:
        wave = multitap_reverb(wave, [0.02,0.04,0.06], layer.reverb, SAMPLE_RATE)
    wave *= layer.volume  # Apply layer gain

    # Stereo panning
    left = wave * (1-layer.pan)
    right = wave * layer.pan
    wave_stereo = np.vstack([left,right]).T  # shape (samples, 2)

    return normalize(wave_stereo)

def generate_final_wave(layers):
    if not layers:
        return np.zeros((1,2))
    max_len = int(SAMPLE_RATE*max(layer.dur for layer in layers))
    final_wave = np.zeros((max_len,2))
    for layer in layers:
        wave = generate_layer_wave(layer)
        final_wave[:len(wave)] += wave
    return normalize(final_wave)
