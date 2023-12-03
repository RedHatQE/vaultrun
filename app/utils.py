import os
import sys
from configparser import ConfigParser

from rofi import Rofi
import dmenu

def parse_config(conf_file, section="SETTING"):
    parser = ConfigParser()
    # Open the file with the correct encoding
    parser.read(conf_file, encoding="utf-8")
    params_dict = {}
    for params in parser.items(section):
        params_dict[params[0]] = params[1]

    return params_dict

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


def call_dmenu(options, abort=True, prompt=None):
    if which("rofi"):
        _rofi = Rofi()
        index, key = _rofi.select(prompt if prompt else "Select:", options)
        if key == -1:
            sys.exit(0)
        return options[index]

    else:
        user_select = dmenu.show(
            options, lines=30, case_insensitive=True, fast=True, prompt=prompt
        )
        if not user_select and abort:
            sys.exit(0)
        return user_select