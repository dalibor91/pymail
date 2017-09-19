#!/usr/bin/python

import os
import sys
import argparse
import logging
from datetime import date
import modules as app_modules
import config as app_config
import custom_lib.db.sqllite3 as sql3 
import custom_lib.log as l


parser = argparse.ArgumentParser(description='Service for sending emails ')
parser.add_argument('--describe', default=False, help='Prints description of module and arguments that it requires', dest='describe_module', action='store_true')
parser.add_argument('-m', help="Module to load from modules directory", dest="module", default=None)
parser.add_argument('-f', help="Action to run from loaded moduke", dest="action", default=None)
#parser.add_argument('--log-level', help="log level for module", dest="log_level", choices=['debug', 'info', 'warning','error','critical'], default="debug")
parser.add_argument('--log-file', help="file to log", dest="log_file", default=None)
parser.add_argument('-a', help="Aditional arguments required for module", dest="carg", default=[], nargs='+', type=str)

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		parser.print_help();
		exit(0)
	
	args = parser.parse_args()
	app_file = os.path.relpath(__file__)
	app_dir = (os.path.dirname(os.path.realpath(__file__)))
	
	if args.describe_module or (args.action is None):
		args.action = 'describe'
		
	if args.module is None:
		args.module = 'init'
	
	if (args.module is None):
		parser.print_help()
		quit();
	
	conf = app_config.context_config('main')
	
	log_file = args.log_file if args.log_file is not None else ("%s/%s" % (conf['log_folder'], date.today().isoformat()))
	
	log_format = "[ %s ] [ %s ] [ %s ] [ %s ] %s:%s - %s" % ( '%(asctime)s', '%(levelname)s', args.module, args.action, '%(filename)s', '%(lineno)d', '%(message)s')

	logging.basicConfig(filename=log_file, format=log_format, level="ERROR")#, level=args.log_level.upper())

	options = {
		"app_dir": app_dir,
		"app_file": os.path.basename(app_file),
		"_app_file": app_file,
		"module": args.module,
		"config": conf,
		"log": logging,
		"db_file": conf['sqlite3']['database'],
		"db": sql3.connection.Connection(conf['sqlite3']['database']),
		"args": app_modules.parse_custom_arguments(args.carg) if len(args.carg) > 0 else {}, 
	}
	
	sql3.create_tables(conf['sqlite3']['database'])
	
	if not app_modules.module_exists("%s/modules/%s"%(app_dir,args.module)):
		l.error("Module %s does not exists" % args.module)
		quit()
	
	mod = app_modules.load_module(args.module) 
	
	if hasattr(mod, args.action):
		method = getattr(mod, args.action)
		v = method(**options)
		
		if v is None:
			v = 0
		
		sys.exit(int(v));
		try:
			options['db'].close()
		except:
			l.warning("Unable to close database %s")
	else:
		l.warning("Module does not have %s action" % args.action)

	sys.exit(255)
