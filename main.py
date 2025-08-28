import sys
from PyQt6.QtWidgets import QApplication
from gui import SFXGenerator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SFXGenerator()
    window.show()
    sys.exit(app.exec())
