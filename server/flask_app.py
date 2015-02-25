from flask import Flask, request

import initial
import file_operations

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Webrecommendar. Download the app and get going!'


@app.route('/', methods=['GET', 'POST'])
def login():
    
    # if operation is of uploading file 
    operation = request.form['operation']

    if operation == 'upload_file':        
        # extract data from received request
        file_name = request.form['file_name']
        usr_id = request.form['user_id']        
        file_data = request.files['file_data']
        
        if file_name.endswith(".csv"):
            # save the file data to a file
            file_operations.save_file(file_data, file_name)
            # make an entry to db as who uploaded which file
            file_operations.add_to_db(usr_id, file_name)

        elif file_name.endswith(".log"):
            # this is for collecting logs
            file_operations.update_logs_file(file_data)

        return 'upload successful'

    # if the user requested for assigning USER id
    elif operation == 'assign_usr_id':
        return str(file_operations.assign_usr_id())


if __name__ == '__main__':
    initial.main()
    app.run(debug=True, host='0.0.0.0')
