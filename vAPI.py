#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Hussein Omar, CSS - ANZ"
__email__ = "husseino@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# ---> Imports
from pprint import pprint
from datetime import datetime
import datetime
import csv
import ipaddress
import getpass
import requests
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ---> Main Code


class vapi(object):
    cookie = ""

    def welcome(self):
        print(
            '''

        |========================================|
        |       Cisco SD-WAN Health Check        |
        |       Tested on version 20.3.3.1       |
        |========================================|

=======================
Please login to vManage
=======================
        ''')

    def login(self):
        '''
        - Receive user input for vmanage information ip-address/username/password
        - Contruct API call base-URL
        '''
        self.vmanage_ip = None
        while self.vmanage_ip == None:
            vmanage_ip_typed = input('vManage IP address: ')
            try:
                self.vmanage_ip = ipaddress.ip_address(vmanage_ip_typed)
            except Exception:
                print(
                    f'ERROR: {vmanage_ip_typed} is not a correct IPv4 or IPv6 address')

        self.port = input('Port Number (default 8443): ')
        if len(self.port) == 0:
            self.port = 8443
        self.username = input('Username: ')
        self.password = getpass.getpass('Password: ')
        self.base_url = f'https://{self.vmanage_ip}:{self.port}'

    def getCookie(self):
        '''
        - Initial first login to vManage and return authentication cookie
        '''
        mount_url = '/j_security_check'
        url = self.base_url + mount_url
        # Format data for loginForm
        payload = {'j_username': self.username, 'j_password': self.password}
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        self.response = requests.request(
            "POST", url, data=payload, headers=headers, verify=False)

        if self.response.status_code >= 300:
            raise BaseException(
                "ERROR : The username/password is not correct.")
        if '<html>' in self.response.text:
            raise BaseException("ERROR : Login Failed.")
        print('--------------------------------------------------------')
        print(f'Authenticated, login to {self.vmanage_ip} is SUCCESSFUL')
        print('--------------------------------------------------------')
        self.cookie = str(self.response.cookies).split(' ')[1]

    def getToken(self):
        '''
        - Generate authentication token to be used in subsequent requests
        '''
        mount_url = '/dataservice/client/token'
        url = self.base_url + mount_url
        # Format data for loginForm
        payload = {}
        headers = {
            'Cookie': self.cookie,
        }
        self.response2 = requests.request(
            "GET", url, data=payload, headers=headers, verify=False)
        self.token = self.response2.text

    def auth(self):
        '''
        - First method to be called in main App
        - Returns session cookie and token
        '''
        vapi.welcome(self)
        vapi.login(self)
        vapi.getCookie(self)
        vapi.getToken(self)

#################################################################
#################### High Level Functions #######################
    def getResponse(self, mountURL):
        '''
        - Args: mounting URL
        - Construct full URL by adding mountURL to baseURL
        - Send a 'GET' request with empty payload with cookie and token
        - Return the data portion (dict) of the JSON response
        '''
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-XSRF-TOKEN': self.token,
            'Cookie': self.cookie
        }
        url = self.base_url + mountURL
        response = requests.request("GET", url, headers=headers, verify=False)
        data = json.loads(response.text)['data']
        return data

    def getDevices(self):
        '''
        - Retrieve list of devices provisioned on vManage
        '''
        mountURL = '/dataservice/device/'
        data = vapi.getResponse(self, mountURL)
        return data

#################################################################
################## Tasks Functions ##############################

########################## Task 1 ###############################

    def fullDeviceList(self, filename):
        '''
        - Generate a device list in csv format
        - Args: This function takes a filename as string variable
        - The CSV file headers are defined by the "fields" list variable
        '''
        devices = vapi.getDevices(self)
        fields = ['chasisNumber', 'configOperationMode', 'defaultVersion', 'deviceIP', 'deviceModel', 'deviceState', 'deviceType', 'globalState', 'hardwareCertSerialNumber', 'host-name', 'lastupdated', 'local-system-ip', 'managementSystemIP', 'model_sku', 'ncsDeviceName',
                  'personality', 'platformFamily', 'reachability', 'rootCertHash', 'serialNumber', 'site-id', 'state', 'subjectSerialNumber', 'system-ip', 'template', 'uuid', 'validity', 'vbond', 'vedgeCSRCommonName', 'vedgeCertificateState', 'version', 'vmanageConnectionState']
        vapi.dict2csv(self, devices, filename, fields)

