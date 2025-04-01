from flask import Flask,  jsonify
from flask_cors import CORS, cross_origin
import datetime
import os

import configparser
from mapepire_python.client.sql_job import SQLJob
from mapepire_python.data_types import DaemonServer

config = configparser.ConfigParser()
config.read('config.ini')

creds = DaemonServer(
    host=config['mapepire']['SERVER'],
    port=config['mapepire']['PORT'],
    user=config['mapepire']['USER'],
    password=config['mapepire']['PASSWORD'],
    ignoreUnauthorized=True,
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
# Added root endpoint
def root():
    content = {}
    content['status'] = "Good"
    now = datetime.datetime.now()
    content['time'] = now.strftime("%H:%M:%S")
    return jsonify(content)

@app.route('/employee/<int:empid>')
@cross_origin()
# One employee
def employee(empid: int):
    with SQLJob(creds) as job:
        with job.query('select * from SAMPLE.employee where EMPNO=' + str(empid)) as query:
            results = query.run(rows_to_fetch=1)
            data = results
        return data

@app.route('/getProducts')
@cross_origin()
# All products
def getProducts():
    with SQLJob(creds) as job:
        with job.query('select * from SAMPLE.product') as query:
            results = query.run()
        return results

@app.route('/getEmployees')
@cross_origin()
# All employees
def getEmployees():
    with SQLJob(creds) as job:
        with job.query('select EMPNO,FIRSTNME,LASTNAME,JOB from SAMPLE.employee') as query:
            results = query.run()
        return results
    
@app.route('/getAllEmployees')
@cross_origin()
# All employees
def getAllEmployees():
    with SQLJob(creds) as job:
        with job.query('select EMPNO,FIRSTNME,LASTNAME,JOB from SAMPLE.employee') as query:
            results = query.run()
        return results

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)