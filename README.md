# RESTful API

## Description
There was a requirement to develop a solution to a problem where use can upload raw data file and get spit out the output that will standardise the data. 

## What script does:
1. Switches on server
2. Creates a database that stores data to loading tracking
3. Gets data by special ID
4. Works on data
5. Spits data out


To run the script you would need Python 3.6 version.

## Commmand line:
```
python app.py
```

Once command is ran then it will switch on Flask server and user will require a knowledge of requests to send in data and knowledge of how API's work

## Things that need to implemented once management signs off the project
1. Build a queue system
2. Put threading on the Q system
3. Implement tokenization
4. Understand how raw data is structured and what standard template is required
