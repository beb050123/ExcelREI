# Excel-to-Trello

Excel-to-Trello is a local host server application that allows users to select Excel files from their local system, process them, and create corresponding cards on Trello.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your local system:

- Python 3.x
- Flask
- pandas
- requests
- openpyxl
- python-dotenv

### Installing

Follow these steps to get the app running on your local system:

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/excel-to-trello.git
    ```

2. **Change into the directory**

    ```bash
    cd excel-to-trello
    ```

3. **Install the requirements**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set your environment variables in a `.env` file**

    Set your Trello API Key, Token, Username, Board Name, and List Name as environment variables in a `.env` file at the root of your project directory.

### Running the Application

To run the application on your local machine, use the command:

```bash
python app.py
```
This will start a local Flask server, which you can access via localhost:5000 on your web browser.

