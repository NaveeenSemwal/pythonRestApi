#!flask/bin/python
from flask import Flask, jsonify
from flask import request, abort, make_response 
import jsonpickle

from dto import Departent
import db 

app = Flask(__name__)


@app.route('/myApp/api/v1.0/department', methods=['GET'])
def getDepartments():
	cursor = db.cnxn.cursor()
	my_objects = []
	cursor.execute('SELECT * FROM departments')
	for row in cursor:
		print('row = %d , %s' % (row.department_id,row.department_name ))
		my_objects.append(Departent(row.department_id, row.department_name))		
	return jsonpickle.encode(my_objects, unpicklable=False);

@app.route('/myApp/api/v1.0/department/<int:department_id>', methods=['GET'])
def getDepartment(department_id):
	if department_id <1 :
		abort(400)
	print('Inpt is :'+str(department_id)+":");
	cursor = db.cnxn.cursor()
	cursor.execute('SELECT * FROM departments where department_id ='+str(department_id))
	myobj= None
	for row in cursor:
		print('row = %d , %s' % (row.department_id,row.department_name ))
		myobj = Departent(row.department_id, row.department_name)
	if myobj is  None :
		abort(404)
	return jsonpickle.encode(myobj, unpicklable=False);

@app.route('/myApp/api/v1.0/department', methods=['POST'])
def createDepartment():
	if not request.json or not 'name' in request.json:
		abort(400)
	print('Adding department :'+request.json['name']);
	cursor = db.cnxn.cursor()
	cursor.execute('SELECT max(department_id) FROM departments')
	myresult = cursor.fetchone()
	maxCount = 1;
	if not myresult[0] is None :		
		maxCount = myresult[0];
		maxCount = maxCount +1;
	sql = "INSERT INTO departments (department_id, department_name) VALUES (?, ?)"
	val = (maxCount,  request.json['name'])
	cursor.execute(sql, val)
	db.cnxn.commit()
	if cursor.rowcount ==1 :
		return jsonpickle.encode(Departent(maxCount,request.json['name']), unpicklable=False);
	else :
		abort(500);

@app.route('/myApp/api/v1.0/department/<int:department_id>', methods=['DELETE'])
def deleteDepartment(department_id):
	if department_id <1 :
		abort(400)
	print('Input for delete is :'+str(department_id)+":");
	cursor = db.cnxn.cursor()
	sql = "DELETE FROM departments WHERE department_id = ?"
	val = (department_id)
	cursor.execute(sql, val)
	db.cnxn.commit()
	if cursor.rowcount > 0 :
		return  make_response(jsonify({'message': 'Deleted Successfully !!!'}), 200)
	else :
		abort(404);

@app.route('/myApp/api/v1.0/department/<int:department_id>', methods=['PUT'])
def updateDepartment(department_id):
	if not request.json or not 'name' in request.json:
		abort(400)
	print('Updating department :'+request.json['name']);
	cursor = db.cnxn.cursor()
	sql = "UPDATE departments SET department_name = ? WHERE department_id = ?"
	val = (request.json['name'], department_id)	
	cursor.execute(sql, val)
	db.cnxn.commit()
	if cursor.rowcount ==1 :
		return jsonpickle.encode(Departent(department_id,request.json['name']), unpicklable=False);
	else :
		abort(500);
		
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
	
@app.errorhandler(400)
def invalidReqest(error):
    return make_response(jsonify({'error': 'Invalid Reqest content'}), 400)

@app.errorhandler(500)
def serverError(error):
    return make_response(jsonify({'error': 'Oppp!!! Some thing went wrong !!!'}), 500)

	
if __name__ == '__main__':
    app.run(debug=True)
	
