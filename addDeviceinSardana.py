from tango import *
from PyTango import *

db = Database()
dev_info = DbDevInfo()
MaxDevice = 8
DeviceList=[]
for i in range(5, MaxDevice+1):
    deviceName='motor/simctrl/'+str(i)
    DeviceList.append(deviceName)
print(DeviceList)
for i in DeviceList:
    dev_info.name = i
    dev_info._class = 'Motor'
    dev_info.server = 'Sardana/simulation'
    db.add_device(dev_info)
    db.put_device_property(dev_info.name, {"ctrl_id": "5"})
