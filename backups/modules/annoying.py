from ctypes import windll
from random import choice, randint
from time import sleep
from webbrowser import open_new_tab

from modules.config import links, pop_up_text


def open_url():
    """Opens urls from list to webbrowser"""
    while 1:
        open_new_tab(choice(links))
        sleep(randint(1, 10))


def popup():
    """Spams popups"""
    while 1:
        windll.user32.MessageBoxW(0, choice(pop_up_text), "LOL", randint(1, 5))
        sleep(randint(1, 5))
