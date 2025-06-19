## 📁 `ui/dashboard.py`
```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QCheckBox
from core.api_manager import simulate_balance_fetch

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.total_label = QLabel("💰 Total Asset Value: USD $0.00")
        self.layout().addWidget(self.total_label)

        top_bar = QHBoxLayout()
        self.dust_toggle = QCheckBox("Show Dust")
        self.refresh_button = QPushButton("🔁 Refresh")
        top_bar.addWidget(self.dust_toggle)
        top_bar.addWidget(self.refresh_button)
        top_bar.addStretch()
        self.layout().addLayout(top_bar)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Exchange", "Subaccount", "Asset", "Balance"])
        self.layout().addWidget(self.table)

        self.refresh_button.clicked.connect(self.load_data)
        self.load_data()

    def load_data(self):
        data = simulate_balance_fetch()
        self.table.setRowCount(0)
        total = 0
        for row in data:
            if not self.dust_toggle.isChecked() and row['usd_value'] < 1:
                continue
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, QTableWidgetItem(row['exchange']))
            self.table.setItem(row_pos, 1, QTableWidgetItem(row['subaccount']))
            self.table.setItem(row_pos, 2, QTableWidgetItem(row['asset']))
            self.table.setItem(row_pos, 3, QTableWidgetItem(f"${row['usd_value']:.2f}"))
            total += row['usd_value']
        self.total_label.setText(f"💰 Total Asset Value: USD ${total:,.2f}")
