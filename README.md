# DroidDesk

## Android Device Management GUI for Linux

DroidDesk is a graphical Android device management application for Linux.

It provides an easy-to-use interface over **Android Debug Bridge (ADB)** so users can perform common Android operations without remembering ADB commands.

### Features

- Android device detection and device selection
- Device information
- Battery information
- Storage information
- Screen mirroring using Scrcpy
- Screenshots
- Device reboot
- APK installation
- Installed application management
- Launch applications
- Force stop applications
- Clear application data
- Enable/disable applications
- Uninstall applications
- Android file browsing
- Push files to Android
- Pull files from Android
- Logcat
- Wireless ADB
- Advanced ADB terminal

---

# 1. Requirements

DroidDesk is designed for Linux, especially Debian/Ubuntu-based distributions.

You need:

- A Linux computer
- An Android phone
- A USB cable
- Internet access for the first installation

No prior Python or ADB knowledge is required. Follow the setup below in order.

---

# 2. Complete Installation

## Step 1 — Open a Terminal

On most Linux desktop environments, press:

```text
Ctrl + Alt + T
```

## Step 2 — Install System Dependencies

Run:

```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    adb \
    ca-certificates
```

These packages provide:

| Package | Purpose |
|---|---|
| `python3` | Runs DroidDesk |
| `python3-pip` | Installs Python packages |
| `python3-venv` | Creates the Python virtual environment |
| `git` | Downloads the project |
| `adb` | Communicates with Android devices |
| `ca-certificates` | HTTPS certificate support |

Verify Python:

```bash
python3 --version
```

Verify pip:

```bash
python3 -m pip --version
```

Verify ADB:

```bash
adb version
```

---

# 3. Download DroidDesk

Clone the repository:

```bash
git clone https://github.com/DhananjayCodes/ADB-Control-Center.git
```

Enter the project:

```bash
cd ADB-Control-Center
```

Check your current directory:

```bash
pwd
```

You should see a path similar to:

```text
/home/your_username/ADB-Control-Center
```

---

# 4. Create the Python Virtual Environment

DroidDesk uses a Python virtual environment so its Python packages remain separate from the Linux system Python installation.

Create it:

```bash
python3 -m venv .venv
```

This creates:

```text
.venv/
```

inside the project.

---

# 5. Activate the Virtual Environment

Run:

```bash
source .venv/bin/activate
```

Your terminal should now look similar to:

```text
(.venv) user@computer:~/ADB-Control-Center$
```

The `(.venv)` means the environment is active.

---

# 6. Install Python Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

The repository should contain `requirements.txt` with the required Python packages, including:

```text
PySide6
```

Verify PySide6:

```bash
python3 -c "import PySide6; print('PySide6 installed successfully')"
```

Expected output:

```text
PySide6 installed successfully
```

---

# 7. Prepare the Android Phone

DroidDesk communicates with Android through ADB.

## Enable Developer Options

On most Android devices:

1. Open **Settings**.
2. Open **About phone**.
3. Find **Build number**.
4. Tap **Build number** 7 times.
5. Return to Settings.
6. Open **Developer options**.
7. Enable **USB debugging**.

The exact menu names may vary between Android manufacturers.

---

# 8. Connect the Android Device

Connect the phone to the Linux computer using USB.

Start the ADB server:

```bash
adb start-server
```

Check connected devices:

```bash
adb devices
```

The first time you connect, the Android phone may show:

```text
Allow USB debugging?
```

Press **Allow**. You may also enable **Always allow from this computer**.

Run again:

```bash
adb devices
```

A successful result looks like:

```text
List of devices attached
DEVICE_SERIAL    device
```

For example:

```text
List of devices attached
0011864AF001009    device
```

The serial number is different for every device.

---

# 9. If the Device Shows `unauthorized`

If you see:

```text
List of devices attached
DEVICE_SERIAL    unauthorized
```

1. Unlock the Android phone.
2. Look for the **Allow USB debugging** dialog.
3. Press **Allow**.
4. Run:

```bash
adb devices
```

again.

The device should now show:

```text
DEVICE_SERIAL    device
```

---

# 10. If No Device Appears

Restart ADB:

```bash
adb kill-server
adb start-server
adb devices
```

If the device is still missing:

- Check the USB cable.
- Try another USB port.
- Make sure USB debugging is enabled.
- Unlock the phone.
- Accept the USB debugging authorization.
- Reconnect the USB cable.

---

# 11. Test ADB Before Starting DroidDesk

This confirms that the Linux computer can communicate with the phone.

Run:

```bash
adb devices
```

Then test the device model:

```bash
adb shell getprop ro.product.model
```

For example:

```text
A015
```

Test battery information:

```bash
adb shell dumpsys battery
```

List installed Android packages:

```bash
adb shell pm list packages
```

If these commands work, ADB communication is working.

---

# 12. Scrcpy Setup

DroidDesk uses Scrcpy for Android screen mirroring.

The project includes Scrcpy under:

```text
tools/scrcpy/
```

The directory should contain files similar to:

```text
tools/scrcpy/
├── adb
├── scrcpy
├── scrcpy-server
├── scrcpy.png
├── disconnected.png
├── LICENSE
└── scrcpy.1
```

