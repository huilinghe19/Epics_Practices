# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana .

# Add motors, controllers in Sardana
Method 1: Spock Operation(standard sardana operation)

Method 2: Jive Operation(for all tango devices)

Method 3: Use Python Script with Tango/PyTango. "addDeviceinSardana.py" can be used to add devices in sardana when the server is ON. This code can also be added in the controller program, then the server must restart. 


# Define Epics PV in spock 

controller is simctrl, motor is sim1

dial/user limit are different in epics and sardana. They are seperate concepts. Users can define both of them in epics and sardana, the ranges must be valid, but the ranges can be different. The dial limit values in sardana do not come from epics module. They are set by the sardana users. The range of the epics PV >= the range of sardana motor.     
	
	>>> Pool_simulation_1.put_property({"PoolPath":["/controllers/simulationEpics"]}) 
	>>> defctrl SimulationsEpicsMotorController2 simctrl PV="IOCsim:m"
	>>> defelem sim1 simctrl 1
	>>>  wa
	Current positions (user, dial) on 2020-07-30 09:42:49.140863

          sim1
	User   10.0000
	Dial   10.0000

	>>> %set_user_pos sim1 1
	sim1 reset from 10.0000 (offset 0.0000) to 1.0000 (offset -9.0000)
	>>> %set_lm sim1 -4 4 
	sim1 limits set to -4.0000 4.0000 (dial units)
	>>> %set_lim sim1 -5 5
	sim1 limits set to -5.0000 5.0000 (user units)
	>>> wm sim1
                   sim1
	User               
	 High               5.0
	 Current            1.0
	 Low               -5.0
	Dial               
	 High               4.0
	 Current           10.0
	 Low               -4.0

Before using sardana tools macroexecutor and sequencer, something must be already set such as storage and measurementGoup and so on. Otherweise the execution can not run well. Add ct, Add channel, measurementGoup, add senv file. 
	
	>>> defctrl NetworkTrafficCounterTimerController netctrlsim interface eno1
	>>> defelem netsim netctrlsim 1 
	>>> uct 1 netsim
    		netsim
    		0.0000

	>>> uct 5 netsim
    		netsim
  		192.0000
	
	>>> expconf (Set configuration. add new measurement Group: simMeasureGroup, add channel: netsim, add storage file name: test.h5, file path: /tmp)
	
	>>> ascan sim1 -2 2 4 1
	Operation will be saved in /tmp/test.h5 (HDF5::NXscan from NXscanH5_FileRecorder)
	Scan #1 started at Wed Aug  5 11:00:37 2020. It will take at least 0:00:13.900000
 	#Pt No     sim1     netsim      dt   
   	0         -2       360     0.21673 
   	1         -1      15249    1.29967 
   	2         0        552     2.37312 
   	3         0        192     3.46593 
   	4         2        454     4.49761 
	Operation saved in /tmp/test.h5 (HDF5::NXscan)
	Scan #1 ended at Wed Aug  5 11:00:43 2020, taking 0:00:05.531525. Dead time 9.6% (motion dead time 2.0%)

# Control properties 
	ctrl_properties = {"PV": {Type:str, Description:"Epics Process Variable", DefaultValue:"IOCsim:m"}}

"PV" is the control property of the controller, which stands for the epics PV name. It is a default value. It can be changed to adapt to the other PVs before the server start. Make sure the control property "PV" is right. A very important issue is, once the sardana server is started(controller program is used) and the controllers and motors are already created in Tango DB/jive, the property is shown in jive and will be not easily changed. Because this is a default value. We can change it directly in jive/Tango DB. We can also delete the server and then restart the sardana server with other control properties in the controller program. That means, if control properties in the program are changed, it may not work because the tango DB has already another default one. 

# Motor Attributes

The standard sardana motor attributes like "position", "velocity", "acceleration", "deceleration", "base_rate", "step_per_unit" can be easily got in spock. Other epics motor attributes can not be got by default attribute settings. But we can write extra neu marcos to get/set them. 

	>>> simctrl.get_db_host()
	Result [3]: 'dide17.basisit.de'
	>>> simctrl.get_db_port()
	Result [4]: '10000'
	>>> simctrl.get_property("PV")
	Result [7]: {'PV': ['IOCsim:m']}
	>>> sim1.position
	Result [51]: 1.0
	>>> sim1.base_rate
	Result [50]: 0.1
	>>>  sim1.velocity
	Result [53]: 1.0
	>>> sim1.limit_switches
	Result [52]: array([False, False, False])


  
# The way to start the epics ca server:
	cd /hzb/EPICS01/motor-6.11-old/iocBoot/iocSim
	### start the simulation server
	./st.cmd.unix
	### run the program in the background
	screen -dmS EPICS-MotorSimulation ./st.cmd.unix
	### set environment variable 
	EPICS_CA_AUTO_ADDR_LIST=NO
	EPICS_CA_ADDR_LIST=192.168.1.255


# Move Implementation.

## The first method is: using ca tools like caget(), caput()
  
## The second method is:
  
  Define a motor from Class Motor, the mv function can be got by motor.put("VAL", int(position)) + motor("SPMG", "Go"), the other parameters can be got by motor.get() function.
  
   mv function can be also got by motor.move(val=int(position)). Some Paramerters can be also got and set by motor.get_position(), motor.set_position()...

# Permissions Problem 
Once the file comes from another computer with the scp method, then there will be a problem to change it or use it under oil@dide17. Because the permissions for the file need to be reconsidered. Sardana needs the original huiling permissions.

On the same computer dide17, if the user is not original huiling, then Sardana can not be used. The error message is:  

"pkg_resources.DistributionNotFound: The 'PyTango>=9.2.5' distribution was not found and is required by sardana"

The problem occurs with tango installation. Wenn I install tango at the first time, it is necessary to put "tango", "tango" as user and password for MySQL. Just user "huiling" has the right to import tango. "import tango" does not work when the user is different. Although jive can be opened, but the usage of tango can not be sure.

# NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. then these two controllers can not be put in the same pool. otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.SimulationsEpicsMotorController.py
