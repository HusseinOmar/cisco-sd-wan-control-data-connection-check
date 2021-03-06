[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/HusseinOmar/cisco-sd-wan-control-data-connection-check)
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

# Requirements

To use this code you will need:

* Python 3.7+
* vManage user login details.

# Install and Setup

- Clone the code to local machine.

```
git clone https://github.com/HusseinOmar/cisco-sd-wan-control-data-connection-check.git
cd cisco-sd-wan-control-data-connection-check
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
![image](https://user-images.githubusercontent.com/25336119/130369414-55ea13fd-8766-4ea9-9fc0-6f7d308226be.png)

# Sample Reports
Sample Reports generated with this code are here https://github.com/HusseinOmar/cisco-sd-wan-control-data-connection-check/tree/main/sample-reports

# Other Files
[templateHeaders-option[2].csv] can be used in option#2 to generate device list with custom headers

# License
CISCO SAMPLE CODE LICENSE
