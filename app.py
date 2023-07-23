from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import requests
from openpyxl import load_workbook
import os
from dotenv import load_dotenv
import logging
from tqdm import tqdm

load_dotenv()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Setup logging
logging.basicConfig(level=logging.INFO, filename='trello_log.log', format='%(asctime)s %(levelname)s:%(message)s')

# Get the environment variables
api_key = os.getenv("TRELLO_API_KEY")
token = os.getenv("TRELLO_TOKEN")
base_url = "https://api.trello.com/1"
username = os.getenv("USERNAME")
board_name = os.getenv("BOARD_NAME")
list_name = os.getenv("LIST_NAME")

# Verify the mandatory environment variables
mandatory_env_vars = ["TRELLO_API_KEY", "TRELLO_TOKEN", "USERNAME", "BOARD_NAME", "LIST_NAME"]
for var in mandatory_env_vars:
    if not os.getenv(var):
        logging.error(f'Missing mandatory environment variable {var}')
        exit(1)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            skiptraced = request.form.get('skiptraced', 'no')
            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), skiptraced)  # Call your Trello processing function
            return 'File uploaded and processed'
        else:
            return 'Invalid file type. Please upload a .xlsx file.'
    return '''
<!doctype html>
<html>
<head>
<title>Upload new File</title>
<style>
    /* ... existing styles ... */
    .spinner {
        display: none;
        width: 40px;
        height: 40px;
        margin: 100px auto;
        background-color: #333;

        border-radius: 100%;  
        animation: spin 1s infinite ease-in-out;
    }

    @keyframes spin {
        0% { transform: scale(0); }
        100% { transform: scale(1.0); opacity: 0; }
    }
</style>
</head>
<body>
<div class="container">
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data onsubmit="showSpinner()">
      <input type=file name=file>
      <label for="skiptraced"><input type=checkbox id="skiptraced" name=skiptraced> Skiptraced</label>
      <input type=submit value=Upload>
    </form>
    <div class="spinner"></div>
    <div class="email">Reach out! <a href="mailto:bbaker@aresinvestments.org">bbaker@aresinvestments.org</a></div>
</div>
<script>
    function showSpinner() {
        document.querySelector('.spinner').style.display = 'block';
    }
</script>
</body>
</html>
    '''

def process_file(file_path, skiptraced):
    try:
        # Excel files
        excel_files = [file_path]

        board_id = get_board_id(username, board_name)
        list_id = get_list_id(board_id, list_name)

        if not board_id or not list_id:
            print("Exiting due to previous errors.")
            exit()

        # Card to Trello
        for file_name in excel_files:
            try:
                df = pd.read_excel(file_name)
            except FileNotFoundError:
                print(f"The file '{file_name}' was not found. Please check the file path and name.")
                continue

            progress_bar = tqdm(total=df.shape[0], ncols=70, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')

            for index, row in df.iterrows():
                progress_bar.update() 
                if skiptraced == 'on':
                    name = f"{row['First Name']} - {row['Street Address']}"
                    
                    desc = f"First Name: {row['First Name']}\nLast Name: {row['Last Name']}\nLandline: {row['Landline']}\nCell: {row['Cell']}\nCell 2: {row['Cell 2']}\nPhone: {row['Phone']}\nPhone 2: {row['Phone 2']}\nEmail 1: {row['Email 1']}"

                    idLabels = [
                        create_label(row['State'], 'sky', board_id),
                        create_label(row['City'], 'sky', board_id)
                    ]
                else:
                    name = f"{row['Owner 1 First Name']} - {row['Address']}"
                    desc = f"Owner 1 First Name: {row['Owner 1 First Name']}\nOwner 1 Last Name: {row['Owner 1 Last Name']}\nBuilding Sqft: {row['Building Sqft']}\nBedrooms: {row['Bedrooms']}\nTotal Bathrooms: {row['Total Bathrooms']}\nEst. Value: {row['Est. Value']}\nMailing Address: {row['Mailing Address']}"
                    idLabels = [
                        create_label(row['State'], 'sky', board_id),
                        create_label(row['City'], 'sky', board_id)
                    ]

                create_card(name, desc, list_id, idLabels)

            progress_bar.close()

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")


def get_board_id(username, board_name):
    try:
        response = requests.get(f"{base_url}/members/{username}/boards?key={api_key}&token={token}")
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return None

    boards = response.json()
    for board in boards:
        if board['name'] == board_name:
            return board['id']
    print("Board not found")
    return None

def get_list_id(board_id, list_name):
    try:
        response = requests.get(f"{base_url}/boards/{board_id}/lists?key={api_key}&token={token}")
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return None

    lists = response.json()
    for list_ in lists:
        if list_['name'] == list_name:
            return list_['id']
    print("List not found")
    return None

def create_card(name, desc, idList, idLabels):
    url = f"{base_url}/cards"
    query = {
        'key': api_key,
        'token': token,
        'name': name,
        'desc': desc,
        'idList': idList,
        'idLabels': idLabels
    }

    try:
        response = requests.request("POST", url, params=query)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return

    print(f'Card created: {response.text}')

def create_label(name, color, idBoard):
    url = f"{base_url}/labels"
    query = {
        'key': api_key,
        'token': token,
        'name': name,
        'color': color,
        'idBoard': idBoard
    }

    try:
        response = requests.request("POST", url, params=query)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return None

    return response.json()['id']

if __name__ == '__main__':
    app.run(port=3063)
