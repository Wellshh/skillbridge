# Chapter 4: Migrating OrCAD Capture Designs

4.1 Introduction
In the OrCAD Capture 16.3 release the database has been upgraded. Designs and libraries created using
OrCAD Capture 15.7 and onwards needs to be upgraded to the current database revision level in-order
to be used in the Capture 16.3. When non 16.3 designs and libraries are opened in Capture 16.3, the
application automatically upgrades the design database to the current revision level. This process is on-
demand.
Once a design or library has been upgraded to the latest database version, it can be opened with a non
16.3 version of the Capture application (15.7 – 16.2) after the database is down-revved to the previous
database version. This can be done by selecting a design/library in the PM window and then performing
a “Save As” operation on the design/library by selecting the “Save as type” as “Capture 16.2 Design
(*.DSN)”/”Capture 16.2 Library (*.OLB)”.
Figure 1 Saving a 16.3 design as a 16.2 design.

---

Figure 2 Saving a 16.3 library as a 16.2 library
Sometimes, you might want to automatically upgrade your designs/libraries to the 16.3 version of the
database as a batch process. Similarly, you might also want to automatically save your 16.3
designs/libraries in the 16.2 version of the database through a batch process. This section presents a TCL
script which lets you to uprev or downrev the database in a batch mode.
4.2 Script and Usage
The TCL script in TCL Script Source for Capture design revision can be used to uprev/downrev the
database as described in the previous section. This script can be run either from a standalone TCL shell
or from within the Capture command window. In order to run it from a standalone TCL shell you would
need to have ActiveTcl installed on your system. The OrCAD Capture installation does not ship a TCL
shell. Refer to the Capture TCL/Tk Advanced Environment Setup of this document on how to install and
setup your environment with ActiveTcl.
Step 1. Create input file containing list of designs/libraries to be revised

---

Before running the utility you need to prepare the batch update process. For revising design files
(*.DSN), create a file containing the fully qualified names of all your designs that needs to be revised.
The format of this file would be something like this:
F:/design_data/capture/original/A8BITBCD.DSN
F:/design_data/capture/test/designs/AA.DSN
F:/uprev_downrev/original/designs/ABC.DSN
Similarly, for revising library files (*.OLB), create a file containing the fully qualified names of all libraries
that you want to revise. The format of this file would be something like this:
F:/design_data/library/gate.olb
F:/cadence/tools/capture/library/fpga.olb
Each line in these file should contain only one fully qualified design/library name. Note that you cannot
include library and design file names in the same input file.
Step 2. Setup TCL shell environment for using Capture DB API (Option – to be performed only when a
standalone TCL shell is used)
This step is required only if you wish to run the script from a standalone TCL shell. If you are using the
command window within the Capture application you do not need this step. Load the OrCAD DB
package into the TCL environment. This can be done by the following command in the TCL shell. The
following load command assumes that an environment variable CDS_INST_DIR is defined which points
to the Cadence OrCAD 16.3 installation root folder.
load [file normalize [file join $env(CDS_INST_DIR)/ tools \
capture orDb_Dll_TCL]] DboTclWriteBasic
Step 3. Source the TCL script
This step is required for running the revision utility from either the standalone TCL shell, or from the
command window within the Capture application. Copy the contents of the TCL script shown in TCL
Script Source for Capture design revision to a file and name it caprev.tcl. Load this file in your TCL
command window by typing the following command:
# the <file_path_to_caprev.tcl> in the following line \
# should be replaced with the actual path where caprev.tcl resides
# e.g. source [file normalize {c:\caprev.tcl}]
source [file normalize {<file_path_to_caprev.tcl>}]
Step 4. Run the revision utility

---

You can now revise your design or library files to the latest Capture database format by typing the
following command:
capRev::rev_main design uprev <path to input file containing full
qualified design paths to be up-revved>
Similarly, to down-rev designs, use:
capRev::rev_main design downrev <path to input file containing full
qualified design paths to be down-revved>
To revise libraries, issue the following command:
capRev::rev_main library uprev <file containing full qualified library
paths to be up-revved>
and to down-rev,
capRev::rev_main library downrev <file containing full qualified
library paths to be down-revved>

---

