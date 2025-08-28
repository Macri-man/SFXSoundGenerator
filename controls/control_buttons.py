from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class ControlButtons(QWidget):
    """Playback, save, and randomize controls."""

    def __init__(self, play_callback=None, save_callback=None, random_callback=None):
        super().__init__()
        self.play_callback = play_callback
        self.save_callback = save_callback
        self.random_callback = random_callback

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_callback)
        layout.addWidget(self.play_btn)

        self.save_btn = QPushButton("Save SFX")
        self.save_btn.clicked.connect(self.save_callback)
        layout.addWidget(self.save_btn)

        self.random_btn = QPushButton("Random SFX")
        self.random_btn.clicked.connect(self.random_callback)
        layout.addWidget(self.random_btn)
