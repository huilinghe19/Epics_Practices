from sardana.macroserver.macro import Macro, macro, Type, ParamRepeat, ViewOption, iMacro

import datetime
from taurus.console.table import Table
import PyTango
from PyTango import DevState
from sardana.macroserver.msexception import StopException
from epics import Motor


@macro()
def hello_world(self):
    self.output('Running hello_world...')


class HelloWorld(Macro):
    """Hello, World! macro"""

    def run(self):
        self.output("Hello, World!")




@macro()
def hello_world2(self):
    """This is an hello world macro"""
    print("Hello, World!")


from sardana import State


@macro([["motor", Type.Motor, None, "Motor to oscilate"],
        ["amplitude", Type.Float, None, "Oscilation amplitude"],
        ["integ_time", Type.Float, None, "Integration time"]])
def oscillate(self, motor, amplitude, integ_time):
    """Acquire with the active measurement group while oscillating a motor.
    """
    motion = self.getMotion([motor])
    curr_pos = motor.getPosition()
    positions = [curr_pos + amplitude / 2,
                 curr_pos - amplitude / 2]

    mnt_grp_name = self.getEnv("ActiveMntGrp")
    mnt_grp = self.getMeasurementGroup(mnt_grp_name)
    mnt_grp.putIntegrationTime(integ_time)

    i = 0
    id_ = mnt_grp.startCount()
    while mnt_grp.State() == State.Moving:
        motion.move(positions[i])
        i += 1
        i %= 2
    mnt_grp.waitCount(id_)

#oscillate('top', '20', '10')

@macro([["motorName", Type.String, None, "Epics Motor Name"]])
def check_motor_state(self, motorName):
    """check a epics motor state"""
    epics_motor = Motor(str(motorName))
    stateID = epics_motor.get("MSTA")
    
    self.output("Epics motor {} state: {}".format(motorName, stateID))
    #stateID_binary_conversion = bin(stateID)
    #print(type(stateID_binary_conversion))
    #self.output(str(stateID_binary_conversion))
    if stateID == 16802:
        self.output("HOMED: the motor has been homed.")
    ## print function will be shown in sardana server.
    #print(epics_motor.get("MSTA"))


    
