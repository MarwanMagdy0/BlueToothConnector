import sys
import time
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget
from PyQt5.QtGui import QIcon
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
# Replace with your Bluetooth headset's MAC address
TARGET_MAC = "F4:B6:2D:1D:BA:0E"

class BluetoothTrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("bluetooth.png"), self.app)
        self.tray_icon.setToolTip("Bluetooth Manager")
        
        # Create a hidden parent widget
        self.parent_widget = QWidget()
        
        # Create a menu
        self.menu = QMenu()
        self.connect_action = QAction("Connect")
        self.connect_action.triggered.connect(self.toggle_connection)
        self.menu.addAction(self.connect_action)
        
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)
        
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.on_tray_icon_clicked)
        self.tray_icon.show()
        
        # Ensure menu reflects current connection state
        self.update_menu()
    
    def is_bluetooth_enabled(self):
        try:
            output = subprocess.check_output("rfkill list bluetooth", shell=True, text=True)
            return "Soft blocked: no" in output and "Hard blocked: no" in output
        except subprocess.CalledProcessError:
            return False
    
    def enable_bluetooth(self):
        try:
            subprocess.check_call("rfkill unblock bluetooth", shell=True)
            time.sleep(2)
        except subprocess.CalledProcessError:
            self.show_notification("Bluetooth", "Failed to enable Bluetooth.")
    
    def is_device_connected(self, mac_address):
        try:
            output = subprocess.check_output(f"bluetoothctl info {mac_address}", shell=True, text=True)
            return "Connected: yes" in output
        except subprocess.CalledProcessError:
            return False
    
    def connect_device(self, mac_address):
        try:
            output = subprocess.check_output(f"bluetoothctl connect {mac_address}", shell=True, text=True)
            return "Connection successful" in output
        except subprocess.CalledProcessError:
            return False
    
    def disconnect_device(self, mac_address):
        try:
            subprocess.check_output(f"bluetoothctl disconnect {mac_address}", shell=True, text=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def toggle_connection(self):
        if not self.is_bluetooth_enabled():
            self.enable_bluetooth()
            time.sleep(2)
        
        if self.is_device_connected(TARGET_MAC):
            if self.disconnect_device(TARGET_MAC):
                self.show_notification("Bluetooth", "Disconnected successfully.")
            else:
                self.show_notification("Bluetooth", "Failed to disconnect.")
        else:
            if self.connect_device(TARGET_MAC):
                self.show_notification("Bluetooth", "Connection successful!")
            else:
                self.show_notification("Bluetooth", "Failed to connect.")
        
        self.update_menu()
    
    def on_tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left-click
            if not self.is_device_connected(TARGET_MAC):
                self.toggle_connection()
        
        elif reason == QSystemTrayIcon.Context:  # Right-click
            self.update_menu()
    
    def update_menu(self):
        # Update menu state before showing
        if self.is_device_connected(TARGET_MAC):
            self.connect_action.setText("Disconnect")
        else:
            self.connect_action.setText("Connect")
        self.tray_icon.setContextMenu(self.menu)
    
    def show_notification(self, title, message):
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 1000)  # 1-second timeout
    
    def quit_app(self):
        self.tray_icon.hide()
        sys.exit()
    
    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    tray_app = BluetoothTrayApp()
    tray_app.run()
