
tables = [
    '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT NOT NULL, 
        password TEXT NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''', 
    'CREATE UNIQUE INDEX username_idx ON users(username);',
    ''' 
    CREATE TABLE servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        port TEXT NOT NULL, 
        ip TEXT NOT NULL,
        pid INTEGER DEFAULT "0",
        auth INTEGER DEFAULT "0",
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''', 
    'CREATE UNIQUE INDEX ip_port_idx ON servers(ip, port);',
    '''
    CREATE TABLE user_to_server (
        user_id INTEGER NOT NULL, 
        server_id INTEGER NOT NULL
    );
    ''',
    'CREATE UNIQUE INDEX user_server_idx ON user_to_server(user_id, server_id)',
    '''
    CREATE TABLE email_to_server (
        server_id INTEGER NOT NULL, 
        email_id INTEGER NOT NULL
    );
    ''',
    'CREATE UNIQUE INDEX email_server_idx ON email_to_server(server_id, email_id)',
    ''' 
    CREATE TABLE email_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email TEXT NOT NULL, 
        name TEXT, 
        username TEXT NOT NULL, 
        password TEXT NOT NULL, 
        host TEXT NOT NULL, 
        port INTEGER NOT NULL, 
        ssl INTEGER DEFAULT "0",
        tls INTEGER DEFAULT "0", 
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''',
    'CREATE UNIQUE INDEX username_email_idx ON email_accounts(username)',
    '''
    CREATE TABLE queque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL, 
        error TEXT NULL,
        done DATETIME DEFAULT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''', 
    'CREATE UNIQUE INDEX path_idx ON queque(path)'
]
