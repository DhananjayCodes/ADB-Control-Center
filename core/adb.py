import subprocess


class ADBManager:

    def __init__(self):
        self.device = None

    def set_device(self, serial):
        self.device = serial

    def run(self, *args):
        command = ["adb"]

        if self.device:
            command.extend(["-s", self.device])

        command.extend(args)

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            }

        except FileNotFoundError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "ADB is not installed.",
                "returncode": -1
            }

    def devices(self):

        result = self.run("devices")

        devices = []

        if not result["success"]:
            return devices

        lines = result["stdout"].splitlines()

        for line in lines[1:]:

            parts = line.split()

            if len(parts) >= 2:

                devices.append({
                    "serial": parts[0],
                    "state": parts[1]
                })

        return devices

    def shell(self, *args):
        return self.run("shell", *args)
