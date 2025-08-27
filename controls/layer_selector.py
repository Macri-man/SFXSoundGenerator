from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QInputDialog, QLabel
import copy

class LayerSelector(QWidget):
    """Layer management: select, add, delete, copy/paste, rename"""
    def __init__(self, layers, layer_changed_callback):
        super().__init__()
        self.layers = layers
        self.layer_changed_callback = layer_changed_callback
        self.current_index = 0
        self.clipboard_layer = None

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Layer dropdown
        self.selector = QComboBox()
        self.selector.currentIndexChanged.connect(self.change_layer)
        self.layout.addWidget(QLabel("Layer:"))
        self.layout.addWidget(self.selector)

        # Buttons
        self.rename_btn = QPushButton("Rename")
        self.rename_btn.clicked.connect(self.rename_layer)
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy_layer)
        self.paste_btn = QPushButton("Paste")
        self.paste_btn.clicked.connect(self.paste_layer)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_layer)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_layer)

        for btn in [self.rename_btn, self.copy_btn, self.paste_btn, self.add_btn, self.delete_btn]:
            self.layout.addWidget(btn)

        self.update_selector()

    def update_selector(self):
        self.selector.clear()
        for i, layer in enumerate(self.layers):
            self.selector.addItem(f"{i+1}: {layer.name}")
        self.selector.setCurrentIndex(self.current_index)
        self.layer_changed_callback(self.current_index)

    def change_layer(self, index):
        if 0 <= index < len(self.layers):
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
        text, ok = QInputDialog.getText(self, "Rename Layer", "New name:", text=layer.name)
        if ok and text.strip():
            layer.name = text.strip()
            self.update_selector()

    def copy_layer(self):
        self.clipboard_layer = copy.deepcopy(self.layers[self.current_index])

    def paste_layer(self):
        if self.clipboard_layer:
            self.layers[self.current_index] = copy.deepcopy(self.clipboard_layer)
            self.update_selector()
