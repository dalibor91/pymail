import connection as connection 
import entity as entity


def create_tables(db):
    c = connection.Connection(db)
    if c.exists():
        return False
    
    _c = c.getConnection()
    _cur = _c.cursor()
    
    import create
    
    for i in create.tables:
        _cur.execute(i)
        
    _c.commit()
