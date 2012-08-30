import re

def indent_line(level, string):
    if string == '':
        return string
    else:
        return '    ' * level + string

def indent(level, code):
    return '\n'.join([indent_line(level, string) for string in re.split(r'[\n\r]+', code)])

def json_pair(key, value):
    return "\"" + key + "\" : \"" + value + "\""
