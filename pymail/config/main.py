import os

home = "%s/.pymailer" % os.path.expanduser("~")

userdb = "%s/userdb.db" % home 
storage = "%s/userstorage" % home 
logfolder = "%s/log" % home 

if not os.path.isdir(storage):
	os.makedirs(storage)
	
if not os.path.isdir(logfolder):
	os.makedirs(logfolder)
	
if not os.path.isdir(storage):
	print "Unable to write in users home directory"
	exit(1);
	
if not os.path.isdir(logfolder):
	print "Unable to write in users home directory"
	exit(1);

config = {
	"sqlite3": {
		"database" : userdb
	},
	"storage_folder": storage, 
	"log_folder": logfolder,
	"messages": {
		"DEBUG" : False, 
		"INFO" : False, 
		"ERROR" : True, 
		"WARNING" : True
	}
}
