from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QMessageBox, QScrollArea,
    QDialog, QListWidget, QListWidgetItem, QDialogButtonBox, QTabWidget, QLineEdit, QGroupBox
)
from PyQt6.QtCore import Qt
import sys
import json
import os

CONFIG_PATH = "config"
API_KEYS_FILE = os.path.join(CONFIG_PATH, "api_keys.json")
USER_PREFS_FILE = os.path.join(CONFIG_PATH, "user_prefs.json")

EXCHANGES = ["Bybit", "Kraken", "Binance", "KuCoin", "Coinbase", "MEXC", "Bitget", "Crypto.com", "Hyperliquid"]

os.makedirs(CONFIG_PATH, exist_ok=True)

def load_user_prefs():
    if os.path.exists(USER_PREFS_FILE):
        with open(USER_PREFS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_prefs(prefs):
    with open(USER_PREFS_FILE, 'w') as f:
        json.dump(prefs, f, indent=4)

def load_api_keys():
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_api_keys(keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

class ExchangeSelectorDialog(QDialog):
    def __init__(self, selected_exchanges):
        super().__init__()
        self.setWindowTitle("Choose Exchanges")
        self.setMinimumWidth(300)
        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for ex in EXCHANGES:
            item = QListWidgetItem(ex)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if ex in selected_exchanges else Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm?")
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.button_box)

        layout.addLayout(confirm_layout)
        self.setLayout(layout)

    def get_selected_exchanges(self):
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count())
                if self.list_widget.item(i).checkState() == Qt.CheckState.Checked]

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.total_label = QLabel("\ud83d\udcb0 Total Asset Value: USD $0.00")
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout().addWidget(self.total_label)

        controls_layout = QHBoxLayout()
        self.dust_filter = QCheckBox("Show Dust (<$1)")
        self.dust_filter.setChecked(False)
        self.dust_filter.stateChanged.connect(self.update_tree)

        self.refresh_button = QPushButton("\ud83d\udd01 Refresh Assets")
        self.refresh_button.clicked.connect(self.load_balances)

        controls_layout.addWidget(self.dust_filter)
        controls_layout.addWidget(self.refresh_button)
        controls_layout.addStretch()
        self.layout().addLayout(controls_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        tree_container = QWidget()
        tree_layout = QVBoxLayout()
        tree_container.setLayout(tree_layout)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Subaccount", "Asset", "Balance (USD)"])
        tree_layout.addWidget(self.tree)

        scroll_area.setWidget(tree_container)
        self.layout().addWidget(scroll_area)

        self.balances = []
        self.load_balances()

    def load_balances(self):
        self.balances = [
            {"exchange": "Binance", "subaccount": "Main", "asset": "BTC", "usd_value": 23450.12},
            {"exchange": "Kraken", "subaccount": "Bot1", "asset": "ETH", "usd_value": 1345.33},
            {"exchange": "KuCoin", "subaccount": "Main", "asset": "DOGE", "usd_value": 0.52},
            {"exchange": "Bybit", "subaccount": "Alt", "asset": "SOL", "usd_value": 85.22}
        ]
        self.update_tree()

    def update_tree(self):
        self.tree.clear()
        show_dust = self.dust_filter.isChecked()
        exchange_totals = {}

        for b in self.balances:
            if not show_dust and b["usd_value"] < 1:
                continue
            exchange_totals.setdefault(b["exchange"], []).append(b)

        total = 0.0
        for exchange, items in exchange_totals.items():
            subtotal = sum(x["usd_value"] for x in items)
            ex_node = QTreeWidgetItem([f"{exchange} \u2014 ${subtotal:,.2f}"])
            for b in items:
                child = QTreeWidgetItem([b["subaccount"], b["asset"], f"${b['usd_value']:.2f}"])
                ex_node.addChild(child)
            self.tree.addTopLevelItem(ex_node)
            ex_node.setExpanded(True)
            total += subtotal

        self.total_label.setText(f"\ud83d\udcb0 Total Asset Value: USD ${total:,.2f}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade")
        self.resize(1024, 650)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard_tab = DashboardTab()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        prefs = load_user_prefs()
        selected_exchanges = prefs.get("selected_exchanges", EXCHANGES)
        self.exchange_tabs = {}
        for name in selected_exchanges:
            tab = QWidget()  # Replace with ExchangeTab(name) when ExchangeTab is available
            self.exchange_tabs[name] = tab
            self.tabs.addTab(tab, name)

        self.settings_tab = QWidget()  # Replace with real SettingsTab class
        self.tabs.addTab(self.settings_tab, "Settings")
