# Chapter 5: Synchronizing PCB Footprint Property Value on Part

Instances with the Property Value on Their Cached Packages
after Replace Cache
5.1 Introduction
If you do a replace cache, with "Replace Schematic Part Properties" checked and "Preserve Ref Des"
selected, the PCB Footprint is not updated on the part instances. If you uncheck "Preserve Ref Des" the
PCB Footprint is updated, however you loss all the Ref Des information for that part. Many a times, it is
also desirable to change PCB footprint values on the placed part instances and match with the PCB
footprint value on the cached package after doing replace cache. This section presents a TCL script
which lets you synchronize the PCB Footprint property value on part instances with the property value
on their cached packages after replace cache.
5.2 Script and Usage
The TCL script in TCL Script Source for synchronizing PCB footprint property value can be used to
synchronize the PCB Footprint property value on part instances with the property value on their cached
packages after replace cache. This script can be run either from a standalone TCL shell or from within
the Capture command window. In order to run it from a standalone TCL shell you would need to have
ActiveTcl installed on your system. The OrCAD Capture installation does not ship a TCL shell. Refer to the
Capture TCL/Tk Advanced Environment Setup of this document on how to install and setup your
environment with ActiveTcl.
Step 1. Setup TCL shell environment for using Capture DB API (Optional – to be performed only when
a standalone TCL shell is used)
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

---

for synchronizing PCB footprint property value to a file and name it capSyncPropPCBFootprint.tcl. Load
this file in your TCL command window by typing the following command:
# the <file_path_to_capSyncPropPCBFootprint.tcl> in the following line \
# should be replaced with the actual path where
capSyncPropPCBFootprint.tcl resides
# e.g. source [file normalize {c:\capSyncPropPCBFootprint.tcl}]
source [file normalize {<file_path_to_capSyncPropPCBFootprint.tcl>}]
Step 3. Run the utility
In the Capture TCL shell, following commands can be run
capSyncPropPCBFootprint::syncActiveDesign ReportAllDiffs
- This command will report (in the session log + TC shell) all the differences in the active design
capSyncPropPCBFootprint::syncActiveDesign ReportNewDiffs
- This command will report (in the session log + TC shell) all the new differences in the active
design (between the last report run and new report run)
capSyncPropPCBFootprint::syncActiveDesign UpdateAllDiffs
- This command will update all the differences in the active design
capSyncPropPCBFootprint::syncActiveDesign UpdateNewDiffs
- This command will update all the new differences in the active design
capSyncPropPCBFootprint::syncDesign <designfilepath> ReportAllDiffs
e.g. capSyncPropPCBFootprint::syncDesign G:/CaptureData/SIGXP1.DSN ReportAllDiffs
- This command will report all the differences in the design specified by the <designfilepath>
capSyncPropPCBFootprint::syncDesign <designfilepath> UpdateAllDiffs
e.g. capSyncPropPCBFootprint::syncDesign G:/CaptureData/SIGXP1.DSN UpdateAllDiffs
- This command will update all the differences in the design specified by the <designfilepath>
In the Standalone TCL shell, following functionality has been provided
capSyncPropPCBFootprint::syncDesign <designfilepath> ReportAllDiffs
e.g. capSyncPropPCBFootprint::syncDesign G:/CaptureData/SIGXP1.DSN ReportAllDiffs
- This command will report all the differences in the design specified by the <designfilepath>
capSyncPropPCBFootprint::syncDesign <designfilepath> UpdateAllDiffs
e.g. capSyncPropPCBFootprint::syncDesign G:/CaptureData/SIGXP1.DSN UpdateAllDiffs
- This command will update all the differences in the design specified by the <designfilepath>

---

