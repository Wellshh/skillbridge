# Chapter 6: Package Corrections in Capture Library or Design

6.1 Introduction
Sometimes, due to network or software issues, some packages inside a library or a design get corrupted.
This leads to unintended database behavior sometimes leading to software crash or errors like CAP0064
(unexpected error in database access). This section presents a TCL script which lets you correct the
package errors inside a library or a design.
6.2 Script and Usage
The TCL script in TCL Script Source for package corrections in library or design can be used to correct the
package errors inside a library or a design. This script currently finds all the packages whose name entry
is still present in the database but the actual package data is not present. In the correction mode, this
script removes all those dangling package name entries. This script can be run either from a standalone
TCL shell or from within the Capture command window. In order to run it from a standalone TCL shell
you would need to have ActiveTcl installed on your system. The OrCAD Capture installation does not
ship a TCL shell. Refer to the Capture TCL/Tk Advanced Environment Setup of this document on how to
install and setup your environment with ActiveTcl.
Step 1. Setup TCL shell environment for using Capture DB API (Option – to be performed only when a
standalone TCL shell is used)
This step is required only if you wish to run the script from a standalone TCL shell. If you are using the
command window within the Capture application you do not need this step. Load the OrCAD DB
package into the TCL environment. This can be done by the following command in the TCL shell. The
following load command assumes that an environment variable CDS_INST_DIR is defined which points
to the Cadence OrCAD 16.3 installation root folder.
load [file normalize [file join $env(CDS_INST_DIR)/ tools \
capture orDb_Dll_TCL]] DboTclWriteBasic
Step 2. Source the TCL script
This step is required for running the utility from either the standalone TCL shell, or from the command
window within the Capture application. Copy the contents of the TCL script shown in TCL Script Source
for package corrections in library or design to a file and name it capLibUtil.tcl. Load this file in your TCL
command window by typing the following command:
# the <file_path_to_capLibUtil.tcl> in the following line \
# should be replaced with the actual path where capLibUtil.tcl resides
# e.g. source [file normalize {c:\capLibUtil.tcl}]

---

source [file normalize {<file_path_to_capLibUtil.tcl>}]
Step 3. Run the utility
In the Capture TCL shell, following commands can be run
capLibUtil::checkPkgs <library or design file path> <report file path>
e.g. capLibUtil::checkPkgs G:/CaptureData/ABC.olb G:/CaptureData/ReportCheckPkgs.txt
- This command will report all the package related issues in the library / design specified by the
<library or design file path>
capLibUtil::correctPkgs <library or design file path> <report file path>
e.g. capLibUtil::correctkPkgs G:/CaptureData/ABC.olb G:/CaptureData/ReportCorrectionPkgs.txt
- This command will correct the package related issues in the library / design specified by the
<library or design file path>
In the Standalone TCL shell, following functionality has been provided
capLibUtil::checkPkgs <library or design file path> <report file path>
e.g. capLibUtil::checkPkgs G:/CaptureData/ABC.olb G:/CaptureData/ReportCheckPkgs.txt
- This command will report all the package related issues in the library / design specified by the
<library or design file path>
capLibUtil::correctPkgs <library or design file path> <report file path>
e.g. capLibUtil::correctkPkgs G:/CaptureData/ABC.olb G:/CaptureData/ReportCorrectionPkgs.txt
- This command will correct the package related issues in the library / design specified by the
<library or design file path>

---

