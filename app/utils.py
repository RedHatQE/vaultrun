import os
import sys
from configparser import ConfigParser

from rofi import Rofi
import dmenu


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ.get("PATH", "").split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def call_rofi_dmenu(options, abort=True, prompt=None):
    if which("rofi"):
        _rofi = Rofi()
        index, key = _rofi.select(prompt or "Select:", options)
        if key == -1:
            sys.exit(0)
        return options[index]

    else:
        user_select = dmenu.show(options, lines=30, case_insensitive=True, fast=True, prompt=prompt)
        if not user_select and abort:
            sys.exit(0)
        return user_select


def parse_user_config():
    config_file = os.path.join(os.path.expanduser("~"), ".config", "vaultrun", "config")
    _config_parser = ConfigParser()
    # Open the file with the correct encoding
    _config_parser.read(config_file, encoding="utf-8")
    sections_from_config = _config_parser.sections()
    if len(sections_from_config) == 1:
        config_section = sections_from_config[0]
    else:
        config_section = call_rofi_dmenu(options=sections_from_config, abort=True, prompt=None)

    _mount_point = _config_parser[config_section]["mount_point"]
    _secret_path = _config_parser[config_section]["secret_path"]
    return _mount_point, _secret_path
