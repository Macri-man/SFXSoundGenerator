from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class ControlButtons(QWidget):
    """
    Provides playback and utility buttons for the SFX generator.
    Buttons: Play, Save, Random
    """
    def __init__(self, play_callback, save_callback, random_callback):
        super().__init__()
        self.play_callback = play_callback
        self.save_callback = save_callback
        self.random_callback = random_callback

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Play button
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self._on_play)
        self.layout.addWidget(self.play_btn)

        # Save button
        self.save_btn = QPushButton("Save WAV")
        self.save_btn.clicked.connect(self._on_save)
        self.layout.addWidget(self.save_btn)

        # Random button
        self.random_btn = QPushButton("Random")
        self.random_btn.clicked.connect(self._on_random)
        self.layout.addWidget(self.random_btn)

    # ------------------- Button callbacks -------------------
    def _on_play(self):
        if self.play_callback:
            self.play_callback()

    def _on_save(self):
        if self.save_callback:
            self.save_callback()

    def _on_random(self):
        if self.random_callback:
            self.random_callback()
