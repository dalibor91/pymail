import custom_lib.db.sqllite3 as sql3
import custom_lib.log as l

def describe(app_file, module, **kwargs):
    print("""
-------------------------------------------------
        Module for handling users in system 
        Add, remove, update and list users 
-------------------------------------------------

%s -m user -f add -a <options>
    Adds user to system 
    Example 
        %s -m user -f add -a username=test password=test 
        Adds user to database 

%s -m user -f list
    List users 
    
%s -m user -f remove -a <options>
    Removes user from system 
    Example 
        %s -m user -f remove -a id=1 
        Removes user from database 
     
%s -m user -f update -a <options>
    Updates user 
    Example 
        %s -m user -f update -a id=1 username=new_username password=new_password
        Updates user with id = 1

-------------------------------------------------
    """.strip() % (app_file,app_file,app_file,app_file,app_file,app_file,app_file))
    
    
def add(db, args, **kwargs):
    l.debug("Add user")
    l.debug(args)
    if len(args) == 0:
        print "No arguments."
        return 0
    
    user = sql3.entity.User(db.getConnection())
    
    for key, val in args.items():
        user.set(key, val);
    
    user.save()
    return 0;
    
def remove(db, args, **kwargs):
    l.debug("Remove user")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for user not found")
        return 1
    user = sql3.entity.User(db.getConnection());
    user.delete()

def update(db, args, **kwargs):
    l.debug("Update user")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for user not found")
        return 1
    user = sql3.entity.User(db.getConnection())
    user.fetch(args['id'])
    
    if 'id' not in user.data:
        print "User does not exists"
        return 2
        
    for key, val in args.items():
        user.set(key, val);
        
    user.update()
    
def list(db, **kwargs):
    l.debug("List users")
    user = sql3.entity.User(db.getConnection())
    
    for i in user.all():
        print i
    
    #print user.all()
