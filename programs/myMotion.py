import time
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