5.2.1 TCL Script Source for synchronizing PCB footprint property value
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: capSyncPropPCBFootprint.tcl
# contains OrCAD Capture Sync PCB Footprint procedures
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package require DboTclWriteBasic 16.3.0
package provide capSyncPropPCBFootprint 1.0
namespace eval ::capSyncPropPCBFootprint {
namespace export syncActiveDesign
namespace export syncDesign
variable mOldDiffs [list]
variable mNewDiffs [list]
}
proc ::capSyncPropPCBFootprint::clearList { pList } {
set pList [lreplace $pList 0 end]
return $pList
}
proc ::capSyncPropPCBFootprint::visitPlacedInst { pPlacedInst pMode } {
set lStatus [DboState]
set lNullObj NULL
variable mOldDiffs
variable mNewDiffs
set lCachedPCBFootprintNameStr [DboTclHelper_sMakeCString]
set lPCBFootprintNameStr [DboTclHelper_sMakeCString]
set lRefDesStr [DboTclHelper_sMakeCString]
set lCachedPackage [$pPlacedInst GetPackage $lStatus]
$lCachedPackage GetPCBFootprint $lCachedPCBFootprintNameStr
$pPlacedInst GetPCBFootprint $lPCBFootprintNameStr
set lCachedPCBFootprintName [DboTclHelper_sGetConstCharPtr $lCachedPCBFootprintNameStr]
set lPCBFootprintName [DboTclHelper_sGetConstCharPtr $lPCBFootprintNameStr]
if { $lCachedPCBFootprintName != "" } {
if { $lPCBFootprintName != $lCachedPCBFootprintName} {
$pPlacedInst GetReferenceDesignator $lRefDesStr
set lOldSearchIndex [lsearch $mOldDiffs $pPlacedInst]
if { $pMode == "ReportAllDiffs"} {
lappend mOldDiffs $pPlacedInst
set lMessage [concat $pMode " : PCB Footprint Mismatch :
" [DboTclHelper_sGetConstCharPtr $lRefDesStr] " :
" $lPCBFootprintName " --> " $lCachedPCBFootprintName]

---

set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
}
if { $pMode == "ReportNewDiffs"} {
if { $lOldSearchIndex == -1} {
lappend mNewDiffs $pPlacedInst
set lMessage [concat $pMode " : PCB Footprint Mismatch:
" [DboTclHelper_sGetConstCharPtr $lRefDesStr] " :
" $lPCBFootprintName " --> " $lCachedPCBFootprintName]
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
}
}
set lNewSearchIndex [lsearch $mNewDiffs $pPlacedInst]
if { $pMode == "UpdateNewDiffs"} {
if { $lNewSearchIndex != -1} {
$pPlacedInst SetPCBFootprint $lCachedPCBFootprintNameStr
$pPlacedInst MarkModified
set lMessage [concat $pMode " : PCB Footprint Changed :
" [DboTclHelper_sGetConstCharPtr $lRefDesStr] " :
" $lPCBFootprintName " --> " $lCachedPCBFootprintName]
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
}
}
if { $pMode == "UpdateAllDiffs"} {
$pPlacedInst SetPCBFootprint $lCachedPCBFootprintNameStr
$pPlacedInst MarkModified
set lMessage [concat $pMode " : PCB Footprint Changed :
" [DboTclHelper_sGetConstCharPtr $lRefDesStr] " :
" $lPCBFootprintName " --> " $lCachedPCBFootprintName]
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
}
}
}
$lStatus -delete
return
}
proc ::capSyncPropPCBFootprint::visitPageInsts { pPage pMode } {
set lStatus [DboState]
set lPartInstIter [$pPage NewPartInstsIter $lStatus]
set lPartInst [$lPartInstIter NextPartInst $lStatus]
set lNullObj NULL
while {$lPartInst!=$lNullObj} {
set lPlacedInst [DboPartInstToDboPlacedInst $lPartInst]
if {$lPlacedInst != $lNullObj} {

---

visitPlacedInst $lPlacedInst $pMode
}
set lPartInst [$lPartInstIter NextPartInst $lStatus]
}
delete_DboPagePartInstsIter $lPartInstIter
$lStatus -delete
return
}
proc ::capSyncPropPCBFootprint::visitPages { pSchematic pMode } {
set lStatus [DboState]
set lPagesIter [$pSchematic NewPagesIter $lStatus]
set lPage [$lPagesIter NextPage $lStatus]
set lNullObj NULL
while {$lPage!=$lNullObj} {
visitPageInsts $lPage $pMode
set lPage [$lPagesIter NextPage $lStatus]
}
delete_DboSchematicPagesIter $lPagesIter
$lStatus -delete
return
}
proc ::capSyncPropPCBFootprint::visitSchematics { pDesign pMode } {
set lStatus [DboState]
set lSchematicIter [$pDesign NewViewsIter $lStatus $::IterDefs_SCHEMATICS]
set lSchematic [$lSchematicIter NextView $lStatus]
set lNullObj NULL
while { $lSchematic!= $lNullObj} {
set lObj [DboViewToDboSchematic $lSchematic]
visitPages $lObj $pMode
set lSchematic [$lSchematicIter NextView $lStatus]
}
delete_DboLibViewsIter $lSchematicIter
$lStatus -delete
return
}
# pMode = ReportAllDiffs | ReportNewDiffs | UpdateAllDiffs | UpdateNewDiffs
proc ::capSyncPropPCBFootprint::syncActiveDesign { pMode } {
set lMessage "---------------------------------------------------------------------------------"
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
set lSession $::DboSession_s_pDboSession
DboSession -this $lSession
set lNullObj NULL
set lDesign [$lSession GetActiveDesign]
if { $lDesign == $lNullObj} {
set lError [DboTclHelper_sMakeCString "Active design not found"]
DboState_WriteToSessionLog $lError
puts [DboTclHelper_sGetConstCharPtr $lError]
return
}
variable mOldDiffs
variable mNewDiffs
if {$pMode == "ReportAllDiffs"} {
set mOldDiffs [clearList $mOldDiffs]

---

set mNewDiffs [clearList $mNewDiffs]
}
if {$pMode == "ReportNewDiffs"} {
set mOldDiffs [concat $mOldDiffs $mNewDiffs]
set mNewDiffs [clearList $mNewDiffs]
}
#updateNewDiffs should forcibly call ReportNewDiffs first
if {$pMode == "UpdateNewDiffs"} {
set mNewDiffs [clearList $mNewDiffs]
visitSchematics $lDesign "ReportNewDiffs"
}
#updateNewDiffs should forcibly call ReportAllDiffs first
if {$pMode == "UpdateAllDiffs"} {
set mOldDiffs [clearList $mOldDiffs]
set mNewDiffs [clearList $mNewDiffs]
visitSchematics $lDesign "ReportAllDiffs"
}
visitSchematics $lDesign $pMode
if {$pMode == "UpdateAllDiffs"} {
set mOldDiffs [clearList $mOldDiffs]
set mNewDiffs [clearList $mNewDiffs]
}
if {$pMode == "UpdateNewDiffs"} {
set mNewDiffs [clearList $mNewDiffs]
}
DboTclHelper_sReleaseAllCreatedPtrs
set lMessage "---------------------------------------------------------------------------------"
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
return
}
# pMode = ReportAllDiffs | UpdateAllDiffs
proc ::capSyncPropPCBFootprint::syncDesign { pDesignPath pMode } {
set lMessage "---------------------------------------------------------------------------------"
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
set lSession [DboTclHelper_sCreateSession]
set lStatus [DboState]
set lDesignPath [DboTclHelper_sMakeCString $pDesignPath]
set lDesign [DboSession_GetDesignAndSchematics $lSession $lDesignPath $lStatus]
set lNullObj NULL
if { $lDesign == $lNullObj} {
set lError [DboTclHelper_sMakeCString [concat "Design not found : " $pDesignPath]]
DboState_WriteToSessionLog $lError
puts [DboTclHelper_sGetConstCharPtr $lError]
return
}
variable mOldDiffs
variable mNewDiffs

---

if {$pMode == "ReportAllDiffs"} {
set mOldDiffs [clearList $mOldDiffs]
set mNewDiffs [clearList $mNewDiffs]
}
visitSchematics $lDesign $pMode
if {$pMode == "UpdateAllDiffs"} {
$lSession MarkAllLibForSave $lDesign
$lSession SaveDesign $lDesign
}
if {$pMode == "UpdateAllDiffs"} {
set mOldDiffs [clearList $mOldDiffs]
set mNewDiffs [clearList $mNewDiffs]
}
$lSession RemoveDesign $lDesign
delete_DboSession $lSession
$lStatus -delete
DboTclHelper_sReleaseAllCreatedPtrs
set lMessage "---------------------------------------------------------------------------------"
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
puts [DboTclHelper_sGetConstCharPtr $lMessageStr]
return
}