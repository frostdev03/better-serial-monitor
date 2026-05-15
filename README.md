# Better Serial Monitor

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, highly responsive desktop serial monitor built with Python and Tkinter. This tool is designed to provide a straightforward debugging environment for embedded systems and IoT development (such as ESP32, Arduino, etc.) without the heavy overhead of a full Integrated Development Environment (IDE).

## 🚀 Features

- **Dual-Pane Interface**: Clean separation between connection settings and the live serial terminal.
- **Dynamic Port Detection**: Refresh active COM ports on the fly without restarting the application.
- **Configurable Baud Rates**: Supports standard communication speeds (9600, 115200, 921600, etc.). Defaulted to 115200 for modern microcontrollers.
- **Data Tracking Controls**:
  - **Show Timestamp**: Prepend local time to every incoming data line.
  - **Auto Scroll**: Automatically pin the view to the latest incoming data.
- **Export System**: Save the entire serial monitor buffer directly to a `.txt` file for offline analysis.
- **Thread-Safe**: Serial reading is handled in the background, ensuring the GUI never freezes during high-speed data transmission.
- **Portable**: Available as a single standalone `.exe` file.

## 📥 Installation & Usage

You can use this application either by running the pre-compiled executable or by running the source code directly.

### Option 1: Using the Executable (Windows Only)
The easiest way to use the Better Serial Monitor is to download the standalone executable. No Python installation is required.

1. Go to the [Releases](../../releases) page of this repository.
2. Download the latest `Better_Serial_Monitor.exe`.
3. Double-click the file to run.

### Option 2: Running from Source
If you prefer to run the script via Python or want to modify the code:

1. Clone this repository:
   ```bash
   git clone https://github.com/frostdev03/better-serial-monitor.git
   cd better-serial-monitor
   ```
2. Install the required dependency:
   ```bash
   pip install pyserial
   ```
3. Run the application:
   ```bash
   python serial_monitor.py
   ```

## 🛠️ Building the Executable

If you modify the source code and want to build your own standalone `.exe` using PyInstaller, run the following command in your terminal:

```bash
python -m PyInstaller --noconsole --onefile --icon=app_icon.ico --add-data "app_icon.ico;." --name="Better Serial Monitor" serial-monitor.py
```
*(Make sure you have installed PyInstaller via `pip install pyinstaller`)*

## 👨‍💻 Author

**Fahril Tanzil**
- GitHub: [@yourusername](https://github.com/frostdev03)

## 📄 License

This project is licensed under the MIT License.
README.md
Displaying README.md.
