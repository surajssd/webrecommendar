import csv
import os
import random
import sqlite3

import config
import file_operations
import upload_file
import logs

FILE_SIZE = config.FILE_SIZE

def table_info(browser_name):
    """ Takes browser info and returns list in following format
        URL_column, Timestamp, Table_name
        
        History table storage varies from browser to browser naming of 
        table names and column names may vary. This function helps by 
        returning related information.
    """            
    info = {'firefox' : ['url', 'last_visit_date', 'moz_places'],
            'chrome' : ['url', 'last_visit_time', 'urls',]
    }
    return info[browser_name]

def check_logs_file():
    """ Checks if the file size has exceeded 512kB. If so upload the file,
        delete it and then create new one.
    """
    file_name = logs.FILE_NAME
    size = file_operations.get_file_size(file_name)

    if size > FILE_SIZE:
        if upload_file.upload(file_name):
            file_operations.delete_file(file_name)
            # this will create logs file afresh file once again
            logs.init()


def import_data_history(browser_name, file_location, old_timestamp):
    """ This import new data in history from history file and makes a csv file
        which then can be uploaded.
    """
    data_fetched = False
    file_name = None
    try:
        conn_native = sqlite3.connect(file_location)
        # this helps in addressing columns using their name
        conn_native.row_factory = sqlite3.Row
        cursor_read = conn_native.cursor()
        # each browser has different table_names and column_names
        url_col, timestamp_col, table_name = table_info(browser_name)
        # read from the database
        cursor_read.execute('select %s, %s from %s where %s > %d' % (url_col,
                    timestamp_col, table_name, timestamp_col, old_timestamp))
        # create a .csv with random number
        num = random.randint(1, 999999)
        file_name = str(num) + ".csv"
        file_data_path = os.path.join(file_operations.FILE_FOLDER,
                                    file_name)
        f = open(file_data_path, 'w')
        writer = csv.writer(f)
        # writing the data to csv file        
        for rec in cursor_read:
            writer.writerow([rec[url_col], rec[timestamp_col]])
            data_fetched = True
        conn_native.close()
    except sqlite3.OperationalError as e:
        error = 'Error: Cannot open history database: ' + str(e)
        logs.info(error)

    # if there is data then only update the last time stamp else dont do that
    if data_fetched == True:
        new_time_stamp = int(rec[timestamp_col])
        return file_name, new_time_stamp
    else:
        # this is because even if no new data is generated the file is being 
        # generated so its just empty file delete it
        if file_name != None:
            file_operations.delete_file(file_name)
        return None, None


def main():
    
    check_logs_file()
    # in windows it is unable to delete the csv files immediately.
    file_operations.delete_csvs()
    browsers_info = file_operations.fetch_browsers_info()

    for browser_name, value in browsers_info.iteritems():
        file_location, timestamp = value
        file_name, new_timestamp = import_data_history(browser_name,
                                             file_location, timestamp)        
        # if we got both file_name and new_time_stamp as Not None
        # then upload file
        if file_name != None and new_timestamp != None:
            if upload_file.upload(file_name):
                # update timestamp and delete files only if upload is
                # successful
                file_operations.update_timestamp(browser_name, new_timestamp)
            file_operations.delete_file(file_name)
    logs.info('Periodic check done.')


if __name__ == '__main__':
    main()