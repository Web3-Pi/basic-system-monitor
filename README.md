# Basic System Monitor
Simplistic system monitor based on `psutils` with a dedicated http endpoint.

It was initially developed on **Windows 10 Pro** with **PyCharm 2022.3.1 (Community Edition)** and **Python 3.11**.

## Configure and Run
To configure and run this project, follow this [README.md](https://github.com/jimmyisthis/web3-reverse-proxy/blob/main/README.md) regarding the Python configuration and the virtualenv use.

## Stats Monitoring
To start the monitoring service, initialize venv and run the `system_monitor.py` script. It will start the monitoring service and serve the data via a http server.

Default settings:
- default HTTP listen port
  - **7197** (variable **MONITOR_PORT** located in _config/conf.py_)
- GET endpoint
  - **/node/system/status** (variable **MONITORING_ENDPOINT** located in _config/conf.py_)

To change the monitored directory, set the required value to variable:
- **SYSTEM_STATS_UPDATE_INTERVAL** located in _config/conf.py_ (currently it should be set either to _~/.ethereum_ or _~/.lighthouse_).

Usage:
```shell
python3 system_monitor.py
```

### Examples
Querying data locally:
```shell
curl -i -H "Accept: application/json" -X GET http://127.0.0.1:7197/node/system/status
```

Querying `myhost.local` in a local network:
```shell
curl -i -H "Accept: application/json" -X GET http://myhost.local:7197/node/system/status
```

### Installation
How to install:
```shell
git clone https://github.com/Web3-Pi/basic-system-monitor.git
pip3 install -r requirements.txt
```
