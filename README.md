# CISCO DNA Center automation POV
This prototype is a mockup interface to DNAC, using DNAC APIs we can automate bussness workflows and start building intgrating bussness applications into the network. this is an exmple using the template editor in DNAC we are able to automate the assigement of vlan trough a network based on a bussness logic, where we orgnise couple of network ports regardless of the switch into logical rooms, and then we use the API to assigne vlans to the rooms, the app would go and update the vlans on the respective ports using DNAC APIs 
The prototype is built using a python Flask server and CISCO UI toolkit and cisco NeXt UI toolkit, the GUI allows the user to group ports into rooms and then assigne vlans to rooms

## Usage:

#### Clone the repo :
```
$ git clone https://github.com/Abdellbar/Asset_tracking_POV
```

#### Install dependencies :
```
$ pip install flask
$ pip install WTForms
```

#### DANC details :
You can deploy this portotype with one of our CISCO DevNet DNAC lab sandboxes availible here.
fill in the details of your DNAC server in the DNAC.py file
```
dnac_host = 'sandboxdnac2.cisco.com'
dnac_user = 'devnetuser'
dnac_pass = 'Cisco123!'
```

#### run script dnachelper.py:
run this file the first time before runing the server, this will create the template in DNAC and genrate the template id and device Ids
```
$ python3 dnachelper.py
```
 - take note of the template id
 - take note of the devices id 

after execution
```
$ python3 dnachelper.py
.
.
.
##### Success! Template id : 90a5164d-8011-4d2f-a205-b6d2219d7cb6
##### Devices list :
Hostname                      ##Ip Address          ##Id                                                                    
3504_WLC                      ##10.10.20.51         ##50c96308-84b5-43dc-ad68-cda146d80290
```

#### update files for your envirenement:

update the template id in the file DNAC.py

```
template_v_id = 'your template id goes here'
```

update the device ids in the rooms.js file :

```
  "ports": [
    {
      "switch_id": "6a49c827-9b28-490b-8df0-8b6c3b582d8a",
      "id": "0",
      "name": "0/0/12"
    },
```
note: you can add ports from diffrent siwtches based on your demo, make sure to update server.py with the ports/updated accordighnly 

```
port = SelectField('Port', choices=[('',''),('0', 'Port 0/0/12'),('1', 'Port 0/0/13'),('2', 'Port 0/0/14'),('3', 'Port 0/0/15'),('4', 'Port 0/0/16'),('5', 'Port 0/0/17	')], validators=[validators.required()])
```

Launch the server by issueing 
```
$ python server.py
```

In a web browser open :
http://127.0.0.1:5000/start

## Integrate to CMX:

Add the url 'http://127.0.0.1:5000/webhook' into CMX to post the location data directly to the app

