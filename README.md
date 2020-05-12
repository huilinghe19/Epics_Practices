# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana 

NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. then these two controllers can not be put in the same pool. otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.

2. Move Implementation.

2.1 
 define a motor from Class Motor, the mv function can be got by motor.put("VAL", int(position)) + motor("SPMG", "Go"), the other parameters can be got by motor.get() function.
 
2.2
 mv function can be also got by motor.move(val=int(position)).



