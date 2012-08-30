import re

def make_erlang_atom(Name):
    return re.sub("^_", "", re.sub("([A-Z])", "_\g<0>", Name).lower())
