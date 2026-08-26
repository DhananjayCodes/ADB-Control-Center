# DroidDesk

> A graphical Android Device Management tool for Linux built around ADB and Scrcpy.

DroidDesk is a desktop GUI application that makes Android Debug Bridge (ADB) functionality easier to use.

Instead of remembering and typing ADB commands manually, users can perform common Android device operations through dedicated graphical buttons and menus.

It also provides an advanced ADB terminal for users who want direct access to commands.

---

## ✨ Features

### 📱 Device Management

- Detect connected Android devices
- Display device serial numbers
- Display connection status
- Switch between multiple connected devices
- Refresh connected devices
- Connect to devices using Wireless ADB

### 📊 Device Information

View important information about the connected Android device:

- Device model
- Manufacturer
- Android version
- SDK version
- Serial number
- Screen resolution
- Battery percentage
- Battery charging/status information
- Storage information

### 📺 Screen Mirroring

DroidDesk includes a bundled Scrcpy executable.

You can mirror and control your Android device directly from the application without manually launching Scrcpy from the terminal.

### 📦 Application Management

View installed Android applications and perform:

- Search applications
- Launch application
- Force stop application
- Clear application data
- Enable application
- Disable application
- Uninstall application
- Install APK files

### 📁 File Management

Interact with files on the Android device:

- Browse device directories
- View `/sdcard`
- Push files from Linux → Android
- Pull files from Android → Linux

### 📋 Logcat

View Android system logs directly inside DroidDesk.

Controls include:

- Start Logcat
- Stop Logcat
- Clear Logcat output

### ⚙ Advanced ADB Terminal

For advanced users, DroidDesk also provides an ADB command terminal.

For example:

```text
shell getprop ro.product.model
