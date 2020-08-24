# Epics_Practices
epics and pyepics practices, in oder to use epics module in Sardana .

# Epics Motor

Problem: 

	>>> motor.MSTA 
	>>> 16802  (100000110100010)
	>>> motor.ATHM
	>>> 1 (at home position, can not move correctly)
	


PV: dist222dh1600:m1

change the address in .bashrc file, in oder to access the EPICS Motor
	
	>>> nano .bashrc
	"""export EPICS_CA_ADDR_LIST=134.30.209.234"""


install ca, ca tools do not work auf dide17

	>>> sudo mkdir /usr/local/share/ca-certificates/extra
	>>> sudo apt-get install ca-certificates -y
	>>> sudo update-ca-certificates

# Add motors, controllers in Sardana
Method 1: Spock Operation(standard sardana operation)

Method 2: Jive Operation(for all tango devices)

Method 3: Use Python Script with Tango/PyTango. "addDeviceinSardana.py" can be used to add devices in sardana when the server is ON. This code can also be added in the controller program, then the server must restart. 


# Operations in spock 

controller is simctrl, motors are called m1, m2 for copley motors. Old motors are called sim1, sim2. Following practices are combined with simulation motors.

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
   	1         -1      15249    1.29967 https://epics.anl.gov/bcda/synApps/motor/motorRecord.html#Fields_status
   	2         0        552     2.37312 
   	3         0        192     3.46593 
   	4         2        454     4.49761 
	Operation saved in /tmp/test.h5 (HDF5::NXscan)
	Scan #1 ended at Wed Aug  5 11:00:43 2020, taking 0:00:05.531525. Dead time 9.6% (motion dead time 2.0%)
	
Epics Motor Attributes:

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




# Control properties 
	ctrl_properties = {"PV": {Type:str, Description:"Epics Process Variable", DefaultValue:"IOCsim:m"}}

"PV" is the control property of the controller, which stands for the epics PV name. It is a default value. It can be changed to adapt to the other PVs before the server start. Make sure the control property "PV" is right. A very important issue is, once the sardana server is started(controller program is used) and the controllers and motors are already created in Tango DB/jive, the property is shown in jive and will be not easily changed. Because this is a default value. We can change it directly in jive/Tango DB. We can also delete the server and then restart the sardana server with other control properties in the controller program. That means, if control properties in the program are changed, it may not work because the tango DB has already another default one. 


For simulation epics motor "IOCsim:m1", "IOCsim:m2"..., the DefaultValue is "IOCsim:m".

For epics copley motor "dist222dh1600:m1" "dist222dh1600:m2", DefaultValue is "dist222dh1600:m". We can change it directly in Controller Properties in jive.

Note: these 2 CA addresses are different. 

Simulationsmotor:  
		
	EPICS_CA_ADDR_LIST=192.168.1.255
	
Copley Motor: 

	EPICS_CA_ADDR_LIST= 134.30.209.234



  
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

The first method is: using ca tools like caget(), caput()
  
The second method is:
  
  Define a motor from Class Motor, the mv function can be got by motor.put("VAL", int(position)) + motor("SPMG", "Go"), the other parameters can be got by motor.get() function. motor.VELO, motor.RBV can be also used to get the attributes directly.
  
   mv function can be also got by motor.move(val=int(position)). Some Paramerters can be also got and set by motor.get_position(), motor.set_position()...

# NOTE:
1, In oder to test the difference between epics process variable and epics motors, 2 different motor controllers should be created. These two controllers can not be put in the same pool, otherweise sardana will be confused and does not work well.  That means, another sardana pool must be created to test them.

2, Epics Module 

https://epics.anl.gov/bcda/synApps/motor/motorRecord.html#Fields_status 
