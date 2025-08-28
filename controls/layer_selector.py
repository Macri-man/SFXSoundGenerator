from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QPushButton, QHBoxLayout, QInputDialog
from layer import Layer
import copy

class LayerSelector(QWidget):
    """
    Dropdown to select active layer and optionally add/remove layers.
    """
    def __init__(self, layers: list[Layer], change_callback):
        super().__init__()
        self.layers = layers
        self.change_callback = change_callback

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Dropdown for selecting layers
        self.selector_layout = QHBoxLayout()
        self.selector = QComboBox()
        self.selector.currentIndexChanged.connect(self._layer_changed)
        self.selector_layout.addWidget(self.selector)

        # Optional: Add layer button
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedWidth(30)
        self.add_btn.clicked.connect(self.add_layer)
        self.selector_layout.addWidget(self.add_btn)

        # Optional: Remove layer button
        self.remove_btn = QPushButton("-")
        self.remove_btn.setFixedWidth(30)
        self.remove_btn.clicked.connect(self.remove_layer)
        self.selector_layout.addWidget(self.remove_btn)

        self.layout.addLayout(self.selector_layout)

        # Initialize dropdown
        self.update_selector()

    # ------------------- Selector -------------------
    def update_selector(self):
        self.selector.clear()
        for i, layer in enumerate(self.layers):
            self.selector.addItem(f"{i+1}: {getattr(layer,'name','Layer')}")

    def _layer_changed(self, index):
        if index >= 0 and index < len(self.layers):
            self.change_callback(index)

    # ------------------- Add / Remove Layers -------------------
    def add_layer(self):
        new_layer = Layer(name=f"Layer {len(self.layers)+1}")
        self.layers.append(new_layer)
        self.update_selector()
        self.selector.setCurrentIndex(len(self.layers)-1)
        self.change_callback(len(self.layers)-1)

    def remove_layer(self):
        index = self.selector.currentIndex()
        if len(self.layers) <= 1:
            return  # Keep at least one layer
        if index >= 0 and index < len(self.layers):
            self.layers.pop(index)
            self.update_selector()
            # Select previous layer if possible
            new_index = max(0, index-1)
            self.selector.setCurrentIndex(new_index)
            self.change_callback(new_index)

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
