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
```
Above is needed since pipx doesn't fetch the package

# Code example

```python
import asyncio
import os

from plugp100.api.tapo_client import TapoClient
from plugp100.common.credentials import AuthCredential
from plugp100.discovery.arp_lookup import ArpLookup
from plugp100.discovery.tapo_discovery import TapoDiscovery
from plugp100.api.plug_device import PlugDevice
from plugp100.api.tapo_client import TapoClient


async def main():
    # create generic tapo api
    username = os.getenv("USERNAME", "youremailaddress")
    password = os.getenv("PASSWORD", "yourpassword")

    credentials = AuthCredential(username, password)
    client = TapoClient.create(credentials, "XX.XX.XX.XX")

    print(await client.get_device_info())
    print(await client.get_energy_usage())
    print(await client.get_current_power())
    print(await client.get_child_device_list())
    print(await client.get_child_device_component_list())
    # print(await client.set_lighting_effect(LightEffectPreset.Aurora.to_effect()))
    # plug = PlugDevice(TapoClient(username, password), "192.168.178.24")
    plug = PlugDevice(client)
    print(await plug.off())

    # light = LightDevice(TapoClient(username, password), "<tapo_device_ip>")
    # ledstrip = LedStripDevice(TapoClient(username, password), "<tapo_device_ip>")

    # - hub example
    # hub = HubDevice(client)
    # print(await hub.get_children())
    # print(await hub.get_state_as_json())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
```

