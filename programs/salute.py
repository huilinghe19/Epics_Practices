from sardana.macroserver.macro import Macro, macro, Type, ParamRepeat, ViewOption, iMacro

import datetime
from taurus.console.table import Table
import PyTango
from PyTango import DevState
from sardana.macroserver.msexception import StopException
from epics import Motor



@macro([["motorName", Type.String, None, "Epics Motor Name"]])
def check_motor_state(self, motorName):
    """check a epics motor state"""
    list_result= {
                  1:"DIRECTION: last raw direction; (0:Negative, 1:Positive)",
                  2:"DONE: motion is complete.",
                  3:"PLUS_LS: plus limit switch has been hit.",
                  4:"HOMELS: state of the home limit switch. ",
                  5:"Unused",
                  6:"POSITION: closed-loop position control is enabled. ",
                  7:"SLIP_STALL: Slip/Stall detected (eg. fatal following error",
                  8:"HOME: if at home position. ",
                  9:"DIRECTION: last raw direction; (0:Negative, 1:Positive)",
                  10:"PROBLEM: driver stopped polling, or hardware problem ",
                  11:"MOVING: non-zero velocity present. ",
                  12: "GAIN_SUPPORT: motor supports closed-loop position control. ",
                  13:"DIRECTION: last raw direction; (0:Negative, 1:Positive",
                  14:"MINUS_LS: minus limit switch has been hit. ",
                  15:"HOMED: the motor has been homed."
                  }

    
    epics_motor = Motor(str(motorName))
    stateID = epics_motor.get("MSTA")
    
    self.output("Epics motor {} state: {}".format(motorName, stateID))
    stateID_binary_conversion = bin(int(stateID))
    #self.output(str(stateID_binary_conversion))
    state_conversion = str(stateID_binary_conversion)[2:]
    #self.output(str(state_conversion))
    state_converse = state_conversion[::-1]
    #self.output(state_converse)
    list_state1 = []
    count = 0
    for each_char in state_converse:
        count += 1
        self.output('Bit {}: {} >>> {}'.format(count, each_char, list_result[count]))
        if each_char == str(1):
            list_state1.append(count)            
    #self.output(list_state1)

    self.output("\nProblem Diagnosis:\n  ")
    if list_state1:
        for i in list_state1:
            self.output("Bit {}: 1  >>>  {} ".format(i, list_result[i]))
    else:
        self.output("None")        
 


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


 



    
    
