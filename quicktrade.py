## 📄 `quicktrade.py`
```python
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.main_window import MainWindowUI

class QuickTradeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade")
        self.setGeometry(100, 100, 1024, 680)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        MainWindowUI(self.tabs).setup()
