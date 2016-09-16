# 2016-09-16-C-on-Si-20kV-4K.py
#
#   Date      Who  Comment
# ----------  ---  -----------------------------------------------
# 2016-09-02  JRM  Analyze data from 2016-09-07
# 
# This script required 17.066 min on ROCPW7ZC5C42 for 10K traj
# Elapse: 0:17:04.4

import sys
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3,FluorescenceXRayGeneration3, XRayTransport3", None)


import os
import glob

import gov.nist.microanalysis.EPQLibrary as epq
import gov.nist.microanalysis.EPQLibrary.Detector as epd
import gov.nist.microanalysis.NISTMonte as nm
import gov.nist.microanalysis.NISTMonte.Gen3 as nm3
import gov.nist.microanalysis.EPQTools as et
import gov.nist.microanalysis.dtsa2 as dt2

import dtsa2.jmGen as jmg
import dtsa2.mcSimulate3 as mc3
import dtsa2.hyperTools as ht

import shutil
import time

import java.util as jutil
import java.io as jio
import java.nio.charset as cs
import string

start = time.time()

gitHom = os.environ['GIT_HOME']
relPrj = "/sirionProbeCurrentProxy"
prjDir = gitHom + relPrj
datDir = prjDir + "/dat"
wrkDir = prjDir + "/py"
csvDir = datDir + "/csv"
spcDir = datDir + "/msa/Si-Cal-20kV"

jmg.ensureDir(wrkDir)

os.chdir(wrkDir)

rptDir = wrkDir + '/2016-09-16-C-on-Si-20kV-4K Results/'


det = findDetector("Oxford p4 05eV 4K")
e0  = 5    # kV

DataManager.clearSpectrumList()

lNa = [] # an array for spectrum name
lPc = [] # an array for PC
lPISimu = [] # an array for mean Si peak integral
lPISiuc = [] # an array for Si peak integral uncertainty
lRatio = [] # an array for C/Si peak ratio

iCount = 0

print(spcDir + '/*.msa')
for name in glob.glob(spcDir + '/*-4K.msa'):
    name = name.replace('\\', '/')
    bn = os.path.basename(name)
    na = bn.split('.msa')[0]
    lNa.append(na)
    print(na)
    spc = wrap(readSpectrum(name))
    sp = spc.getProperties()
    pc = sp.getNumericProperty(epq.SpectrumProperties.FaradayBegin)
    lt = sp.getNumericProperty(epq.SpectrumProperties.LiveTime)
    spc.display()
    res = jmg.anaCSi(spc, det, digits=2, display=True)
    cI = res["C"]
    siI = res["Si"]
    ratio = cI[0]/siI[0]
    lPc.append(pc)
    lPISimu.append(siI[0])
    lPISiuc.append(siI[1])
    lRatio.append(ratio)
    print((na, pc, siI[0], siI[1], ratio))
    iCount += 1

basFile ="2016-09-16-C-on-Si-20kV-4K.csv"
strOutFile = csvDir + "/" + basFile

f=open(strOutFile, 'w')
strLine = "spc, pc, "
strLine = strLine +  "Si.Int.mu, Si.Int.unc, C.to.Si\n"
f.write(strLine)
for i in range(iCount):
    strLine = "%s" % lNa[i] + ","
    strLine = strLine + "%.3f" % lPc[i] + ","
    strLine = strLine + "%.3f" % lPISimu[i] + ","
    strLine = strLine + "%.3f" % lPISiuc[i] + ","
    strLine = strLine + "%.3f" % lRatio[i] + "\n"
    f.write(strLine)  
f.close()

# clean up cruft
shutil.rmtree(rptDir)
print "Done!"

end = time.time()
delta = (end-start)/60
msg = "This script required %.3f min" % delta
print msg
if(delta > 60):
    delta = delta/60
    msg = "...or %.3f hr" % delta
    print msg
