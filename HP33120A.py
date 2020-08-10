import pyvisa
import glob
import os
import time

class HP33120A(object):
    """
    This class using for connecting HP/Agilent 33120A.
    Methods of this class :
          setFreq   - input frequency
                      Sets the output frequency
          readFREQ  - reads the frequency of an external source or own
                      :return (float-type) Frequency of an external source or own
          setShape  - input shape
                      {SINusoid|SQUare|TRIangle|RAMP|NOISe|DC|}
                      sets the waveform to be specified
          readShape - read the waveform
                      :return (str-type) shape
          setVPP    - input amplitude
                      sets the voltage amplitude
          readVPP   - input parameter are MIN = False, MAX = False
                      :return (float-type) the voltage amplitude
          setVoltOffset - input  {<offset>|MINimum|MAXimum}
          readVoltOffset - return: (float-type) the value of offset
          setDcycle - set Dcucle using parameter from CFG-file
          readDcycle - return: Dcycle
          setVoltUnit - set Volt Unit using parameter from CFG-file
          readVoltUnit - return: VoltUnit
          setDefaultConfig -
          printConfig - print parameters of config
          MakeCFG_file - write CGF-file with default configuration
          readCFGfile - input FileName
                        read CGF-file with user configuration

    """
    def __init__(self, GPIB_adress):
        self.addres    = GPIB_adress
        self.shape     = "SIN"
        self.Vpp       = 1.5
        self.VU        = "VPP"
        self.RM        = pyvisa.ResourceManager() # set resource manager
        self.defaultFN = "HPcfg.dat"

#OUTPUT CONFIGURATION COMMANDS

    def setFREQ(self, value):
        self.RM.open_resource(self.addres).write("SOUR:FREQ %f"%value)

    def readFREQ(self):
        return float(self.RM.open_resource(self.addres).query("SOUR:FREQ?"))

    def setShape(self, param):
        if str(param) == "SIN":
            self.RM.open_resource(self.addres).write("FUNC:SHAP SIN")
        elif str(param) == "SQU":
            self.RM.open_resource(self.addres).write("FUNC:SHAP SQU")
        elif str(param) == "TRI":
            self.RM.open_resource(self.addres).write("FUNC:SHAP TRI")
        elif str(param) == "RAMP":
            self.RM.open_resource(self.addres).write("FUNC:SHAP RAMP")
        elif str(param) == "NOIS":
            self.RM.open_resource(self.addres).write("FUNC:SHAP NOIS")
        elif str(param) == "DC":
            self.RM.open_resource(self.addres).write("FUNC:SHAP DC")
        else:
            self.RM.open_resource(self.addres).write("FUNC:SHAP SIN")

    def readShape(self):
        return str(self.RM.open_resource(self.addres).query("FUNC:SHAP?"))

    def setVPP(self, value):
        value = float(value)
        self.RM.open_resource(self.addres).write("VOLT %f"%(value))

    def readVPP(self, MIN = False, MAX = False):
        if MIN:
            return float(self.RM.open_resource(self.addres).query("VOLT? MIN"))
        elif MAX:
            return float(self.RM.open_resource(self.addres).query("VOLT? MAX"))
        else:
            return float(self.RM.open_resource(self.addres).query("VOLT?"))

    def setVoltOffset(self, offset):
        self.RM.open_resource(self.addres).write("VOLT:OFFS %f" % (offset))

    def readVoltOffset(self, MIN = False, MAX = False):
        if MIN:
            return float(self.RM.open_resource(self.addres).query("VOLT:OFFS? MIN"))
        elif MAX:
            return float(self.RM.open_resource(self.addres).query("VOLT:OFFS? MAX"))
        else:
            return float(self.RM.open_resource(self.addres).query("VOLT:OFFS?"))

    def setDcycle(self, value):
        self.RM.open_resource(self.addres).write("PULS:DCYC %f" % (value))

    def readDcycle(self):
        return  str(self.RM.open_resource(self.addres).query("PULS:DCYC?"))

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
        return float(self.RM.open_resource(self.addres).query("VOLT:UNIT?"))

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
            return str(self.RM.open_resource(self.addres).query("OUTP:LOAD? MIN"))
        elif MAX:
            return str(self.RM.open_resource(self.addres).query("OUTP:LOAD? MAX"))
        else:
            return str(self.RM.open_resource(self.addres).query("OUTP:LOAD? MIN"))

    def setOutPutSYNC(self, status = "ON"):
        if "ON" in status:
            self.RM.open_resource(self.addres).write("OUTP:SYNC ON")
        elif "OFF" in status:
            self.RM.open_resource(self.addres).write("OUTP:SYNC OFF")
        else:
            self.RM.open_resource(self.addres).write("OUTP:SYNC ON")

    def readOutPutSYNC(self):
        return str(self.RM.open_resource(self.addres).query("OUTP:SYNC?"))

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
        time.sleep(2)

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
        if self.defaultFN in glob.glob('*.dat'):
            try:
                # print("File wt/")
                os.rename(self.defaultFN, "Old_"+self.defaultFN)
            except:
                print("File with config is find")
                pass

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
                if "Function:Shape - " in line:
                    self.shape = line.split('-')[1].split()[0]
                if "Voltage:Unit - " in line:
                    self.VU = line.split('-')[1].split()[0]
                if "Voltage:Amplitude - " in line:
                    self.Vpp = line.split('-')[1].split()[0]

if __name__ == "__main__":
    address = 'GPIB0::16::INSTR'
    FileName = 'HPcfg.dat'
    HP = HP33120A(address)
    HP.MakeCFG_file()