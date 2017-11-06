import custom_lib.db.sqllite3 as sql3
import custom_lib.log as l
import custom_lib.mailer as cmailer

def describe(app_file, **kwargs):
    print("""
-------------------------------------------------
    Module for handling email queque in system 
        Add, remove, update and list emails
           Resend, send waiting emails
-------------------------------------------------

%s -m quequ -f add -a <options>
    Adds email to queque to system 
    Example 
        %s -m queque -f add -a path=/tmp/test.json
        Adds queque to database 

%s -m queque -f remove -a id=<id>
    <id>    Queque id
    Removes queque  
    
%s -m queque -f update -a id=<id> ['<option>=<value>']
    <id>    Queque id 
    Updates queque 

%s -m queque -f list
    List all emails - send and not sent 

%s -m queque -f list -a failed 
    List all email that failed to send 

%s -m queque -f list -a done 
    List all emails that are sent 
    
%s -m queque -f list -a waiting 
    List all emails that are waiting to send 
    
%s -m queque -f resend -a id=<id>
    <id>    Queque id 
    Resend email 
    
%s -m queque -f sendwaiting 
    Sends all emails in queque that are waiting 
    This is usally put in crontab
    
%s -m queque -f sendfailed
    Tries to resend emails 
    that failed 

-------------------------------------------------
    """.strip() % (app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file, app_file))
    
def add(db, args, **kwargs):
    l.debug("Add queque")
    l.debug(args)
    if len(args) == 0:
        print "No arguments."
        return 0
    
    q = sql3.entity.Queque(db.getConnection())
    
    for key, val in args.items():
        q.set(key, val);
    
    q.save()
    
def remove(db, args, **kwargs):
    l.debug("Remove queque")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for queque not found")
        return 1
    q = sql3.entity.Queque(db.getConnection());
    q.fetch(args['id'])
    q.delete()

def update(db, args, **kwargs):
    l.debug("Update queque")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for queque not found")
        return 1
    q = sql3.entity.Queque(db.getConnection())
    q.fetch(args['id'])
    
    if 'id' not in user.data:
        l.error("Queque does not exists")
        return 2
        
    for key, val in args.items():
        q.set(key, val);
        
    q.update()
    
def sendwaiting(db, **kwargs):
    l.debug("Send waiting emails in queque")
    
    q = sql3.entity.Queque(db.getConnection())
    
    for i in q.allWaitingWithLimit():
        tmpq = sql3.entity.Queque(db.getConnection())
        tmpq.fetch(i['id'])
        
        if 'id' not in tmpq.data:
            l.error("Unable to find queque")
            l.error(str(i))
            continue 
        
        u = cmailer.load(tmpq.get('path'))
        acc = sql3.entity.EmailAccount(db.getConnection())
        acc.data = acc.fetchBy('email', u['from'])
        
        if 'id' not in acc.data:
            l.error("Unable to find email %s" % u['from'])
            
        try :
            l.debug("Send email ")
            l.debug(str(i))
            cmailer.sendEmail(u, acc, tmpq)
        except Exception, e:
            l.error("Error in queque")
            l.error(str(e))
            
def sendfailed(db, **kwargs):
    l.debug("Send waiting emails in queque")
    
    q = sql3.entity.Queque(db.getConnection())
    
    for i in q.allFailed():
        tmpq = sql3.entity.Queque(db.getConnection())
        tmpq.fetch(i['id'])
        
        if 'id' in tmpq.data:
            l.error("Unable to find queque")
            l.error(str(i))
            continue 
        
        u = cmailer.load(q.get('path'))
        acc = sql3.entity.EmailAccount(db.getConnection())
        acc.data = acc.fetchBy('email', u['from'])
        
        if 'id' not in acc.data:
            l.error("Unable to find email %s" % u['from'])
            
        try :
            l.debug("Send email ")
            l.debug(str(i))
            cmailer.sendEmail(u, acc, q)
        except Exception, e:
            l.error("Error in queque")
            l.error(str(e))
    
def resend(db, args, **kwargs):
    l.debug("Load queque")
    l.debug(args)
    if 'id' not in args:
        l.error("Id for queque not found")
        return 1
        
    q = sql3.entity.Queque(db.getConnection())
    q.fetch(args['id'])
    
    if 'id' not in q.data:
        l.error("Queque does not exists")
        return 2 
        
    u = cmailer.load(q.get('path'))
    
    acc = sql3.entity.EmailAccount(db.getConnection())
    acc.data = acc.fetchBy('email', u['from'])
    
    if 'id' not in acc.data:
        l.error("Unable to find email %s" % u['from'])
    try :
        cmailer.sendEmail(u, acc, q)
    except Exception, e:
        l.error("Error in queque")
        l.error(str(e))
    
def list(db, args, **kwargs):
    l.debug("List queques")
    q = sql3.entity.Queque(db.getConnection())
    
    if 'failed' in args:
        for i in q.allFailed():
            print i
        return 
        
    if 'done' in args:
        for i in q.allDone():
            print i
        return 
        
    if 'waiting' in args:
        for i in q.allWaiting():
            print i
        return 
        
    for i in q.all():
        print i
    
