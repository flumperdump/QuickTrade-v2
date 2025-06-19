# quicktrade.py
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.dashboard import DashboardTab
from ui.settings import SettingsTab
from ui.trade_tabs import create_exchange_tab_widgets
from core.data_store import load_user_prefs

class QuickTradeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTrade")
        self.setMinimumSize(1024, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard_tab = DashboardTab()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        user_prefs = load_user_prefs()
        enabled_exchanges = user_prefs.get("enabled_exchanges", [])

        self.exchange_tabs = {}
        for ex_name, tab_widget in create_exchange_tab_widgets(enabled_exchanges):
            self.exchange_tabs[ex_name] = tab_widget
            self.tabs.addTab(tab_widget, ex_name)

        self.settings_tab = SettingsTab()
        self.tabs.addTab(self.settings_tab, "Settings")

        self.tabs.setCurrentIndex(0)
