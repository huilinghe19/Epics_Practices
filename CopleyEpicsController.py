from epics import *
from sardana import State, SardanaValue
from sardana.pool.controller import MotorController
from sardana.pool.controller import DefaultValue, Description, FGet, FSet, Type

class EpicsObject(object):   
    def __init__(self):
        pass
    def definePosition(self, axis, position):
        #caput("difftarget",  int(int(position) - int(caget("pos"))))
        caput("axis0:target", int(position))
    def move(self, axis):
        caput("axis0:start", 1)
    def getPosition(self, axis):
        return float(caget("axis0:pos"))
    def getState(self, axis):
        return int(caget("axis0:state"))
        
    

          
class CopleyEpicsController(MotorController):

    STATES = {"ON": State.On, "MOVING": State.Moving, "FALUT": State.Fault}

    def __init__(self, inst, props, *args, **kwargs):
        MotorController.__init__(self,inst, props, *args, **kwargs)
        #super_class = super(CopleyController, self)
        #super_class.__init__(inst, props, *args, **kwargs)
        self.copleyController = EpicsObject()
    def __del__(self):
        del self.copleyController

    def StateOne(self, axis):
        """
        Read the axis state. One axis is defined as one motor in spock. 
      
        """
        
        controller = self.copleyController
        motorState = int(controller.getState(axis))
        if motorState == 0:
            state = self.STATES["ON"]
        elif motorState == 134217728:
            state = self.STATES["MOVING"]
        else: 
            state = self.STATES["FAULT"]
        limit_switches = MotorController.NoLimitSwitch
        return state, limit_switches
        
    def ReadOne(self, axis):
        """
        Read the position of the axis(motor). When "wa" or "wm motor_name"is called in spock, this method is used. 
        """
 
        controller = self.copleyController
        return controller.getPosition(axis)

    def DefinePosition(self, axis, position):
      
        controller = self.copleyController
        controller.definePosition(axis, position)
        #caput("difftarget",  int(position) - int(caget("pos")))
        #caput("target", int(position))
        
    def StartOne(self, axis, position):
        """
        Move the axis(motor) to the given position. 
        """
        controller = self.copleyController
        controller.definePosition(axis, position)
        controller.move(axis)
      
    def AbortOne(self, axis):
        """
        Abort the axis(motor).
        """
        caput('axis0:stop', 1)
        
    def GetAxisPar(self, axis, name):
        if name == "velocity":
            ans = float(caget("axis0:vel"))  
            
        #elif name == "acceleration":    
        #elif name == "deceleration":
        
        return ans
    
    def SetAxisPar(self, axis, name, value):
        if name == "velocity":
            caput("axis0:vel", value) 
        #elif name == "acceleration":
        #elif name == "deceleration":
        
