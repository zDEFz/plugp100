# Plug P100
This is a fork of original work of ...

The means of this fork is to provide the library as PyPi package. 
This is used also as core part of HomeAssistant integration for TP-Link P100 at following repo.

# How to install
```pip install plugp100```

# Code example
```python
from plugp100 import p100

switch = p100.P100("<ip_address>")
switch.handshake()
switch.login_request("<username>", "<password>")

# change state of plug
switch.change_state(1, "88-00-DE-AD-52-E1") # (0 -> off, 1 -> on)

# retrieve the state of plug
is_on = switch.is_on()
state = switch.get_state() # this retrieve a complete status
```