6.2.1 TCL Script Source for package corrections in library or design
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: capLibUtil.tcl
# contains OrCAD Capture Library data sanity checking and correction
# procedures
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package require DboTclWriteBasic 16.3.0
package provide capLibUtil 1.0
namespace eval ::capLibUtil {
namespace export checkPkgs
namespace export correctPkgs
}
proc ::capLibUtil::checkPkgs { pLibName pReportFilePath } {
do $pLibName Report $pReportFilePath
return
}
proc ::capLibUtil::correctPkgs { pLibName pReportFilePath } {
do $pLibName Correct $pReportFilePath
return
}
#pMode = Report/Correct
proc ::capLibUtil::do {pLibName pMode pReportFilePath} {
if { $pReportFilePath == "" } {
puts $lFile "Please specify the report file name"
}
set lFile [open $pReportFilePath a]
puts -nonewline [concat "Library :" $pLibName]
puts $lFile [concat "Library :" $pLibName]
flush $lFile
#puts $lFile ReadLibraryEntry
set lSession [DboTclHelper_sCreateSession]
set lLibName [DboTclHelper_sMakeCString $pLibName]
set lStatus [DboState]
set lLib [$lSession GetLib $lLibName $lStatus]
set lNullObj NULL
if { $lLib == $lNullObj} {
puts $lFile " : Open Failed"
puts " : Open Failed"
return
}
set lAllPkgNames [list]
set lValidPkgNames [list]
set lAliasPkgNames [list]

---

puts $lFile "Reading package names"
flush $lFile
set pkgNameIter [$lLib NewPackageNamesIter $lStatus]
set pPkgName [DboTclHelper_sMakeCString]
set lStatus [$pkgNameIter NextName $pPkgName]
set lStatusVal [$lStatus Failed]
while {$lStatusVal != 1} {
lappend lAllPkgNames [DboTclHelper_sGetConstCharPtr $pPkgName]
# read all aliases also
set pkgAliasNameIter [$lLib NewPackageAliasesIter $pPkgName $lStatus]
set pPkgAliasName [DboTclHelper_sMakeCString]
set lStatus [$pkgAliasNameIter NextAlias $pPkgAliasName]
set lStatusVal [$lStatus Failed]
while {$lStatusVal != 1} {
lappend lAliasPkgNames [DboTclHelper_sGetConstCharPtr $pPkgAliasName]
set lStatus [$pkgAliasNameIter NextAlias $pPkgAliasName]
set lStatusVal [$lStatus Failed]
}
delete_DboLibPackageAliasesIter $pkgAliasNameIter
set lStatus [$pkgNameIter NextName $pPkgName]
set lStatusVal [$lStatus Failed]
}
delete_DboLibPackageNamesIter $pkgNameIter
puts $lFile "Completed reading package names"
flush $lFile
puts $lFile ""
flush $lFile
puts $lFile ""
flush $lFile
puts $lFile "Reading packages"
flush $lFile
set pkgIter [$lLib NewPackagesIter $lStatus]
set pPkg [$pkgIter NextPackage $lStatus]
set lNullObj NULL
while {$pPkg!=$lNullObj} {
set pActualPkgName [DboTclHelper_sMakeCString]
$pPkg GetName $pActualPkgName
lappend lValidPkgNames [DboTclHelper_sGetConstCharPtr $pActualPkgName]
set pPkg [$pkgIter NextPackage $lStatus]
}
delete_DboLibPackagesIter $pkgIter
puts $lFile "Completed reading packages"
flush $lFile
puts $lFile ""
flush $lFile
puts $lFile ""
flush $lFile
lsort $lAllPkgNames
lsort $lValidPkgNames
lsort $lAliasPkgNames
set lNumberTotalPkgNames [llength $lAllPkgNames]
set lNumberValidPkgNames [llength $lValidPkgNames]
set lNumberAliasPkgNames [llength $lAliasPkgNames]
puts -nonewline $lFile "Number of total package names : "
puts $lFile $lNumberTotalPkgNames
puts -nonewline $lFile "Number of valid package names : "
puts $lFile $lNumberValidPkgNames
puts -nonewline $lFile "Number of alias package names : "
puts $lFile $lNumberAliasPkgNames

---

flush $lFile
set lNonRecoverablePackageErrors 0
puts $lFile ""
puts $lFile ""
puts $lFile "Following packages are corrupt (non-recoverable) : "
puts $lFile "------------------Start-------------------- "
flush $lFile
foreach lPkgName $lAllPkgNames {
# if this is an alias pkg name, just skip
set lSearchIndex [lsearch -exact $lAliasPkgNames $lPkgName]
if {$lSearchIndex == -1} {
# search this pkg name in lValidPkgNames
set lSearchIndex [lsearch -exact $lValidPkgNames $lPkgName]
if {$lSearchIndex == -1} {
if {$pMode == "Report"} {
puts $lFile $lPkgName
incr lNonRecoverablePackageErrors
}
if {$pMode == "Correct"} {
set lName [DboTclHelper_sMakeCString $lPkgName]
$lLib ExplicitlyRemovePartDirName $lName
$lLib MarkModified
puts $lFile [concat "Removed non-recoverable package name : " $lPkgName]
}
}
}
}
puts $lFile "------------------End-------------------- "
puts $lFile ""
puts $lFile ""
flush $lFile
if { $lNonRecoverablePackageErrors > 0 } {
puts $lFile [concat "Number of Non-recoverable package errors : " $lNonRecoverablePackageErrors]
}
flush $lFile
if { $lNonRecoverablePackageErrors == 0 } {
puts $lFile "Library has no package errors"
puts $lFile " : PASSED"
} else {
puts $lFile " : FAILED"
}
puts $lFile "-------------------------------------- "
puts $lFile "-------------------------------------- "
flush $lFile
if {$pMode == "Correct"} {
$lSession MarkAllLibForSave $lLib
$lSession SaveLib $lLib
}
$lSession RemoveLib $lLib
flush $lFile
close $lFile
DboTclHelper_sDeleteSession $lSession

---

return
}
# source d:/workdata/capture/dbcheck/capLibUtil.tcl
# capLibUtil::checkPkgs D:/temp/capture/TT_USER_LIB/TT_USER_LIB.olb PkgCheckReport.txt
# capLibUtil::correctPkgs D:/temp/capture/TT_USER_LIB/TT_USER_LIB.olb PkgCorrectionReport.txt