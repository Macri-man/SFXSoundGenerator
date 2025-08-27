from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel, QInputDialog


class LayerSelector(QWidget):
    def __init__(self, layers, layer_changed_callback):
        super().__init__()
        self.layers = layers
        self.layer_changed_callback = layer_changed_callback
        self.current_index = 0
        self.clipboard_layer = None  # Temporary storage for copy/paste

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top row: Layer dropdown + rename
        top_row = QHBoxLayout()
        self.selector = QComboBox()
        self.selector.currentIndexChanged.connect(self.change_layer)
        top_row.addWidget(QLabel("Current Layer:"))
        top_row.addWidget(self.selector)
        self.rename_btn = QPushButton("Rename")
        self.rename_btn.clicked.connect(self.rename_layer)
        top_row.addWidget(self.rename_btn)
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy_layer)
        top_row.addWidget(self.copy_btn)
        self.paste_btn = QPushButton("Paste")
        self.paste_btn.clicked.connect(self.paste_layer)
        top_row.addWidget(self.paste_btn)
        self.layout.addLayout(top_row)

        # Bottom row: Add / Delete / Move
        bottom_row = QHBoxLayout()
        self.add_btn = QPushButton("Add Layer")
        self.add_btn.clicked.connect(self.add_layer)
        self.delete_btn = QPushButton("Delete Layer")
        self.delete_btn.clicked.connect(self.delete_layer)
        self.up_btn = QPushButton("Move Up")
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn = QPushButton("Move Down")
        self.down_btn.clicked.connect(self.move_down)
        bottom_row.addWidget(self.add_btn)
        bottom_row.addWidget(self.delete_btn)
        bottom_row.addWidget(self.up_btn)
        bottom_row.addWidget(self.down_btn)
        self.layout.addLayout(bottom_row)

        self.update_selector()

    def update_selector(self):
        self.selector.clear()
        for i, layer in enumerate(self.layers):
            self.selector.addItem(f"{i+1}: {layer.name}")
        self.selector.setCurrentIndex(self.current_index)
        self.layer_changed_callback(self.current_index)

    def change_layer(self, index):
        if index < 0 or index >= len(self.layers):
            return
        self.current_index = index
        self.layer_changed_callback(self.current_index)

    def add_layer(self):
        from layer import Layer
        self.layers.append(Layer(name=f"Layer {len(self.layers)+1}"))
        self.current_index = len(self.layers)-1
        self.update_selector()

    def delete_layer(self):
        if len(self.layers) <= 1:
            return
        self.layers.pop(self.current_index)
        self.current_index = max(0, self.current_index-1)
        self.update_selector()

    def rename_layer(self):
        layer = self.layers[self.current_index]
        from PyQt6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, "Rename Layer", "New name:", text=layer.name)
        if ok and text.strip():
            layer.name = text.strip()
            self.update_selector()

    def move_up(self):
        if self.current_index == 0:
            return
        self.layers[self.current_index-1], self.layers[self.current_index] = self.layers[self.current_index], self.layers[self.current_index-1]
        self.current_index -= 1
        self.update_selector()

    def move_down(self):
        if self.current_index >= len(self.layers)-1:
            return
        self.layers[self.current_index+1], self.layers[self.current_index] = self.layers[self.current_index], self.layers[self.current_index+1]
        self.current_index += 1
        self.update_selector()

    # --- Copy / Paste Layer ---
    def copy_layer(self):
        import copy
        self.clipboard_layer = copy.deepcopy(self.layers[self.current_index])

    def paste_layer(self):
        if self.clipboard_layer is None:
            return
        import copy
        self.layers[self.current_index] = copy.deepcopy(self.clipboard_layer)
        self.update_selector()


class ControlButtons(QWidget):
    def __init__(self, layers):
        super().__init__()
        self.layers = layers
        layout = QHBoxLayout()
        self.play_btn = QPushButton("Play SFX")
        self.save_btn = QPushButton("Save SFX")
        self.random_btn = QPushButton("Random SFX")
        layout.addWidget(self.play_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.random_btn)
        self.setLayout(layout)
