import os
import time

import config
import file_operations

FILE_NAME = config.FILE_NAME
DEBUGMODE = config.DEBUGMODE

def info(string):
    """ Input a message as string and this function prints this
        sent msg along with timestamp of machine
    """
    timestamp = time.asctime()

    data_file_path = os.path.join(file_operations.FILE_FOLDER, 
                                  FILE_NAME)
    file_name = open(data_file_path,'a') 
    msg = '{} : {}\n'.format(timestamp, string)
    if DEBUGMODE:
        print msg
    file_name.write(msg)
    file_name.close()

def init():
    """ This is just so if the file already exists then just over-write it
        and create new file.
    """
    data_file_path = os.path.join(file_operations.FILE_FOLDER, 
                                  FILE_NAME)
    f = open(data_file_path, 'w')
    f.close()
