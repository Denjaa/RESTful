import flask
from flask import Flask, request, jsonify, Response
from flask_restful import Api, Resource, reqparse
import os, pandas as pd, hashlib, werkzeug, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc
from common.handler import CSV
import time
import threading
import pandas as pd

application = Flask(__name__)																		# activating Flask framework
api = Api(application) 																				# activating Flask-RESTful framework

APP_ROOT = os.path.dirname(os.path.abspath(__file__))												# retrieve directory of app.py

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(APP_ROOT, 'db.sqlite') 	# configuration setup for database
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 										# configuration to stop throwing error out when database is called

db = SQLAlchemy(application)																		# activating SQL Alchemy framework

if not os.path.exists(os.path.join(APP_ROOT, 'uploads\\')):											# checking if directory uploads exist
	os.makedirs(os.path.join(APP_ROOT, 'uploads\\'), exist_ok = True)								# creating directory if it does not exist

if not os.path.exists(os.path.join(APP_ROOT, 'downloads\\')):
	os.makedirs(os.path.join(APP_ROOT, 'downloads\\'), exist_ok = True)

# function that takes in the input and convert it to hexidemial
def hashGenerator(data):
    hash_ob = hashlib.md5()
    hash_ob.update(data.encode())
    
    return hash_ob.hexdigest()

# creating storage database
class DatabaseStorage(db.Model):
	id = db.Column(db.Integer, primary_key = True)													# id column in database
	entity = db.Column(db.String(255), unique = True)												# entity column in database [unique ID made from file location + timestamp in ISO format]
	directory = db.Column(db.String(255))															# directory column in database storing where file was saved
	format = db.Column(db.String(255))																# format column in database storing file format		
	status = db.Column(db.String(255))																# stauts column in database storing status of processing	
	completed_directory = db.Column(db.String(255))													# completed directory column in database storing status of processing

# class that is responsible for uploading file and data needed to database
class FileUpload(Resource):

	def post(self):
		inputFile = request.files['file']															# uploading the file
		inputFile.save('/'.join([os.path.join(APP_ROOT, 'uploads/'), inputFile.filename]))			# saving file to specified directory
		
		process_id, file_dir, file_fmt = hashGenerator(str(os.path.join(APP_ROOT, inputFile.filename)) + str((datetime.datetime.now().isoformat()))), str(os.path.join(APP_ROOT, 'uploads\\' + str(inputFile.filename))), str(os.path.join(APP_ROOT, inputFile.filename)).split('.')[-1]

		data = DatabaseStorage(
								entity = process_id, 
								directory = file_dir, 
								format = file_fmt, 
								status = 'Processing',
								completed_directory = ''
								)							
		db.session.add(data)																		# adding data to the database
		db.session.commit()																			# commiting query

		# t = threading.Thread(target = processingFile(trigger = True, file = file_dir, process_id = process_id))
		# t.daemon = True
		# t.start()

		processingFile(trigger = True, file = file_dir, process_id = process_id)					# passing in parameters into main handler that uses external classes
		
		

		return 	{	
					'process_id' : process_id,
					'file_name' : str(inputFile).split("'")[1],
					'file_format': file_fmt
				}

		time.sleep(10)

api.add_resource(FileUpload, '/v1/upload')

class FileStatus(Resource):

	def get(self):
		status_id = request.args['status_id']														# taking in the argument from the user
		try:
			fetch = DatabaseStorage.query.filter_by(entity=status_id).one()							# querying data from database by its unique id
			
			return 	{
						'process_id' : fetch.entity,
						'status' : fetch.status
					}

		except exc.SQLAlchemyError: return {'error' : 'The ID provided does not exist'}

api.add_resource(FileStatus, '/v1/status')

def processingFile(file, process_id, trigger = None):

	while trigger == True:
		extension = str(file).split('.')[-1]
		
		if extension.endswith('csv'):
			csv = CSV()
			csv.GBI(file, process_id, root = APP_ROOT)
			fetch = DatabaseStorage.query.filter_by(entity=process_id).one()
			fetch.status = 'Successful'
			fetch.completed_directory = str(os.path.join(APP_ROOT, 'downloads\\' + str(process_id) + '.csv'))
			db.session.commit()
			trigger = False

class FileDownload(Resource):

	def get(self):
		status_id = request.args['status_id']

		try: 
			fetch = DatabaseStorage.query.filter_by(entity=status_id).one()
			csv = fetch.completed_directory
			csv = open(csv, 'r', encoding = 'UTF-8').readlines()
			return Response(csv, mimetype='text/csv', headers = {'Content-disposition': 'attachment; filename=myplot.csv'})

		except exc.SQLAlchemyError: return {'error' : 'The ID provided does not exist'}


api.add_resource(FileDownload, '/v1/download')

# run server
if __name__ == '__main__':
	application.run(debug = True)

































# import os
# from flask import Flask
# from flask import render_template
# from flask import request, send_from_directory, flash
# import time

# app = Flask(__name__) # creating an application for Flask

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # gets the abosule path of the running file

# # Function is returning the template called index which is the
# # main page that is being used by user to load data into server
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Function is taking in the file that user has loaded and loads it
# # into the server and then back end begins to work
# @app.route('/processing', methods=['POST', 'GET'])
# def processing():

# 	if not os.path.isdir(os.path.join(APP_ROOT, 'uploads/')):
# 		os.mkdir(os.path.join(APP_ROOT, 'uploads/'))

# 	for uploadedFile in request.files.getlist('file-name'):
# 		filename = uploadedFile.filename
# 		uploadedFile.save('/'.join([os.path.join(APP_ROOT, 'uploads/'), filename]))

# 	return "Succesfully uploaded document"






# # switching on the script if it is being called by its name
# if __name__ == "__main__":
# 	app.run(port = 5000, debug = True)
















# ########################################################################################
# 	# saveDir = os.path.join(APP_ROOT, 'uploads/') # specifying directory where files should be saved

# 		# if request.files['file-name'].filename != '':
# 		# 	pass			
# 		# # else:
# 		# # 	return 'Please select file to be loaded'