########################## Task 2 ###############################

    def custom_DeviceList(self, filename, inputHeadersfile):
        '''
        - This function will generate a device list file with headers similar to input file headers
        - Args: "filename" output file name, generated file is in CSV format
        - Args: "inputHeaderfile" this must be a CSV file, the function will read first row to generate the headers
        '''
        with open(inputHeadersfile, 'r') as inputHeader:
            newDictHeaders = next((csv.reader(inputHeader)), None)

        devices = vapi.getDevices(self)
        vapi.dict2csv(self, devices, filename, newDictHeaders)

########################## Task 3 ###############################
    def getFabricHealth(self, filename):
        '''
        - This function generate a CSV file with headers in "fields" variable
        - The 
        '''
        devices = vapi.getDevices(self)
        data = vapi.getControlConn(self, devices)
        fields = ['site-id', 'system-ip', 'host-name', 'reachability', 'status', 'device-type', 'board-serial',
                  'uuid', 'bfdSessions', 'controlConnections', 'device-model', 'version', 'validity']
        vapi.dict2csv(self, data, filename, fields)

    def getControlConn(self, devices):
        for device in devices:
            mountURL = f'/dataservice/device/control/synced/connections?deviceId={device["system-ip"]}&&'
            data = vapi.getResponse(self, mountURL)
            connNumber = len(data)
            upstate = 0
            for i in data:
                if i['state'] == 'up':
                    upstate += 1
            state = f'({upstate}/{connNumber})'
            if device['reachability'] == 'reachable':
                device['controlConnections'] = state
            else:
                device['controlConnections'] = 'unknown'
        return devices


########################## Task 4 ###############################

    def getUnreachableDevices(self, filename):
        mountURL = '/dataservice/device/control/networksummary?state=down'
        devices = vapi.getResponse(self, mountURL)

        for device in devices:
            device['uptime-date'] = vapi.unixTimeStamp(
                self, device['uptime-date'])
            device['lastupdated'] = vapi.unixTimeStamp(
                self, device['lastupdated'])
        fields = ['site-id', 'system-ip', 'host-name', 'reachability',
                  'device-model', 'version', 'board-serial', 'uuid', 'uptime-date', 'lastupdated']
        vapi.dict2csv(self, devices, filename, fields)

########################## Task 5 ###############################

    def getPartialControlConnections(self, filename):
        devices = vapi.getDevicesPartialCon(self)
        template0 = vapi.template0(self, devices)
        vapi.writeReport(self, template0, filename)
        for device in devices:
            template1 = vapi.template1(self, device)
            vapi.writeReport(self, template1, filename)
            data, newData = vapi.getConnectionHistory(self, device)
            if newData:
                for item in newData:
                    template2 = vapi.template2(self, item)
                    vapi.writeReport(self, template2, filename)
            else:
                template2b = vapi.template2b(self, data)
                vapi.writeReport(self, template2b, filename)
            wanIntfs = vapi.getWanInterfaces(self, device)
            for intf in wanIntfs:
                template3 = vapi.template3(self, intf)
                vapi.writeReport(self, template3, filename)
            endDevice = vapi.endOfDeviceData(self, device)
            vapi.writeReport(self, endDevice, filename)
        endReport = vapi.endOfReportData(self)
        vapi.writeReport(self, endReport, filename)
        print(
            '------------------------------------------------------------------------------')
        print(f'File {filename} has been written to disk')
        print(
            '------------------------------------------------------------------------------')

    def getDevicesPartialCon(self):
        mountURL = '/dataservice/device/control/networksummary?state=partial'
        devices = vapi.getResponse(self, mountURL)
        return devices

    def getWanInterfaces(self, device):
        mountURL = f'/dataservice/device/control/waninterface?deviceId={device["system-ip"]}'
        data = vapi.getResponse(self, mountURL)
        return data

    def getConnectionHistory(self, device):
        mountURL = f'/dataservice/device/control/connectionshistory?deviceId={device["system-ip"]}'
        data = vapi.getResponse(self, mountURL)
        newData = []
        for item in data:
            if item['peer-type'] == 'vsmart':
                newData.append(item)
        return data, newData

