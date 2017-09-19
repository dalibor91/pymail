import custom_lib.db.sqllite3 as sql3
import custom_lib.log as l

def describe(app_file, module, args, **kwargs):
    print("""
-------------------------------------------------
    Module for handling email queque in system 
        Add, remove, update and list emails
           Resend, send waiting emails
-------------------------------------------------

%s -m email -f add -a <options>
    Adds email to system 
    Example 
        %s -m email -f add -a email=test@test.com username=test@test.com password=1234 tls=1
        Adds email to database 

%s -m email -f remove -a id=<id>
    <id>    Email id
    Removes email  
    
%s -m email -f update -a id=<id> ['<option>=<value>']
    <id>    Email id 
    Updates email 

%s -m email -f list
    List all emails - send and not sent 

-------------------------------------------------
    """.strip() % (app_file,app_file,app_file,app_file,app_file))
    
def add(db, args, **kwargs):
    l.debug("Add user accounts")
    l.debug(args)
    if len(args) == 0:
        print "No arguments."
        return 1
    
    user = sql3.entity.EmailAccount(db.getConnection())
    
    for key, val in args.items():
        user.set(key, val);
    
    user.save()
    return 0;

def remove(db, args, **kwargs):
    l.debug("Remove user acciunt")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for user not found")
        return 1
    user = sql3.entity.EmailAccount(db.getConnection());
    user.delete()

def update(db, args, **kwargs):
    l.debug("Update user")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for user not found")
        return 1
    user = sql3.entity.EmailAccount(db.getConnection())
    user.fetch(args['id'])
    
    if 'id' not in user.data:
        print "User account does not exists"
        return 2
        
    for key, val in args.items():
        user.set(key, val);
        
    user.update()
    
def list(db, **kwargs):
    l.debug("List user accounts")
    user = sql3.entity.EmailAccount(db.getConnection())
    
    for i in user.all():
        print i
    
    
