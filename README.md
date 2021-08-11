# Cisco sd-wan-control-data-connection-check

This repo is designed to provide a quick snapshot of the SD-WAN fabric Health.

User will be prompt to choose from the following options:
```
        [1] Generate full device list
        [2] Generate device list with custom headers
        [3] Gather device health baseline
        [4] Get Report - Unreachable Devices
        [5] Get Report - Partial Control Connections
        [6] Get Report - Partial WAN overlay failure
        [7] Generate All reports
        [8] Exit
```

The generated reports will display only devices with issues and relevant information to troubleshoot.

To use this code you will need:

* Python 3.7+
* vManage user login details.

# Install and Setup

- Clone the code to local machine.

```
git clone https://github.com/HusseinOmar/cisco-sd-wan-control-data-connection-check.git
cd SD-WAN-health-check
```
- Setup Python Virtual Environment (requires Python 3.7+)

```
python3.7 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

- Run application file
```
python3 app.py
```
