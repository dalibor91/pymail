import validator
import os
import json

def validateJSON(_json):
    return validator.Validator(_json)

def load(f):
    if not os.path.isfile(f):
        raise Exception("File not found")
    
    data = None
    with open(f) as df:
        try:
            data = json.load(df)
        except:
            data = None
            
    if data is None:
        raise Exception("Unable to load json")

    validateJSON(data)
    
    return data
    
def sendEmail(data, acc, queque):
    from .mailer import sendEmail 
    
    return sendEmail(data, acc, queque)
        
    
    
    
    
    
    
    
    
