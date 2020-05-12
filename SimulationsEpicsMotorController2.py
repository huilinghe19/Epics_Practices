#from epics import *
from epics import Motor
from sardana import State, SardanaValue
from sardana.pool.controller import MotorController
from sardana.pool.controller import DefaultValue, Description, FGet, FSet, Type
import time

class SimulationsEpicsMotorController2(MotorController):

    STATES = {"ON": State.On, "MOVING": State.Moving, "FALUT": State.Fault}

    def __init__(self, inst, props, *args, **kwargs):
        MotorController.__init__(self,inst, props, *args, **kwargs)
        #super_class = super(CopleyController, self)
        #super_class.__init__(inst, props, *args, **kwargs)
    #def __del__(self):
        #del self.copleyController

    def StateOne(self, axis):
        """
        Read the axis state. One axis is defined as one motor in spock.

        """
        print "StateOne() start"
        #motorState = int(caget("IOCsim:m{}.MSTA".format(axis)))
        motor = Motor('IOCsim:m{}'.format(axis))
        motorState = int(motor.get('MSTA'))
        print "motor State :", motorState
        if int(motorState) == 2:
            state = self.STATES["ON"]
        elif int(motorState) == 1024: 
            state = self.STATES["MOVING"]
        elif int(motorState) == 1025:
            state = self.STATES["MOVING"]
        else:
            state = self.STATES["FAULT"]
        limit_switches = MotorController.NoLimitSwitch
        print "StateOne() finished"
        return state, limit_switches

    def ReadOne(self, axis):
        """
        Read the position of the axis(motor). 
        """
        print "ReadOne() start"
        #return float(caget("IOCsim:m{}.RBV".format(axis)))
        motor = Motor('IOCsim:m{}'.format(axis))
        #return float(motor.get('RBV'))
	return float(motor.get_position())
        print "ReadOne finished"

    def StartOne(self, axis, position):
        """
        Move the axis(motor) to the given position.
        """
        print "StartOne() start"
        #caput("IOCsim:m{}.VAL".format(axis), int(position))
        #caput("IOCsim:m{}.SPMG".format(axis), "Go")
        motor = Motor('IOCsim:m{}'.format(axis))
        #motor.put('VAL', int(position))
        #motor.put('SPMG', 'Go')
	motor.move(val=int(position))        
        time.sleep(0.5)
        print "StartOne() finished"

    def AbortOne(self, axis):
        """
        Abort the axis(motor).
        """
        #caput("IOCsim:m{}.SPMG".format(axis), "Stop")
        motor = Motor('IOCsim:m{}'.format(axis))
        motor.put('SPMG', 'Stop')  
        
    def GetAxisPar(self, axis, name):
        if name == "velocity":            
            #ans = float(caget("IOCsim:m{}.VELO".format(axis)))
            motor = Motor('IOCsim:m{}'.format(axis))
            ans = float(motor.get('VELO'))
            
        #elif name == "acceleration":
        #elif name == "deceleration":
        return ans

    def SetAxisPar(self, axis, name, value):
        if name == "velocity":
            #caput("IOCsim:m{}.VELO".format(axis), value)
            motor = Motor('IOCsim:m{}'.format(axis))
            motor.put('VELO', value)


