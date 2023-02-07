import os
from colorama import init, Style, Fore
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent

init()

def path(*paths: tuple[Any], base_dir: str = str(ROOT_DIR)):
    resolve_paths = []

    for path in paths:
        if isinstance(path, str):
            resolve_paths.append(path)
        else:
            resolve_paths.extend(path)

    return os.path.join(base_dir, *resolve_paths)
    

def colorize(msg: str, color: str) -> str:
    color = color.lower()
    colors = {
        'red': Fore.RED,
        'blue': Fore.BLUE,
        'black': Fore.BLACK,
        'green': Fore.GREEN,
        'cyan': Fore.CYAN,
        'magenta': Fore.MAGENTA,
        'yellow': Fore.YELLOW,
    }
    if (col := colors.get(color, False)):
        return f'{col}{msg}{Style.RESET_ALL}'
    return msg