Make the executables runnable:

```bash
chmod +x tools/scrcpy/scrcpy
chmod +x tools/scrcpy/adb
```

Test Scrcpy directly:

```bash
./tools/scrcpy/scrcpy
```

If the Android screen appears, Scrcpy is working. Close the Scrcpy window and continue.

DroidDesk launches this bundled Scrcpy automatically when **Screen Mirror** is selected.

---

# 13. Start DroidDesk

From the project directory:

```bash
cd ADB-Control-Center
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Check the Android device:

```bash
adb devices
```

Then start the application:

```bash
python3 main.py
```

The DroidDesk graphical interface should open.

---

# 14. Starting DroidDesk After the First Installation

You do not need to recreate the virtual environment or reinstall dependencies every time.

After the first setup, connect the Android phone and run:

```bash
cd ~/ADB-Control-Center
source .venv/bin/activate
adb devices
python3 main.py
```

If you cloned the repository somewhere else, use that directory instead.

---

# 15. Dashboard

The Dashboard provides an overview of the selected Android device.

It displays:

- Model
- Manufacturer
- Android version
- SDK version
- Serial number
- Screen resolution
- Battery percentage
- Battery status
- Storage information

It also provides quick actions such as:

- Screen Mirror
- Screenshot
- Reboot
- Install APK
- Refresh device information
- Refresh battery information

---

# 16. Devices

The Devices tab displays Android devices detected by ADB.

Example:

```text
Serial              Status
--------------------------------
0011864AF001009      device
```

Use **Refresh Devices** to scan for devices again.

If multiple devices are connected, select the device you want DroidDesk to control.

---

# 17. Applications

The Applications tab retrieves installed Android packages.

You can search the list and select an application.

Available actions:

```text
Launch
Force Stop
Clear Data
Enable
Disable
Uninstall
```

You can also install an APK using **Install APK**.

## Launch Application

Select an application and click **Launch**.

## Force Stop

Select an application and click **Force Stop**.

The underlying operation is equivalent to:

```bash
adb shell am force-stop PACKAGE_NAME
```

## Clear Application Data

Select an application and click **Clear Data**. DroidDesk asks for confirmation before clearing the application's stored data.

The underlying operation is equivalent to:

```bash
adb shell pm clear PACKAGE_NAME
```

## Enable / Disable Applications

Select an application and use **Enable** or **Disable**. Android may restrict these operations for certain protected system applications.

## Uninstall Application

Select an application and click **Uninstall**. DroidDesk asks for confirmation.

The underlying operation is equivalent to:

```bash
adb uninstall PACKAGE_NAME
```

Some system applications cannot be uninstalled on normal non-rooted devices.

---

# 18. Install APK

Click **Install APK** and select an `.apk` file from the Linux computer.

DroidDesk installs it on the selected Android device.

The equivalent ADB command is:

```bash
adb install application.apk
```

---

# 19. Screen Mirror

Click **Screen Mirror**.

DroidDesk launches the bundled Scrcpy executable.

The operation is conceptually equivalent to:

```bash
scrcpy -s DEVICE_SERIAL
```

The user does not need to type this command.

---

# 20. Screenshot

Click **Screenshot** and choose where to save the image.

DroidDesk captures the Android display and saves the screenshot as a PNG image.

The underlying ADB functionality is:

```bash
adb exec-out screencap -p
```

---

# 21. Reboot Device

Click **Reboot**. DroidDesk asks for confirmation before restarting the device.

The underlying command is:

```bash
adb reboot
```

---

# 22. File Manager

The Files tab provides access to Android storage.

The default location is:

```text
/sdcard
```

You can:

- Browse directories
- Push files to Android
- Pull files from Android

## Push File

Push copies a file from Linux to Android.

Example:

```text
document.pdf
    ↓
/sdcard/Download/
```

Equivalent command:

```bash
adb push document.pdf /sdcard/Download/
```

## Pull File

Pull copies a file from Android to Linux.

Equivalent command:

```bash
adb pull /sdcard/Download/document.pdf
```

---

# 23. Logcat

The Logcat tab displays Android system logs.

Controls:

```text
Start Logcat
Stop
Clear
```

The underlying command is:

```bash
adb logcat
```

Logcat can be useful for Android application debugging, investigating crashes, monitoring system behavior, and troubleshooting devices.

---

# 24. Wireless ADB

DroidDesk can connect to an Android device over a network when Wireless ADB is configured.

Select **Connect over Wi-Fi** and enter the device address, for example:

```text
192.168.1.10:5555
```

The underlying command is:

```bash
adb connect 192.168.1.10:5555
```

The Android device and Linux computer must be configured for network ADB.

---

# 25. Advanced ADB Terminal

DroidDesk includes an Advanced ADB terminal for commands that do not yet have a dedicated GUI button.

Example:

```text
shell getprop ro.product.model
```

Equivalent command:

```bash
adb shell getprop ro.product.model
```

Another example:

```text
shell pm list packages
```

Equivalent command:

```bash
adb shell pm list packages
```

The Advanced terminal is optional. Normal users can operate DroidDesk using the graphical controls without remembering ADB syntax.

---

# 26. Project Structure

```text
ADB-Control-Center/
│
├── main.py
│
├── core/
│   ├── __init__.py
│   ├── adb.py
│   ├── apps.py
│   ├── device.py
│   ├── files.py
│   └── scrcpy.py
│
├── tools/
│   └── scrcpy/
│       ├── adb
│       ├── scrcpy
│       ├── scrcpy-server
│       ├── scrcpy.png
│       ├── disconnected.png
│       ├── LICENSE
│       └── scrcpy.1
│
├── requirements.txt
├── README.md
└── .gitignore
```

The `.venv/` directory is created locally and should not be committed to Git.

---

# 27. Architecture

DroidDesk uses a modular architecture:

```text
                    DroidDesk GUI
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     DeviceManager   AppManager    FileManager
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                    ADBManager
                         │
                         ▼
                        ADB
                         │
                         ▼
                  Android Device

                         +
                         │
                         ▼
                  Scrcpy Manager
                         │
                         ▼
                      Scrcpy
