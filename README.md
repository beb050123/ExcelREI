# Trello Bot for Creating Cards from Excel

This Python application reads data from an Excel file, scrubs the data, and creates Trello cards with specific labels based on specific columns in the Excel sheet.

## Prerequisites

1. Python 3.x 
2. pip (Python package manager)

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the following command to install the necessary Python packages:

    ```
    pip install -r requirements.txt
    ```

## Getting Trello API Key, Token, Board ID, and List ID

1. **API Key & Token**: Visit the [Trello API Key page](https://trello.com/app-key). Here, you will find your API key. Generate your token by clicking on the `Token` link on the page.

2. **Board ID**: Visit your Trello board in your web browser. The URL will be something like `https://trello.com/b/BOARD_ID/BOARD_NAME`. The `BOARD_ID` is what you need.

3. **List ID**: Use the [Trello API](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get) to get the list ID. Replace `BOARD_ID` in the following URL with your actual board ID, then visit it in your browser: `https://api.trello.com/1/boards/BOARD_ID/lists?fields=name&key=YOUR_API_KEY&token=YOUR_TOKEN`.

## Running the Script

1. Store your API key and token in a `.env` file in the project directory as follows:

    ```
    TRELLO_API_KEY=your_api_key
    TRELLO_TOKEN=your_token
    ```

    Replace `your_api_key` and `your_token` with your actual API key and token.

2. Replace the placeholders in the `trello_bot.py` script with your actual board and list IDs.

3. Run the Python script:

    ```
    python trello_bot.py
    ```

## Support

For any questions or support, please contact me at [bbaker@aresinvestments.org](mailto:bbaker@aresinvestments.org).
