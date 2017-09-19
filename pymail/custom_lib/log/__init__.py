import config.main as config


def debug(s):
    if not config.config['messages']['DEBUG']:
        return None
    print "[  DEBUG  ] %s" % s
    
def warning(s):
    if not config.config['messages']['WARNING']:
        return None
    print "[ WARNING ] %s" % s
    
def info(s):
    if not config.config['messages']['INFO']:
        return None
    print "[  INFO   ] %s" % s

def error(s):
    if not config.config['messages']['ERROR']:
        return None
    print "[  ERROR  ] %s" % s
