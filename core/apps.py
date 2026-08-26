class AppManager:

    def __init__(self, adb):
        self.adb = adb

    def list_packages(self):

        result = self.adb.shell(
            "pm",
            "list",
            "packages"
        )

        if not result["success"]:
            return []

        packages = []

        for line in result["stdout"].splitlines():

            if line.startswith("package:"):

                package = line[
                    len("package:"):
                ]

                packages.append(package)

        return packages

    def uninstall(self, package):

        return self.adb.run(
            "uninstall",
            package
        )

    def force_stop(self, package):

        return self.adb.shell(
            "am",
            "force-stop",
            package
        )

    def clear_data(self, package):

        return self.adb.shell(
            "pm",
            "clear",
            package
        )

    def disable(self, package):

        return self.adb.shell(
            "pm",
            "disable-user",
            "--user",
            "0",
            package
        )

    def enable(self, package):

        return self.adb.shell(
            "pm",
            "enable",
            package
        )

    def launch(self, package):

        return self.adb.shell(
            "monkey",
            "-p",
            package,
            "1"
        )

    def install(self, apk):

        return self.adb.run(
            "install",
            apk
        )
