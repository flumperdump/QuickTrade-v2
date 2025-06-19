# main.py
import sys
from PyQt6.QtWidgets import QApplication
from quicktrade import QuickTradeMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuickTradeMainWindow()
    window.show()
    sys.exit(app.exec())
