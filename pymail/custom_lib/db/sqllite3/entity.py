import custom_lib.log as l

class Entity():
    def __init__(self, con):
        self.con = con;
        self.data = {}

    def get_table_name(self):
        return 'table';

    def set(self, name, val):
        self.data[name]=val;


    def get(self, name):
        if name in self.data:
            return self.data[name]
        return None
        
    def getdata(self):
        return self.data
        
    def getLastInsertId(self):
        c = self.con.cursor()
        l.debug("SELECT last_insert_rowid() as id")
        c.execute("SELECT last_insert_rowid() as id")
        u = c.fetchone()
        c.close()
        return u['id'] if 'id' in u else None

    def fetchBy(self, name, val):
        c = self.con.cursor()
        l.debug("SELECT * FROM %s WHERE %s = ?" % (self.get_table_name(), name))
        l.debug("%s = %s" % (name, val))
        c.execute("SELECT * FROM %s WHERE %s = ?" % (self.get_table_name(), name), (val,))
        u= c.fetchone()
        if u is None:
            u = {}
        c.close();
        return u

    def fetch(self, _id):
        self.data = self.fetchBy('id', _id)
        return self.data
        
    def delete(self, id=None):
        if id is None:
            id = self.get('id')
        c = self.con.cursor()
        l.debug("DELETE FROM %s WHERE id = %d" % (self.get_table_name(), int(id)))
        l.debug("id = %d" % int(id))
        c.execute("DELETE FROM %s WHERE id = %d" % (self.get_table_name(), int(id)))
        self.data = c.fetchone()
        c.close();
        self.con.commit()
        return self.data
        
    def update(self):
        q = "UPDATE %s SET " % self.get_table_name()
        up = ""
        param = ()
        for name, value in self.data.items():
            up = "%s, %s = ?" % (up, name)
            param = param + (value,)
        
        param = param + (self.data['id'],)
        c = self.con.cursor()
        #debug
        l.debug("%s %s WHERE id = ?" % (q, up[2:]))
        l.debug(str(param))
        c.execute("%s %s WHERE id = ?" % (q, up[2:]), param)
        self.con.commit()
        c.close();
        
    def save(self):
        q = "INSERT INTO %s " % self.get_table_name()
        param = ()
        columns = ""
        values = ""
        for name, value in self.data.items():
            columns = "%s, %s" % (columns, name)
            values = "%s, ?" % values
            param = param + (value,)

        c = self.con.cursor()
        l.debug("%s (%s) VALUES (%s)" % (q, columns[2:], values[2:]))
        l.debug(str(param))
        c.execute("%s (%s) VALUES (%s)" % (q, columns[2:], values[2:]), param)
        self.con.commit()
        c.close();

    def all(self):
        c = self.con.cursor()
        c.execute("SELECT * FROM %s" % self.get_table_name())
        return c.fetchall()


class User(Entity):
    def get_table_name(self):
        return 'users';
        
    def getServers(self):
        c = super().con.cursor()
        c.execute("SELECT server_id FROM %s WHERE user_id = ?" % 'user_to_server', (self.get('id')))
        servers = []
        
        for i in c.fetchall():
            servers.append(i['server_id'])
        
        c.close();
        return servers
        
    def fetchByUsername(self, username):
        self.data = self.fetchBy('username', username)
        return self
        
        
class Server(Entity):
    def get_table_name(self):
        return 'servers';
        
    def getUsers(self):
        c = self.con.cursor()
        l.debug("SELECT user_id FROM %s WHERE server_id = ? " % 'user_to_server')
        l.debug(str(self.get('id')))
        c.execute("SELECT user_id FROM %s WHERE server_id = ? " % 'user_to_server', str(self.get('id')))
        users = []
        
        for i in c.fetchall():
            users.append(i['user_id'])
        c.close();
        return users
        
    def getEmailAccounts(self):
        c = self.con.cursor()
        l.debug("SELECT email_id FROM %s WHERE server_id = ? " % 'email_to_server')
        l.debug(str(self.get('id')))
        c.execute("SELECT email_id FROM %s WHERE server_id = ? " % 'email_to_server', str(self.get('id')))
        users = []
        
        for i in c.fetchall():
            users.append(i['email_id'])
        c.close();
        return users
        
    def addUser(self, user):
        c = self.con.cursor()
        l.debug("INSERT INTO %s (user_id, server_id) VALUES ( ?, ?) " % 'user_to_server')
        l.debug([str(user), str(self.get('id'))])
        c.execute("INSERT INTO %s (user_id, server_id) VALUES ( ?, ?) " % 'user_to_server', (str(user), str(self.get('id'))))
        self.con.commit()
        c.close();
        
    def addEmailAccount(self, email):
        c = self.con.cursor()
        l.debug("INSERT INTO %s (email_id, server_id) VALUES ( ?, ?) " % 'email_to_server')
        l.debug([str(email), str(self.get('id'))])
        c.execute("INSERT INTO %s (email_id, server_id) VALUES ( ?, ?) " % 'email_to_server', (str(email), str(self.get('id'))))
        self.con.commit()
        c.close();
        
    def removeUser(self, user):
        c = self.con.cursor()
        l.debug("DELETE FROM %s WHERE user_id = ? AND server_id = ? " % 'user_to_server')
        l.debug([str(user), str(self.get('id'))])
        c.execute("DELETE FROM %s WHERE user_id = ? AND server_id = ? " % 'user_to_server', (str(user), str(self.get('id'))))
        self.con.commit()
        c.close();
        
    def removeEmailAccount(self, email):
        c = self.con.cursor()
        l.debug("DELETE FROM %s WHERE email_id = ? AND server_id = ? " % 'email_to_server')
        l.debug([str(email), str(self.get('id'))])
        c.execute("DELETE FROM %s WHERE email_id = ? AND server_id = ? " % 'email_to_server', (str(email), str(self.get('id'))))
        self.con.commit()
        c.close();
        

class EmailAccount(Entity):
    def get_table_name(self):
        return 'email_accounts';
        
class Queque(Entity):
    def get_table_name(self):
        return 'queque';
        
    def allWaiting(self):
        c = self.con.cursor();
        l.debug("SELECT * FROM %s WHERE error IS NULL AND done IS NULL" % self.get_table_name())
        c.execute("SELECT * FROM %s WHERE error IS NULL AND done IS NULL" % self.get_table_name())
        
        return c.fetchall() 
    
    def allWaitingWithLimit(self, limit=10):
        c = self.con.cursor();
        if not isinstance(limit, int):
            raise Exception("Limit must be integer")
        l.debug("SELECT * FROM %s WHERE error IS NULL AND done IS NULL LIMIT %d" % (self.get_table_name(), limit))
        c.execute("SELECT * FROM %s WHERE error IS NULL AND done IS NULL LIMIT %d" % (self.get_table_name(), limit))
        
        return c.fetchall() 
        
    def allFailed(self):
        c = self.con.cursor();
        l.debug("SELECT * FROM %s WHERE error IS NOT NULL AND done IS NULL" % self.get_table_name())
        c.execute("SELECT * FROM %s WHERE error IS NOT NULL AND done IS NULL" % self.get_table_name())
        return c.fetchall() 
        
    def allDone(self):
        c = self.con.cursor();
        l.debug("SELECT * FROM %s WHERE done IS NOT NULL" % self.get_table_name())
        c.execute("SELECT * FROM %s WHERE done IS NOT NULL" % self.get_table_name())
        return c.fetchall() 
    
    
        
        
