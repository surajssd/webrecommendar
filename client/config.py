##############################################################
# initial
URL = 'http://webrecommendar.pythonanywhere.com'
#URL = 'http://192.168.230.1:5000'
#URL = 'http://172.16.59.1:5000'
#URL = 'http://127.0.0.1:5000'
FF_FILE = 'places.sqlite'

##############################################################
# __init__
# this is interval of periodic history checking in seconds
INTERVAL = 7200

##############################################################
# logs
FILE_NAME = 'event_logs.log'
DEBUGMODE = True

##############################################################
# periodic
FILE_SIZE = 524288

##############################################################
# upload
# if user id not received wait for this time interval
USER_ID_INTERVAL = 30

##############################################################
# file_operations
FILE_FOLDER = 'data'
DATA_FILE_NAME = 'data.txt'
STATIC_FILE_NAME = 'static.txt'