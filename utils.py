import re

def indent(level, code):
    return '\n'.join(['    ' * level + string for string in re.split(r'[\n\r]+', code)])
