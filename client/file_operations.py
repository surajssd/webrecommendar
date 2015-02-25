import os
import pickle

import config
import logs

FILE_FOLDER = config.FILE_FOLDER
DATA_FILE_NAME = config.DATA_FILE_NAME
STATIC_FILE_NAME = config.STATIC_FILE_NAME


def write_browsers_info(browsers_info):
    """ Write the browser info to file
        Input is 'dict' of 'list'
        'dict' is in following format
        browser_name : [file_location, timestamp]
    """
    data_file_path = os.path.join(FILE_FOLDER, DATA_FILE_NAME)
    data_file = open(data_file_path, 'w')    
    # write that data structure to file
    pickle.dump(browsers_info, data_file)
    data_file.close()      
    logs.info('Writing browsers data to file {}'.format(data_file_path))


def fetch_browsers_info():    
    """ Reads data from file and returns 'dict' of 'list'
        'dict' is in following format
        browser_name : [file_location, timestamp]
    """
    data_file_path = os.path.join(FILE_FOLDER, DATA_FILE_NAME)
    data_file =  open(data_file_path,'r')
    browser_info = pickle.load(data_file)
    data_file.close()
    return browser_info
   
    
def update_timestamp(browser, new_timestamp):
    """ Updates the timestamp of browser
        takes in browser name and new timestamp
        makes necessary changes to the file
    """
    # read old data from file
    browsers_info = fetch_browsers_info()
    browsers_info[browser][1] = new_timestamp
    write_browsers_info(browsers_info)
    logs.info('Timestamp: {} updated for Browser: {}'.format(new_timestamp,
                                                                 browser))
                                                                 
def initial_setup():
    """ This makes folder required to keep all data files    
    """
    try:
        os.mkdir('data')
    except OSError as e:
        # folder data already exists this means maybe files init already
        # exists so we create the log file using below function
        logs.init()
        logs.info('Error:' + str(e))


def write_static_data(usr_id, url):
    """ Input User_ID and URL
        Write the User ID and url to static file
    """
    static_data = [usr_id, url]
    data_file_path = os.path.join(FILE_FOLDER, STATIC_FILE_NAME)
    file_name = open(data_file_path, 'w')
    pickle.dump(static_data, file_name)
    file_name.close()
    logs.info('Static File created at {}'.format(data_file_path))


def fetch_static_data():
    """ Return usr_id and URL that is statically changed
    """
    data_file_path = os.path.join(FILE_FOLDER, STATIC_FILE_NAME)
    file_name = open(data_file_path, 'r')
    usr_id, url = pickle.load(file_name)
    file_name.close()
    return usr_id, url


def delete_file(file_name):
    """ Input file name and delete the specified file from
        FILE_FOLDER specified
    """
    file_path = os.path.join(FILE_FOLDER, file_name)
    try:
        os.remove(file_path)
    except WindowsError as e:
        # file being accessed by somebody so cannot delete file
        # happens in windows usually
        error = 'Error: Cannot delete the file {}. '.format(file_path)
        logs.info(error + str(e))

def delete_csvs():
    """ This function deletes all the csv files in the ./data folder
    """
    files = os.listdir(FILE_FOLDER)    
    for file_name in files:
        if '.csv' in file_name:
            delete_file(file_name)

def get_file_size(file_name):
    """ Inputs name of file in ./data folder. Returns the size of
        file in bytes.
    """
    file_path = os.path.join(FILE_FOLDER, file_name)
    return os.stat(file_path).st_size