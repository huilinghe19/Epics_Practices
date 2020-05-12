# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana 

NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. then these two controllers can not be put in the same pool. otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.

2, if we use Class Motor from epics, the mv function in sardana dose not work, "CASeverityException:  put returned 'Write access denied'". We can get the position, velocity and state. But we can not write things into the motor. 

