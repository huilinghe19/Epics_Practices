from tango import *
from PyTango import *
db = Database()
dev_info = DbDevInfo()
dev_info.name = 'motor/simctrl/4'
dev_info._class = 'Motor'
dev_info.server = 'Sardana/simulation'
db.add_device(dev_info)
db.put_device_property(dev_info.name, {"axis":"4", "ctrl_id": "5", "id":"9"})