########################## Task 6 ###############################
    def getPartialBfdConnections(self, filename):
        devices = vapi.getDevicesPartialBFD(self)
        bfdTemplate0 = vapi.bfdTemplate0(self, devices)
        vapi.writeReport(self, bfdTemplate0, filename)
        for device in devices:
            bfdTemplate1 = vapi.bfdTemplate1(self, device)
            vapi.writeReport(self, bfdTemplate1, filename)
            tunnelData = vapi.getDeviceDownTunnels(self, device)
            for tunnel in tunnelData:
                bfdTemplate2 = vapi.bfdTemplate2(self, tunnel)
                vapi.writeReport(self, bfdTemplate2, filename)
            bfdTemplate3 = vapi.bfdTemplate3(self, device)
            vapi.writeReport(self, bfdTemplate3, filename)
            bfdTLOCs = vapi.getDeviceBfdTLOCs(self, device)
            for tloc in bfdTLOCs:
                bfdTemplate4 = vapi.bfdTemplate4(self, tloc)
                vapi.writeReport(self, bfdTemplate4, filename)
            endDevice = vapi.endOfDeviceData(self, device)
            vapi.writeReport(self, endDevice, filename)
        endReport = vapi.endOfReportData(self)
        vapi.writeReport(self, endReport, filename)
        print(
            '------------------------------------------------------------------------------')
        print(f'File {filename} has been written to disk')
        print(
            '------------------------------------------------------------------------------')

    def getDevicesPartialBFD(self):
        mountURL = f'/dataservice/device/bfd/sites/detail?state=sitepartial'
        devices = vapi.getResponse(self, mountURL)
        return devices

    def getDeviceBfdTLOCs(self, device):
        mountURL = f'/dataservice/device/bfd/tloc?deviceId={device["system-ip"]}'
        data = vapi.getResponse(self, mountURL)
        return data

    def getDeviceDownTunnels(self, device):
        mountURL = f'/dataservice/device/bfd/sessions?deviceId={device["system-ip"]}'
        data = vapi.getResponse(self, mountURL)
        newData = []
        for item in data:
            if item['state'] == 'down':
                newData.append(item)
        return newData


########################## Supporting Code ###############################
####### Text Templates ###################################################
############## Control Connection Templates ##############################

    def template0(self, devices):
        templateText = f"""
=================================================================
Partial Control  connections Report - {datetime.datetime.now()}
Total Number of devices with partial control connections: {len(devices)}
=================================================================

    """
        return templateText

    def template1(self, device):
        templateText = f"""

*** Device Info for {device['host-name']} ***
-------------------------------------------
site-id: {device["site-id"]}
system-ip: {device["system-ip"]}
host-name: {device["host-name"]}
device-model: {device["device-model"]}
software version: {device["version"]}
serial number: {device["board-serial"]}
system-ip: {device["system-ip"]}
device uptime: {vapi.unixTimeStamp(self,device["uptime-date"])}
last updated: {vapi.unixTimeStamp(self, device["lastupdated"])}

*** Control Connections Info ****
----------------------------------------
reachability: {device["reachability"]}
vSmart Connections: {device["controlConnectionsToVsmarts"]}
        """
        return templateText

    def template2(self, data):
        templateText = f"""

*** Control Connections History ****
----------------------------------------
==> Connection to {data['peer-type']} - system-ip: {data['system-ip']} - public-address: {data['public-ip']}
==> Connection Status: {data['state']}
------------------------------------------------------------------------------------------------------------
protocol: {data['protocol']} - port number: {data['public-port']} - vSmart error: {data['remote_enum']}
local-color: {data['local-color']} - local error: {data['local_enum']}
downtime: {data['downtime']}
downtime date: {vapi.unixTimeStamp(self, data['downtime-date'])}
lastupdated: {vapi.unixTimeStamp(self, data['lastupdated'])}
        """
        return templateText

    def template2b(self, data):
        templateText = f"""

*** Control Connections History ****
----------------------------------------
No control connections history on {data[0]['remote-color']}
Local Error: {data[0]['local_enum-desc']} - {data[0]['local_enum']}
vBond side error: {data[0]['remote_enum-desc']}
    """
        return templateText

    def template3(self, data):
        templateText = f"""

----------------------------------------
Interface {data['interface']}
----------------------------------------
transport color: {data['color']}
admin-state: {data['admin-state']}
operational-state: {data['operation-state']}
private-ip-address: {data['private-ip']}
public-ip-address: {data['public-ip']}
connections to vSmarts: {data['num-vsmarts']}
connection to vManages: {data['num-vmanages']}
vManage connection preference: {data['vmanage-connection-preference']}
Configured as Last resort: {data['last-resort']}
last connection time: {vapi.unixTimeStamp(self, data['last-conn-time-date'])}
lastupdated: {vapi.unixTimeStamp(self, data['lastupdated'])}
        """
        return templateText


