@echo off

pip install -r requirements.txt
pyarmor pack RuntimeBroker.py --clean -e " --onefile --console --add-data 'modules;.' --add-data 'include.zip;.'"


RD build /Q /S