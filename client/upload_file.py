import os
import requests
import sys
import time

import config
import file_operations
import logs

USER_ID_INTERVAL = config.USER_ID_INTERVAL   # if user id not received wait for this time interval


def upload(file_name):
    """ Input a file name. Upload the file to webserver from the ./data
        directory.
    """    
    file_path = os.path.join(file_operations.FILE_FOLDER, file_name)
    user_id, url = file_operations.fetch_static_data()
    
    #print 'User_ID: {}, URL: {}'.format(user_id, url)

    data = {    'file_name' : file_name,
                'user_id' : user_id,
                'operation' : 'upload_file'
         }
    files = {'file_data': open(file_path, 'rb')}
    try:
        reply = requests.post(url, data, json=None, files=files)

        if reply.text == 'upload successful':
            logs.info('Uploaded file: {}'.format(file_name))
            return True
    except requests.exceptions.ConnectionError as e:
        error = 'Error: Cannot upload file: ' + file_name + ' ' + str(e)
        logs.info(error)
        return False


def get_usr_id(url):
    """ Fetch user id from the server and return this value.
    """
    data = {'operation' : 'assign_usr_id'}
    
    while True:
        try:
            usr_id = requests.post(url, data)
        except IOError as e:
            error = "Error: Couldn't connect to web-server to fetch User-ID. " 
            logs.info(error + str(e))
        else:
            return usr_id.text
        time.sleep(USER_ID_INTERVAL)
