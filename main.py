import numpy as np
import pyvisa
import time
from SR844 import Standford
from HP33120A import HP33120A

import testlib

def main():
    # constant
    delay = 0.05  # in sec
    Vpp = 1.8
    Aver = 1
    stepF = 1
    # startFreq = 0.95e6
    # finishFreq = 1.1e6

    # connetc with device
    rm = pyvisa.ResourceManager()

    addresHP = 'GPIB0::15::INSTR'
    addresSF = 'GPIB0::8::INSTR'

    SF = Standford(addresSF)
    HP = HP33120A(addresHP)

    # write settings for SF
    # testlib.initSetupSF(SF)

    SF.CFG_file("SFcfg.dat")
    SF.DefaultConfig()
    HP.readCFGfile(("HPcfg.dat"))
    HP.setDefaultConfig()
    # write settings for HP
    print("VPP = %f"%(HP.readVPP()))

    # for average data
    Xmass = np.zeros((Aver), float)
    Ymass = np.zeros((Aver), float)
    Rmass = np.zeros((Aver), float)
    PHmass = np.zeros((Aver), float)
    FRmass = np.zeros((Aver), float)
    FRHPmass = np.zeros((Aver), float)

    # MassFreq = [[200000, 200300],
    #             [394160, 394240],
    #             [788422, 788460],
    #             [788350, 788600],
    #             [329480, 329520]]

    MassFreq = [[2685500, 2685610]]

    print("Freq= " + SF.getFreq())
    print("Phase = " + SF.getPhase())
    print("X = " + SF.getX())
    print("Y = " + SF.getY())
    print("R = " + SF.getR())
    print("R[dBm] = " + SF.getRdBm())
    print("Theta = " + SF.getTheta())

    # prepare SF
    # SF.query("*RST") #Reset to its default configuration

    for sfFreq in MassFreq:
        startFreq = sfFreq[0]
        finishFreq = sfFreq[1]

        NumSteP = (finishFreq - startFreq) / stepF + 1
        freqMass = np.linspace(startFreq, finishFreq, int(NumSteP))
        fileName = '04082020/spec_from_{}_{}_{}_{}_{}_{}.dat'.format(time.gmtime().tm_hour, time.gmtime().tm_min,
                                                                     time.gmtime().tm_sec, time.gmtime().tm_mday,
                                                                     time.gmtime().tm_mon, time.gmtime().tm_year)

        print('File name: %s'%(fileName))
        print("\tStart write data")
        # print('freq(Hz)\tfreq(Hz)HP\tfreq(Hz)SF\tX(V)\tY(V)\tR(V)\tPhase(Deg)')

        with open(fileName, 'a') as File:
            File.write("freq(Hz)\tfreq(Hz)HP\tfreq(Hz)SF\tX(V)\tY(V)\tR(V)\tPhase(Deg)\n")
            for i, freq in enumerate(freqMass):
                HP.setFREQ(freq)
                for j in range(Aver):
                    Xmass[j] = float(SF.getX())
                    Ymass[j] = float(SF.getY())
                    Rmass[j] = float(SF.getR())
                    PHmass[j] = float(SF.getTheta())
                    FRmass[j] = float(SF.getFreq())
                    FRHPmass[j] = float(HP.readFREQ())
                # print "freq(Hz)\tfreq(Hz)HP\tfreq(Hz)SF\tX(V)\tY(V)\tR(V)\tPhase(Deg)\n"
                # print("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (freq, float(HP.query("FREQ?")),
                #     np.mean(FRmass), np.mean(Xmass), np.mean(Ymass), np.mean(Rmass),
                #     np.mean(PHmass)))
                File.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (freq, float(HP.readFREQ()),
                    np.mean(FRmass), np.mean(Xmass), np.mean(Ymass), np.mean(Rmass),
                    np.mean(PHmass)))
        print("\tFinished write date")

    print("******************************")
    print("---------Work is done---------")
    print("******************************")



main()