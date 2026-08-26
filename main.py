import sys
import os
import shlex
import subprocess
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QLabel,
    QComboBox,
    QMessageBox,
    QInputDialog,
    QFileDialog,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
    QProgressBar,
    QListWidget,
)

from core.adb import ADBManager
from core.device import DeviceManager
from core.apps import AppManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # CORE MANAGERS
        # -----------------------------

        self.adb = ADBManager()

        self.device_manager = DeviceManager(
            self.adb
        )

        self.app_manager = AppManager(
            self.adb
        )

        # -----------------------------
        # SCRCPY PATH
        # -----------------------------

        self.scrcpy_path = (
            Path(__file__).resolve().parent
            / "tools"
            / "scrcpy"
            / "scrcpy"
        )

        self.logcat_process = None

        self.app_packages = []

        # -----------------------------
        # WINDOW
        # -----------------------------

        self.setWindowTitle(
            "DroidDesk - Android Device Manager"
        )

        self.resize(
            1200,
            750
        )

        self.setup_ui()

        self.refresh_devices()

    # =========================================================
    # UI
    # =========================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "DroidDesk"
        )

        title.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            """
        )

        header.addWidget(
            title
        )

        subtitle = QLabel(
            "Android Device Management"
        )

        subtitle.setStyleSheet(
            "color: #999999;"
        )

        header.addWidget(
            subtitle
        )

        header.addStretch()

        self.status_label = QLabel(
            "● No device"
        )

        self.status_label.setStyleSheet(
            "color: #ff6b6b; font-weight: bold;"
        )

        header.addWidget(
            self.status_label
        )

        main_layout.addLayout(
            header
        )

        # -----------------------------------------------------
        # DEVICE SELECTOR
        # -----------------------------------------------------

        device_layout = QHBoxLayout()

        device_layout.addWidget(
            QLabel("Connected Device:")
        )

        self.device_combo = QComboBox()

        self.device_combo.currentIndexChanged.connect(
            self.device_changed
        )

        device_layout.addWidget(
            self.device_combo,
            1
        )

        refresh_button = QPushButton(
            "🔄 Refresh Devices"
        )

        refresh_button.clicked.connect(
            self.refresh_devices
        )

        device_layout.addWidget(
            refresh_button
        )

        main_layout.addLayout(
            device_layout
        )

        # -----------------------------------------------------
        # TABS
        # -----------------------------------------------------

        self.tabs = QTabWidget()

        self.tabs.addTab(
            self.create_dashboard(),
            "🏠 Dashboard"
        )

        self.tabs.addTab(
            self.create_devices_tab(),
            "📱 Devices"
        )

        self.tabs.addTab(
            self.create_apps_tab(),
            "📦 Applications"
        )

        self.tabs.addTab(
            self.create_files_tab(),
            "📁 Files"
        )

        self.tabs.addTab(
            self.create_logcat_tab(),
            "📋 Logcat"
        )

        self.tabs.addTab(
            self.create_terminal_tab(),
            "⚙ Advanced"
        )

        main_layout.addWidget(
            self.tabs
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def create_dashboard(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        # -----------------------------------------------------
        # DEVICE INFORMATION
        # -----------------------------------------------------

        info_group = QGroupBox(
            "Device Information"
        )

        grid = QGridLayout(
            info_group
        )

        self.model_label = QLabel("-")
        self.manufacturer_label = QLabel("-")
        self.android_label = QLabel("-")
        self.sdk_label = QLabel("-")
        self.serial_label = QLabel("-")
        self.resolution_label = QLabel("-")

        information = [
            ("Model", self.model_label),
            ("Manufacturer", self.manufacturer_label),
            ("Android Version", self.android_label),
            ("SDK", self.sdk_label),
            ("Serial", self.serial_label),
            ("Resolution", self.resolution_label),
        ]

        for row, (
            name,
            widget
        ) in enumerate(information):

            grid.addWidget(
                QLabel(
                    f"<b>{name}</b>"
                ),
                row,
                0
            )

            grid.addWidget(
                widget,
                row,
                1
            )

        layout.addWidget(
            info_group
        )

        # -----------------------------------------------------
        # BATTERY
        # -----------------------------------------------------

        battery_group = QGroupBox(
            "Battery"
        )

        battery_layout = QHBoxLayout(
            battery_group
        )

        self.battery_label = QLabel(
            "Battery: --"
        )

        self.battery_bar = QProgressBar()

        self.battery_bar.setRange(
            0,
            100
        )

        battery_layout.addWidget(
            self.battery_label
        )

        battery_layout.addWidget(
            self.battery_bar
        )

        layout.addWidget(
            battery_group
        )

        # -----------------------------------------------------
        # STORAGE
        # -----------------------------------------------------

        self.storage_label = QLabel(
            "Storage: --"
        )

        layout.addWidget(
            self.storage_label
        )

        # -----------------------------------------------------
        # QUICK ACTIONS
        # -----------------------------------------------------

        actions_group = QGroupBox(
            "Quick Actions"
        )

        actions = QGridLayout(
            actions_group
        )

        buttons = [
            (
                "📺 Screen Mirror",
                self.start_scrcpy
            ),
            (
                "📸 Screenshot",
                self.take_screenshot
            ),
            (
                "🔄 Reboot",
                self.reboot_device
            ),
            (
                "📦 Install APK",
                self.install_apk
            ),
            (
                "📱 Refresh Info",
                self.refresh_device_info
            ),
            (
                "🔋 Refresh Battery",
                self.refresh_battery
            ),
        ]

        for index, (
            text,
            function
        ) in enumerate(buttons):

            button = QPushButton(
                text
            )

            button.setMinimumHeight(
                45
            )

            button.clicked.connect(
                function
            )

            actions.addWidget(
                button,
                index // 3,
                index % 3
            )

        layout.addWidget(
            actions_group
        )

        layout.addStretch()

        return page

    # =========================================================
    # DEVICES TAB
    # =========================================================

    def create_devices_tab(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.addWidget(
            QLabel(
                "<h2>Connected Android Devices</h2>"
            )
        )

        self.device_table = QTableWidget(
            0,
            3
        )

        self.device_table.setHorizontalHeaderLabels(
            [
                "Serial",
                "Status",
                "Selected"
            ]
        )

        self.device_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.device_table
        )

        buttons = QHBoxLayout()

        refresh = QPushButton(
            "🔄 Refresh"
        )

        refresh.clicked.connect(
            self.refresh_devices
        )

        buttons.addWidget(
            refresh
        )

        wifi = QPushButton(
            "📡 Connect over Wi-Fi"
        )

        wifi.clicked.connect(
            self.connect_wifi
        )

        buttons.addWidget(
            wifi
        )

        layout.addLayout(
            buttons
        )

        return page

    # =========================================================
    # APPLICATIONS TAB
    # =========================================================

    def create_apps_tab(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        top = QHBoxLayout()

        self.app_search = QLineEdit()

        self.app_search.setPlaceholderText(
            "Search installed applications..."
        )

        self.app_search.textChanged.connect(
            self.filter_apps
        )

        top.addWidget(
            self.app_search
        )

        refresh = QPushButton(
            "🔄 Refresh Apps"
        )

        refresh.clicked.connect(
            self.refresh_apps
        )

        top.addWidget(
            refresh
        )

        install = QPushButton(
            "📦 Install APK"
        )

        install.clicked.connect(
            self.install_apk
        )

        top.addWidget(
            install
        )

        layout.addLayout(
            top
        )

        self.app_table = QTableWidget(
            0,
            2
        )

        self.app_table.setHorizontalHeaderLabels(
            [
                "Application",
                "Package Name"
            ]
        )

        self.app_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.app_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        layout.addWidget(
            self.app_table
        )

        actions = QHBoxLayout()

        buttons = [
            (
                "▶ Launch",
                self.launch_app
            ),
            (
                "⏹ Force Stop",
                self.force_stop_app
            ),
            (
                "🧹 Clear Data",
                self.clear_app_data
            ),
            (
                "✓ Enable",
                self.enable_app
            ),
            (
                "✕ Disable",
                self.disable_app
            ),
            (
                "🗑 Uninstall",
                self.uninstall_app
            ),
        ]

        for text, function in buttons:

            button = QPushButton(
                text
            )

            button.clicked.connect(
                function
            )

            actions.addWidget(
                button
            )

        layout.addLayout(
            actions
        )

        return page

    # =========================================================
    # FILES TAB
    # =========================================================

    def create_files_tab(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        path_layout = QHBoxLayout()

        path_layout.addWidget(
            QLabel("Device Path:")
        )

        self.file_path = QLineEdit(
            "/sdcard"
        )

        path_layout.addWidget(
            self.file_path
        )

        browse = QPushButton(
            "Browse"
        )

        browse.clicked.connect(
            self.browse_files
        )

        path_layout.addWidget(
            browse
        )

        layout.addLayout(
            path_layout
        )

        self.file_list = QListWidget()

        layout.addWidget(
            self.file_list
        )

        buttons = QHBoxLayout()

        refresh = QPushButton(
            "🔄 Refresh"
        )

        refresh.clicked.connect(
            self.browse_files
        )

        buttons.addWidget(
            refresh
        )

        push = QPushButton(
            "⬆ Push File"
        )

        push.clicked.connect(
            self.push_file
        )

        buttons.addWidget(
            push
        )

        pull = QPushButton(
            "⬇ Pull File"
        )

        pull.clicked.connect(
            self.pull_file
        )

        buttons.addWidget(
            pull
        )

        layout.addLayout(
            buttons
        )

        return page

    # =========================================================
    # LOGCAT TAB
    # =========================================================

    def create_logcat_tab(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        buttons = QHBoxLayout()

        start = QPushButton(
            "▶ Start Logcat"
        )

        start.clicked.connect(
            self.start_logcat
        )

        buttons.addWidget(
            start
        )

        stop = QPushButton(
            "⏹ Stop"
        )

        stop.clicked.connect(
            self.stop_logcat
        )

        buttons.addWidget(
            stop
        )

        clear = QPushButton(
            "🧹 Clear"
        )

        clear.clicked.connect(
            lambda:
            self.logcat_output.clear()
        )

        buttons.addWidget(
            clear
        )

        layout.addLayout(
            buttons
        )

        self.logcat_output = QTextEdit()

        self.logcat_output.setReadOnly(
            True
        )

        layout.addWidget(
            self.logcat_output
        )

        return page

    # =========================================================
    # ADVANCED TAB
    # =========================================================

    def create_terminal_tab(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.addWidget(
            QLabel(
                "Advanced ADB Command Terminal"
            )
        )

        self.terminal_output = QTextEdit()

        self.terminal_output.setReadOnly(
            True
        )

        layout.addWidget(
            self.terminal_output
        )

        command_layout = QHBoxLayout()

        self.command_input = QLineEdit()

        self.command_input.setPlaceholderText(
            "Example: shell getprop ro.product.model"
        )

        self.command_input.returnPressed.connect(
            self.run_command
        )

        command_layout.addWidget(
            self.command_input
        )

        run = QPushButton(
            "RUN"
        )

        run.clicked.connect(
            self.run_command
        )

        command_layout.addWidget(
            run
        )

        layout.addLayout(
            command_layout
        )

        return page

    # =========================================================
    # DEVICE MANAGEMENT
    # =========================================================

    def refresh_devices(self):

        self.device_combo.blockSignals(
            True
        )

        self.device_combo.clear()

        devices = self.adb.devices()

        self.device_table.setRowCount(
            0
        )

        for row, device in enumerate(
            devices
        ):

            serial = device["serial"]
            state = device["state"]

            self.device_combo.addItem(
                f"{serial} ({state})",
                serial
            )

            self.device_table.insertRow(
                row
            )

            self.device_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    serial
                )
            )

            self.device_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    state
                )
            )

            self.device_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    ""
                )
            )

        self.device_combo.blockSignals(
            False
        )

        if devices:

            serial = devices[0]["serial"]

            self.adb.set_device(
                serial
            )

            self.status_label.setText(
                f"● Connected: {serial}"
            )

            self.status_label.setStyleSheet(
                "color: #4ade80; font-weight: bold;"
            )

            self.device_combo.setCurrentIndex(
                0
            )

            self.refresh_device_info()
            self.refresh_battery()
            self.refresh_storage()
            self.refresh_apps()

        else:

            self.status_label.setText(
                "● No device"
            )

            self.status_label.setStyleSheet(
                "color: #ff6b6b; font-weight: bold;"
            )

        self.log(
            f"Found {len(devices)} device(s)."
        )

    def device_changed(
        self,
        index
    ):

        if index < 0:
            return

        serial = self.device_combo.itemData(
            index
        )

        if not serial:
            return

        self.adb.set_device(
            serial
        )

        self.status_label.setText(
            f"● Connected: {serial}"
        )

        self.refresh_device_info()
        self.refresh_battery()
        self.refresh_storage()
        self.refresh_apps()

    # =========================================================
    # DEVICE INFORMATION
    # =========================================================

    def refresh_device_info(self):

        if not self.adb.device:
            return

        info = self.device_manager.get_info()

        self.model_label.setText(
            info["model"]
        )

        self.manufacturer_label.setText(
            info["manufacturer"]
        )

        self.android_label.setText(
            info["android"]
        )

        self.sdk_label.setText(
            info["sdk"]
        )

        self.serial_label.setText(
            info["serial"]
        )

        result = self.adb.shell(
            "wm",
            "size"
        )

        if result["success"]:

            self.resolution_label.setText(
                result["stdout"]
            )

    # =========================================================
    # BATTERY
    # =========================================================

    def refresh_battery(self):

        if not self.adb.device:
            return

        result = self.device_manager.battery()

        if not result["success"]:
            return

        level = None
        status = "Unknown"

        for line in result["stdout"].splitlines():

            line = line.strip()

            if line.startswith(
                "level:"
            ):

                try:

                    level = int(
                        line.split(
                            ":"
                        )[1].strip()
                    )

                except ValueError:
                    pass

            elif line.startswith(
                "status:"
            ):

                status = line.split(
                    ":",
                    1
                )[1].strip()

        if level is not None:

            self.battery_bar.setValue(
                level
            )

            self.battery_label.setText(
                f"Battery: {level}% | Status: {status}"
            )

    # =========================================================
    # STORAGE
    # =========================================================

    def refresh_storage(self):

        if not self.adb.device:
            return

        result = self.adb.shell(
            "df",
            "-h",
            "/sdcard"
        )

        if not result["success"]:
            return

        lines = result["stdout"].splitlines()

        if len(lines) >= 2:

            parts = lines[-1].split()

            if len(parts) >= 4:

                self.storage_label.setText(
                    f"Storage: "
                    f"{parts[2]} used / "
                    f"{parts[1]} total | "
                    f"{parts[3]} available"
                )

    # =========================================================
    # SCRCPY
    # =========================================================

    def start_scrcpy(self):

        if not self.adb.device:

            QMessageBox.warning(
                self,
                "No Device",
                "Connect an Android device first."
            )

            return

        if not self.scrcpy_path.exists():

            QMessageBox.critical(
                self,
                "Scrcpy Not Found",
                str(self.scrcpy_path)
            )

            return

        try:

            subprocess.Popen(
                [
                    str(
                        self.scrcpy_path
                    ),
                    "-s",
                    self.adb.device
                ]
            )

            self.log(
                "Scrcpy started."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Scrcpy Error",
                str(e)
            )

    # =========================================================
    # SCREENSHOT
    # =========================================================

    def take_screenshot(self):

        if not self.adb.device:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Screenshot",
            "android_screenshot.png",
            "PNG Images (*.png)"
        )

        if not path:
            return

        result = subprocess.run(
            [
                "adb",
                "-s",
                self.adb.device,
                "exec-out",
                "screencap",
                "-p"
            ],
            capture_output=True
        )

        if result.returncode == 0:

            with open(
                path,
                "wb"
            ) as file:

                file.write(
                    result.stdout
                )

            QMessageBox.information(
                self,
                "Screenshot",
                f"Saved:\n{path}"
            )

        else:

            QMessageBox.critical(
                self,
                "Screenshot Error",
                result.stderr.decode(
                    errors="replace"
                )
            )

    # =========================================================
    # REBOOT
    # =========================================================

    def reboot_device(self):

        if not self.adb.device:
            return

        answer = QMessageBox.question(
            self,
            "Confirm Reboot",
            "Reboot the connected Android device?"
        )

        if answer != QMessageBox.Yes:
            return

        result = self.adb.run(
            "reboot"
        )

        self.show_result(
            result
        )

    # =========================================================
    # APPLICATION MANAGEMENT
    # =========================================================

    def refresh_apps(self):

        if not self.adb.device:
            return

        self.app_packages = (
            self.app_manager.list_packages()
        )

        self.populate_apps(
            self.app_packages
        )

    def populate_apps(
        self,
        packages
    ):

        self.app_table.setRowCount(
            0
        )

        for package in packages:

            row = self.app_table.rowCount()

            self.app_table.insertRow(
                row
            )

            self.app_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    package
                )
            )

            self.app_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    package
                )
            )

    def filter_apps(
        self,
        text
    ):

        text = text.lower()

        filtered = [
            package
            for package
            in self.app_packages
            if text in package.lower()
        ]

        self.populate_apps(
            filtered
        )

    def selected_package(self):

        row = self.app_table.currentRow()

        if row < 0:
            return None

        item = self.app_table.item(
            row,
            1
        )

        if not item:
            return None

        return item.text()

    def launch_app(self):

        package = self.selected_package()

        if not package:
            return

        result = self.app_manager.launch(
            package
        )

        self.show_result(
            result
        )

    def force_stop_app(self):

        package = self.selected_package()

        if not package:
            return

        result = self.app_manager.force_stop(
            package
        )

        self.show_result(
            result
        )

    def clear_app_data(self):

        package = self.selected_package()

        if not package:
            return

        answer = QMessageBox.question(
            self,
            "Clear Application Data",
            f"Clear data for {package}?"
        )

        if answer != QMessageBox.Yes:
            return

        result = self.app_manager.clear_data(
            package
        )

        self.show_result(
            result
        )

    def enable_app(self):

        package = self.selected_package()

        if not package:
            return

        result = self.app_manager.enable(
            package
        )

        self.show_result(
            result
        )

    def disable_app(self):

        package = self.selected_package()

        if not package:
            return

        result = self.app_manager.disable(
            package
        )

        self.show_result(
            result
        )

    def uninstall_app(self):

        package = self.selected_package()

        if not package:
            return

        answer = QMessageBox.question(
            self,
            "Confirm Uninstall",
            f"Uninstall {package}?"
        )

        if answer != QMessageBox.Yes:
            return

        result = self.app_manager.uninstall(
            package
        )

        self.show_result(
            result
        )

        if result["success"]:
            self.refresh_apps()

    def install_apk(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select APK",
            "",
            "Android APK (*.apk)"
        )

        if not path:
            return

        result = self.app_manager.install(
            path
        )

        self.show_result(
            result
        )

        if result["success"]:
            self.refresh_apps()

    # =========================================================
    # FILE MANAGEMENT
    # =========================================================

    def browse_files(self):

        if not self.adb.device:
            return

        path = self.file_path.text().strip()

        result = self.adb.shell(
            "ls",
            "-1",
            path
        )

        self.file_list.clear()

        if not result["success"]:

            self.file_list.addItem(
                "Error: " + result["stderr"]
            )

            return

        for item in result["stdout"].splitlines():

            if item.strip():

                self.file_list.addItem(
                    item
                )

    def push_file(self):

        local, _ = QFileDialog.getOpenFileName(
            self,
            "Select File"
        )

        if not local:
            return

        remote = self.file_path.text()

        result = self.adb.run(
            "push",
            local,
            remote
        )

        self.show_result(
            result
        )

        self.browse_files()

    def pull_file(self):

        item = self.file_list.currentItem()

        if not item:
            return

        name = item.text()

        remote = (
            self.file_path.text().rstrip("/")
            + "/"
            + name
        )

        local, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            name
        )

        if not local:
            return

        result = self.adb.run(
            "pull",
            remote,
            local
        )

        self.show_result(
            result
        )

    # =========================================================
    # LOGCAT
    # =========================================================

    def start_logcat(self):

        if not self.adb.device:
            return

        self.stop_logcat()

        self.logcat_process = subprocess.Popen(
            [
                "adb",
                "-s",
                self.adb.device,
                "logcat"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        self.logcat_output.append(
            "=== LOGCAT STARTED ==="
        )

    def stop_logcat(self):

        if self.logcat_process:

            self.logcat_process.terminate()

            self.logcat_process = None

            self.logcat_output.append(
                "=== LOGCAT STOPPED ==="
            )

    # =========================================================
    # WI-FI ADB
    # =========================================================

    def connect_wifi(self):

        address, ok = QInputDialog.getText(
            self,
            "Wireless ADB",
            "Device address (example 192.168.1.10:5555):"
        )

        if not ok or not address:
            return

        result = subprocess.run(
            [
                "adb",
                "connect",
                address
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            QMessageBox.information(
                self,
                "ADB Wi-Fi",
                result.stdout
            )

            self.refresh_devices()

        else:

            QMessageBox.critical(
                self,
                "ADB Wi-Fi",
                result.stderr
            )

    # =========================================================
    # ADVANCED COMMAND TERMINAL
    # =========================================================

    def run_command(self):

        command = self.command_input.text().strip()

        if not command:
            return

        self.terminal_output.append(
            f"$ adb {command}"
        )

        try:

            args = shlex.split(
                command
            )

        except ValueError as e:

            self.terminal_output.append(
                f"Command error: {e}"
            )

            return

        result = self.adb.run(
            *args
        )

        if result["stdout"]:

            self.terminal_output.append(
                result["stdout"]
            )

        if result["stderr"]:

            self.terminal_output.append(
                result["stderr"]
            )

        self.terminal_output.append(
            f"Exit code: {result['returncode']}\n"
        )

        self.command_input.clear()

    # =========================================================
    # HELPERS
    # =========================================================

    def show_result(
        self,
        result
    ):

        if result["stdout"]:

            self.log(
                result["stdout"]
            )

        if result["stderr"]:

            self.log(
                result["stderr"]
            )

    def log(
        self,
        text
    ):

        if hasattr(
            self,
            "output"
        ):

            self.output.append(
                str(text)
            )


# =============================================================
# APPLICATION
# =============================================================

app = QApplication(
    sys.argv
)

app.setStyleSheet(
    """
    QWidget {
        font-size: 13px;
    }

    QPushButton {
        padding: 8px;
    }

    QTableWidget {
        gridline-color: #555555;
    }

    QGroupBox {
        font-weight: bold;
        margin-top: 10px;
    }
    """
)

window = MainWindow()

window.show()

sys.exit(
    app.exec()
)
