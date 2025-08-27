from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox, QGroupBox

class BasicTab(QWidget):
    def __init__(self, layers, current_index, update_callback):
        super().__init__()
        self.layers = layers
        self.current_index = current_index
        self.update_callback = update_callback
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.waveform_dropdown = None
        self.freq_slider = None
        self.freq_label = None
        self.dur_slider = None
        self.dur_label = None

        self._init_ui()
        self.load_layer()

    # ------------------- UI Initialization -------------------
    def _init_ui(self):
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
        self.freq_slider.setMinimum(100)
        self.freq_slider.setMaximum(5000)
        self.freq_slider.valueChanged.connect(lambda val: self.update_layer())
        freq_layout.addWidget(self.freq_label)
        freq_layout.addWidget(self.freq_slider)
        self.layout.addLayout(freq_layout)

        # Duration
        dur_layout = QHBoxLayout()
        self.dur_label = QLabel("Duration: 0.5 s")
        self.dur_slider = QSlider()
        self.dur_slider.setMinimum(50)
        self.dur_slider.setMaximum(2000)
        self.dur_slider.valueChanged.connect(lambda val: self.update_layer())
        dur_layout.addWidget(self.dur_label)
        dur_layout.addWidget(self.dur_slider)
        self.layout.addLayout(dur_layout)

    # ------------------- Load & Update -------------------
    def load_layer(self):
        layer = self.layers[self.current_index]
        self.waveform_dropdown.setCurrentText(layer.waveform)
        self.freq_slider.setValue(layer.freq)
        self.freq_label.setText(f"Frequency: {layer.freq} Hz")
        self.dur_slider.setValue(int(layer.dur * 1000))
        self.dur_label.setText(f"Duration: {layer.dur:.2f} s")

    def update_layer(self):
        layer = self.layers[self.current_index]
        layer.waveform = self.waveform_dropdown.currentText()
        layer.freq = self.freq_slider.value()
        self.freq_label.setText(f"Frequency: {layer.freq} Hz")
        layer.dur = self.dur_slider.value() / 1000
        self.dur_label.setText(f"Duration: {layer.dur:.2f} s")
        self.update_callback()


