import custom_lib.db.sqllite3 as sql3

class Validator():
    def __init__(self, json):
        self.data = json;
        #self.server = server
        
    def doCheck(self):
        self.checkMainFields()
        self.checkRecievers()
        self.checkText()
        self.checkAttachements()
        
    def checkMainFields(self):
        required = [ 'recieve', 'from', 'subject', 'body' ]
        
        for i in required:
            if i not in self.data:
                raise Exception("Field %s is missing")
        
    def checkRecievers(self):
        self.__checkReciever('to')
        if 'cc' in self.data:
            self.__checkReciever('cc')
        
        if 'bcc' in self.data:
            self.__checkReciever('bcc')
            
    def checkFrom(self):
        if not isinstance(self.data['from'], (str, unicode)):
            raise Exception("From must be string, email")

    def checkText(self):
        if not isinstance(self.data['subject'], (str, unicode)):
            raise Exception("Subject must be string")

        if self.data['subject'].strip() == "":
            raise Exception("Subject must be non empty")
            
        if not isinstance(self.data['body'], (str, unicode)):
            raise Exception("Body must be text")

        if self.data['body'].strip() == '':
            raise Exception("Body must be non empty")
            
    def checkAttachements(self):
        if 'attach' in self.data:
            if not isinstance(self.data['attach'], list):
                raise Exception("Attachements must be added as list")
                
            attachCnt = 0
            for i in self.data['attach']:
                if 'name' not in i:
                    raise Exception("Error in Attachement %d , name not found" % attachCnt)
                    
                if 'content' not in i:
                    raise Exception("Error in Attachement %d , content not found" % attachCnt)
                    
                if (not isinstance(i['name'], (str, unicode))) or(i['name'].strip() == ''):
                    raise Exception("Name of attachement must be nonempty string")
                    
                if (not isinstance(i['content'], (str, unicode))) or(i['content'].strip() == ''):
                    raise Exception("Content of attachement must be nonempty string")
                    
                attachCnt += 1

    def __checkReciever(self, field):
        if field not in self.data['recieve']:
            raise Exception("%s is missing" % field)
        
        if not isinstance(self.data['recieve'][field], list):
            raise Exception("%s must be list" % field)
        
        for to in self.data['recieve'][field]:
            self.__validateReciever(to)
    
    def __validateReciever(self, data):
        if 'email' not in data:
            raise Exception("Reciever email is missing")
        
        #if 'name' not in data:
            #raise Exception("Reciever name is missing")

        
