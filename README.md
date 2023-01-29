# QuadLingo Dictionary

## Overview
![QuadLingo Home Page](screenshot.png)

View Demo: https://dictionary-data-api.onrender.com

QuadLingo is a user-friendly tool for searching slangs and their meanings in English, Deutsch, Mandarin and Tagalog.
This app serves as a basic application of the Flask Framework using Google Sheets as its source of information and easy deployment on Render. Google Sheets as a database offers non-developers a simple, accessible, and cost-effective solution for storing and managing non-sensitive data. For a Flask setup that will process sensitive data, [view this project instead](https://github.com/kayesokua/flask-store-dummy).

## Package Requirements
1. `Flask` provides a simple and flexible way to build web applications. Without Flask, you would have to write low-level code to handle HTTP requests, handle routing, and handle templates, among other things.
2. `gTTS` generates text-to-speech using Google Translate
3. `gunicorn` is a production-ready HTTP server for Python web applications. Flask, by itself, is not designed to be used in production and is only meant to be used for development purposes.
4. `jsons`  to parse the data received from the Google Sheets API
5. `urllib3`makes an HTTP request to the Google Sheets API

## Run the Application on Local Environment
1. Clone repository `git clone https://github.com/kayesokua/flask-dictionary flask-dir`
2. Go to the new directory`cd flask-dir`
3. Install required modules `pip3 install -r -requirements.txt`
4. Run the application `flask run`

## How to Use

### Get API JSON
*  `https://dictionary-data-api.onrender.com/api/json/` to to get all items in the dictionary
*  `https://dictionary-data-api.onrender.com/api/json/<int>` to get 1 item detail

### Modify Dictionary
Currently the app does not have a single page to configure the contents of the dictionary, but here is the list of instructions on how you can modify the content.

1. Create a new spreadsheet using Google Sheets. The columns represent the key names and the rows will be the dictionary's items. [Follow this format](https://docs.google.com/spreadsheets/d/1b-ri2DlWLIhqB-E8xUCqnh9fsxJJ5J-KGV52rJ250Dk/edit#gid=81166623)

2. Publish the spreadsheet to the web and get the generated end point `https://spreadsheets.google.com/feeds/cells/<your_google_sheet_code>/<sheet_page_no>/public/full?alt=json`

3. Go to `app.py` and change the url source.
```python
self.dictionary_url = "<your google sheet json url>"
```

4. 

## Resources 
1. [Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
2. [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
3. [Google Sheet as a JSON Endpoint](https://www.freecodecamp.org/news/cjn-google-sheets-as-json-endpoint/)
4. [Deploy a Flask App on Render](https://render.com/docs/deploy-flask)
