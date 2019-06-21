from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
import json
#import dnachelper
import requests
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Details for DNA Center Platform API calls
dnac_host = 'sandboxdnac.cisco.com'
dnac_user = 'admin'
dnac_pass = 'Cisco1234!'
dnac_headers = {'content-type': 'application/json'}
dnac_session = requests.Session()
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
from requests.auth import HTTPBasicAuth
import sys
 
class RoomPort_Form(Form):
	room = SelectField('Room', choices=[('',''),('0', 'Room 1'), ('1', 'Room 2'), ('A', 'ALL Rooms')], validators=[validators.required()]) #can be created from teh dict ?
	port = SelectField('Port', choices=[('',''),('0', 'Port 0/0/0'),('1', 'Port 0/0/1'),('2', 'Port 0/0/2'),('3', 'Port 0/0/3'),('4', 'Port 0/0/4'),('5', 'Port 0/0/5')], validators=[validators.required()])
 
class RoomVlan_Form(Form):
	room = SelectField('Room', choices=[('',''),('0', 'Room 1'), ('1', 'Room 2'), ('A', 'ALL Rooms')], validators=[validators.required()]) 
	vlan = SelectField('Vlan', choices=[('',''),('1', 'Vlan 1'), ('2', 'Vlan 2')], validators=[validators.required()]) 



@app.route("/start", methods=['GET'])
def start():
	formport = RoomPort_Form()
	formvlan = RoomVlan_Form()
	status=request.args.get('status')
	creat_topology()
	rooms_data = json.loads(open('js/rooms.js').read())
	rooms_details=[]
	for room in rooms_data['rooms']:
		room['ports']=",".join(room['ports'])
		rooms_details.append(room)

	return render_template('index.html', formport=formport, formvlan=formvlan , status=status, rooms_details=rooms_details)

@app.route("/topology", methods=['GET'])
def topology():
	html = render_template('topology.html')
	return html

@app.route("/add_port_to_room", methods=['POST'])
def add_port_to_room():
	form = RoomPort_Form(request.form)
	print form.errors
	if request.method == 'POST':

		port=request.form['port']
		room=request.form['room']
		print port
 
		if form.validate():
		# Save the comment here.
			f_add_port_to_room(port,room)
			creat_topology()
			flash('Port succefully added'+port,'OK')

		else:
			flash('All the form fields are required.','ERROR')

	return redirect(url_for('start',status='PRT'))


@app.route("/add_vlan", methods=['POST'])
def add_vlan():
	form = RoomVlan_Form(request.form)
	print form.errors
	if request.method == 'POST':

		vlan=request.form['vlan']
		room=request.form['room']
		print vlan
 
		if form.validate():
		# Save the comment here.
			f_add_vlan(vlan,room)
			#update_dnac(room,vlan)
			flash('vlan succefully added'+vlan,'OK')

		else:
			flash('All the form fields are required.','ERROR')

	return redirect(url_for('start',status='VLAN'))

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-cache'
    return response


def f_add_vlan(form_vlan,form_room):
	rooms_data = json.loads(open('js/rooms.js').read())
	for room in rooms_data['rooms']: 
		if room['id'] == form_room and form_vlan != room['vlan']:
			room['vlan'] = form_vlan
			update_room_vlan_dnac(room,ports_data)
			with open('js/rooms.js', 'w') as jsonfile:
				json.dump(rooms_data,jsonfile,indent=4)

def prety_port(port):
    return ('nodesDict.getItem("Port{}")'.format(str(port)))

def f_add_port_to_room(form_port,form_room):
	rooms_data = json.loads(open('js/rooms.js').read())
	for room in rooms_data['rooms']: 
		if room['id'] == form_room and not (form_port in room['ports']):
			room['ports'].append(form_port)
		else :
			if form_port in room['ports']:
				room['ports'].remove(form_port)

	with open('js/rooms.js', 'w') as jsonfile:
		json.dump(rooms_data,jsonfile,indent=4)


def creat_topology():
	with open('static/index.js', 'w') as outfile, open('index.js.template', 'r') as infile:
		rooms_data = json.loads(open('js/rooms.js').read())
		infile_data=infile.read()
		for room in rooms_data['rooms']:
			infile_data=infile_data.replace("{"+room['name']+"}",(",".join(prety_port(x) for x in room['ports'])))
		outfile.write(infile_data)


def update_room_vlan_dnac(room,ports_data):
		for port in ports_data:
			if port['id'] in room['ports']:
				print("hello")
				#dnachelper.call_vlan_template(dnac_session, dnac_host, dnac_headers,port['name'],port['switch_id'],room['vlan'])
				#mydnac.deploy_template('template-name',data_dict, device) ? the data dict will be compiled directly into params // the device will be coverted to device uuid 

	


if __name__ == "__main__":
	app.run(threaded=True)