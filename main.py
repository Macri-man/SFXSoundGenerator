import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QComboBox, QFileDialog, QGroupBox, QTabWidget
)
from PyQt6.QtCore import Qt
import random
from scipy.signal import sawtooth, square, butter, lfilter

SAMPLE_RATE = 44100

class Layer:
    def __init__(self, name="Layer 1"):
        self.name = name
        self.waveform = "Sine"
        self.freq = 440
        self.dur = 0.5
        self.adsr = {"Attack":50,"Decay":50,"Sustain":70,"Release":50}
        self.lfo_freq = 0
        self.lfo_depth = 0
        self.distortion = 0
        self.reverb = 0
        self.filter_freq = 0

class SFXGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Layer SFX Generator")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layers = [Layer()]
        self.current_layer_index = 0

        # Tabs
        self.tabs = QTabWidget()
        self.basic_tab = QWidget()
        self.advanced_tab = QWidget()
        self.tabs.addTab(self.basic_tab, "Basic SFX")
        self.tabs.addTab(self.advanced_tab, "Advanced FX")
        self.layout.addWidget(self.tabs)

        self.init_basic_tab()
        self.init_advanced_tab()
        self.init_layer_controls()
        self.init_buttons()
        self.update_ui_from_layer()

    # ---------------- Layer Selection ----------------
    def init_layer_controls(self):
        layer_layout = QHBoxLayout()
        layer_layout.addWidget(QLabel("Select Layer:"))
        self.layer_selector = QComboBox()
        self.update_layer_selector()
        self.layer_selector.currentIndexChanged.connect(self.change_layer)
        layer_layout.addWidget(self.layer_selector)
        self.add_layer_button = QPushButton("Add Layer")
        self.add_layer_button.clicked.connect(self.add_layer)
        layer_layout.addWidget(self.add_layer_button)
        self.layout.addLayout(layer_layout)

    def update_layer_selector(self):
        self.layer_selector.blockSignals(True)
        self.layer_selector.clear()
        for i, layer in enumerate(self.layers):
            self.layer_selector.addItem(f"{i+1}: {layer.name}")
        self.layer_selector.setCurrentIndex(self.current_layer_index)
        self.layer_selector.blockSignals(False)

    def change_layer(self, index):
        self.current_layer_index = index
        self.update_ui_from_layer()

    def add_layer(self):
        new_layer = Layer(name=f"Layer {len(self.layers)+1}")
        self.layers.append(new_layer)
        self.current_layer_index = len(self.layers)-1
        self.update_layer_selector()
        self.update_ui_from_layer()

    # ---------------- Basic Tab ----------------
    def init_basic_tab(self):
        layout = QVBoxLayout()
        self.basic_tab.setLayout(layout)

        # Waveform
        wf_layout = QHBoxLayout()
        wf_layout.addWidget(QLabel("Waveform:"))
        self.basic_waveform = QComboBox()
        self.basic_waveform.addItems(["Sine","Square","Triangle","Sawtooth"])
        self.basic_waveform.currentIndexChanged.connect(self.sync_waveform_from_basic)
        wf_layout.addWidget(self.basic_waveform)
        layout.addLayout(wf_layout)

        # Frequency
        freq_layout = QHBoxLayout()
        self.basic_freq_label = QLabel("Frequency: 440 Hz")
        self.basic_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.basic_freq_slider.setMinimum(100)
        self.basic_freq_slider.setMaximum(5000)
        self.basic_freq_slider.valueChanged.connect(self.sync_freq_from_basic)
        freq_layout.addWidget(self.basic_freq_label)
        freq_layout.addWidget(self.basic_freq_slider)
        layout.addLayout(freq_layout)

        # Duration
        dur_layout = QHBoxLayout()
        self.basic_dur_label = QLabel("Duration: 0.5 s")
        self.basic_dur_slider = QSlider(Qt.Orientation.Horizontal)
        self.basic_dur_slider.setMinimum(100)
        self.basic_dur_slider.setMaximum(2000)
        self.basic_dur_slider.valueChanged.connect(self.sync_dur_from_basic)
        dur_layout.addWidget(self.basic_dur_label)
        dur_layout.addWidget(self.basic_dur_slider)
        layout.addLayout(dur_layout)

    # ---------------- Advanced Tab ----------------
    def init_advanced_tab(self):
        layout = QVBoxLayout()
        self.advanced_tab.setLayout(layout)

        # Waveform & ADSR
        wave_group = QGroupBox("Waveform & ADSR")
        wave_layout = QVBoxLayout()
        layout.addWidget(wave_group)
        wave_group.setLayout(wave_layout)

        # Waveform
        wave_layout.addWidget(QLabel("Waveform:"))
        self.adv_waveform = QComboBox()
        self.adv_waveform.addItems(["Sine","Square","Triangle","Sawtooth"])
        self.adv_waveform.currentIndexChanged.connect(self.sync_waveform_from_adv)
        wave_layout.addWidget(self.adv_waveform)

        # Frequency
        self.adv_freq_label = QLabel("Frequency: 440 Hz")
        self.adv_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.adv_freq_slider.setMinimum(100)
        self.adv_freq_slider.setMaximum(5000)
        self.adv_freq_slider.valueChanged.connect(self.sync_freq_from_adv)
        wave_layout.addWidget(self.adv_freq_label)
        wave_layout.addWidget(self.adv_freq_slider)

        # Duration
        self.adv_dur_label = QLabel("Duration: 0.5 s")
        self.adv_dur_slider = QSlider(Qt.Orientation.Horizontal)
        self.adv_dur_slider.setMinimum(100)
        self.adv_dur_slider.setMaximum(2000)
        self.adv_dur_slider.valueChanged.connect(self.sync_dur_from_adv)
        wave_layout.addWidget(self.adv_dur_label)
        wave_layout.addWidget(self.adv_dur_slider)

        # ADSR sliders
        self.adsr_sliders={}
        self.adsr_values={"Attack":50,"Decay":50,"Sustain":70,"Release":50}
        for param in ["Attack","Decay","Sustain","Release"]:
            label = QLabel(f"{param}: {self.adsr_values[param]} ms" if param!="Sustain" else f"{param}: {self.adsr_values[param]/100:.2f}")
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(1000)
            slider.valueChanged.connect(lambda val,p=param,l=label:self.update_adsr_label(p,l,val))
            wave_layout.addWidget(label)
            wave_layout.addWidget(slider)
            self.adsr_sliders[param]=slider

        # LFO
        lfo_group = QGroupBox("LFO / Vibrato")
        lfo_layout = QVBoxLayout()
        layout.addWidget(lfo_group)
        lfo_group.setLayout(lfo_layout)
        self.lfo_freq_label = QLabel("LFO Freq: 0 Hz")
        self.lfo_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.lfo_freq_slider.setMinimum(0)
        self.lfo_freq_slider.setMaximum(20)
        self.lfo_freq_slider.valueChanged.connect(self.update_lfo_label)
        self.lfo_depth_label = QLabel("LFO Depth: 0 Hz")
        self.lfo_depth_slider = QSlider(Qt.Orientation.Horizontal)
        self.lfo_depth_slider.setMinimum(0)
        self.lfo_depth_slider.setMaximum(200)
        self.lfo_depth_slider.valueChanged.connect(self.update_lfo_label)
        lfo_layout.addWidget(self.lfo_freq_label)
        lfo_layout.addWidget(self.lfo_freq_slider)
        lfo_layout.addWidget(self.lfo_depth_label)
        lfo_layout.addWidget(self.lfo_depth_slider)

        # FX
        fx_group = QGroupBox("Effects")
        fx_layout = QVBoxLayout()
        layout.addWidget(fx_group)
        fx_group.setLayout(fx_layout)

        self.dist_label = QLabel("Distortion: 0%")
        self.dist_slider = QSlider(Qt.Orientation.Horizontal)
        self.dist_slider.setMinimum(0)
        self.dist_slider.setMaximum(100)
        self.dist_slider.valueChanged.connect(lambda val:self.dist_label.setText(f"Distortion: {val}%"))
        fx_layout.addWidget(self.dist_label)
        fx_layout.addWidget(self.dist_slider)

        self.reverb_label = QLabel("Reverb: 0%")
        self.reverb_slider = QSlider(Qt.Orientation.Horizontal)
        self.reverb_slider.setMinimum(0)
        self.reverb_slider.setMaximum(100)
        self.reverb_slider.valueChanged.connect(lambda val:self.reverb_label.setText(f"Reverb: {val}%"))
        fx_layout.addWidget(self.reverb_label)
        fx_layout.addWidget(self.reverb_slider)

        self.filter_label = QLabel("Lowpass Filter: 0 Hz")
        self.filter_slider = QSlider(Qt.Orientation.Horizontal)
        self.filter_slider.setMinimum(0)
        self.filter_slider.setMaximum(20000)
        self.filter_slider.valueChanged.connect(lambda val:self.filter_label.setText(f"Lowpass Filter: {val} Hz"))
        fx_layout.addWidget(self.filter_label)
        fx_layout.addWidget(self.filter_slider)

    # ---------------- Buttons ----------------
    def init_buttons(self):
        btn_layout = QHBoxLayout()
        self.play_button = QPushButton("Play SFX")
        self.play_button.clicked.connect(self.play_sfx)
        self.save_button = QPushButton("Save SFX")
        self.save_button.clicked.connect(self.save_sfx)
        self.random_button = QPushButton("Random SFX")
        self.random_button.clicked.connect(self.random_sfx)
        btn_layout.addWidget(self.play_button)
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.random_button)
        self.layout.addLayout(btn_layout)

    # ---------------- UI Sync ----------------
    def update_ui_from_layer(self):
        layer = self.layers[self.current_layer_index]
        # Basic tab
        self.basic_waveform.setCurrentText(layer.waveform)
        self.basic_freq_slider.setValue(int(layer.freq))
        self.basic_dur_slider.setValue(int(layer.dur*1000))
        # Advanced tab
        self.adv_waveform.setCurrentText(layer.waveform)
        self.adv_freq_slider.setValue(int(layer.freq))
        self.adv_dur_slider.setValue(int(layer.dur*1000))
        for param in ["Attack","Decay","Sustain","Release"]:
            self.adsr_sliders[param].setValue(layer.adsr[param])
        self.lfo_freq_slider.setValue(layer.lfo_freq)
        self.lfo_depth_slider.setValue(layer.lfo_depth)
        self.dist_slider.setValue(layer.distortion)
        self.reverb_slider.setValue(layer.reverb)
        self.filter_slider.setValue(layer.filter_freq)

    # ---------------- Basic Sync ----------------
    def sync_waveform_from_basic(self, index): self.layers[self.current_layer_index].waveform=self.basic_waveform.currentText(); self.adv_waveform.setCurrentText(self.basic_waveform.currentText())
    def sync_freq_from_basic(self, val): self.basic_freq_label.setText(f"Frequency: {val} Hz"); self.layers[self.current_layer_index].freq=val; self.adv_freq_slider.setValue(val)
    def sync_dur_from_basic(self, val): self.basic_dur_label.setText(f"Duration: {val/1000:.2f} s"); self.layers[self.current_layer_index].dur=val/1000; self.adv_dur_slider.setValue(val)
    # ---------------- Advanced Sync ----------------
    def sync_waveform_from_adv(self, index): self.layers[self.current_layer_index].waveform=self.adv_waveform.currentText(); self.basic_waveform.setCurrentText(self.adv_waveform.currentText())
    def sync_freq_from_adv(self, val): self.adv_freq_label.setText(f"Frequency: {val} Hz"); self.layers[self.current_layer_index].freq=val; self.basic_freq_slider.setValue(val)
    def sync_dur_from_adv(self, val): self.adv_dur_label.setText(f"Duration: {val/1000:.2f} s"); self.layers[self.current_layer_index].dur=val/1000; self.basic_dur_slider.setValue(val)

    def update_adsr_label(self,param,label,value):
        layer = self.layers[self.current_layer_index]
        layer.adsr[param]=value
        if param=="Sustain": label.setText(f"{param}: {value/100:.2f}")
        else: label.setText(f"{param}: {value} ms")

    def update_lfo_label(self,_=0):
        layer = self.layers[self.current_layer_index]
        layer.lfo_freq = self.lfo_freq_slider.value()
        layer.lfo_depth = self.lfo_depth_slider.value()
        self.lfo_freq_label.setText(f"LFO Freq: {layer.lfo_freq} Hz")
        self.lfo_depth_label.setText(f"LFO Depth: {layer.lfo_depth} Hz")

    # ---------------- Wave Generation ----------------
    def generate_layer_wave(self, layer:Layer):
        t = np.linspace(0, layer.dur, int(SAMPLE_RATE*layer.dur), endpoint=False)
        # Phase accumulation FM
        phase = np.cumsum(2*np.pi*(layer.freq + layer.lfo_depth*np.sin(2*np.pi*layer.lfo_freq*t))/SAMPLE_RATE)
        if layer.waveform=="Sine": wave = np.sin(phase)
        elif layer.waveform=="Square": wave = square(phase)
        elif layer.waveform=="Triangle": wave = sawtooth(phase,0.5)
        elif layer.waveform=="Sawtooth": wave = sawtooth(phase)
        else: wave = np.zeros_like(t)

        # Apply ADSR
        wave *= self.apply_adsr(len(wave), layer.adsr)

        # Distortion
        if layer.distortion>0: wave = np.tanh(wave*(1+5*layer.distortion/100))

        # Multi-tap Reverb
        if layer.reverb>0:
            taps = [0.02, 0.04, 0.06]  # in seconds
            reverb_wave = np.zeros_like(wave)
            for tap in taps:
                delay = int(SAMPLE_RATE * tap)
                if delay < len(wave):
                    temp = np.zeros_like(wave)
                    temp[delay:] = wave[:-delay]
                    reverb_wave += temp
            reverb_wave /= len(taps)
            wave = (1-layer.reverb/100)*wave + (layer.reverb/100)*reverb_wave

        # Lowpass filter
        if layer.filter_freq>0:
            filter_cut = min(layer.filter_freq, SAMPLE_RATE/2-1)
            b,a = butter(2, filter_cut/(SAMPLE_RATE/2), 'low')
            wave = lfilter(b,a,wave)

        # Normalize
        if np.max(np.abs(wave))>0: wave /= np.max(np.abs(wave))
        return wave

    def apply_adsr(self,length,adsr):
        attack = int(SAMPLE_RATE*adsr["Attack"]/1000)
        decay = int(SAMPLE_RATE*adsr["Decay"]/1000)
        sustain_level = adsr["Sustain"]/100
        release = int(SAMPLE_RATE*adsr["Release"]/1000)
        sustain_length = max(length-(attack+decay+release),0)
        env = np.zeros(length)
        if attack>0: env[:attack] = np.linspace(0,1,attack)
        if decay>0: env[attack:attack+decay] = np.linspace(1,sustain_level,decay)
        if sustain_length>0: env[attack+decay:attack+decay+sustain_length] = sustain_level
        if release>0: env[-release:] = np.linspace(sustain_level,0,release)
        return env

    # ---------------- Final Wave ----------------
    def generate_final_wave(self):
        max_len = int(SAMPLE_RATE * max(layer.dur for layer in self.layers))
        final_wave = np.zeros(max_len)
        for layer in self.layers:
            wave = self.generate_layer_wave(layer)
            final_wave[:len(wave)] += wave
        if len(self.layers)>0: final_wave /= len(self.layers)
        return final_wave

    # ---------------- Playback / Save ----------------
    def play_sfx(self):
        final_wave = self.generate_final_wave()
        sd.play(final_wave, SAMPLE_RATE)

    def save_sfx(self):
        final_wave = self.generate_final_wave()
        file_path,_ = QFileDialog.getSaveFileName(self,"Save SFX","","WAV Files (*.wav)")
        if file_path: sf.write(file_path, final_wave, SAMPLE_RATE)

    # ---------------- Random ----------------
    def random_sfx(self):
        for layer in self.layers:
            layer.waveform = random.choice(["Sine","Square","Triangle","Sawtooth"])
            layer.freq = random.randint(200,4000)
            layer.dur = random.uniform(0.1,2)
            layer.adsr = {"Attack":random.randint(0,500),
                          "Decay":random.randint(0,500),
                          "Sustain":random.randint(20,100),
                          "Release":random.randint(0,500)}
            layer.lfo_freq = random.randint(0,10)
            layer.lfo_depth = random.randint(0,100)
            layer.distortion = random.randint(0,50)
            layer.reverb = random.randint(0,50)
            layer.filter_freq = random.randint(0,5000)
        self.update_ui_from_layer()
        self.play_sfx()

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=SFXGenerator()
    window.show()
    sys.exit(app.exec())
