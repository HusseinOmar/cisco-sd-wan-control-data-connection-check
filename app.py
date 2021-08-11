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

import vAPI
from datetime import datetime


def getTimeStamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d%m%Y-%H%M%S")
    return timestampStr


session = vAPI.vapi()
session.auth()


def task1():
    filename = input(
        'Please enter filename with .csv extension (default = FullDeviceList-<timeStamp>.csv): ')
    if filename == '':
        filename = f'FullDeviceList-{getTimeStamp()}.csv'
    session.fullDeviceList(filename)


def task2():
    inputHeadersfile = input('please enter source csv file for headers: ')
    filename = input(
        'Please enter filename with .csv extension (default = DeviceList-CustomHeaders-<timeStamp>.csv): ')
    if filename == '':
        filename = f'DeviceList-CustomHeaders-{getTimeStamp()}.csv'
    session.custom_DeviceList(filename, inputHeadersfile)


def task3():
    filename = input(
        'Please enter file name with .csv extension (default = FabricHeath-<timeStamp>.csv): ')
    if filename == '':
        filename = f'FabricHeath-{getTimeStamp()}.csv'
    session.getFabricHealth(filename)


def task4():
    filename = input(
        'Please enter file name with .csv extension (default = UnreachableDevices-<timeStamp>.csv): ')
    if filename == '':
        filename = f'UnreachableDevices-{getTimeStamp()}.csv'
    session.getUnreachableDevices(filename)


def task5():
    filename = input(
        'Please enter file name with .csv extension (default = UnreachableDevices-<timeStamp>.csv): ')
    if filename == '':
        filename = f'Report-PartialControl-{getTimeStamp()}.txt'
    session.getPartialControlConnections(filename)


def task6():
    filename = input(
        'Please enter file name with .csv extension (default = UnreachableDevices-<timeStamp>.csv): ')
    if filename == '':
        filename = f'Report-PartialBFD-{getTimeStamp()}.txt'
    session.getPartialBfdConnections(filename)


def task7():
    filename = f'FullDeviceList-{getTimeStamp()}.csv'
    session.fullDeviceList(filename)
    filename = f'FabricHeath-{getTimeStamp()}.csv'
    session.getFabricHealth(filename)
    filename = f'UnreachableDevices-{getTimeStamp()}.csv'
    session.getUnreachableDevices(filename)
    filename = f'Report-PartialControl-{getTimeStamp()}.txt'
    session.getPartialControlConnections(filename)
    filename = f'Report-PartialBFD-{getTimeStamp()}.txt'
    session.getPartialBfdConnections(filename)


def promptOptions():
    print('''
    Please choose one of the following options:
        [1] Generate full device list
        [2] Generate device list with custom headers
        [3] Gather device health baseline
        [4] Get Report - Unreachable Devices
        [5] Get Report - Partial Control Connections
        [6] Get Report - Partial WAN overlay failure
        [7] Generate All reports
        [8] Exit''')

    task_id = input('Please input number from 1 - 8: ')
    return task_id


task_id = '0'
while task_id != '00':
    task_id = promptOptions()
    if task_id == '1':
        task1()
    if task_id == '2':
        task2()
    if task_id == '3':
        task3()
    if task_id == '4':
        task4()
    if task_id == '5':
        task5()
    if task_id == '6':
        task6()
    if task_id == '7':
        task7()
    if task_id == '8':
        exit()


if session.cookie:
    promptOptions()
