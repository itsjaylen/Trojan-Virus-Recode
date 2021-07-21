from os import path
from sys import argv
from time import sleep
from pymem import Pymem


def anti_debug():
    """Checks for dlls from being injected"""
    running_dlls = []
    app = path.basename(argv[0])

    def check():
        """Checking dll amount"""
        try:
            pm = Pymem(app)
            modules = list(pm.list_modules())
            for module in modules:
                running_dlls.append(module.name)
        except Exception:
            pass

        if len(running_dlls) > 15:
            print("Tamper Detected")

    while 1:
        sleep(3)
        check()
        running_dlls.clear()
