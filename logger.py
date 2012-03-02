fverbose = True
fdebug = True

def set_debug(is_enabled):
    fdebug = is_enabled

def set_verbose(is_verbose):
    fverbose = is_verbose

def debug(str):
	if (fdebug):
		print str

def verbose(str):
	if (fverbose):
		print str

def info(str):
	print str

def warn(str):
	print str

def error(str):
	print str
