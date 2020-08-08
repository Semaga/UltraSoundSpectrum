import pyvisa
import time
import numpy as np

def RST(SF):
    SF.write("*RST")
def CLS(SF):
    SF.write("*CLS")

def ReferMode(SF, mode):
    '''Set (Query) the Reference Mode to External (0) or Internal (1)'''
    if mode == 0:
        SF.write("FMOD 0")
    else:
        SF.write("FMOD 1")

def SetSensetivity(SF, level = "10m"):
    '''
    :param SF:
    :param level:
    :return:
    '''
    if level == "100n":
        SF.write("SENS %d" % (0))
    elif level == "300n":
        SF.write("SENS %d" % (1))
    elif level == "1mk":
        SF.write("SENS %d" % (2))
    elif level == "3mk":
        SF.write("SENS %d" % (3))
    elif level == "10mk":
        SF.write("SENS %d" % (4))
    elif level == "30mk":
        SF.write("SENS %d" % (5))
    elif level == "100mk":
        SF.write("SENS %d" % (6))
    elif level == "300mk":
        SF.write("SENS %d" % (7))
    elif level == "1m":
        SF.write("SENS %d" % (8))
    elif level == "3m":
        SF.write("SENS %d" % (9))
    elif level == "10m":
        SF.write("SENS %d" % (10))
    elif level == "30m":
        SF.write("SENS %d" % (11))
    elif level == "100m":
        SF.write("SENS %d" % (12))
    elif level == "300m":
        SF.write("SENS %d" % (13))
    elif level == "1":
        SF.write("SENS %d" % (14))
    else:
        SF.write("AGAN")

def SetCloseDynamicRM(SF, level = 1):
    '''
    Set (Query) the Close Dynamic Reserve Mode
    to High Reserve (0),
    Normal (1) or
    Low Noise (2).
    '''
    if level == 0:
        SF.write("CRSV 0")
    elif level == 1:
        SF.write("CRSV 1")
    elif level == 2:
        SF.write("CRSV 2")
    else:
        SF.write("CRSV 1")

def SetTimeConstant(SF):
    '''set the Time Constant to 100mks (0) throught 30 ks (17)'''

def initSetupSF(SF):
    RST(SF)
    CLS(SF)
    ReferMode(SF, 0)
    SetSensetivity(SF, '30m')
    SetCloseDynamicRM(SF)

    # set the Time Constant
    SF.write("OFLT %d" % (0))  #
    # set the Time Constant filter

    SF.write("OFSL %d" % (1))  # Set the Time Constant Filter Slope to 6 (i=1), 12 (2), 18 (3),24 (4) dB/oct, or NoFilter Mode (i=0)
    # set Signal input
    # wide reserve
    # print SF.query("WRSV?")
    SF.write("WRSV 0")  # Set (Query) the Wide Reserve Mode to High Reserve (0), Normal (1), orLow Noise (2).
    # INPZ(?){i}
    # print SF.query("INPZ?")
    SF.write("INPZ 0")  # Set (Query) the Signal Input Impedance to 50 Om (0) or 1MOm
    time.sleep(5)

def tst_SF(addres):
    rm = pyvisa.ResourceManager()
    addresSF = addres
    Aver = 2
    stepF = 1
    SF = rm.open_resource(addresSF)
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
        # FRHPmass[j] = float(HP.query("FREQ?"))

if __name__ == "__main__":
    tst_SF('GPIB0::8::INSTR')