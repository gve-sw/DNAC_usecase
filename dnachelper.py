#!/usr/bin/env python



import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import DNAC



dnac_headers = {'X-Auth-Token':'',
                'content-type': 'application/json'}
dnac_session = requests.Session()
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


#print HTTPBasicAuth(dnac_user, dnac_pass)

def dnac_open_session(dnac_host,
                      dnac_headers,
                      dnac_username,
                      dnac_password):
    """DNA Center login and adding cookie to session"""
    print('DNAC Login to ' + dnac_host + ' as ' + dnac_username + ' ...')
    dnac_auth_api = 'https://%s/dna/system/api/v1/auth/token' % dnac_host
    r = requests.post(dnac_auth_api,
                         verify=False,  
                         auth=HTTPBasicAuth(dnac_username, dnac_password))

    dnac_headers['X-Auth-Token']=r.json()["Token"]

    return r


def DNAC_creat_project(dnac_host, dnac_headers,project_name):
    """DNAC Module Creat a template progrmamer project"""
    print('Creating new project in template programmer : ' + project_name)
    tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/project' % dnac_host
    payload = {"name": project_name}

    r = requests.post(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         data=json.dumps(payload))
    #r.raise_for_status()
    print('DNAC Response Body: ' + r.text)
    return r.text  

def DNAC_get_project_id(dnac_host, dnac_headers,project_name):
    """DNAC Module Get project by name"""
    print('Get template programer project id : ' + project_name)
    tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/project' % dnac_host

    r = requests.get(tmp_url,
                         verify=False,
                         headers=dnac_headers)
    #r.raise_for_status()
    print('DNAC Response Body: ' + r.text)
    project_id=''
    for project in r.json():
      if project['name']==project_name:
        project_id=project['id']
        print('Project id : '+project_id)
    return project_id     

def DNAC_create_template(dnac_host, dnac_headers,project_id,template_name):
    """DNAC Module Get project by name"""
    print('create template programer : ' + template_name)
    tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/project/%s/template' % (dnac_host,project_id)
    payload = {
                    "composite": False,
                    "deviceTypes": [
                            {
                              "productFamily": "Switches and Hubs"
                            }
                          ],
                      "failurePolicy": "ABORT_ON_ERROR",
                  "name": template_name,
                  "softwareType": "IOS-XE",
                  "softwareVariant": "XE",
                  "templateContent": "interface tenGigabitEthernet $port\n  switchport access vlan $vlan",
                  "templateParams": [
                              {
                                "parameterName": "port",
                                "dataType": None,
                                "defaultValue": None,
                                "description": None,
                                "required": True,
                                "notParam": False,
                                "paramArray": False,
                                "displayName": None,
                                "instructionText": None,
                                "group": None,
                                "order": 1,
                                "selection": None,
                                "range": [],
                                "key": None,
                                "provider": None,
                                "binding": ""
                              },
                              {
                                "parameterName": "vlan",
                                "dataType": None,
                                "defaultValue": None,
                                "description": None,
                                "required": True,
                                "notParam": False,
                                "paramArray": False,
                                "displayName": None,
                                "instructionText": None,
                                "group": None,
                                "order": 2,
                                "selection": None,
                                "range": [],
                                "key": None,
                                "provider": None,
                                "binding": ""
                              }
                            ],
                  "version": "1"
              }
    r = requests.post(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         data=json.dumps(payload))
    #r.raise_for_status()
    print('DNAC Response Body: ' + r.text)
    return r  

def DNAC_commit_template(dnac_host, dnac_headers,template_name,project_name):
    """DNAC Module Get project by name"""
    print('Get template programer project id : ' + project_name)
    tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/project' % dnac_host

    r = requests.get(tmp_url,
                         verify=False,
                         headers=dnac_headers)
    #r.raise_for_status()
    print('DNAC Response Body: ' + r.text)
    
    for project in r.json():
      if project['name']==project_name:
        for template in project['templates']:
          if template['name']==template_name:
            tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/template/version' % dnac_host
            payload = { "comments": "first commit", "templateId": template['id']  }
            r = requests.post(tmp_url,
                                 verify=False,
                                 headers=dnac_headers,
                                 data=json.dumps(payload))
            print('DNAC Response Body: ' + r.text)
    return r  

def DNAC_get_template_id(dnac_host, dnac_headers,template_name,project_name,version='1'):
    """DNAC Module Get project by name"""
    print('Get template id : ' + template_name)
    tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/template' % dnac_host

    r = requests.get(tmp_url,
                         verify=False,
                         headers=dnac_headers)
    #r.raise_for_status()
    print('DNAC Response Body: ' + r.text)
    template_id=''
    for template in r.json():
      if template['name']==template_name and template['projectName']==project_name:
        template_id=template['templateId']
        print('Template id : '+template_id)
        for element in template['versionsInfo']:
          if element['version']==version:
            template_v_id=element['id']
            print('Template version id : '+template_v_id)
        
    return {'template_id':template_id,'template_version_id':template_v_id}

def DNAC_deploy_vlan_template(dnac_host, dnac_headers,template_v_id,data={'switch_id':'','switch_port':'','vlan':''}):
    """DNAC Module deploy vlan template"""
    print('create template programer : ' + template_name)
    tmp_url = 'https://%s/dna/intent/api/v1/template-programmer/project/%s/template' % (dnac_host,project_id)
    payload = {
                  "targetInfo": [
                      {
                          "id": data['switch_id'] ,
                          "params": {"port": data['switch_port'] ,"vlanid": data['vlan'] },
                          "type": "MANAGED_DEVICE_UUID"
                      }
                  ],
                  "templateId": template_v_id
              }
    r = requests.post(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         data=json.dumps(payload))
    #r.raise_for_status()
    print('DNAC Response Body: ' + r.text)
    #verfy return for confimration
    return r 

def DNAC_get_devices(dnac_host, dnac_headers):
    """DNAC Module Get project by name"""
    print('Get template id : ' )
    tmp_url = 'https://%s/dna/intent/api/v1/network-device' % dnac_host

    r = requests.get(tmp_url,
                         verify=False,
                         headers=dnac_headers)
    #r.raise_for_status()
    #print('DNAC Response Body: ' + r.text)
    return r.json()['response']


if __name__ == "__main__":

    r = dnac_open_session(DNAC.dnac_host,dnac_headers,DNAC.dnac_user,DNAC.dnac_pass)
    print(dnac_headers)

    c = DNAC_creat_project(DNAC.dnac_host, dnac_headers,"newonetest")
    project_id = DNAC_get_project_id(DNAC.dnac_host, dnac_headers,"newonetest")
    c = DNAC_create_template(DNAC.dnac_host, dnac_headers,project_id,"newtemplate")
    c = DNAC_commit_template(DNAC.dnac_host, dnac_headers,template_name,project_name)
    c = DNAC_get_template_id(DNAC.dnac_host, dnac_headers,'Test-Template','New Project')
    if c['template_version_id']:
      print("##### Success! Template id : "+ c['template_version_id'])
    else :
      print ("Failed check logs")
    c = DNAC_get_devices(DNAC.dnac_host, dnac_headers)
    print( '{0:30}  {1:20}  {2:70}'.format('Hostname','Ip Address','Id')  )
    for device in c :
      try:
        print('{0:30}  {1:20}  {2:70}'.format(device['hostname'],device['managementIpAddress'],device['id']))
      except:
        print("error")
        continue


