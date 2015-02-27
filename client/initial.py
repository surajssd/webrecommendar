import os
import platform

import config
import file_operations
import logs
import upload_file

FF_FILE = config.FF_FILE
URL = config.URL


def concat_links(folder_list):
    """ Input is list of folders that form a path
        concat them to form the path and return this
    """
    path = ''
    for folder in folder_list:
        path = os.path.join(path, folder)
    return path

def firefox_dir_find(path):
    """ Inputs the partial path to firefox history file folder returns
        complete path.
        Firefox puts all its data into a folder that has some 
        random name and it ends with .default. On the other hand 
        chrome puts all its data in a fixed folder location.
    """
    dir_list = os.listdir(path)
    
    default_folder = ''
    for folder in dir_list:
        if '.default' in folder:
            default_folder = folder
            break
    return os.path.join(path, default_folder, FF_FILE)

def expand_links(browsers_static_info):
    """ Input dict of browser : path
        Returns expanded paths dict as browser : expanded_paths
        Initially the history files of respective browser is stored
        statically but the links are relative to home folder so these 
        links need to be expanded.
    """
    browsers_path = {}
    # returns the home folder path
    home = os.path.expanduser('~')    
    for browser in browsers_static_info:        
        path = concat_links(browsers_static_info[browser])
        complete_path = os.path.join(home, path)
        # if browser is not installed
        if not os.path.exists(complete_path):
            continue

        if browser == 'firefox':
            complete_path = firefox_dir_find(complete_path)
        browsers_path[browser] = complete_path

    return browsers_path


def format_browsers_info(browsers_path):
    """ Formats the input for data to be used later
        input is path of browser's history file
        returns a formatted 'dict' of 'list'
        'dict' is in following format
        browser_name : [file_location, timestamp]
    """    
    browsers_info = {}
    # check if firefox, chrome has its history file in place
    for browser in browsers_path:
        if os.path.exists(browsers_path[browser]):
            browsers_info[browser] = [browsers_path[browser], 0]
    return browsers_info
    

def static_data():
    """ Fetches user ID from the web server. And stores this id and url
        in a file.
    """
    user_id = upload_file.get_usr_id(URL)
    usr_id = int(user_id)

    logs.info('User ID assigned: {}'.format(usr_id))
    # specially written function just to handle this write operation
    file_operations.write_static_data(usr_id, URL)


def main():

    browsers_static_info = {
    'windows-7' : {'firefox' : ['AppData','Roaming','Mozilla','Firefox','Profiles'],
                    'chrome' : ['AppData','Local','Google','Chrome','User Data','Default','History']},

    'linux'     : {'firefox' : ['.mozilla','firefox'],
                    'chrome' : ['.config','google-chrome','Default','History']},

    'windows-xp': {'firefox' : ['Application Data','Mozilla','Firefox','Profiles'],
                    'chrome' : ['Local Settings','Application Data','Google','Chrome','User Data','Default','Preferences']}

    }
    file_operations.initial_setup()
    os_name = platform.platform().lower()
    if 'linux' in os_name:
        # this is linux
        browsers_path = expand_links(browsers_static_info['linux'])
    elif 'windows-7' in os_name or 'windows-8' in os_name:
        # this is windows 7 or 8
        browsers_path = expand_links(browsers_static_info['windows-7'])
    elif 'windows-xp' in os_name:
        # this is windows xp
        browsers_path = expand_links(browsers_static_info['windows-xp'])

    browsers_info = format_browsers_info(browsers_path)
    file_operations.write_browsers_info(browsers_info)
    static_data()
    logs.info('All initial configuration done.')

if __name__ == '__main__':
    main()