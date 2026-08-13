# Chapter 7: Enumerating All Open Libraries and Designs in Active

Session
7.1 Introduction
Sometimes, you are interested in knowing all the library and design names opened in the
current Capture session. This section presents a TCL script which lets you enumerate all open libraries
and designs in currently active session.
7.2 Script and Usage
The TCL script in TCL Script Source for enumerating open libraries and designs in the currently
active Capture session can be used to enumerate all open libraries and designs in currently active
session. This script reports the open library and design names in the session log. This script can be run
only from within the Capture command window.
Step 1. Source the TCL script
This step is required for running the utility from the TCL command window within the Capture
application. Copy the contents of the TCL script shown in TCL Script Source for enumerating open
libraries and designs in the currently active Capture session to a file and name it capSessionUtil.tcl.
Load this file in your TCL command window by typing the following command:
# the <file_path_to_capSessionUtil.tcl> in the following line \
# should be replaced with the actual path where capSessionUtil.tcl
resides
# e.g. source [file normalize {c:\capSessionUtil.tcl}]
source [file normalize {<file_path_to_capSessionUtil.tcl>}]
Step 2. Run the utility
In the Capture TCL shell, following commands can be run
capSessionUtil::enumerateOpenLibsAndDesigns
- This command will report all the open library and design names in the session log

---

7.2.1 TCL Script Source for enumerating open libraries and designs in the
currently active Capture session
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: capSessionUtil.tcl
# contains OrCAD Capture active session utility
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package require DboTclWriteBasic 16.3.0
package provide capSessionUtil 1.0
namespace eval ::capSessionUtil {
namespace export enumerateOpenLibsAndDesigns
}
proc ::capSessionUtil::enumerateOpenLibsAndDesigns { } {
set lSession $::DboSession_s_pDboSession
DboSession -this $lSession
set lStatus [DboState]
set lName [DboTclHelper_sMakeCString]
set lMessageStr [DboTclHelper_sMakeCString "Open Designs -->"]
DboState_WriteToSessionLog $lMessageStr
set lDesignsIter [$lSession NewDesignsIter $lStatus]
set lDesign [$lDesignsIter NextDesign $lStatus]
set lNullObj NULL
while { $lDesign!= $lNullObj} {
$lDesign GetName $lName
DboState_WriteToSessionLog $lName
set lDesign [$lDesignsIter NextDesign $lStatus]
}
delete_DboSessionDesignsIter $lDesignsIter
set lMessageStr [DboTclHelper_sMakeCString "Open Libraries -->"]
DboState_WriteToSessionLog $lMessageStr
set lLibsIter [$lSession NewLibsIter $lStatus]
set lLib [$lLibsIter NextLib $lStatus]
set lNullObj NULL
while { $lLib!= $lNullObj} {
$lLib GetName $lName
DboState_WriteToSessionLog $lName
set lLib [$lLibsIter NextLib $lStatus]
}
delete_DboSessionLibsIter $lLibsIter
$lStatus -delete
}
# source D:/WorkData/Capture/dbcheck/capSessionUtil.tcl
# capSessionUtil::enumerateOpenLibsAndDesigns