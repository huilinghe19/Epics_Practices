
#from epics import *
import epics
from epics import Motor
from sardana import State, SardanaValue
from sardana.pool.controller import MotorController
from sardana.pool.controller import DefaultValue, Description, FGet, FSet, Type
from sardana.macroserver.macro import Macro, macro, Type
import time
#import configparser

#config = configparser.ConfigParser()
#config.read('configurationFile.ini')
#EPICS_PVNAME = config['EPICS_PV']['PVname']

class EpicsMotorHW(object):
    

    def __init__(self, pv_prefix, motor_prefix):
        self.EPICS_PVNAME = "{}:{}".format(str(pv_prefix), str(motor_prefix))

    def connectMotor(self, motorName, axis):
        try:
            motorHW = Motor(motorName + str(axis))
            return motorHW
        except epics.motor.MotorException:
            print("MotorException, check the epics Motor Hardware. ")
            return False

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

    STATES = {1: State.On, 2: State.Moving, 3: State.Alarm, 4: State.Fault, 5: State.Unknown}
    
    def __init__(self, inst, props, *args, **kwargs):
        MotorController.__init__(self,inst, props, *args, **kwargs)
        self.epicsmotorHW = EpicsMotorHW("IOCsim", "m")
        #super_class = super(CopleyController, self)
        #super_class.__init__(inst, props, *args, **kwargs)
    #def __del__(self):
        #del self.epicsmotorHW

    def StateOne(self, axis):
        """
        Read the axis state. One axis is defined as one motor in spock.

        """
        print("StateOne() start: read axis {} state. ".format(axis))
        
        motorHW = self.epicsmotorHW
        stateID = motorHW.getStateID(axis)
        state = self.STATES[stateID]
        #status = motorHW.getStatus(axis)
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
        position = float(motorHW.getPosition(axis))
        print("ReadOne() finished: axis {} position is {}.  ".format(axis, position))
        return position
    
    def StartOne(self, axis, position):
        """
        Move the axis(motor) to the given position.
        """
        print("StartOne() start, start the motion of axis {} ".format(axis))
        try:
            motorHW = self.epicsmotorHW        
            motorHW.move(axis, position)
        except:
            print("MotorHW MOVE ERROR")
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