class AdvancedTab(QWidget):
    def __init__(self, layers, current_index, update_callback):
        super().__init__()
        self.layers = layers
        self.current_index = current_index
        self.update_callback = update_callback
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.adsr_sliders = {}
        self.lfo_sliders = {}
        self.fx_sliders = {}

        self._init_ui()
        self.load_layer()

    # ------------------- UI Initialization -------------------
    def _init_ui(self):
        self._init_adsr_group()
        self._init_lfo_group()
        self._init_fx_group()

    # ADSR Group
    def _init_adsr_group(self):
        adsr_group = QGroupBox("ADSR")
        adsr_layout = QVBoxLayout()
        adsr_group.setLayout(adsr_layout)
        for param in ["Attack", "Decay", "Sustain", "Release"]:
            label = QLabel(f"{param}: 0")
            slider = QSlider()
            slider.setMinimum(0)
            slider.setMaximum(1000)
            slider.valueChanged.connect(lambda val, p=param, l=label: self._update_adsr(p, l, val))
            adsr_layout.addWidget(label)
            adsr_layout.addWidget(slider)
            self.adsr_sliders[param] = slider
        self.layout.addWidget(adsr_group)

    # LFO / Vibrato Group
    def _init_lfo_group(self):
        lfo_group = QGroupBox("LFO / Vibrato")
        lfo_layout = QVBoxLayout()
        lfo_group.setLayout(lfo_layout)

        # Frequency
        self.lfo_freq_label = QLabel("LFO Frequency: 0 Hz")
        self.lfo_freq_slider = QSlider()
        self.lfo_freq_slider.setMinimum(0)
        self.lfo_freq_slider.setMaximum(20)
        self.lfo_freq_slider.valueChanged.connect(lambda val: self._update_lfo("freq", val))
        lfo_layout.addWidget(self.lfo_freq_label)
        lfo_layout.addWidget(self.lfo_freq_slider)

        # Depth
        self.lfo_depth_label = QLabel("LFO Depth: 0 Hz")
        self.lfo_depth_slider = QSlider()
        self.lfo_depth_slider.setMinimum(0)
        self.lfo_depth_slider.setMaximum(200)
        self.lfo_depth_slider.valueChanged.connect(lambda val: self._update_lfo("depth", val))
        lfo_layout.addWidget(self.lfo_depth_label)
        lfo_layout.addWidget(self.lfo_depth_slider)

        self.lfo_sliders = {"freq": self.lfo_freq_slider, "depth": self.lfo_depth_slider}
        self.layout.addWidget(lfo_group)

    # FX Group
    def _init_fx_group(self):
        fx_group = QGroupBox("Effects")
        fx_layout = QVBoxLayout()
        fx_group.setLayout(fx_layout)

        self.dist_label = QLabel("Distortion: 0%")
        self.dist_slider = QSlider()
        self.dist_slider.setMinimum(0)
        self.dist_slider.setMaximum(100)
        self.dist_slider.valueChanged.connect(lambda val: self._update_fx("distortion", val))
        fx_layout.addWidget(self.dist_label)
        fx_layout.addWidget(self.dist_slider)

        self.reverb_label = QLabel("Reverb: 0%")
        self.reverb_slider = QSlider()
        self.reverb_slider.setMinimum(0)
        self.reverb_slider.setMaximum(100)
        self.reverb_slider.valueChanged.connect(lambda val: self._update_fx("reverb", val))
        fx_layout.addWidget(self.reverb_label)
        fx_layout.addWidget(self.reverb_slider)

        self.filter_label = QLabel("Lowpass Filter: 0 Hz")
        self.filter_slider = QSlider()
        self.filter_slider.setMinimum(0)
        self.filter_slider.setMaximum(20000)
        self.filter_slider.valueChanged.connect(lambda val: self._update_fx("filter_freq", val))
        fx_layout.addWidget(self.filter_label)
        fx_layout.addWidget(self.filter_slider)

        self.fx_sliders = {
            "distortion": self.dist_slider,
            "reverb": self.reverb_slider,
            "filter_freq": self.filter_slider
        }

        self.layout.addWidget(fx_group)

    # ------------------- Load Layer Values -------------------
    def load_layer(self):
        layer = self.layers[self.current_index]
        for param in ["Attack", "Decay", "Sustain", "Release"]:
            self.adsr_sliders[param].setValue(layer.adsr.get(param, 0))
        self.lfo_freq_slider.setValue(layer.lfo_freq)
        self.lfo_depth_slider.setValue(layer.lfo_depth)
        self.dist_slider.setValue(layer.distortion)
        self.reverb_slider.setValue(layer.reverb)
        self.filter_slider.setValue(layer.filter_freq)

    # ------------------- Update Functions -------------------
    def _update_adsr(self, param, label, value):
        layer = self.layers[self.current_index]
        layer.adsr[param] = value
        label.setText(f"{param}: {value/100:.2f}" if param == "Sustain" else f"{param}: {value} ms")
        self.update_callback()

    def _update_lfo(self, typ, value):
        layer = self.layers[self.current_index]
        if typ == "freq":
            layer.lfo_freq = value
            self.lfo_freq_label.setText(f"LFO Frequency: {value} Hz")
        else:
            layer.lfo_depth = value
            self.lfo_depth_label.setText(f"LFO Depth: {value} Hz")
        self.update_callback()

    def _update_fx(self, param, value):
        layer = self.layers[self.current_index]
        setattr(layer, param, value)
        if param == "distortion":
            self.dist_label.setText(f"Distortion: {value}%")
        elif param == "reverb":
            self.reverb_label.setText(f"Reverb: {value}%")
        elif param == "filter_freq":
            self.filter_label.setText(f"Lowpass Filter: {value} Hz")
        self.update_callback()
