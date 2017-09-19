import custom_lib.db.sqllite3 as sql3 
import custom_lib.mailer as cmailer
import custom_lib.log as l
import shutil
import json
import uuid
import os


def describe(app_file, module, config, db, **kwargs):
    print("""
Availible options
    %s -m user      User module 
        Module for managing users  

    %s -m server    Server module
        Starts for managing server instances
        
    %s -m email     Email module
        Service for managing emails 
         
    %s -m queque    Queque module
        Service for managing email queques
        
    %s -f load -a file=<file.json>
        <file.json> file with email data
    """.strip() % (app_file, app_file, app_file, app_file))



def load(args, db, config, **kwargs):
    if not os.path.isdir("%s/custom" % config['storage_folder']):
        os.makedirs("%s/custom" % config['storage_folder'])

    if not os.path.isdir("%s/custom" % config['storage_folder']):
        l.error("Directory does not exists")
        return 1 
        
    if ('file' in args) and (os.path.isfile(args['file'])):
        validator = None;
        ejson = None
        with open(args['file']) as f:
            ejson = json.load(f)
            validator = cmailer.validateJSON(ejson)
            
        if validator is None:
            l.error("Unable to load json from file")
            return 1
        
        try:
            l.debug("validate check")
            validator.doCheck()
            
            newfile = "%s/custom/%s.json" % (config['storage_folder'], str(uuid.uuid4()))
            
            with open(newfile, 'w') as fw:
                fw.write(json.dumps(ejson))
                
                q = sql3.entity.Queque(db.getConnection())
                q.set('path', newfile)
                q.save()
            
        except Exception, e:
            l.error(str(e))
    else:
        l.error("Please pass correct path ")
        return 1
        
