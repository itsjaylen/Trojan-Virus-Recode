from os import listdir, remove, rmdir, system
from zipfile import ZIP_DEFLATED, ZipFile

from modules.config import pack_include


def build():
    if pack_include == True:
        with ZipFile("include.zip", "w", compression=ZIP_DEFLATED) as zip:
            try:
                for filename in listdir("include"):
                    zip.write(f"./include/{filename}")
            except Exception:
                pass

    system("complie.bat")

    try:
        remove("include.zip")
        rmdir("__pycache__")
    except OSError:
        pass


if __name__ == "__main__":
    build()
