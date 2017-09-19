import time
import flask
import json
import os
from functools import wraps
import custom_lib.log as l
import custom_lib.mailer as cmailer
import custom_lib.db.sqllite3 as sql3 
from custom_lib.file import FileManager


def run(server, database_file, storage_folder):
    
    _db = sql3.connection.Connection(database_file)
    _id = server.get('id')
    server = sql3.entity.Server(_db.getConnection())
    l.info("Fetch server by ID = %s " % str(_id))
    l.info(str(server.fetch(str(_id))))
    
    l.info("Host:  %s" % server.get('ip'))
    l.info("Port:  %s" % server.get('port'))
    l.info("User:  %s" % server.get('uid'))
    l.info("Group: %s" % server.get('gid'))
    
    app = flask.Flask("server-%s" % server.get('id'))
    appStorage = FileManager(storage_folder, server)
    
    def check_auth(username, password):            
        user = sql3.entity.User(_db.getConnection())
        user.fetchByUsername(username)

        if 'id' not in user.data:
            l.info("Auth. User %s not found" % username)
            return False
            
        u = server.getUsers()
        try:
            u.index(user.data['id'])
        except:
            l.info("Auth. User %s not allowed for server %s" %(user.get('id'), server.get('id')))
            return False;

        u = (username == user.get('username') and password == user.get('password'))
        
        if not u:
            l.info("Auth. User %s failed to login." % user.get('id'))
            
        return u

    def authenticate():
        """Sends a 401 response that enables basic auth"""
        return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = flask.request.authorization
            if (not auth or not check_auth(auth.username, auth.password)) and (server.get('auth') == 1):
                return authenticate()
            return f(*args, **kwargs)
        return decorated
    
    
    
    @app.route('/')
    @requires_auth
    def home():
        return """
        <pre>
Server %s running
        
IP:   %s
PORT: %s
PID:  %s
        </pre>
        """.strip() % (server.get('id'), server.get('ip'), server.get('port'), server.get('pid'))
        
    @app.route('/send', methods=['POST'])
    @requires_auth
    def send():
        l.debug("New email send request")
        u = flask.request.get_json(silent=True)
        
        validator = cmailer.validateJSON(u)
        
        quid = 0
        
        try:
            l.debug("validate check")
            validator.doCheck()
            
            f = appStorage.flush_to_file(json.dumps(u))
            
            q = sql3.entity.Queque(_db.getConnection())
            q.set('path', f)
            q.save()
            #print q.getLastInsertId()
            quid = int(q.getLastInsertId())
                        
        except Exception, e:
            return json.dumps({ "success": False, "msg": str(e) })
        
        return json.dumps({ "success": True, "msg": quid }) 
    
        
    @requires_auth
    def all():
        pass;
        
    try:
        l.info("Starting new instance of server ID = %s " % server.get('id'))
        server.set('pid', os.getpid())
        server.update()
        app.run(threaded=False, host=server.get('ip'), port=server.get('port'))
    except Exception:
        l.error("Error with server %s" % server.get('id'))
        raise


def stop(server):
    l.info("Stoping server instance...")
    l.info("ID:    %s" % server.get('id'))
    l.info("Host:  %s" % server.get('ip'))
    l.info("Port:  %s" % server.get('port'))
    l.info("User:  %s" % server.get('uid'))
    l.info("Group: %s" % server.get('gid'))
    l.info("Pid:   %s" % server.get('pid'))
    
    pid = int(server.get('pid'))
    
    if pid > 0:
        try:
            os.kill(pid, 0);
        except :
            l.error("Process %d does not exists" % pid)
            return False
            
        os.kill(pid, 9)
        server.set('pid', 0)
        server.update()
        return True
    else:
        l.warning("Service not runing")
    return False;
    

def restart(server, database_file):
    l.info("Restarting server instance...")
    l.info("ID:    %s" % server.get('id'))
    l.info("Host:  %s" % server.get('ip'))
    l.info("Port:  %s" % server.get('port'))
    l.info("User:  %s" % server.get('uid'))
    l.info("Group: %s" % server.get('gid'))
    pass 
