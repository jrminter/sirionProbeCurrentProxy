# test.py
#
#   Date      Who  Comment
# ----------  ---  -----------------------------------------------
# 2016-09-15  JRM  Simulate the peak intensity of Si at a series
#                  of accelerating voltages at a standard probe
#                  current. Use output to normalize probe current
#                  series at a singke voltage. 
#                  
# This script required  min on ROCPW7ZC5C42 for 10K traj
# Elapse: 

import sys
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3,FluorescenceXRayGeneration3, XRayTransport3", None)


import os

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
jmg.ensureDir(datDir)
jmg.ensureDir(csvDir)

os.chdir(wrkDir)
rptDir = wrkDir + '/test Results/'


det      = findDetector("Oxford p4 05eV 2K")
nTraj    = 100    # trajectories
lt       =   100    # sec
pc       =     1.0  # nA




dose = pc * lt  # na-sec"

DataManager.clearSpectrumList()

si = material("Si", density=2.3296)


lE0 = [5.0, 7.0, 10.0, 15.0, 20.0, 30.0]

lPISimu = [] # an array for mean Si peak integral
lPISiuc = [] # an array for Si peak integral uncertainty


iCount = 0

for e0 in lE0:

    spc = mc3.simulate(si, det, e0, dose, False, nTraj,True, True, {})

    sName = "Si-%g-kV" % (e0)
    spc.rename(sName)
    sp = spc.getProperties()
    sp.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
    sp.setNumericProperty(epq.SpectrumProperties.FaradayEnd, pc)
    sp.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
    spc.display()





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
