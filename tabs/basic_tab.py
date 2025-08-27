from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox

class BasicTab(QWidget):
    """Basic waveform, frequency, duration controls."""
    def __init__(self, layers, current_index, update_callback):
        super().__init__()
        self.layers = layers
        self.current_index = current_index
        self.update_callback = update_callback
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Waveform
        wf_layout = QHBoxLayout()
        wf_layout.addWidget(QLabel("Waveform:"))
        self.waveform_dropdown = QComboBox()
        self.waveform_dropdown.addItems(["Sine", "Square", "Triangle", "Sawtooth", "Noise"])
        self.waveform_dropdown.currentIndexChanged.connect(lambda _: self.update_layer())
        wf_layout.addWidget(self.waveform_dropdown)
        self.layout.addLayout(wf_layout)

        # Frequency
        freq_layout = QHBoxLayout()
        self.freq_label = QLabel("Frequency: 440 Hz")
        self.freq_slider = QSlider()
        self.freq_slider.setMinimum(100); self.freq_slider.setMaximum(5000)
        self.freq_slider.valueChanged.connect(lambda _: self.update_layer())
        freq_layout.addWidget(self.freq_label)
        freq_layout.addWidget(self.freq_slider)
        self.layout.addLayout(freq_layout)

        # Duration
        dur_layout = QHBoxLayout()
        self.dur_label = QLabel("Duration: 0.5 s")
        self.dur_slider = QSlider()
        self.dur_slider.setMinimum(50); self.dur_slider.setMaximum(2000)
        self.dur_slider.valueChanged.connect(lambda _: self.update_layer())
        dur_layout.addWidget(self.dur_label)
        dur_layout.addWidget(self.dur_slider)
        self.layout.addLayout(dur_layout)

        self.load_layer()

    def load_layer(self):
        layer = self.layers[self.current_index]
        self.waveform_dropdown.setCurrentText(layer.waveform)
        self.freq_slider.setValue(int(layer.freq))
        self.freq_label.setText(f"Frequency: {layer.freq} Hz")
        self.dur_slider.setValue(int(layer.dur*1000))
        self.dur_label.setText(f"Duration: {layer.dur:.2f} s")

    def update_layer(self):
        layer = self.layers[self.current_index]
        layer.waveform = self.waveform_dropdown.currentText()
        layer.freq = self.freq_slider.value()
        layer.dur = self.dur_slider.value()/1000
        self.freq_label.setText(f"Frequency: {layer.freq} Hz")
        self.dur_label.setText(f"Duration: {layer.dur:.2f} s")
        self.update_callback()
