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
        if not motor:
            print("No axis {} connected. ".format(axis))
            return 
             
        else:
            motorState = int(motor.get('MSTA'))
            HighLimitSwitch = motor.get('HIGH')
            LowLimitSwitch = motor.get('LOW')
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
             HighLimitSwitch = motor.get('HIGH')
             LowLimitSwitch = motor.get('LOW')

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
    
    def setLimitsw(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        HighLimitSwitch = motor.put('HIGH', 1)
        LowLimitSwitch = motor.put('LOW', 1)
        switchstate = 3 * [False, ]
        if HighLimitSwitch == 1:
            switchstate[1] = True
        if LowLimitSwitch == 1:
            switchstate[2] = True
        
        return switchstate
    
    def getLimitsw(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        HighLimitSwitch = int(motor.get('HIGH'))
        LowLimitSwitch = int(motor.get('LOW'))
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
        
### The following methods are the extra attributes in epics motor.
### These attributes are not used in MotorController class.
    def getBackSpeed(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('BVEL'))    
    def setBackspeed(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('BVEL', value)
        
### in spock, %set_lim, %set_lm are used to set the user limits and dial limits.
### %set_pos and %set_user_pos are used to set the dial and user position.
    def getDial_high_limit(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DHLM'))
    def setDial_high_limit(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DHLM', value)
        
    def getDial_low_limit(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DLLM'))    
    def setDial_low_limit(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DLLM', value)
        
    def getDone_moving(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DMOV'))    
    def setDone_moving(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DMOV', value)
    
    def getDial_readback(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DRBV'))    
    def setDial_readback(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DRBV', value)
    
    def getDial_drive(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DVAL'))    
    def setDial_drive(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DVAL', value)
        
    def getDial_drive(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DVAL'))    
    def setDial_drive(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DVAL', value)
        
    def getDial_drive(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('DVAL'))    
    def setDial_drive(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('DVAL', value)
        
    def getLow_limit(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('LLM'))    
    def setLow_limit(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('LLS', value)
        
    def getHigh_limit(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('HLM'))    
    def setHigh_limit(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('HLS', value)
        
    def getReadback(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('RBV'))    
    def setReadback(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('RBV', value)
        
    def getRaw_readback(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('RRBV'))    
    def setRaw_readback(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('RRBV', value)
        
    def getRaw_drive(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('RVAL'))    
    def setRaw_drive(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('RVAL', value)
        
    def getStop_go(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('SPMG'))    
    def setStop_go(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('SPMG', value)
        
    def getDrive(self, axis):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        return float(motor.get('VAL'))    
    def setDrive(self, axis, value):
        motor = self.connectMotor(self.EPICS_PVNAME, str(axis))
        motor.put('VAL', value)
    
    
class SimulationsEpicsMotorController2(MotorController):
    #PV_NAME = "IOCsim:m"

    MaxDevice = 8
    
    ctrl_properties = {"PV": {Type:str, Description:"Epics Process Variable", DefaultValue:"IOCsim:m"}}
    
    STATES = {1: State.On, 2: State.Moving, 3: State.Alarm, 4: State.Fault, 5: State.Unknown}
    
    def __init__(self, inst, props, *args, **kwargs):
        MotorController.__init__(self, inst, props, *args, **kwargs)
        self.epicsmotorHW = EpicsMotorHW(self.PV)
        #super_class = super(CopleyController, self)
        #super_class.__init__(inst, props, *args, **kwargs)
        ### initialization
        print("Epics PV Initialization:::", self.epicsmotorHW)
        print("Epics PV Prefix:::", self.PV)
            
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
        print("State ID: ", stateID)
        
        ### if just state is needed, then use the following, the status is default in sardana
        state = self.STATES[stateID]
        #print("Result state : ",  state)
        #status = motorHW.getStatus(axis)
        ###
        
        if not stateID:
            print("No State ID from epicsmotorHW")
          
        ### if state and status are needed, then use the following
        #elif stateID == 1:
            #return State.On, " \n Motor is stopped after moving"
        #elif stateID == 2:
            #return State.Moving, " \n Motor is moving, do not break the motion"
        #elif stateID == 3:
            #return State.Alarm, " Motor is in Alarm"
        #elif stateID == 4:
            #return State.Alarm, " Motor has an error"
        #elif stateID == 5:
            #return State.Unknown, " Motor is Unknown, please check the epics PV and the connection."

        limit_switches = MotorController.NoLimitSwitch
        hw_limit_switches = motorHW.getLimitsw(axis)
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
        ans = float(motorHW.getPosition(axis))
        print("ReadOne() finished, position is: {} ".format(ans))
        return ans
    
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
        #elif name == "dial_low_limit":
            #ans = motorHW.getDial_low_limit(axis)
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
        #elif name == "dial_low_limit":
            #motorHW.setDial_low_limit(axis, value)

