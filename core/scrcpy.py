from pathlib import Path
import subprocess


class ScrcpyManager:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        self.scrcpy_path = (
            project_root
            / "tools"
            / "scrcpy"
            / "scrcpy"
        )

    def start(self, serial=None):

        if not self.scrcpy_path.exists():

            return {
                "success": False,
                "error": (
                    f"scrcpy executable not found:\n"
                    f"{self.scrcpy_path}"
                )
            }

        command = [
            str(self.scrcpy_path)
        ]

        if serial:
            command.extend([
                "-s",
                serial
            ])

        try:

            subprocess.Popen(
                command
            )

            return {
                "success": True,
                "error": ""
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }
