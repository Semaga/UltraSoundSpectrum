import numpy as np
import pyvisa
import time

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

    HP = rm.open_resource(addresHP)
    SF = rm.open_resource(addresSF)

    # write settings for SF
    testlib.initSetupSF(SF)

    # write settings for HP
    HP.write('VOLT %f' % (1.8))
    print(HP.query('VOLT?'))

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

    MassFreq = [[2685500, 3e6]]

    # print "Freq = " + SF.query("FREQ?")
    # print "Phase = " + SF.query("PHAS?")
    # print "X = " + SF.query("OUTP?1")
    # print "Y = " + SF.query("OUTP?2")
    # print "R = " + SF.query("OUTP?3")
    # print "R[dBm] = " + SF.query("OUTP?4")
    # print "Theta = " + SF.query("OUTP?5")

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
                HP.write("FREQ %f" % (freq))
                for j in range(Aver):
                    Xmass[j] = float(SF.query("OUTP?1"))
                    Ymass[j] = float(SF.query("OUTP?2"))
                    Rmass[j] = float(SF.query("OUTP?3"))
                    PHmass[j] = float(SF.query("OUTP?5"))
                    FRmass[j] = float(SF.query("FREQ?"))
                    FRHPmass[j] = float(HP.query("FREQ?"))
                # print "freq(Hz)\tfreq(Hz)HP\tfreq(Hz)SF\tX(V)\tY(V)\tR(V)\tPhase(Deg)\n"
                # print("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (freq, float(HP.query("FREQ?")),
                #     np.mean(FRmass), np.mean(Xmass), np.mean(Ymass), np.mean(Rmass),
                #     np.mean(PHmass)))
                File.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (freq, float(HP.query("FREQ?")),
                    np.mean(FRmass), np.mean(Xmass), np.mean(Ymass), np.mean(Rmass),
                    np.mean(PHmass)))
        print("\tFinished write date")
    print("******************************")
    print("---------Work is done---------")
    print("******************************")



main()