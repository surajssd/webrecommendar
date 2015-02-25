import os

import file_operations

def main():
    file_operations.make_data_folder()
    file_operations.make_db()
    file_operations.make_usr_id_file()

if __name__ == '__main__':
    main()
