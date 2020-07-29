import time
import epics
from epics import Motor
from sardana import State, SardanaValue
from sardana.pool.controller import MotorController, Type, Description,\
    DefaultValue

#import configparser
#config = configparser.ConfigParser()
#config.read('configurationFile.ini')
#EPICS_PVNAME = config['EPICS_PV']['PVname']

class EpicsMotorHW(object):
    

    def __init__(self, name):
        self.EPICS_PVNAME = str(name)
        
    #def getPVname(self, pv_prefix, motor_prefix):
        #return "{}:{}".format(str(pv_prefix), str(motor_prefix))
    
    def connectMotor(self, name, axis):
        try:
            motorHW = Motor(str(name) + str(axis))
            print("EpicsMotor {} Connected ".format(motorHW))
            return motorHW
        except epics.motor.MotorException:
            print("MotorException, check the epics Motor Hardware. ")
            return 

    def getStateID(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        stateID = 5
        if not motor:
            print("No axis {} connected. ".format(axis))
            stateID = 4
        else:
            motorState = int(motor.get('MSTA'))
            HighLimitSwitch = motor.get('HLS')
            LowLimitSwitch = motor.get('LLS')
            if motorState == 10 or motorState == 2:
                stateID = 1
            elif motorState == 1024: 
                stateID = 2
            elif motorState == 1025:
                stateID = 2
            elif HighLimitSwitch == 1:
                stateID = 3
            elif LowLimitSwitch == 1:
                stateID = 3
      
        return stateID
    
    def getStatus(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        status = "Motor HW is Unknown"
        if not motor:
             status = "Motor HW is Fault"
 
        else:            
             motorState = int(motor.get('MSTA'))
             HighLimitSwitch = motor.get('HLS')
             LowLimitSwitch = motor.get('LLS')

             if motorState == 10 or motorState == 2:
                 status = "Motor HW is ON"
             elif motorState == 1024 or motorState == 1025:
                 status = "Motor HW is MOVING"
             elif HighLimitSwitch == 1:
                 status = "Motor HW is in ALARM. Hit hardware upper limit switch"
             elif LowLimitSwitch == 1:
                 status = "Motor HW is in ALARM. Hit hardware lower limit switch"
             elif motorState == 5:
                 status = "Motor is powered off"

        return status
    
    def getLimits(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        HighLimitSwitch = motor.get('HLS')
        LowLimitSwitch = motor.get('LLS')
        switchstate = 3 * [False, ]
        if HighLimitSwitch == 1:
            switchstate[1] = True
        if LowLimitSwitch == 1:
            switchstate[2] = True
        
        return switchstate
    
    def getPosition(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get_position())
    
    def getAcceleration(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('ACCL'))

    def getDeceleration(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('ACCL'))
        
    
    def getVelocity(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('VELO'))
    
    def getStepPerUnit(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('MRES'))
    
    def getBaseRate(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('VBAS'))
    
    def setAcceleration(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('ACCL', value)

    def setDeceleration(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('ACCL', value)

    def setVelocity(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('VELO', value)
        
    def setBaseRate(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('VBAS', value)
        
    def move(self, axis, position):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.move(val=int(position))  
        
    def stop(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('SPMG', 'Stop')  

    def abort(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('SPMG', 'Stop')  

class SimulationsEpicsMotorController2(MotorController):
    #PV_NAME = "IOCsim:m"

    MaxDevice = 9
    
    ctrl_properties = {"PV": {Type:str, Description:"Epics Process Variable", DefaultValue:"IOCsim:m"}}
    
    STATES = {1: State.On, 2: State.Moving, 3: State.Alarm, 4: State.Fault, 5: State.Unknown}
    
    def __init__(self, inst, props, *args, **kwargs):
        MotorController.__init__(self, inst, props, *args, **kwargs)
        self.epicsmotorHW = EpicsMotorHW(self.PV)
        #super_class = super(CopleyController, self)
        #super_class.__init__(inst, props, *args, **kwargs)
        

        
    def AddDevice(self, axis):
        if axis > self.MaxDevice:
            raise Exception("Max. 10 devices are allowed")

    def DeleteDevice(self, axis):
        pass
    
    
    def StateOne(self, axis):
        """
        Read the axis state. One axis is defined as one motor in spock.

        """
        print("StateOne() start: read axis {} state. ".format(axis))
        
        motorHW = self.epicsmotorHW
        stateID = motorHW.getStateID(axis)
        ### if just state is needed, then use the following, the status is default in sardana
        state = self.STATES[stateID]
        #status = motorHW.getStatus(axis)
        ###

        ### if state and status are needed, then use the following
        if stateID == 1:
            return State.On, " \n Motor is stopped after moving"
        elif stateID == 2:
            return State.Moving, " \n Motor is moving, do not break the motion"
        elif stateID == 3:
            return State.Alarm, " Motor is in Alarm"
        elif stateID == 4:
            return State.Alarm, " Motor has an error"
        elif stateID == 5:
            return State.Unknown, " Motor is Unknown, please check the epics PV and the connection."

       
        print("Result state : ",  state)
        limit_switches = MotorController.NoLimitSwitch
        hw_limit_switches = motorHW.getLimits(axis)
        if hw_limit_switches[0]:
            limit_switches |= MotorController.HomeLimitSwitch
        if hw_limit_switches[1]:
            limit_switches |= MotorController.UpperLimitSwitch
        if hw_limit_switches[2]:
            limit_switches |= MotorController.LowerLimitSwitch

        print("StateOne() finished. ")
        return state,  limit_switches
  
    def ReadOne(self, axis):
        """
        Read the position of the axis(motor). 
        """
        print("ReadOne() start: read axis {}  position. ".format(axis))
        motorHW = self.epicsmotorHW
        
        return float(motorHW.getPosition(axis))
    
    def StartOne(self, axis, position):
        """
        Move the axis(motor) to the given position.
        """
        print("StartOne() start, start the motion of axis {} ".format(axis))
        
        motorHW = self.epicsmotorHW        
        motorHW.move(axis, position)
       
        print("StartOne() finished: the motion of axis {} is started. ")

    def AbortOne(self, axis):
        """
        Abort the axis(motor).
        """
        print("AbortOne() start: abort the motion of axis {} ".format(axis))
        motorHW = self.epicsmotorHW
        motorHW.abort(axis)
        print("AbortOne() finished: the motion of axis {} is aborted. ")
        
    def GetAxisPar(self, axis, name):
        motorHW = self.epicsmotorHW
        #name = name.lower()
        if name == "velocity":            
            ans = motorHW.getVelocity(axis)
        elif name == "acceleration":
            ans = motorHW.getAcceleration(axis)      
        elif name == "deceleration":
            ans = motorHW.getDeceleration(axis)  
        elif name == "base_rate":
            ans = motorHW.getBaseRate(axis)        
        elif name == "step_per_unit":
            ans = motorHW.getStepPerUnit(axis)
            
        return ans

    def SetAxisPar(self, axis, name, value):
        motorHW = self.epicsmotorHW
        #name = name.lower()
        
        if name == "velocity":
            motorHW.setVelocity(axis, value)
        elif name == "acceleration":
            motorHW.setAcceleration(axis, value)
        elif name == "deceleration":
            motorHW.setDeceleration(axis, value)
        elif name == "base_rate":
            motorHW.setBaseRate(axis, value)
        elif name == "step_per_unit":
            motorHW.setStepPerUnit(axis, value)

