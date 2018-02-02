TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = Hameg_8123
# Hameg_8123.dbd will be created and installed
DBD += Hameg_8123.dbd

# Hameg_8123.dbd will be made up from these files:
Hameg_8123_DBD += base.dbd asyn.dbd

# Include dbd files from all support applications:
Hameg_8123_DBD += lvDCOM.dbd devIocStats.dbd

# Add all the support libraries needed by this IOC
Hameg_8123_LIBS += lvDCOM asyn autosave devIocStats pcrecpp pcre

# Hameg_8123_registerRecordDeviceDriver.cpp derives from Hameg_8123.dbd
Hameg_8123_SRCS += Hameg_8123_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
Hameg_8123_SRCS_DEFAULT += Hameg_8123Main.cpp
Hameg_8123_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#Hameg_8123_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
Hameg_8123_LIBS += $(EPICS_BASE_IOC_LIBS)

Hameg_8123_SYS_LIBS_WIN32 += msxml2

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

