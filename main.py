import sys
from PySide6.QtWidgets import QApplication
from ui_main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Aplikasi Ekstraksi Text dari Citra")
    window.show()
    sys.exit(app.exec())
