import pyvisa
import time

class HP33120A(object):
    """doc"""
    def __init__(self, GPIB_adress):
        self.addres    = GPIB_adress
        self.shape     = "SIN"
        self.Vpp       = 1.5
        self.VU        = "VPP"
        self.RM        = pyvisa.ResourceManager() # set resource manager


#OUTPUT CONFIGURATION COMMANDS

    def setFREQ(self, value):
        self.RM.open_resource(self.addres).write("SOUR:FREQ %f"%value)

    def readFREQ(self):
        return self.RM.open_resource(self.addres).query("SOUR:FREQ?")

    def setShape(self, param):
        if str(param) == "SIN":
            self.RM.open_resource(self.addres).write("FUNC:SHAP SIN")

    def readShape(self):
        return self.RM.open_resource(self.addres).query("FUNC:SHAP?")

    def setVPP(self, value):
        self.RM.open_resource(self.addres).write("VOLT %f"%(value))

    def readVPP(self, MIN = False, MAX = False):
        if MIN:
            return self.RM.open_resource(self.addres).query("VOLT? MIN")
        elif MAX:
            return self.RM.open_resource(self.addres).query("VOLT? MAX")
        else:
            return self.RM.open_resource(self.addres).query("VOLT?")

    def setVoltOffset(self, value):
        self.RM.open_resource(self.addres).write("VOLT:OFFS %f" % (value))

    def readVoltOffset(self, MIN = False, MAX = False):
        if MIN:
            return self.RM.open_resource(self.addres).query("VOLT:OFFS? MIN")
        elif MAX:
            return self.RM.open_resource(self.addres).query("VOLT:OFFS? MAX")
        else:
            return self.RM.open_resource(self.addres).query("VOLT:OFFS?")

    def setDcycle(self, value):
        self.RM.open_resource(self.addres).write("PULS:DCYC %f" % (value))

    def readDcycle(self):
        return  self.RM.open_resource(self.addres).query("PULS:DCYC?")

    def setVoltUnit(self):
        if "VPP" in self.VU:
            self.RM.open_resource(self.addres).write("VOLT:UNIT VPP")
        elif "VRMS" in self.VU:
            self.RM.open_resource(self.addres).write("VOLT:UNIT VRMS")
        elif "DBM" in self.VU:
            self.RM.open_resource(self.addres).write("VOLT:UNIT DBM")
        elif "DEF" in self.VU:
            self.RM.open_resource(self.addres).write("VOLT:UNIT DEF")
        else:
            self.RM.open_resource(self.addres).write("VOLT:UNIT DEF")

    def readVoltUnit(self):
        return self.RM.open_resource(self.addres).query("VOLT:UNIT?")

    def setOutPutLoad(self, value = "50"):
        if "INF" in value:
            self.RM.open_resource(self.addres).write("OUTP:LOAD INF")
        elif "MIN" in value:
            self.RM.open_resource(self.addres).write("OUTP:LOAD MIN")
        elif "MAX" in value:
            self.RM.open_resource(self.addres).write("OUTP:LOAD MIN")
        else:
            self.RM.open_resource(self.addres).write("OUTP:LOAD 50")

    def readOutPutLoad(self, MIN = False, MAX = False):
        if MIN:
            return self.RM.open_resource(self.addres).query("OUTP:LOAD? MIN")
        elif MAX:
            return self.RM.open_resource(self.addres).query("OUTP:LOAD? MAX")
        else:
            return self.RM.open_resource(self.addres).query("OUTP:LOAD? MIN")

    def setOutPutSYNC(self, status = "ON"):
        if "ON" in status:
            self.RM.open_resource(self.addres).write("OUTP:SYNC ON")
        elif "OFF" in status:
            self.RM.open_resource(self.addres).write("OUTP:SYNC OFF")
        else:
            self.RM.open_resource(self.addres).write("OUTP:SYNC ON")

    def readOutPutSYNC(self):
        return self.RM.open_resource(self.addres).query("OUTP:SYNC?")

    def setDefaultConfig(self):
        self.setShape("SIN")
        self.VU = "DEF"
        self.setVoltUnit()
        self.setFREQ(200000.5)
        self.setVPP(self.Vpp)
        self.setVoltOffset(0.0)
        # self.setDcycle(0)
        self.setOutPutLoad("50")
        self.setOutPutSYNC("ON")

    def printConfig(self):
        print("Config of setup")
        print("\tShape: " + self.readShape())
        print("\tVoltage units : " + self.readVoltUnit())
        print("\tFrequency: " + self.readFREQ())
        print("\tVPP = " +  self.readVPP())
        print("\tVoltage offset = "+ self.readVoltOffset())
        print("\tDcycle = " + self.readDcycle())
        print("\tOutPutLoad = " + self.readOutPutLoad())
        # print(len(self.readOutPutSYNC()))

    def MakeCFG_file(self):
        with open("HPcfg.dat", 'w') as write:
            write.write("#HP/Agilent config file\n")
            write.write("Addres : %s\n"% self.addres)
            write.write("Function:Shape - %s\n"%self.shape)
            write.write("Voltage:Unit - %s\n"%self.VU)
            write.write("Voltage:Amplitude - %s\n"%self.Vpp)
        print("***********************")
        print("**CFG file is written**")
        print("***********************")

    def readCFGfile(self, FileName):
        with open(FileName, 'r') as read:
            for line in read:
                if ""

if __name__ == "__main__":
    address = 'GPIB0::16::INSTR'
    FileName = 'HPcfg.dat'
    HP = HP33120A(address)
    HP.MakeCFG_file()