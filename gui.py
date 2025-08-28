from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from tabs.basic_tab import BasicTab
from tabs.advanced_tab import AdvancedTab
from layer import Layer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layers = [Layer()]
        self.current_index = 0

        self.tabs = QTabWidget()
        self.basic_tab = BasicTab(self.layers, self.current_index, self.update_audio)
        self.advanced_tab = AdvancedTab(self.layers, self.current_index, self.update_audio)

        self.tabs.addTab(self.basic_tab, "Basic")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.setCentralWidget(self.tabs)

    def update_audio(self):
        # Here you would trigger synth/effects update
        layer = self.layers[self.current_index]
        print(f"Updating audio: {layer}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
