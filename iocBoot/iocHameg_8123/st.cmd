#!../../bin/windows-x64/Hameg_8123

< envPaths

epicsEnvSet "IOCNAME" "$(P=$(MYPVPREFIX))HAMEG_8123"
epicsEnvSet "IOCSTATS_DB" "$(DEVIOCSTATS)/db/iocAdminSoft.db"

cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/Hameg_8123.dbd"
Hameg_8123_registerRecordDeviceDriver pdbbase

## main args are:  portName, configSection, configFile, host, options (see lvDCOMConfigure() documentation in lvDCOMDriver.cpp)
##
## there are additional optional args to specify a DCOM ProgID for a compiled LabVIEW application 
## and a different username + password for remote host if that is required 
##
## the "options" argument is a combination of the following flags (as per the #lvDCOMOptions enum in lvDCOMInterface.h)
##    viWarnIfIdle=1, viStartIfIdle=2, viStopOnExitIfStarted=4, viAlwaysStopOnExit=8

# FPNUM environment variable will be assigned outside of this script - it is then substituted in db file and Hameg_8123.xml
# epicsEnvSet("FPNUM", "1")

lvDCOMConfigure("frontpanel", "frontpanel", "$(TOP)/Hameg_8123App/protocol/Hameg_8123.xml", "ndxchipir", 6, "", "spudulike", "reliablebeam")

dbLoadRecords("$(TOP)/db/Hameg_8123.db","P=$(IOCNAME):")
dbLoadRecords("$(IOCSTATS_DB)","IOC=$(IOCNAME)")

cd ${TOP}/iocBoot/${IOC}
iocInit

