import csv
import io
import os
import pickle


FILE_FOLDER = 'data'
APPLICATION = 'webapp'
DB_FILE = 'db.csv'
ASSIGN_USR_ID = 'usr.txt'
USERS_LOGS = "user_logs.txt"

def make_data_folder():
    if not os.path.exists(FILE_FOLDER):
        os.mkdir(FILE_FOLDER)


def make_db():
    if not os.path.exists(DB_FILE):
        db_file = open(DB_FILE, 'w')


def add_to_db(usr_id, file_name):
    # Make an entry in database of which user uploaded what file    
    db_file = open(DB_FILE, 'a')
    db_writer = csv.writer(db_file)
    db_writer.writerow([usr_id, file_name])
    db_file.close()


def save_file(file_data, file_name):
    # save the file uploaded 
    file_path = os.path.join(FILE_FOLDER, file_name)
    file_data.save(file_path)

def update_logs_file(file_data):
    # save the uploaded logs file into existing logs file
    file_path = os.path.join(FILE_FOLDER, USERS_LOGS)
    
    f = open(file_path, 'a')
    f.write(file_data.read())
    f.close()


def make_usr_id_file():
    if not os.path.exists(ASSIGN_USR_ID):
        usr_file = open(ASSIGN_USR_ID, 'w')
        usr_id = 1
        pickle.dump(usr_id, usr_file)
        usr_file.close()


def assign_usr_id():
    
    # read the user id saved in advance 
    # and then increment and save the user id to file
    read_usr_file = open(ASSIGN_USR_ID, 'r')
    usr_id = pickle.load(read_usr_file)
    read_usr_file.close()
    
    #import pdb; pdb.set_trace()
    write_usr_file = open(ASSIGN_USR_ID, 'w')
    pickle.dump(usr_id + 1, write_usr_file)
    write_usr_file.close()
    return usr_id