4.2.1 TCL Script Source for Capture design revision
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: caprev.tcl
# contains OrCAD Capture Design File revision procedures
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package require DboTclWriteBasic 16.3.0
package provide capRev 1.0
namespace eval ::capRev {
variable REVISION_ERRNO_ENV_VAR_NOT_FOUND 100
variable REVISION_ERRNO_DBOPACKAGE_NOT_FOUND 101
variable REVISION_ERRNO_LIST_FILE_NOT_FOUND 102
namespace export rev_main
}
proc ::capRev::rev_logerror { pCode pString } {
puts "\[REVISION ERROR:$pCode\] $pString"
}
proc ::capRev::rev_design { pSession pDesignFile pStatus pDoWhat } {
set lDesignPath [DboTclHelper_sMakeCString $pDesignFile]
set lDboDesign [DboSession_GetDesignAndSchematics $pSession \
$lDesignPath $pStatus]
if { $lDboDesign == "NULL" } {
rev_logerror $pStatus "Unable to open $pDesignFile"
} else {
if { $pDoWhat == "uprev" } {
puts -nonewline "Upreving $pDesignFile "
set lDoConvert [DboLib_ConvertRequired $lDboDesign]
if { $lDoConvert == 1 } {
DboSession_MarkAllLibForSave $pSession $lDboDesign
set lStatus [DboSession_SaveDesign $pSession $lDboDesign]
if { [DboState_Failed $lStatus] == 1 } {
rev_logerror $lStatus "- Error"
} else {
puts "- Success"
}
} else {
puts "- Current"
}
} else {
DboSession_MarkAllLibForSave $pSession $lDboDesign
puts -nonewline "Downreving $pDesignFile "
set lStatus [DboSession_SaveDesignAs $pSession $lDboDesign \
2 0 $lDesignPath 1]
if { [DboState_Failed $lStatus] == 1 } {

---

rev_logerror $lStatus "- Error"
} else {
puts "- Success"
}
}
DboSession_RemoveDesign $pSession $lDboDesign
}
}
proc ::capRev::rev_library { pSession pLibraryFile pStatus pDoWhat } {
set lLibraryPath [DboTclHelper_sMakeCString $pLibraryFile]
set lDboLibrary [DboSession_GetLibAndSchematics $pSession \
$lLibraryPath $pStatus]
if { $lDboLibrary == "NULL" } {
rev_logerror $pStatus "Unable to open library $pLibraryFile"
} else {
if { $pDoWhat == "uprev" } {
set lDoConvert [DboLib_ConvertRequired $lDboLibrary]
puts -nonewline "Upreving $pLibraryFile "
if { $lDoConvert == 1 } {
DboSession_MarkAllLibForSave $pSession $lDboLibrary
DboSession_SaveLib $pSession $lDboLibrary
if { [DboState_Failed $pStatus] == 1 } {
rev_logerror $pStatus "- Error"
} else {
puts "- Success"
}
} else {
puts "- Current"
}
} else {
DboSession_MarkAllLibForSave $pSession $lDboLibrary
puts -nonewline "Downreving $pLibraryFile "
set lStatus [DboSession_SaveLibAs $pSession $lDboLibrary \
2 0 $lLibraryPath 1]
if { [DboState_Failed $lStatus] == 1 } {
rev_logerror $lStatus "- Error"
} else {
puts "- Success"
}
}
DboSession_RemoveLib $pSession $lDboLibrary
}
}
proc ::capRev::get_file_list { pListFile } {
set lFileName [file normalize $pListFile]
if { [ catch { open $lFileName r } lFileHandle ] } {
rev_logerror $DboUtils::REVISION_ERRNO_LIST_FILE_NOT_FOUND \"Unable to open revision file-list
$pListFile"
return 0
}
set lFiles [ read $lFileHandle ]
close $lFileHandle

---

set lRet {}
foreach lFile $lFiles {
lappend lRet $lFile
}
return $lRet
}
proc ::capRev::rev_main { { pReviseWhat "NONE" } { pDoWhat "NONE" } \
{ pListFile "-" } } {
if { $pReviseWhat == "NONE" || $pDoWhat == "NONE" || $pListFile == "-" } {
puts "Usage: capRev::rev_main {design|library} {uprev|downrev} list_file"
return 0
}
set lSession [DboTclHelper_sCreateSession]
set lStatus [DboState]
set file_list [get_file_list $pListFile]
if { $file_list == 0 } {
return 0
}
if { $pReviseWhat == "design" } {
foreach lDesignFile $file_list {
rev_design $lSession $lDesignFile $lStatus $pDoWhat
}
} else {
if { $pReviseWhat == "library" } {
foreach lLibraryFile $file_list {
rev_library $lSession $lLibraryFile $lStatus $pDoWhat
}
}
}
delete_DboSession $lSession
}
# end of file