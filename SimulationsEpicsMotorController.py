#from epics import *
from epics import Motor
from sardana import State, SardanaValue
from sardana.pool.controller import MotorController
from sardana.pool.controller import DefaultValue, Description, FGet, FSet, Type
import time
import configparser

config = configparser.ConfigParser()
config.read('configurationFile.ini')
EPICS_PVNAME = config['EPICS_PV']['PVname']

class EpicsMotorHW(object):
        
    def __init__(self):
        pass
        
    def getState(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motorState = int(motor.get('MSTA'))
        HighLimitSwitch = motor.get('HLS')
        LowLimitSwitch = motor.get('LLS')
        
        if motorState == 2:
            state = 1
        elif motorState == 1024: 
            state = 2
        elif motorState == 1025:
            state = 2
        elif HighLimitSwitch == 1:
            state = 3
        elif LowLimitSwitch == 1:
            state = 3
        
        return state
    
    def getStatus(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motorState = int(motor.get('MSTA'))
        HighLimitSwitch = motor.get('HLS')
        LowLimitSwitch = motor.get('LLS')
        status = "Motor HW is Unknown"
        
        if motorState == 2:
            status = "Motor HW is ON"
        elif motorState == 1024 or motorState == 1025:
            status = "Motor HW is MOVING"
        elif HighLimitSwitch == 1:
            status = "Motor HW is in ALARM. Hit hardware upper limit switch"
        elif LowLimitSwitch == 1:
            status = "Motor HW is in ALARM. Hit hardware lower limit switch"
        #elif motorState == 5:
            #status = "Motor is powered off"
        else:
            status = "Motor HW is Fault"
            
    def getLimits(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        HighLimitSwitch = motor.get('HLS')
        LowLimitSwitch = motor.get('LLS')
        switchstate = 3 * [False, ]
        if HighLimitSwitch == 1:
            switchstate[1] = True
        if LowLimitSwitch == 1:
            switchstate[2] = True
        
        return switchstate
    
    def getPosition(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        return float(motor.get_position())
    
    def getAcceleration(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        return float(motor.get('ACCL'))

    def getDeceleration(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        return float(motor.get('ACCL'))
        
    
    def getVelocity(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        return float(motor.get('VELO'))
    
    def getStepPerUnit(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        return float(motor.get('MRES'))
    
    def getBaseRate(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        return float(motor.get('VBAS'))
    
    def setAcceleration(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('ACCL', value)

    def setDeceleration(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('ACCL', value)

    def setVelocity(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('VELO', value)
        
    def setBaseRate(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('VBAS', value)
        
    def move(self, axis, position):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.move(val=int(position))  
        
    def stop(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('SPMG', 'Stop')  

    def abort(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('SPMG', 'Stop')  

class SimulationsEpicsMotorController2(MotorController):

    STATES = {1: State.On, 2: State.Moving, 3: State.Alarm, 4: State.Fault}
    
    def __init__(self, inst, props, *args, **kwargs):
        MotorController.__init__(self,inst, props, *args, **kwargs)
        self.epicsmotorHW = EpicsMotorHW()
        #super_class = super(CopleyController, self)
        #super_class.__init__(inst, props, *args, **kwargs)
    #def __del__(self):
        #del self.copleyController

    def StateOne(self, axis):
        """
        Read the axis state. One axis is defined as one motor in spock.

        """
        #print("StateOne() start")
        motorHW = self.epicsmotorHW
        state = self.STATES[motorHW.getState(axis)]
        status = motorHW.getStatus(axis)

        limit_switches = MotorController.NoLimitSwitch
        hw_limit_switches = motorHW.getLimits(axis)
        if hw_limit_switches[0]:
            limit_switches |= MotorController.HomeLimitSwitch
        if hw_limit_switches[1]:
            limit_switches |= MotorController.UpperLimitSwitch
        if hw_limit_switches[2]:
            limit_switches |= MotorController.LowerLimitSwitch
        return state,  limit_switches
  
        limit_switches = MotorController.NoLimitSwitch
        print("StateOne() finished")
        return state, limit_switches

    def ReadOne(self, axis):
        """
        Read the position of the axis(motor). 
        """
        print("ReadOne() start")

        motorHW = self.epicsmotorHW
        return float(motorHW.getPosition(axis))
        print("ReadOne finished")

    def StartOne(self, axis, position):
        """
        Move the axis(motor) to the given position.
        """
        print("StartOne() start")
        motorHW = self.epicsmotorHW
        motorHW.move(axis, position)
        print("StartOne() finished")

    def AbortOne(self, axis):
        """
        Abort the axis(motor).
        """
       
        motorHW = self.epicsmotorHW
        motorHW.abort(axis)
        
    def GetAxisPar(self, axis, name):
        motorHW = self.epicsmotorHW
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



