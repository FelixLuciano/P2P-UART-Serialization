import time

class Log:
    def __init__ (self, filename):
        self.filename = filename


    def clear(self):
        with open(self.filename, 'w', encoding='utf-8') as logfile:
            logfile.write('')


    def write (self, message:str):
        data = time.strftime(f'%d/%m/%Y %H:%M:%S: {message}')

        with open(self.filename, 'rw', encoding='utf-8') as logfile:
            logfile.write(data)
