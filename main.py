import numpy as np
import pyvisa
from datetime import datetime
from SR844 import Standford
from HP33120A import HP33120A
import os
import time
import testlib

def main():
    home_dir = os.getcwd()
    date = str(datetime.today())
    dirName = str(date).split()[0]



    # os.chdir(home_dir)
    # constant
    delay = 0.05  # in sec
    Vpp = 1.8
    Aver = 2
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


    MassFreq = [[1054550, 1054650],
                [1066900, 1067000],
                [1054500, 1054700],
                [267688, 267900],
                [394000, 394110],
                [426218, 426333],
                [510890, 510998],
                [788100, 788230],
                [1576205, 1576335],
                [2342970, 2343080],
                [1446970, 1447090],
                [200125, 200240],
                [394130, 394270],
                [788370, 788510],
                [394140, 394260],
                [788380, 788510]
                ]

    # MassFreq = [[1054550, 1054650]]

    # print("Freq= " + SF.getFreq())
    # print("Phase = " + SF.getPhase())
    # print("X = " + SF.getX())
    # print("Y = " + SF.getY())
    # print("R = " + SF.getR())
    # print("R[dBm] = " + SF.getRdBm())
    # print("Theta = " + SF.getTheta())

    try:
        os.chdir(home_dir)
        os.chdir('..')
        os.mkdir(dirName)
        os.chdir(dirName)
    except:
        os.chdir(home_dir)
        os.chdir('..')
        os.chdir(dirName)


    # prepare SF
    # SF.query("*RST") #Reset to its default configuration

    for sfFreq in MassFreq:
        if (sfFreq[0] > sfFreq[1]):
            startFreq = sfFreq[1]
            finishFreq = sfFreq[0]
        else:
            startFreq = sfFreq[0]
            finishFreq = sfFreq[1]

        NumSteP = (finishFreq - startFreq) / stepF + 1
        freqMass = np.linspace(startFreq, finishFreq, int(NumSteP))
        fileName = 'step01_spec_from_{}_{}_{}_{}_{}_{}.dat'.format(time.gmtime().tm_hour, time.gmtime().tm_min,
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



start = datetime.now()
main()
print("Время работы:")
print(datetime.now() - start)
