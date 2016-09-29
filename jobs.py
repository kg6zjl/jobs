from flask import Flask, render_template, jsonify, request
from flask_restful import reqparse
import sqlite3, os

app = Flask(__name__) #start flask app

@app.route('/') #view all through web browser
def hello_world():
	query = "SELECT * FROM jobs order by ID DESC;"
	data = sql(query)
	return render_template('jobs.html',data=data)

@app.route('/jobs',methods=['GET']) #view all through api
def view_all_api():
	query = "SELECT * FROM jobs order by ID DESC;"
	data = str(sql(query))
	return jsonify(data=data)

@app.route('/submit',methods=['POST']) # add new job via api
def new_job():
	#parse api POST
	parser = reqparse.RequestParser()
	parser.add_argument('job',required=True,help="Job cannot be blank!")
	args = parser.parse_args()
	new_job = str(args['job'])
	if new_job:#call add_job function and pass new_job var
		if add_job(new_job):
			num_of_jobs = str(sql('select count(*) from jobs;'))
			return jsonify(new_job=new_job, total_num_of_jobs=num_of_jobs)
	else:
		return jsonify(status='broken')

@app.route('/delete/job/<job_id>',methods=['DELETE']) # add new job via api
def delete_job_api(job_id=None):
	#parse api POST
#	parser = reqparse.RequestParser()
#	parser.add_argument('id',required=True,help="id cannot be blank!")
#	args = parser.parse_args()
#	new_job = str(args['id'])
	if job_id:
		delete_job(job_id)
		return jsonify(success=('deleted id: %s'%job_id))
	else:
		return jsonify(status='broken')

def sql(query): # sql to view records, pass query
	conn = sqlite3.connect(db_filename) #write to local sqlite file
	cursor = conn.cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	conn.close()
	return data

def delete_job(job_id):
	try:
		conn = sqlite3.connect(db_filename)
		cursor = conn.cursor()
		query = ('''delete from jobs where id = "%s";''') % str(job_id)
		cursor.execute(query)
		conn.commit()
		conn.close()
		return True
	except:
		return False

def add_job(job): #sql to insert new job, pass job
	try:
		conn = sqlite3.connect(db_filename)
		cursor = conn.cursor()
		query = ('''insert into jobs (job) values ("%s");''') % job
		cursor.execute(query)
		conn.commit()
		conn.close()
		return True
	except:
		return False

def check_db(db): # create db schema if db doesn't exist
	if not os.path.exists(db):
		with sqlite3.connect(db) as conn:
			print 'Creating schema'
			with open('schema.sql', 'rt') as f:
				schema = f.read()
			conn.executescript(schema)

if __name__ == "__main__":
	db_filename = 'jobs.db' #define db filename
	check_db(db_filename) # initize db
	app.run(host='0.0.0.0', port=5000, debug=True) #run web server