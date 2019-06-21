#!/usr/bin/python
import json
"""
Rooms  = (json.loads(open('js/rooms.js').read()))['rooms']
Ports  = (json.loads(open('js/rooms.js').read()))['ports']


print Rooms

print Ports
def prety_port(port):
    return ('nodesDict.getItem("Port{}")'.format(str(port)))

print prety_port('0')


for room in Rooms :
	print (",".join(prety_port(x) for x in room['ports']))
"""

"""existing_data = json.loads(open('js/rooms.js').read())

form_port = 5
form_room = 1
new_data = existing_data
for room in new_data['rooms']: 
	if room['id'] == form_room:
		room['ports'].append(form_port)
	else :
		if form_port in room['ports']:
			room['ports'].remove(form_port)

print(json.dumps(new_data, indent=4, sort_keys=True))
"""

rooms_data = json.loads(open('js/rooms.js').read())
rooms_details=[]

for room in rooms_data['rooms']:
	print room
	room['ports']=",".join(room['ports'])
	rooms_details.append(room)

print rooms_details