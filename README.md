# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana 

The way to define the epics ca server:


> EPICS_CA_AUTO_ADDR_LIST=NO

> EPICS_CA_ADDR_LIST=192.168.1.256


NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. then these two controllers can not be put in the same pool. otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.SimulationsEpicsMotorController.py


2. Move Implementation.

  The first method is: using caget(), caput()
  
  The second method is:
  
  Define a motor from Class Motor, the mv function can be got by motor.put("VAL", int(position)) + motor("SPMG", "Go"), the other parameters can be got by motor.get() function.
  
   mv function can be also got by motor.move(val=int(position)). Some Paramerters can be also got and set by motor.get_position(), motor.set_position()...


Once the file comes from another computer with the scp method, then there will be a problem to change it or use it under oil@dide17. Because the permissions for the file need to be reconsidered. Sardana needs the oil permissions.
