import sys, threading, json
import numpy as np
import sounddevice as sd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QComboBox, QPushButton, QFileDialog, QCheckBox

from layer import Layer
from synth import generate_final_wave
from ui_controls import ControlButtons
from ui_tabs import BasicTab, AdvancedTab
from ui_controls import LayerSelector

SAMPLE_RATE = 44100

class SFXGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SFX Generator")
        self.layers = [Layer()]
        self.current_index = 0
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- Tabs ---
        self.tabs = QTabWidget()
        self.basic_tab = BasicTab(self.layers, self.current_index, self.update_wave)
        self.advanced_tab = AdvancedTab(self.layers, self.current_index, self.update_wave)
        self.tabs.addTab(self.basic_tab, "Basic")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.layout.addWidget(self.tabs)

        # --- Layer Selector ---
        layer_layout = QHBoxLayout()
        layer_label = QLabel("Select Layer:")
        self.layer_selector = LayerSelector(self.layers, self.change_layer)
        layer_layout.addWidget(layer_label)
        layer_layout.addWidget(self.layer_selector)
        self.layout.addLayout(layer_layout)

        # --- Presets ---
        preset_layout = QHBoxLayout()
        preset_label = QLabel("Preset:")
        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(["Random", "Explosion", "Laser", "Whoosh", "Impact", "Power-Up"])
        self.preset_dropdown.currentTextChanged.connect(self.apply_preset)
        preset_layout.addWidget(preset_label)
        preset_layout.addWidget(self.preset_dropdown)

        self.load_preset_btn = QPushButton("Load Preset")
        self.load_preset_btn.clicked.connect(self.load_preset_file)
        self.save_preset_btn = QPushButton("Save Preset")
        self.save_preset_btn.clicked.connect(self.save_preset_file)
        self.preview_checkbox = QCheckBox("Preview")
        preset_layout.addWidget(self.load_preset_btn)
        preset_layout.addWidget(self.save_preset_btn)
        preset_layout.addWidget(self.preview_checkbox)
        self.layout.addLayout(preset_layout)

        # --- Controls ---
        self.controls = ControlButtons(self.layers)
        self.layout.addWidget(self.controls)
        self.controls.play_btn.clicked.connect(self.play_sfx)
        self.controls.save_btn.clicked.connect(self.save_sfx)
        self.controls.random_btn.clicked.connect(lambda: self.random_sfx())

    # ------------------- Layer Management -------------------
    def change_layer(self, index):
        self.current_index = index
        self.basic_tab.current_index = index
        self.advanced_tab.current_index = index
        self.basic_tab.load_layer()
        self.advanced_tab.load_layer()

    # ------------------- Wave / Playback -------------------
    def update_wave(self):
        if self.preview_checkbox.isChecked():
            wave = generate_final_wave(self.layers)
            sd.stop()
            sd.play(wave, SAMPLE_RATE)

    def play_sfx(self):
        wave = generate_final_wave(self.layers)
        if hasattr(self, "play_thread") and self.play_thread.is_alive():
            sd.stop()
        self.play_thread = threading.Thread(target=lambda: sd.play(wave, SAMPLE_RATE))
        self.play_thread.start()

    def save_sfx(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save SFX", "", "WAV Files (*.wav)")
        if path:
            from scipy.io.wavfile import write
            wave = generate_final_wave(self.layers)
            write(path, SAMPLE_RATE, (wave*32767).astype(np.int16))

    # ------------------- Preset Functions -------------------
    def apply_preset(self, preset_name):
        if preset_name == "Random":
            self.random_sfx()
        else:
            self.random_sfx(sfx_type=preset_name.lower())

    def load_preset_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Preset", "", "JSON Files (*.json)")
        if not path:
            return
        with open(path, "r") as f:
            preset_data = json.load(f)
        self.layers = []
        for layer_data in preset_data.get("layers", []):
            layer = Layer()
            for key, val in layer_data.items():
                setattr(layer, key, val)
            self.layers.append(layer)
        self.layer_selector.layers = self.layers
        self.layer_selector.update_selector()
        self.basic_tab.layers = self.layers
        self.advanced_tab.layers = self.layers
        self.basic_tab.load_layer()
        self.advanced_tab.load_layer()
        self.update_wave()

    def save_preset_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Preset", "", "JSON Files (*.json)")
        if not path:
            return
        preset_data = {"layers":[{k:getattr(layer,k) for k in vars(layer)} for layer in self.layers]}
        with open(path,"w") as f:
            json.dump(preset_data, f, indent=4)

    # ------------------- Random SFX -------------------
    def random_sfx(self, sfx_type=None):
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

            # Preset tweaks
            if sfx_type=="explosion":
                layer.waveform="Noise"; layer.dur=random.uniform(0.2,1.0)
            elif sfx_type=="laser":
                layer.waveform=random.choice(["Sine","Square"]); layer.freq=random.randint(800,5000); layer.freq_end=random.randint(200,3000)
            elif sfx_type=="whoosh":
                layer.waveform="Noise"; layer.freq=random.randint(100,1000); layer.freq_end=random.randint(500,4000)
            elif sfx_type=="impact":
                layer.waveform=random.choice(["Square","Triangle","Noise"]); layer.dur=random.uniform(0.05,0.3)
            elif sfx_type=="powerup":
                layer.waveform="Sine"; layer.freq=random.randint(400,1500); layer.freq_end=random.randint(1500,4000)

        self.basic_tab.load_layer()
        self.advanced_tab.load_layer()
        self.update_wave()


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = SFXGenerator()
    window.show()
    sys.exit(app.exec())
