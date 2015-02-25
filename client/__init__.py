import os
import sys
import time

import config
import initial
import logs
import periodic
import file_operations


INTERVAL = config.INTERVAL  # this is interval of periodic history checking in seconds

    

def is_first_time():
    """ If any of required file doesnt exist, this means this is our first 
        time to execute
    """
    FILE_FOLDER = file_operations.FILE_FOLDER        
    if not os.path.exists(FILE_FOLDER):
        return True
    DATA_FILE_NAME = file_operations.DATA_FILE_NAME
    DATA_FILE_NAME = os.path.join(FILE_FOLDER, DATA_FILE_NAME)
    if not os.path.exists(DATA_FILE_NAME):
        return True
    STATIC_FILE_NAME = file_operations.STATIC_FILE_NAME
    STATIC_FILE_NAME = os.path.join(FILE_FOLDER, STATIC_FILE_NAME)
    if not os.path.exists(STATIC_FILE_NAME):
        return True
    # all of them exists so this is not our first time
    return False

def main():
    
    # this is try so that any uncaught exception will be caught here
    try:
        # check if this is our first time of run?
        if is_first_time():
            # do all the initial setup
            initial.main()
    
        while True:
            periodic.main()
            time.sleep(INTERVAL)
    except Exception as e:
        logs.info('Error: UNEXPECTED ERROR CAUGHT. '+ str(e))
    

if __name__ == '__main__':
    main()