# Basic System Monitor
Simplistic system monitor based on `psutils` with a dedicated http endpoint.

It was initially developed on **Windows 10 Pro** with **PyCharm 2022.3.1 (Community Edition)** and **Python 3.11**.

## Configure and Run
To configure and run this project, follow this [README.md](https://github.com/Web3-Pi/web3-reverse-proxy/blob/main/README.md) regarding the Python configuration and the virtualenv use.

## Stats Monitoring

To start the monitoring service
- Clone the repository
- Update Python (if older than 3.11)
- Initialize venv and run the `system_monitor.py` script. It will start the monitoring service and serve the data via a http server.

### Default settings:
- default HTTP listen port
  - **7197** (variable **MONITOR_PORT** located in _config/conf.py_)
- GET endpoint
  - **/node/system/status** (variable **MONITORING_ENDPOINT** located in _config/conf.py_)

To change the monitored directory, set the required value to a variable:
- **DEFAULT_PATH** located in _config/conf.py_ (currently it should be set either to _~/.ethereum_ or _~/.lighthouse_).

### Installation
How to install (Ubuntu):
- Prerequisites
  - If necessary, configure github PAT - for details, refer to [README.md](https://github.com/Web3-Pi/web3-reverse-proxy/blob/main/README.md)
  - If necessary, install Python 3.11 and update the system configuration - more details in [README.md](https://github.com/Web3-Pi/web3-reverse-proxy/blob/main/README.md)
- Monitor
```shell
cd APPROPRIATE_DIRECTORY
git clone https://github.com/Web3-Pi/basic-system-monitor.git
cd basic-system-monitor
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
deactivate
```
- If during the installation of requirements there is a problem with `psutils`, run this command to install the required packages:
```shell
sudo apt-get install gcc python3-dev libpython3.11-dev
```

### Simple use
To run the service, follow the steps below:
```shell
cd APPROPRIATE_DIRECTORY/basic-system-monitor
source venv/bin/activate
python3 system_monitor.py  # Ctrl-c to shut down the monitor
deactivate
```

Command line parameters accepted by the script:
```shell
usage: system_monitor.py [-h] [-p PORT]

A simple monitoring tool with a HTTP endpoint

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  HTTP server listen port (default: 7197)

```

## Examples

### Running with a screen session
To run the service from an automatically created screen session named **monitor**, use this script (may be called _start_monitor.sh_) - it assumes that monitor is located in _/home/ethereum/dev/basic-system-monitor_ directory:
```shell
screen -S monitor -dm bash -c 'cd /home/ethereum/dev/basic-system-monitor;source venv/bin/activate;python3 system_monitor.py;deactivate'
```

### Queries
Querying data locally:
```shell
curl -i -H "Accept: application/json" -X GET http://127.0.0.1:7197/node/system/status
```

Querying `myhost.local` in a local network:
```shell
curl -i -H "Accept: application/json" -X GET http://myhost.local:7197/node/system/status
```
