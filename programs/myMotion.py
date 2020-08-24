import time
import datetime
from sardana.macroserver.msexception import StopException
from sardana.macroserver.macro import Macro, macro, Type


@macro([["moveables", [
             ["moveable", Type.Moveable, None, "moveable to get position"]
             ],
             None, "list of moveables to get positions"]])
def where_moveables(self, moveables):
    """This macro prints the current moveables positions"""
    for moveable in moveables:
        self.output("%s is now at %s", moveable.getName(), moveable.getPosition())



@macro([["m_p_pairs", [
             ["moveable", Type.Moveable, None, "moveable to be moved"],
             ["position", Type.Float, None, "absolute position"]
             ],
             None, "list of moveables and positions to be moved to"]])
def move_multiple(self, m_p_pairs):
    """This macro moves moveables to the specified positions"""
    for moveable, position in m_p_pairs:
        moveable.move(position)
        self.output("%s is now at %s", moveable.getName(), moveable.getPosition())


        

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
