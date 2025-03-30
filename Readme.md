# Bluetooth Tray App

## Overview
Bluetooth Tray App is a simple Python application that allows users to manage Bluetooth connections through a system tray icon. It enables users to connect and disconnect a specified Bluetooth device with ease.

## Features
- System tray integration with an icon.
- Click the tray icon to connect/disconnect a Bluetooth device.
- Right-click menu with options to connect/disconnect or quit.
- Automatic Bluetooth enabling if it's turned off.
- Notifications for connection status.
- Ensures menu state reflects the actual connection status.

## Prerequisites
- Linux-based system with Bluetooth capabilities.
- Python 3 installed.
- PyQt5 installed (`pip3 install PyQt5`).
- `bluetoothctl` and `rfkill` commands available on the system.

## Installation
1. Clone the repository or copy the script to your local machine.
2. Install required dependencies:
   ```sh
   pip3 install PyQt5
   ```
3. Replace `TARGET_MAC` in `main.py` with your Bluetooth device's MAC address.
4. Ensure the script is executable:
   ```sh
   chmod +x main.py
   ```

## Usage
Run the script using:
```sh
python3 main.py
```

### Interacting with the App
- **Left-click** on the tray icon:
  - Connects to the Bluetooth device if not connected.
  - Does nothing if already connected.
- **Right-click** to access the menu:
  - `Connect` / `Disconnect` toggles the Bluetooth device connection.
  - `Quit` exits the application.

## Troubleshooting
- **Bluetooth not turning on?** Run `rfkill unblock bluetooth` manually.
- **Device not connecting?** Ensure the MAC address is correct and the device is paired.
- **Icon not showing?** Ensure `bluetooth.png` is in the same directory as `main.py`.

## License
This project is open-source and free to use.

