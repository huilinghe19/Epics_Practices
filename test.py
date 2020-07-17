import configparser

config = configparser.ConfigParser()
config.read('configurationFile.ini')


class EpicsMotorHW(object):
    
    EPICS_PVNAME = config['EPICS_PV']['PVname']
    EPICS_PVNUMBER = config['EPICS_PV']['PVnumber']
    
    def __init__(self):
        pass
        
    def getState(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motorState = int(motor.get('MSTA'))
        return motorState
    
    def getStatus(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motorState = int(motor.get('MSTA'))
        status = "Motor HW is Unknown"
        if motorState == 1024 or motorState == 1025:
            status = "Motor HW is MOVING"
        elif motorState == 2:
            status = "Motor HW is ON"
        #elif motorState == 3:
            #status = "Motor HW is in ALARM. Hit hardware lower limit switch"
        #elif motorState == 4:
            #status = "Motor HW is in ALARM. Hit hardware upper limit switch"
        #elif motorState == 5:
            #status = "Motor is powered off"
            
    def getLimits(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        HighLimitSwitch = motor.get('HLS')
        LowLimitSwitch = motor.get('LLS')
        switchstate = 3 * [False, ]
        if LowLimitSwitch:
            switchstate[2] = True
        if HighLimitSwitch:
            switchstate[1] = True
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
    
    def setAcceleration(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('ACCL', value)

    def setDeceleration(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('ACCL', value)

    def setVelocity(self, axis, value):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('VELO', value)
        
    def move(self, axis, position):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.move(val=int(position))  
        
    def stop(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('SPMG', 'Stop')  

    def abort(self, axis):
        motor = Motor(EPICS_PVNAME + str(axis))
        motor.put('SPMG', 'Stop')  
