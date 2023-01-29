# QuadLingo Dictionary

## Overview
![QuadLingo Home Page](screenshot.png)

View Demo: https://dictionary-data-api.onrender.com

QuadLingo is a user-friendly tool for searching slangs and their meanings in English, Deutsch, Mandarin and Tagalog.
This app serves as a basic application of the Flask Framework using Google Sheets as its source of information and easy deployment on Render. For a setup that requires a relational database setup, [view this project instead](https://github.com/kayesokua/flask-store-dummy).

## Package Requirements
1. `Flask`
2. `gTTS`
3. `gunicorn`
4. `jsons`
5. `urllib3`

## Run the Application on Local Environment
1. Clone repository `git clone https://github.com/kayesokua/flask-dictionary flask-dir`
2. Go to the new directory`cd flask-dir`
3. Install required modules `pip3 install -r -requirements.txt`
4. Run the application `flask run`

## How to Use

### Get API JSON

*  `https://dictionary-data-api.onrender.com/api/json/` to to get all items in the dictionary
*  `https://dictionary-data-api.onrender.com/api/json/<int>` to get 1 item detail

### Create Your Own Dictionary


## Resources 
1. [Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
2. [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
3. [Google Sheet as a JSON Endpoint](https://www.freecodecamp.org/news/cjn-google-sheets-as-json-endpoint/)
4. [Deploy a Flask App on Render](https://render.com/docs/deploy-flask)
