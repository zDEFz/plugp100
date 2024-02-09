# Plug P100
This is a fork of original work of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python)

The purpose of this fork is to provide the library as PyPi package. 

# How to install
```bash
git clone https://github.com/petretiandrea/plugp100
cd plugp100
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-dev.txt
nano turn-off-turn-on.py # add your data
nano ~/.bashrc
speaker-right-off() { cd ~/git/plugp100; source venv/bin/activate;  python3 turn-off-turn-on.py 192.168.178.21 off ; }
speaker-left-off() { cd ~/git/plugp100; source venv/bin/activate;  python3 turn-off-turn-on.py 192.168.178.24 off ; }
speaker-right-on() { cd ~/git/plugp100; source venv/bin/activate;  python3 turn-off-turn-on.py 192.168.178.21 on ; }
speaker-left-on() { cd ~/git/plugp100; source venv/bin/activate;  python3 turn-off-turn-on.py 192.168.178.24 on ; }
```
Above is needed since pipx doesn't fetch the package

# Code example

```python
#　turn-off-turn-on.py 
import asyncio
import os
import sys

from plugp100.api.tapo_client import TapoClient
from plugp100.common.credentials import AuthCredential
from plugp100.api.plug_device import PlugDevice

async def main(ip_address, action):
    # create generic tapo api
    username = os.getenv("USERNAME", "youremail")
    password = os.getenv("PASSWORD", "yourpassword")

    credentials = AuthCredential(username, password)
    client = TapoClient.create(credentials, ip_address)

    print(await client.get_device_info())
    print(await client.get_energy_usage())
    print(await client.get_current_power())
    print(await client.get_child_device_list())
    print(await client.get_child_device_component_list())

    plug = PlugDevice(client)
    if action.lower() == "on":
        print("Turning plug on...")
        print(await plug.on())
    elif action.lower() == "off":
        print("Turning plug off...")
        print(await plug.off())
    else:
        print("Invalid action. Please specify 'on' or 'off'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python turn-off-turn-on.py <ip_address> <action>")
        sys.exit(1)

    ip_address = sys.argv[1]
    action = sys.argv[2]
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(ip_address, action))
    loop.close()
```

