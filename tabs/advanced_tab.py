from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QSlider

class AdvancedTab(QWidget):
    """
    Advanced parameters: ADSR, LFO, FX (distortion, reverb, filter)
    """
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

        self._init_adsr_group()
        self._init_lfo_group()
        self._init_fx_group()
        self.load_layer()

    # ------------------- Groups -------------------
    def _init_adsr_group(self):
        group = QGroupBox("ADSR")
        layout = QVBoxLayout()
        group.setLayout(layout)
        for param in ["Attack","Decay","Sustain","Release"]:
            label = QLabel(f"{param}: 0")
            slider = QSlider()
            slider.setMinimum(0)
            slider.setMaximum(1000)
            slider.valueChanged.connect(lambda val, p=param, l=label: self._update_adsr(p,l,val))
            layout.addWidget(label)
            layout.addWidget(slider)
            self.adsr_sliders[param] = slider
        self.layout.addWidget(group)

    def _init_lfo_group(self):
        group = QGroupBox("LFO / Vibrato")
        layout = QVBoxLayout()
        group.setLayout(layout)

        # LFO Frequency scaled by 10 for float precision
        self.lfo_freq_label = QLabel("LFO Frequency: 0 Hz")
        self.lfo_freq_slider = QSlider()
        self.lfo_freq_slider.setMinimum(0)
        self.lfo_freq_slider.setMaximum(200)  # 0.0 to 20.0 Hz scaled by 10
        self.lfo_freq_slider.valueChanged.connect(lambda val: self._update_lfo("freq", val/10))
        layout.addWidget(self.lfo_freq_label)
        layout.addWidget(self.lfo_freq_slider)

        self.lfo_depth_label = QLabel("LFO Depth: 0 Hz")
        self.lfo_depth_slider = QSlider()
        self.lfo_depth_slider.setMinimum(0)
        self.lfo_depth_slider.setMaximum(200)  # depth 0-200
        self.lfo_depth_slider.valueChanged.connect(lambda val: self._update_lfo("depth", val))
        layout.addWidget(self.lfo_depth_label)
        layout.addWidget(self.lfo_depth_slider)

        self.lfo_sliders = {"freq": self.lfo_freq_slider, "depth": self.lfo_depth_slider}
        self.layout.addWidget(group)

    def _init_fx_group(self):
        group = QGroupBox("Effects")
        layout = QVBoxLayout()
        group.setLayout(layout)

        self.dist_label = QLabel("Distortion: 0%")
        self.dist_slider = QSlider()
        self.dist_slider.setMinimum(0)
        self.dist_slider.setMaximum(100)
        self.dist_slider.valueChanged.connect(lambda val: self._update_fx("distortion", val))
        layout.addWidget(self.dist_label)
        layout.addWidget(self.dist_slider)

        self.reverb_label = QLabel("Reverb: 0%")
        self.reverb_slider = QSlider()
        self.reverb_slider.setMinimum(0)
        self.reverb_slider.setMaximum(100)
        self.reverb_slider.valueChanged.connect(lambda val: self._update_fx("reverb", val))
        layout.addWidget(self.reverb_label)
        layout.addWidget(self.reverb_slider)

        self.filter_label = QLabel("Lowpass Filter: 0 Hz")
        self.filter_slider = QSlider()
        self.filter_slider.setMinimum(0)
        self.filter_slider.setMaximum(20000)
        self.filter_slider.valueChanged.connect(lambda val: self._update_fx("filter_freq", val))
        layout.addWidget(self.filter_label)
        layout.addWidget(self.filter_slider)

        self.fx_sliders = {
            "distortion": self.dist_slider,
            "reverb": self.reverb_slider,
            "filter_freq": self.filter_slider
        }
        self.layout.addWidget(group)

    # ------------------- Load Layer -------------------
    def load_layer(self):
        layer = self.layers[self.current_index]
        for param in ["Attack","Decay","Sustain","Release"]:
            self.adsr_sliders[param].setValue(layer.adsr.get(param,0))

        # Cast floats to int (scaled if needed)
        self.lfo_freq_slider.setValue(int(layer.lfo_freq * 10))  # scaled
        self.lfo_depth_slider.setValue(int(layer.lfo_depth))
        self.dist_slider.setValue(layer.distortion)
        self.reverb_slider.setValue(layer.reverb)
        self.filter_slider.setValue(layer.filter_freq)

    # ------------------- Update -------------------
    def _update_adsr(self, param, label, value):
        layer = self.layers[self.current_index]
        layer.adsr[param] = value
        label.setText(f"{param}: {value/100:.2f}" if param=="Sustain" else f"{param}: {value} ms")
        self.update_callback()

    def _update_lfo(self, typ, value):
        layer = self.layers[self.current_index]
        if typ=="freq":
            layer.lfo_freq = value
            self.lfo_freq_label.setText(f"LFO Frequency: {value:.1f} Hz")
        else:
            layer.lfo_depth = value
            self.lfo_depth_label.setText(f"LFO Depth: {value} Hz")
        self.update_callback()

    def _update_fx(self, param, value):
        layer = self.layers[self.current_index]
        setattr(layer, param, value)
        if param=="distortion":
            self.dist_label.setText(f"Distortion: {value}%")
        elif param=="reverb":
            self.reverb_label.setText(f"Reverb: {value}%")
        else:
            self.filter_label.setText(f"Lowpass Filter: {value} Hz")
        self.update_callback()
