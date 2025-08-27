from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class ControlButtons(QWidget):
    """Play, Save, Random SFX buttons with callbacks."""
    def __init__(self, play_callback, save_callback, random_callback):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.play_btn = QPushButton("Play SFX")
        self.play_btn.clicked.connect(play_callback)
        self.save_btn = QPushButton("Save SFX")
        self.save_btn.clicked.connect(save_callback)
        self.random_btn = QPushButton("Random SFX")
        self.random_btn.clicked.connect(random_callback)

        for btn in [self.play_btn, self.save_btn, self.random_btn]:
            layout.addWidget(btn)
