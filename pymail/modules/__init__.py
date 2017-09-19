import importlib
import os

def load_module(name):
	return importlib.import_module("modules.%s" % name.replace('/', '.'))
	
def module_exists(name):
	return os.path.isdir(name)

def parse_custom_arguments(arguments):
	u = {}
	for i in arguments:
		try:
			name, value = i.split('=', 1)
		except:
			name = i 
			value = True
		u[name] = value

	return u
