import custom_lib.db.sqllite3 as sql3
import custom_lib.log as l
import getpass
import os 
import time

def describe(app_file, module, **kwargs):
    print("""
-------------------------------------------------
        Module for handling server instances 
          Add, remove or update, start, 
             stop and list  servers 
-------------------------------------------------

%s -m server -f add -a <options>
    Adds server to system 
    Example 
        %s -m server -f add -a ip=127.0.0.1 port=1 auth=1 
        Adds server to database, and server requires auth  

%s -m server -f list
    - List servers

%s -m server -f list -a id=<id> users
    <id>        server id 
    - Lists users assigned to this server 
    
%s -m server -f list -a id=<id> emails 
    <id>        server id 
    - List email assigned to this server 
    
%s -m server -f addemail -a server=<server> email=<email>
    <server>    server id
    <email>     email id
    - Adds email for server
    
%s -m server -f removeemail -a server=<server> email=<email>
    <server>    server id
    <email>     email id
    - Removes emial from server 
    
%s -m server -f adduser -a server=<server> user=<user>
    <server>    server id
    <user>      user id
    - Adds user for server
    
%s -m server -f removeuser -a server=<server> user=<user>
    <server>    server id
    <user>      user id
    - Removes user from server 
    
%s -m server -f start -a id=<id>
    <id>        server id 
    - Start server 
    
%s -m server -f stop -a id=<id>
    <id>        server id 
    - Stop server 
    
%s -m server -f restart -a id=<id>
    <id>        server id
    - Restart server 

-------------------------------------------------
    """.strip() %(app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file))
    
def __is_valid_iser__():
    if getpass.getuser() is 'root':
        return True
    return False
    
def add(db, args, **kwargs):
    l.debug("Add server")
    l.debug(args)
        
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
    
    if len(args) == 0:
        l.error("No arguments.")
        return 0
    
    user = sql3.entity.Server(db.getConnection())
    
    for key, val in args.items():
        user.set(key, val);
    
    user.save()
    return 0;
    
def remove(db, args, **kwargs):
    l.debug("Remove server")
    l.debug(args)
        
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
    
    if 'id' not in args:
        l.error("Id for user not found")
        return 1
    user = sql3.entity.Server(db.getConnection());
    user.delete()

def update(db, args, **kwargs):
    l.debug("Update user")
    l.debug(args)
        
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
    
    if 'id' not in args:
        l.error("Id for user not found")
        return 1
    user = sql3.entity.Server(db.getConnection())
    user.fetch(args['id'])
    
    if 'id' not in user.data:
        l.error("User does not exists")
        return 2
        
    for key, val in args.items():
        user.set(key, val);
        
    user.update()
    
def start(db, db_file, args, config, **kwargs):
    l.debug("Start server instance");
    l.debug(args)
    
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
    
    if 'id' not in args:
        l.error("Please provide server id")
        return 1
        
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['id'])
    
    if 'id' not in server.data:
        l.error("Server Instance not found")
        return 2 
        
    if int(server.get('pid')) > 0:
        l.error("Server already running PID=%s" % server.get('pid'))
        return 3
        
    pid = os.fork()
    
    if pid == 0:
        from .server import run
        run(server, db_file, config['storage_folder'])
    
    return 0

def stop(db, args, **kwargs):
    l.debug("Stop server instance")
    l.debug(args)
    
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
    
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['id'])
    
    if 'id' not in server.data:
        l.error("Server Instance not found")
        return 2 
        
    if int(server.get('pid')) <= 0:
        l.error("Server not running.")
        return 3

    from .server import stop 
    stop(server)

        
def restart(db, db_file, args, config, **kwargs):
    l.debug("Restart server instance ")
    l.debug(args)
        
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
        
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['id'])
    
    if 'id' not in server.data:
        l.error("Server Instance not found")
        return 2 
        
    if int(server.get('pid')) <= 0:
        l.error("Server not running.")
        return 3

    import server as s
    s.restart(server, db_file)
    
    s.stop(server)
    time.sleep(3)

    pid = os.fork()
    
    if pid == 0:
        s.run(server, db_file, config['storage_folder'])
    
def adduser(db, args, **kwargs):
    l.debug("Add user to server")
    
    if 'user' not in args:
        l.error("User id not provided")
        return 1
        
    if 'server' not in args:
        l.error("Server id not provided")
        return 1
        
    user = sql3.entity.User(db.getConnection())
    user.fetch(args['user'])
    
    if 'id' not in user.data:
        l.error("User %s not found" % args['user'])
        return 1
        
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['server'])
    
    if 'id' not in server.data:
        l.error("Server %s not found" % args['server'])
        return 1
        
    server.addUser(user.get('id'))
    
def removeuser(db, args, **kwargs):
    l.debug("Remove user from server ")
    
    if 'user' not in args:
        l.error("User id not provided")
        return 1
        
    if 'server' not in args:
        l.error("Server id not provided")
        return 1
        
    user = sql3.entity.User(db.getConnection())
    user.fetch(args['user'])
    
    if 'id' not in user.data:
        l.error("User %s not found" % args['user'])
        return 1
        
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['server'])
    
    if 'id' not in server.data:
        l.error("Server %s not found" % args['server'])
        return 1
        
    server.removeUser(user.get('id'))
    
def addemail(db, args, **kwargs):
    l.debug("Add email to server")
    
    if 'email' not in args:
        l.error("Email id not provided")
        return 1
        
    if 'server' not in args:
        l.error("Server id not provided")
        return 1
        
    user = sql3.entity.EmailAccount(db.getConnection())
    user.fetch(args['email'])
    
    if 'id' not in user.data:
        l.error("Email %s not found" % args['user'])
        return 1
        
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['server'])
    
    if 'id' not in server.data:
        l.error("Server %s not found" % args['server'])
        return 1
        
    server.addEmailAccount(user.get('id'))
    
def removeemail(db, args, **kwargs):
    l.debug("Remove email from server ")
    
    if 'email' not in args:
        l.error("Email id not provided")
        return 1
        
    if 'server' not in args:
        l.error("Server id not provided")
        return 1
        
    user = sql3.entity.EmailAccount(db.getConnection())
    user.fetch(args['email'])
    
    if 'id' not in user.data:
        l.error("User %s not found" % args['user'])
        return 1
        
    server = sql3.entity.Server(db.getConnection())
    server.fetch(args['server'])
    
    if 'id' not in server.data:
        l.error("Server %s not found" % args['server'])
        return 1
        
    server.removeEmailAccount(user.get('id'))
    
        
def list(db, args, **kwargs):
    l.debug("List Servers") 
        
    if __is_valid_iser__():
        l.error("User %s does not have permission" % getpass.getuser())
        return 1
    
    srv = sql3.entity.Server(db.getConnection())
    
    if 'users' in args and 'id' in args:   
        l.debug("List users for server %s" % args['id']) 
        srv.fetch(args['id'])
        
        if 'id' not in srv.data:
            l.error("Server %s not found" % str(args['id']))
            return 1
        
        for i in srv.getUsers():
            user = sql3.entity.User(db.getConnection())
            print user.fetch(i)
            
        return 1
        
    if 'emails' in args and 'id' in args:
        l.debug("List email accounts for server %s" % args['id'])
        srv.fetch(args['id'])
        
        if 'id' not in srv.data:
            l.error("Server %s not found" % str(args['id']))
            return 1
        
        for i in srv.getEmailAccounts():
            ea = sql3.entity.EmailAccount(db.getConnection())
            print ea.fetch(i)
            
        return 1
    
    for i in srv.all():
        print i
    