```

---

# 28. Core Components

## `main.py`

Responsible for:

- Graphical interface
- Tabs
- Buttons
- User interaction
- Displaying results

## `core/adb.py`

Responsible for:

- ADB communication
- Device detection
- Executing ADB commands
- Running Android shell commands

## `core/device.py`

Responsible for:

- Device information
- Battery information

## `core/apps.py`

Responsible for:

- Application listing
- APK installation
- Application launching
- Force stopping applications
- Clearing application data
- Enabling/disabling applications
- Uninstalling applications

## `core/files.py`

Responsible for Android file operations.

## `core/scrcpy.py`

Responsible for Scrcpy integration.

---

# 29. Troubleshooting

## DroidDesk does not start

Make sure the project directory is correct:

```bash
cd ~/ADB-Control-Center
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Check Python:

```bash
python3 --version
```

Check PySide6:

```bash
python3 -c "import PySide6; print(PySide6.__version__)"
```

Then run:

```bash
python3 main.py
```

## PySide6 is missing

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## `ModuleNotFoundError: No module named 'core'`

Make sure you are running from the project directory:

```bash
cd ADB-Control-Center
source .venv/bin/activate
python3 main.py
```

Make sure this file exists:

```text
core/__init__.py
```

If it is missing:

```bash
touch core/__init__.py
```

## ADB command not found

Install ADB:

```bash
sudo apt update
sudo apt install -y adb
```

Then verify:

```bash
adb version
```

## Android device is not detected

Run:

```bash
adb devices
```

Then restart ADB:

```bash
adb kill-server
adb start-server
adb devices
```

Make sure USB debugging is enabled and the phone has authorized the computer.

## Device says `unauthorized`

Unlock the phone and accept **Allow USB debugging?**, then run:

```bash
adb devices
```

again.

## Scrcpy does not start

Check that the executable exists:

```bash
ls -l tools/scrcpy/scrcpy
```

Make it executable:

```bash
chmod +x tools/scrcpy/scrcpy
```

Test it:

```bash
./tools/scrcpy/scrcpy
```

## APK installation fails

Check the Android connection:

```bash
adb devices
```

Then test the APK manually:

```bash
adb install your-file.apk
```

Some APKs may be incompatible with the Android version or device architecture.

## An application cannot be uninstalled

Some Android system applications are protected. DroidDesk does not bypass Android security restrictions.

---

# 30. Virtual Environment Commands

### Create

```bash
python3 -m venv .venv
```

### Activate

```bash
source .venv/bin/activate
```

### Deactivate

```bash
deactivate
```

### Delete

```bash
rm -rf .venv
```

### Recreate

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# 31. Requirements

The repository contains:

```text
requirements.txt
```

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

---

# 32. Security and Permissions

DroidDesk uses the permissions provided by Android Debug Bridge.

It does not bypass Android security.

Some operations may be unavailable for:

- Protected applications
- System applications
- Non-rooted devices
- Restricted Android versions

Only use DroidDesk with devices that you own or have permission to manage.

---

# 33. Quick Start After Initial Installation

After the first setup, connect your Android phone and run:

```bash
cd ~/ADB-Control-Center
source .venv/bin/activate
adb devices
python3 main.py
```

The DroidDesk GUI will start.

---

# 34. Author

**Dhananjay Rawat**

GitHub:

https://github.com/DhananjayCodes

Project:

https://github.com/DhananjayCodes/ADB-Control-Center

---

# 35. License

See the `LICENSE` file included with the project.

---

# DroidDesk

DroidDesk turns Android device management from a command-line workflow into an easy-to-use Linux desktop application.

The basic workflow is:

```text
Install Linux dependencies
        ↓
Clone DroidDesk
        ↓
Create virtual environment
        ↓
Install Python dependencies
        ↓
Set up ADB
        ↓
Connect Android device
        ↓
Set up bundled Scrcpy
        ↓
Run DroidDesk
        ↓
Manage Android through the GUI
```

The goal is simple:

```text
ADB Command Line
       ↓
Graphical Interface
       ↓
Easy Android Device Management
```
