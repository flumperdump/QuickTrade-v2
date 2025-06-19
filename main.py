## 📄 `main.py`
```python
from PyQt6.QtWidgets import QApplication
import sys
from quicktrade import QuickTradeApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuickTradeApp()
    window.show()
    sys.exit(app.exec())
