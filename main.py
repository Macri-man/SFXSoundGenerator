import sys, json
import numpy as np
import random 
import sounddevice as sd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QComboBox, QPushButton, QFileDialog, QCheckBox
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer

from layer import Layer
from synth import generate_final_wave
from preset_manager import DEFAULT_PRESETS, PresetManager

from ui_controls import LayerSelector, ControlButtons
from ui_tabs import BasicTab, AdvancedTab

SAMPLE_RATE = 44100

class SFXGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SFX Generator")

        # Layer management
        self.layers = [Layer()]
        self.current_index = 0

        # Playback
        self._preview_timer = QTimer()
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._play_preview)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Setup UI
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
        preset_layout.addWidget(self.load_preset_btn)
        preset_layout.addWidget(self.save_preset_btn)

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
            self._preview_timer.start(100)  # debounce updates by 100ms

    def _play_preview(self):
        sd.stop()
        wave = generate_final_wave(self.layers)
        sd.play(wave, SAMPLE_RATE)

    def play_sfx(self):
        sd.stop()
        wave = generate_final_wave(self.layers)
        sd.play(wave, SAMPLE_RATE)

    def save_sfx(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save SFX", "", "WAV Files (*.wav)")
        if not path:
            return
        from scipy.io.wavfile import write
        wave = generate_final_wave(self.layers)
        write(path, SAMPLE_RATE, (wave * 32767).astype(np.int16))

    # ------------------- Presets -------------------
    def load_preset_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Preset", "", "JSON Files (*.json)")
        if not path:
            return
        with open(path, "r") as f:
            preset_data = json.load(f)
        self.layers = [Layer.from_dict(d) for d in preset_data.get("layers", [])]
        self.current_index = 0
        self._update_layer_widgets()
        self.update_wave()


    def save_preset_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Preset", "", "JSON Files (*.json)")
        if not path:
            return
        preset_data = {"layers": [layer.to_dict() for layer in self.layers]}
        with open(path, "w") as f:
            json.dump(preset_data, f, indent=4)

    def save_preset_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Preset", "", "JSON Files (*.json)")
        if not path: return
        preset_data = {"layers": [layer.to_dict() for layer in self.layers]}
        with open(path, "w") as f:
            json.dump(preset_data, f, indent=4)

    # ------------------- Random SFX -------------------
    def random_sfx(self):
        self.layers = [self._random_layer() for _ in self.layers]
        self.current_index = 0
        self._update_layer_widgets()
        self.update_wave()


    def _random_layer(self):
        """
        Generate a random Layer using a dictionary and Layer.from_dict
        """
        layer_data = {
            "waveform": random.choice(["Sine", "Square", "Triangle", "Sawtooth", "Noise"]),
            "freq": random.randint(100, 4000),
            "freq_end": None,  # Will be set to freq if None
            "dur": random.uniform(0.05, 1.5),
            "adsr": {
                "Attack": random.randint(0, 50),
                "Decay": random.randint(10, 300),
                "Sustain": random.randint(10, 70),
                "Release": random.randint(10, 300)
            },
            "lfo_freq": random.uniform(0, 15),
            "lfo_depth": random.randint(0, 50),
            "distortion": random.randint(0, 80),
            "reverb": random.randint(0, 50),
            "filter_freq": random.randint(500, 8000),
            "volume": random.uniform(0.5, 1.0),
            "pan": random.uniform(0, 1)
        }

        # If freq_end is None, set it equal to freq
        if layer_data["freq_end"] is None:
            layer_data["freq_end"] = layer_data["freq"]

        return Layer.from_dict(layer_data)

    # ------------------- Helpers -------------------
    def _update_layer_widgets(self):
        self.layer_selector.layers = self.layers
        self.layer_selector.update_selector()
        self.basic_tab.layers = self.layers
        self.advanced_tab.layers = self.layers
        self.basic_tab.load_layer()
        self.advanced_tab.load_layer()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SFXGenerator()
    window.show()
    sys.exit(app.exec())
