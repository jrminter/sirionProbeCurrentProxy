# 2016-09-16-C-on-Cu-20kV-2K.py
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
spcDir = datDir + "/msa/Cu-Cal-20kV"

jmg.ensureDir(wrkDir)

os.chdir(wrkDir)

rptDir = wrkDir + '/2016-09-16-C-on-Cu-20kV-2K Results/'


det = findDetector("Oxford p4 05eV 2K")
e0  = 5    # kV

DataManager.clearSpectrumList()

lNa = [] # an array for spectrum name
lPc = [] # an array for PC
lPICumu = [] # an array for mean Cu peak integral
lPICuuc = [] # an array for Cu peak integral uncertainty
lRatio = [] # an array for C/Cu peak ratio

iCount = 0

print(spcDir + '/*.msa')
for name in glob.glob(spcDir + '/*-2K.msa'):
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
    res = jmg.anaCCu(spc, det, digits=2, display=True)
    cI = res["C"]
    cuI = res["Cu"]
    ratio = cI[0]/cuI[0]
    lPc.append(pc)
    lPICumu.append(cuI[0])
    lPICuuc.append(cuI[1])
    lRatio.append(ratio)
    print((na, pc, cuI[0], cuI[1], ratio))
    iCount += 1

basFile ="2016-09-16-C-on-Cu-20kV-2K.csv"
strOutFile = csvDir + "/" + basFile

f=open(strOutFile, 'w')
strLine = "spc, pc, "
strLine = strLine +  "Cu.Int.mu, Cu.Int.unc, C.to.Cu\n"
f.write(strLine)
for i in range(iCount):
    strLine = "%s" % lNa[i] + ","
    strLine = strLine + "%.3f" % lPc[i] + ","
    strLine = strLine + "%.3f" % lPICumu[i] + ","
    strLine = strLine + "%.3f" % lPICuuc[i] + ","
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
