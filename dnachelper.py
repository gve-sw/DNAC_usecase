#!/usr/bin/env python



import json
import os
import requests




def dnac_open_session(dnac_session,
                      dnac_host,
                      dnac_headers,
                      dnac_username,
                      dnac_password):
    """DNA Center login and adding cookie to session"""
    print('DNAC Login to ' + dnac_host + ' as ' + dnac_username + ' ...')
    dnac_auth_api = 'https://%s/api/system/v1/auth/login' % dnac_host
    r = dnac_session.get(dnac_auth_api,
                         verify=False,
                         headers=dnac_headers,
                         auth=HTTPBasicAuth(dnac_username, dnac_password))
    r.raise_for_status()
    # print('DNAC Login: Response Headers: ' + str(r.headers))
    # print('DNAC Login: Response Body: ' + r.text)

    session_token_val = ((r.headers['Set-Cookie']).split('=')[1]).split(';')[0]
    # session_token_val = r.json()["Token"]
    cookies = {'X-JWT-ACCESS-TOKEN': session_token_val}
    dnac_session.cookies.update(cookies)
    print('DNAC Login: Session Cookie: ' + str(cookies))
    return r



def dnac_get_device_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Device Count"""
    tmp_url = 'https://%s/api/v1/network-device/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']




def dnac_get_devices(dnac_session, dnac_host, dnac_headers):
    """DNAC Network Devices"""
    tmp_url = 'https://%s/api/v1/network-device' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']



def dnac_get_host_count(dnac_session, dnac_host, dnac_headers):
    """DNAC Host Count"""
    tmp_url = 'https://%s/api/v1/host/count' % dnac_host
    r = dnac_session.get(tmp_url, verify=False, headers=dnac_headers)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']



def dnac_get_modules(dnac_session, dnac_host, dnac_headers, device_id):
    """DNAC Modules of a Network Device"""
    tmp_url = 'https://%s/api/v1/' % dnac_host
    tmp_url = tmp_url + 'network-device/module?deviceId=%s' % device_id

    r = dnac_session.get(tmp_url,
                         verify=False,
                         headers=dnac_headers
                         )
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']


def dnac_get_module_count(dnac_session, dnac_host, dnac_headers, device_id):
    """DNAC Module Count of a Network Device"""
    tmp_url = 'https://%s/api/v1/network-device/module/count' % dnac_host
    tmp_params = {'deviceId': device_id}

    r = dnac_session.get(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         params=tmp_params)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']


def call_vlan_template(dnac_session, dnac_host, dnac_headers, port , switch_id , vlan ):
    """DNAC Module Count of a Network Device"""
    tmp_url = 'https://%s/api/v1/network-device/module/count' % dnac_host
    payload = {'deviceId': device_id}

    r = dnac_session.post(tmp_url,
                         verify=False,
                         headers=dnac_headers,
                         data=payload)
    r.raise_for_status()
    # print('DNAC Response Body: ' + r.text)
    return r.json()['response']


with requests.Session() as dnac_session:
    r = dnac_open_session(dnac_session,
                          dnac_host,
                          dnac_headers,
                          dnac_user,
                          dnac_pass)

    # Getting DNAC Device Count and Host Count verbose after login
    c = dnac_get_device_count(dnac_session, dnac_host, dnac_headers)
    print('DNAC Network Device Count: ' + str(c))
    c = dnac_get_host_count(dnac_session, dnac_host, dnac_headers)
    print('DNAC Host Count: ' + str(c))



