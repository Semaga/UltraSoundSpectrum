import pyvisa
import os
import time


class Standford(object):
    """doc"""
    def __init__(self, GPIB_adress):
        self.addres    = GPIB_adress
        self.RST       = 0         # Reset to default configuration
        self.CLS       = 0         # Clear all status bytes
        self.SENS      = "30m"     # Sensitivity
        self.CDRM      = "Normal"  # Close Dynamic Reserve Mode
        self.TimeConst = "100mks"  # Time Constant
        self.TCFS      = "6"       # Time Constant Filter Slope
        self.SII       = "50"      # Signal Input Impedance
        self.RM        = "0"       # Reference Mode
        self.WRM       = "High"    # Wide Reserve Mode
        self.SF        = pyvisa.ResourceManager()

    def DefaultConfig(self):
        self.RST       = 0         # Reset to default configuration
        self.CLS       = 0         # Clear all status bytes
        self.SENS      = "30m"     # Sensitivity
        self.CDRM      = "Normal"  # Close Dynamic Reserve Mode
        self.TimeConst = "100mks"  # Time Constant
        self.TCFS      = "6"       # Time Constant Filter Slope
        self.SII       = "50"      # Signal Input Impedance
        self.RM        = "0"       # Reference Mode
        self.WRM       = "High"

        self.setReferMode()
        self.setSensetivity()
        self.setTimeConstant()
        self.setInputImpedance()
        self.setWideReserveMode()
        self.setTimeConstantFilterSlope()
        self.setCloseDynamcReserve()
        time.sleep(2)

    def setConfig(self):
        self.setReferMode()
        self.setSensetivity()
        self.setTimeConstant()
        self.setInputImpedance()
        self.setWideReserveMode()
        self.setTimeConstantFilterSlope()
        self.setCloseDynamcReserve()
        time.sleep(2)

    def PrintConfig(self):
        print("Config data")
        print("\tAddres - " + self.addres)
        print("\tRST - " + str(self.RST))
        print("\tCLS - " + str(self.CLS))
        print("\tSENS - " + str(self.SENS))
        print("\tRM - "+ self.RM)
        print("\tCDRM - " + self.CDRM)
        print("\tTimeConst - " + str(self.TimeConst))
        print("\tTime Constant Filter Slope - " + self.TCFS + " dB/Octave")
        print("\tSignal Input Impedance - " + self.SII)
        print("\tWide Reserve Mode - " + self.WRM)

    def MakeCFG_file(self):
        with open('SFcfg.dat', 'w') as write:
            buf = ""
            write.write("#Standfor config file\n")
            write.write("Addres : %s\n"%self.addres)
            if self.RST == 1:
                write.write("Reset the SR844 to its default configuration(Yes/No) - Yes\n")
            else:
                write.write("Reset the SR844 to its default configuration(Yes/No) - No\n")

            if self.CLS == 1:
                write.write("Clear all status bytes(Yes/No) - Yes\n")
            else:
                write.write("Clear all status bytes(Yes/No) - No\n")
            write.write("Set the Reference Mode to External (0) or Internal (1) - %s\n"%self.RM)
            write.write("Set the Sensitivity - %s\n" % self.SENS)
            write.write("Set the Close Dynamic Reserve Mode(High/Normal/Low) - %s\n"%self.CDRM)
            write.write("Set the Time Constant - %s\n" % self.TimeConst)
            write.write("Set the Time Constant Filter Slope - %s\n"%self.TCFS)
            write.write("Set the Wide Reserve Mode - %s\n"%self.WRM)
            write.write("Set the Signal Input Impedance - %s\n"%self.SII)

    def CFG_file(self, FileName):
        with open(FileName, 'r') as read:
            for line in read:
                if "Reset the SR844 to its default configuration(Yes/No)" in line:
                    if "No" in line.split('-')[1]:
                        self.RST = 0
                    elif "Yes" in line.split('-')[1]:
                        self.RST = 1
                    else:
                        print("Err - not correct value")
                        pass
                if "Clear all status bytes(Yes/No)" in line:
                    if "Yes" in line.split('-')[1]:
                        self.CLS = 1
                    elif "No" in line.split('-')[1]:
                        self.CLS = 0
                    else:
                        print("Err - not correct value")
                        pass
                if "Set the Sensitivity" in line:
                    self.SENS = line.split('-')[1].split()[0]

                if "Set the Close Dynamic Reserve Mode(High/Normal/Low)" in line:
                    self.CDRM = line.split('-')[1].split()[0]

                if "Set the Wide Reserve Mode - " in line:
                    self.WRM = line.split('-')[1].split()[0]

                if "Set the Time Constant -" in line:
                    self.TimeConst = line.split('-')[1].split()[0]

                if "Set the Time Constant Filter Slope -" in line:
                    self.TCFS = line.split('-')[1].split()[0]

                if "Set the Signal Input Impedance -" in line:
                    self.SII = line.split('-')[1].split()[0]
                if "Set the Reference Mode to External (0) or Internal (1) - " in line:
                    self.RM = line.split('-')[1].split()[0]

    #Blyadoblock
    def RST(self):
        self.SF.write("*RST")

    def CLS(self):
        self.SF.write("*CLS")

    def setReferMode(self):
        '''Set the Reference Mode to External (0) or Internal (1)'''
        if int(self.RM) == 0:
            self.SF.open_resource(self.addres).write("FMOD 0")
        elif int(self.RM) == 1:
            self.SF.open_resource(self.addres).write("FMOD 1")
        else:
            pass

    def readReferMode(self):
        if self.SF.open_resource(self.addres).query("FMOD?") == "1":
            self.RM = "1"
        else:
            self.RM = "0"

    def setSensetivity(self):
        '''
        :param SF:
        :param level:
        :return:
        '''
        level = self.SENS
        if level == "100n":
            self.SF.open_resource(self.addres).write("SENS %d" % (0))
        elif level == "300n":
            self.SF.open_resource(self.addres).write("SENS %d" % (1))
        elif level == "1mk":
            self.SF.open_resource(self.addres).write("SENS %d" % (2))
        elif level == "3mk":
            self.SF.open_resource(self.addres).write("SENS %d" % (3))
        elif level == "10mk":
            self.SF.open_resource(self.addres).write("SENS %d" % (4))
        elif level == "30mk":
            self.SF.open_resource(self.addres).write("SENS %d" % (5))
        elif level == "100mk":
            self.SF.open_resource(self.addres).write("SENS %d" % (6))
        elif level == "300mk":
            self.SF.open_resource(self.addres).write("SENS %d" % (7))
        elif level == "1m":
            self.SF.open_resource(self.addres).write("SENS %d" % (8))
        elif level == "3m":
            self.SF.open_resource(self.addres).write("SENS %d" % (9))
        elif level == "10m":
            self.SF.open_resource(self.addres).write("SENS %d" % (10))
        elif level == "30m":
            self.SF.open_resource(self.addres).write("SENS %d" % (11))
        elif level == "100m":
            self.SF.open_resource(self.addres).write("SENS %d" % (12))
        elif level == "300m":
            self.SF.open_resource(self.addres).write("SENS %d" % (13))
        elif level == "1":
            self.SF.open_resource(self.addres).write("SENS %d" % (14))
        else:
            self.SF.open_resource(self.addres).write("AGAN")

    def readSensetivity(self):
        return  self.SENS

    def setCloseDynamcReserve(self):
        if self.CDRM == "High":
            self.SF.open_resource(self.addres).write("CRSV 0")
        elif self.CDRM == "Normal":
            self.SF.open_resource(self.addres).write("CRSV 1")
        elif self.CDRM == "Low":
            self.SF.open_resource(self.addres).write("CRSV 2")
        else:
            self.SF.open_resource(self.addres).write("CRSV 1")

    def readCloseDynamcReserve(self):
        if self.SF.open_resource(self.addres).query("CRSV?") == "1":
            self.CDRM = "Normal"
        elif self.SF.open_resource(self.addres).query("CRSV?") == "0":
            self.CDRM = "High"
        elif self.SF.open_resource(self.addres).query("CRSV?") == "2":
            self.CDRM = "Low"
        else:
            self.CDRM = "Normal"

    def setTimeConstant(self):
        level = 0
        if self.TimeConst == "100mks":
            self.SF.open_resource(self.addres).write("OFLT 0")
        elif self.TimeConst == "300mks":
            self.SF.open_resource(self.addres).write("OFLT 1")
        elif self.TimeConst == "1ms":
            self.SF.open_resource(self.addres).write("OFLT 2")
        elif self.TimeConst == "3ms":
            self.SF.open_resource(self.addres).write("OFLT 3")
        elif self.TimeConst == "10ms":
            self.SF.open_resource(self.addres).write("OFLT 4")
        elif self.TimeConst == "30ms":
            self.SF.open_resource(self.addres).write("OFLT 5")
        elif self.TimeConst == "100ms":
            self.SF.open_resource(self.addres).write("OFLT 6")
        elif self.TimeConst == "300ms":
            self.SF.open_resource(self.addres).write("OFLT 7")
        elif self.TimeConst == "1s":
            self.SF.open_resource(self.addres).write("OFLT 8")
        elif self.TimeConst == "3s":
            self.SF.open_resource(self.addres).write("OFLT 9")
        elif self.TimeConst == "10s":
            self.SF.open_resource(self.addres).write("OFLT 10")
        elif self.TimeConst == "30s":
            self.SF.open_resource(self.addres).write("OFLT 11")
        elif self.TimeConst == "100s":
            self.SF.open_resource(self.addres).write("OFLT 12")
        elif self.TimeConst == "300s":
            self.SF.open_resource(self.addres).write("OFLT 13")
        elif self.TimeConst == "1ks":
            self.SF.open_resource(self.addres).write("OFLT 14")
        elif self.TimeConst == "3ks":
            self.SF.open_resource(self.addres).write("OFLT 15")
        elif self.TimeConst == "10ks":
            self.SF.open_resource(self.addres).write("OFLT 16")
        elif self.TimeConst == "30ks":
            self.SF.open_resource(self.addres).write("OFLT 17")

    def readTimeConstant(self):
        if "0" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "100mks"
        elif "1" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "300mks"
        elif "2" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "1ms"
        elif "3" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "3ms"
        elif "4" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "10ms"
        elif "5" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "30ms"
        elif "6" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "100ms"
        elif "7" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "300ms"
        elif "8" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "1s"
        elif "9" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "3s"
        elif "10" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "10s"
        elif "11" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "30s"
        elif "12" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "100s"
        elif "13" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "300s"
        elif "14" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "1ks"
        elif "15" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "3ks"
        elif "16" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "10ks"
        elif "17" in self.SF.open_resource(self.addres).query("OFLT?"):
            self.TimeConst = "30ks"

    def setTimeConstantFilterSlope(self):
        if self.TCFS == "6":
            self.SF.open_resource(self.addres).write("OFSL 1")
        elif self.TCFS == "12":
            self.SF.open_resource(self.addres).write("OFSL 2")
        elif self.TCFS == "18":
            self.SF.open_resource(self.addres).write("OFSL 3")
        elif self.TCFS == "24":
            self.SF.open_resource(self.addres).write("OFSL 4")
        elif self.TCFS == "No":
            self.SF.open_resource(self.addres).write("OFSL 0")
        else:
            self.SF.open_resource(self.addres).write("OFSL 1")

    def readTimeConstantFilterSlope(self):
        if "0" in self.SF.open_resource(self.addres).query("OFSL?"):
            self.TCFS = "No"
        elif "1" in self.SF.open_resource(self.addres).query("OFSL?"):
            self.TCFS = "6"
        elif "2" in self.SF.open_resource(self.addres).query("OFSL?"):
            self.TCFS = "12"
        elif "3" in self.SF.open_resource(self.addres).query("OFSL?"):
            self.TCFS = "18"
        elif "4" in self.SF.open_resource(self.addres).query("OFSL?"):
            self.TCFS = "24"
        else:
            self.TCFS = "6"

    def setWideReserveMode(self):
        if "High" in self.WRM:
            self.SF.open_resource(self.addres).write("WRSV 0")
        elif "Normal" in self.WRM:
            self.SF.open_resource(self.addres).write("WRSV 1")
        elif "Low" in self.WRM:
            self.SF.open_resource(self.addres).write("WRSV 2")
        else:
            self.SF.open_resource(self.addres).write("AWRS")

    def readWideReserveMode(self):
        if "0" in self.SF.open_resource(self.addres).query("WRSV?"):
            self.WRM = "High"
        elif "1" in self.SF.open_resource(self.addres).query("WRSV?"):
            self.WRM = "Normal"
        elif "2" in self.SF.open_resource(self.addres).query("WRSV?"):
            self.WRM = "Low"
        else:
            self.WRM = "High"

    def setInputImpedance(self):
        if "50" in self.SII:
            self.SF.open_resource(self.addres).write("INPZ 0")
        elif "1" in self.SII:
            self.SF.open_resource(self.addres).write("INPZ 1")
        else:
            self.SF.open_resource(self.addres).write("INPZ 0")

    def readInputImpedance(self):
        if "1" in self.SF.open_resource(self.addres).query("INPZ?"):
            self.SII = "1"
        else:
            self.SII = "0"

    #Take data

    def getX(self):
        return self.SF.open_resource(self.addres).query("OUTP?1")

    def getY(self):
        return self.SF.open_resource(self.addres).query("OUTP?2")

    def getR(self):
        return self.SF.open_resource(self.addres).query("OUTP?3")

    def getPhase(self):
        return self.SF.open_resource(self.addres).query("OUTP?5")

    def getFreq(self):
        return self.SF.open_resource(self.addres).query("FREQ?")



if __name__ == "__main__":
    addres = 'GPIB0::8::INSTR'
    FileName = 'SFcfg.dat'
    SF = Standford(addres)
    # SF.MakeCFG_file()
    # SF.CFG_file(FileName)
    # SF.setConfig()
    # SF.PrintConfig()
    SF.DefaultConfig()
    # SF.PrintConfig()
    print(SF.getY())