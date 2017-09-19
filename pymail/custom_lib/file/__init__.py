from datetime import date
import uuid
import os
import custom_lib.log as l

class FileManager():
    def __init__(self, location, server):
        self.current = date.today().strftime("%Y_%m_%d")
        self.server = server
        self.location = location
        self.__check_dir__()

    def get_server_location(self):
        return "%s/%s" % (self.location, self.server.get('id'))

    def __check_dir__(self):
        if not os.path.exists(self.get_server_location()):
            os.makedirs(self.get_server_location())
            if not os.path.isdir(self.get_server_location()):
                raise Exception("Unable to create %s" %self.get_server_location())

    def flush_to_file(self, data):
        unique_filename = "%s.json" % str(uuid.uuid4())
        
        file_loc = "%s/%s" % (self.get_server_location(), unique_filename)
        l.debug("flush to file %s" %file_loc)
        
        with open(file_loc, "w") as f:
            f.write(data)
        
        return file_loc
        