############## Control Connection Templates ##############################


    def bfdTemplate0(self, devices):
        templateText = f"""
=================================================================
Partial BFD connections Report - {datetime.datetime.now()}
Total Number of devices with partial BFD connections: {len(devices)}
=================================================================

        """
        return templateText

    def bfdTemplate1(self, device):
        templateText = f"""

*** Device Info for {device['host-name']} ***
-------------------------------------------
site-id: {device["site-id"]}
system-ip: {device["system-ip"]}
host-name: {device["host-name"]}
device-model: {device["device-model"]}
software version: {device["version"]}
serial number: {device["board-serial"]}
system-ip: {device["system-ip"]}
device uptime: {vapi.unixTimeStamp(self, device["uptime-date"])}
last updated: {vapi.unixTimeStamp(self, device["lastupdated"])}

*** BFD Connections Info ****
----------------------------------------
reachability: {device["reachability"]}
BFD Connections: {device["bfdSessions"]}

*** BFD Connections Details ****
----------------------------------------
        """
        return templateText

    def bfdTemplate2(self, data):
        templateText = f"""
====> {data['vdevice-dataKey']} - {data['state']} - Last updated: {vapi.unixTimeStamp(self, data['lastupdated'])}"""
        return templateText

    def bfdTemplate3(self, device):
        templateText = f"""

====> {device['system-ip']} BFD TLOC Interfaces
------------------------------------------------------
        """
        return templateText

    def bfdTemplate4(self, data):
        templateText = f"""
=> Interface: {data['if-name']} - 
=======> Down BFD Sessions: {(int(data['sessions-total'])-(int(data['sessions-up'])))}
=======> Up BFD Sessions: {data['sessions-up']}
=======> Total BFD Sessions: {data['sessions-total']}

        """
        return templateText

############## General Templates ##########################################

    def endOfDeviceData(self, device):
        text = f"""
|<--------------------------------------------------------->|
|------> End of Device {device['host-name']} data <---------|
|<--------------------------------------------------------->|
"""
        return text

    def endOfReportData(self):
        text = f"""
|<--------------------------------------------------------->|
|------> End of Report data at {datetime.datetime.now()} <---------|
|<--------------------------------------------------------->|
"""
        return text

###################### Tools ###########################
    def dict2csv(self, dict, filename, fields):
        new_dict = []
        for item in dict:
            temp_dict = {}
            for field in fields:
                try:
                    temp_dict[field] = item[field]
                except KeyError:
                    temp_dict[field] = 'NA'
            new_dict.append(temp_dict)
        with open(filename, 'w') as csvFile:
            wr = csv.DictWriter(csvFile, fieldnames=fields)
            wr.writeheader()
            for ele in new_dict:
                wr.writerow(ele)
        print(
            '------------------------------------------------------------------------------')
        print(f'File {filename} has been written to disk')
        print(
            '------------------------------------------------------------------------------')

    def unixTimeStamp(self, unixStamp):
        stampNumber = int(unixStamp)/1000
        return datetime.datetime.fromtimestamp(stampNumber).strftime('%Y-%m-%d %H:%M:%S')

    def writeReport(self, text, filename):
        file = open(filename, 'a')
        file.write(text)
        file.close()
