import os
from datetime import datetime

class Logger(object):
    LOG_FILE_TEMPLATE = '%s.log'
    LOG_TEMPLATE = '{"component": "%s", "section": "%s", "timestamp": "%s", "message": "%s"}'
    
    def __init__(self, component):
        self.component = component
        self.log_file = self.LOG_FILE_TEMPLATE % component
    
    def log(self, section, message):
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
        log = self.LOG_TEMPLATE % (self.component, section, time, message)
        with open(self.log_file, 'aw') as f:
            f.write(log.replace('\n', '') + '\n')
