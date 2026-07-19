from termcolor import colored

def error_text(string: str) -> str:
    return colored(string, 'red', attrs=['bold'])

def warning_text(string: str) -> str:
    return colored(string, 'light_yellow')

def highlight_text(string: str) -> str:
    return colored(string, 'magenta')

def info_text(string: str) -> str:
    return colored(string, 'blue')
