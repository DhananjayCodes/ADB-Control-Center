class DeviceManager:

    def __init__(self, adb):
        self.adb = adb

    def get_property(self, name):

        result = self.adb.shell(
            "getprop",
            name
        )

        if result["success"]:
            return result["stdout"]

        return "Unknown"

    def get_info(self):

        return {
            "model": self.get_property(
                "ro.product.model"
            ),

            "manufacturer": self.get_property(
                "ro.product.manufacturer"
            ),

            "android": self.get_property(
                "ro.build.version.release"
            ),

            "sdk": self.get_property(
                "ro.build.version.sdk"
            ),

            "serial": self.get_property(
                "ro.serialno"
            )
        }

    def battery(self):

        return self.adb.shell(
            "dumpsys",
            "battery"
        )
