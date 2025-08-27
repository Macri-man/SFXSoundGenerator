import sys
import numpy as np
import sounddevice as sd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QComboBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

SAMPLE_RATE = 44100

class SFXGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SFX Generator")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Type selector
        self.type_label = QLabel("SFX Type:")
        self.layout.addWidget(self.type_label)

        self.sfx_type = QComboBox()
        self.sfx_type.addItems(["Beep", "Sweep", "Noise", "Boop"])
        self.layout.addWidget(self.sfx_type)

        # Frequency slider
        self.freq_label = QLabel("Frequency: 440 Hz")
        self.layout.addWidget(self.freq_label)

        self.freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.freq_slider.setMinimum(100)
        self.freq_slider.setMaximum(5000)
        self.freq_slider.setValue(440)
        self.freq_slider.valueChanged.connect(self.update_freq_label)
        self.layout.addWidget(self.freq_slider)

        # Duration slider
        self.dur_label = QLabel("Duration: 0.5 s")
        self.layout.addWidget(self.dur_label)

        self.dur_slider = QSlider(Qt.Orientation.Horizontal)
        self.dur_slider.setMinimum(100)
        self.dur_slider.setMaximum(2000)
        self.dur_slider.setValue(500)
        self.dur_slider.valueChanged.connect(self.update_dur_label)
        self.layout.addWidget(self.dur_slider)

        # Play button
        self.play_button = QPushButton("Play SFX")
        self.play_button.clicked.connect(self.play_sfx)
        self.layout.addWidget(self.play_button)

    def update_freq_label(self, value):
        self.freq_label.setText(f"Frequency: {value} Hz")

    def update_dur_label(self, value):
        self.dur_label.setText(f"Duration: {value/1000:.2f} s")

    def play_sfx(self):
        sfx_type = self.sfx_type.currentText()
        freq = self.freq_slider.value()
        dur = self.dur_slider.value() / 1000.0

        t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
        if sfx_type == "Beep":
            wave = 0.5 * np.sin(2 * np.pi * freq * t)
        elif sfx_type == "Sweep":
            wave = 0.5 * np.sin(2 * np.pi * np.linspace(freq, freq*0.2, len(t)) * t)
        elif sfx_type == "Noise":
            wave = 0.5 * np.random.uniform(-1, 1, len(t))
        elif sfx_type == "Boop":
            wave = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-5 * t)
        else:
            wave = np.zeros_like(t)

        sd.play(wave, SAMPLE_RATE)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SFXGenerator()
    window.show()
    sys.exit(app.exec())
