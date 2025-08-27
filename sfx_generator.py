import sys, threading, json
import numpy as np
import sounddevice as sd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QComboBox, QPushButton, QFileDialog, QCheckBox
)
from PyQt6.QtGui import QGuiApplication
from layer import Layer
from synth import generate_final_wave
from preset_manager import DEFAULT_PRESETS, generate_layer_from_preset, save_presets, load_presets

from ui_controls import LayerSelector, ControlButtons
from ui_tabs import BasicTab, AdvancedTab

SAMPLE_RATE = 44100

QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    QGuiApplication.HighDpiScaleFactorRoundingPolicy.PassThrough
)

class SFXGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SFX Generator")
        self.layers = [Layer()]
        self.current_index = 0
        self.play_thread = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._setup_tabs()
        self._setup_layer_selector()
        self._setup_presets()
        self._setup_controls()

    # ------------------- UI Setup -------------------
    def _setup_tabs(self):
        self.tabs = QTabWidget()
        self.basic_tab = BasicTab(self.layers, self.current_index, self.update_wave)
        self.advanced_tab = AdvancedTab(self.layers, self.current_index, self.update_wave)
        self.tabs.addTab(self.basic_tab, "Basic")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.layout.addWidget(self.tabs)

    def _setup_layer_selector(self):
        layer_layout = QHBoxLayout()
        layer_label = QLabel("Select Layer:")
        self.layer_selector = LayerSelector(self.layers, self.change_layer)
        layer_layout.addWidget(layer_label)
        layer_layout.addWidget(self.layer_selector)
        self.layout.addLayout(layer_layout)

    def _setup_presets(self):
        preset_layout = QHBoxLayout()
        preset_label = QLabel("Preset:")
        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(["Random"] + list(DEFAULT_PRESETS.keys()))
        self.preset_dropdown.currentTextChanged.connect(self.apply_preset)
        preset_layout.addWidget(preset_label)
        preset_layout.addWidget(self.preset_dropdown)

        self.preview_checkbox = QCheckBox("Preview")
        self.preview_checkbox.setChecked(True)
        preset_layout.addWidget(self.preview_checkbox)

        self.load_preset_btn = QPushButton("Load Preset")
        self.load_preset_btn.clicked.connect(self.load_preset_file)
        self.save_preset_btn = QPushButton("Save Preset")
        self.save_preset_btn.clicked.connect(self.save_preset_file)
        for btn in [self.load_preset_btn, self.save_preset_btn]:
            preset_layout.addWidget(btn)

        self.layout.addLayout(preset_layout)

    def _setup_controls(self):
        self.controls = ControlButtons(
            play_callback=self.play_sfx,
            save_callback=self.save_sfx,
            random_callback=self.random_sfx
        )
        self.layout.addWidget(self.controls)

    # ------------------- Layer Management -------------------
    def change_layer(self, index):
        self.current_index = index
        self.basic_tab.current_index = index
        self.advanced_tab.current_index = index
        self.basic_tab.load_layer()
        self.advanced_tab.load_layer()

    # ------------------- Wave / Playback -------------------
    def update_wave(self):
        if getattr(self, "preview_checkbox", None) and self.preview_checkbox.isChecked():
            wave = generate_final_wave(self.layers)
            sd.stop()
            sd.play(wave, SAMPLE_RATE)

    def play_sfx(self):
        wave = generate_final_wave(self.layers)
        if self.play_thread and self.play_thread.is_alive():
            sd.stop()
        self.play_thread = threading.Thread(target=lambda: sd.play(wave, SAMPLE_RATE))
        self.play_thread.start()

    def save_sfx(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save SFX", "", "WAV Files (*.wav)")
        if path:
            from scipy.io.wavfile import write
            wave = generate_final_wave(self.layers)
            write(path, SAMPLE_RATE, (wave*32767).astype(np.int16))

    # ------------------- Presets -------------------
    def apply_preset(self, preset_name):
        if preset_name == "Random":
            self.random_sfx()
        else:
            self.layers = generate_layer_from_preset(preset_name)
            self.current_index = 0
            self._update_layer_widgets()
            self.update_wave()

    def load_preset_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Preset", "", "JSON Files (*.json)")
        if not path: return
        with open(path, "r") as f:
            preset_data = json.load(f)
        self.layers.clear()
        for layer_data in preset_data.get("layers", []):
            layer = Layer()
            for key, val in layer_data.items():
                setattr(layer, key, val)
            self.layers.append(layer)
        self._update_layer_widgets()

    def save_preset_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Preset", "", "JSON Files (*.json)")
        if not path: return
        preset_data = {"layers":[{k:getattr(layer,k) for k in vars(layer)} for layer in self.layers]}
        with open(path,"w") as f: json.dump(preset_data,f,indent=4)

    # ------------------- Random SFX -------------------
    def random_sfx(self):
        import random
        for layer in self.layers:
            layer.waveform = random.choice(["Sine","Square","Triangle","Sawtooth","Noise"])
            layer.freq = random.randint(100,4000)
            layer.freq_end = layer.freq
            layer.dur = random.uniform(0.05,1.5)
            layer.adsr = {
                "Attack": random.randint(0,50),
                "Decay": random.randint(10,300),
                "Sustain": random.randint(10,70),
                "Release": random.randint(10,300)
            }
            layer.lfo_freq = random.uniform(0,15)
            layer.lfo_depth = random.randint(0,50)
            layer.distortion = random.randint(0,80)
            layer.reverb = random.randint(0,50)
            layer.filter_freq = random.randint(500,8000)
            layer.volume = random.uniform(0.5,1.0)
            layer.pan = random.uniform(0,1)
        self._update_layer_widgets()
        self.update_wave()

    # ------------------- Helpers -------------------
    def _update_layer_widgets(self):
        self.layer_selector.layers = self.layers
        self.layer_selector.update_selector()
        self.basic_tab.layers = self.layers
        self.advanced_tab.layers = self.layers
        self.basic_tab.load_layer()
        self.advanced_tab.load_layer()


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = SFXGenerator()
    window.show()
    sys.exit(app.exec())
