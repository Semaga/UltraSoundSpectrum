import numpy as np
import pyvisa
import time

import testlib
def test():
    rm = pyvisa.ResourceManager()

    addresHP = 'GPIB0::15::INSTR'
    addresSF = 'GPIB0::8::INSTR'

    SF = rm.open_resource(addresSF)
    HP = rm.open_resource(addresHP)

    # testlib.initSetupSF(SF)

    Aver = 2
    freq = 2e5
    Xmass = np.zeros((Aver), float)
    Ymass = np.zeros((Aver), float)
    Rmass = np.zeros((Aver), float)
    PHmass = np.zeros((Aver), float)
    FRmass = np.zeros((Aver), float)
    FRHPmass = np.zeros((Aver), float)

    for j in range(Aver):
        Xmass[j] = float(SF.query("OUTP?1"))
        Ymass[j] = float(SF.query("OUTP?2"))
        Rmass[j] = float(SF.query("OUTP?3"))
        PHmass[j] = float(SF.query("OUTP?5"))
        FRmass[j] = float(SF.query("FREQ?"))

        FRHPmass[j] = float(HP.query("FREQ?"))

    print("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (freq, float(HP.query("FREQ?")),
        np.mean(FRmass), np.mean(Xmass), np.mean(Ymass), np.mean(Rmass),
        np.mean(PHmass)))
    # print("SF.query(OUTP?1): X %s" % (SF.query("OUTP?1")))
    # print("SF.query(OUTP?2): Y %s"%(SF.query("OUTP?2")))
    # print("SF.query(OUTP?3): R %s"%(SF.query("OUTP?3")))
    # print("SF.query(OUTP?5): Phase %s" % (SF.query("OUTP?5")))

def CFG_file(FileName):
    RST = 0           # Reset to default configuration
    CLS = 0           # Clear all status bytes
    SENS = str()      # Sensitivity
    CDRM = str()      # Close Dynamic Reserve Mode
    TimeConst = str() # Time Constant
    TCFS = str()      # Time Constant Filter Slope
    SII = str()       # Signal Input Impedance
    with open(FileName, 'r') as read:
        for line in read:
            if "Reset the SR844 to its default configuration(Yes/No)" in line:
                if "No" in line.split('-')[1]:
                    RST = 0
                    print("Reset - No")
                elif "Yes" in line.split('-')[1]:
                    RST = 1
                    print("Reset - Yes")
                else:
                    print("Err - not correct value")
            if "Clear all status bytes(Yes/No)" in line:
                if "Yes" in line.split('-')[1]:
                    CLS = 1
                    print("CLS - Yes")
                elif "No" in line.split('-')[1]:
                    CLS = 0
                    print("CLS - No")
                else:
                    pass
            if "Set the Sensitivity" in line:
                SENS = line.split('-')[1].split()[0]+line.split('-')[1].split()[1]
                print("SENS - "+SENS)
            if "Set the Close Dynamic Reserve Mode(High/Normal/Low)" in line:
                CDRM = line.split('-')[1].split()[0]
                print("CDRM - " + CDRM)
            if "Set the Time Constant -" in line:
                TimeConst = line.split('-')[1].split()[0]+line.split('-')[1].split()[1]
                print("TimeConst - " + TimeConst)
            if "Set the Time Constant Filter Slope -" in line:
                TCFS = line.split('-')[1].split()[0]
                print("Time Constant Filter Slope - "+TCFS)
            if "Set the Signal Input Impedance -" in line:
                SII = line.split('-')[1].split()[0]
                print("Signal Input Impedance - " + SII)

if __name__ == "__main__":
   CFG_file('SFcfg.dat')