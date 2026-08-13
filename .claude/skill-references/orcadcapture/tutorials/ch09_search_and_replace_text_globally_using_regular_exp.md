# Chapter 9: Search and Replace Text Globally using Regular Expression

9.1 Introduction
Sometimes, you are interested in searching and replacing text globally in a design using regular
expression. This section presents a TCL script which lets you search and replace text globally in the
currently active session.
9.2 Script and Usage
The TCL script in TCL Script Source for searching and replacing text globally in design in
the currently active Capture session can be used to search and replace text globally in the currently
active session. This script reports the searched and replaced text locations in the session log. This script
can be run only from within the Capture command window.
Step 1. Source the TCL script
This step is required for running the utility from the TCL command window within the Capture
application. Copy the contents of the TCL script shown in TCL Script Source for searching and
replacing text globally in design in the currently active Capture session to a file and name it
capDesignUtil.tcl. Load this file in your TCL command window by typing the following command:
# the <file_path_to_capDesignUtil.tcl> in the following line \
# should be replaced with the actual path where capSessionUtil.tcl
resides
# e.g. source [file normalize {c:\capDesignUtil.tcl}]
source [file normalize {<file_path_to_capDesignUtil.tcl>}]
Step 2. Run the utility
In the Capture TCL shell, following commands can be run
capDesignUtil::searchText <text>
e.g. capDesignUtil::searchText USB1.0
capDesignUtil::replaceText <text to search> <text to replace with>
e.g. capDesignUtil::replaceText USB1.0 USB2.0
Regular expression examples
For replacing *J32* to *J35*, e.g. SN_J32_45 to SN_J35_45, give the following command-
capDesignUtil::replaceText {(.*)J32(.*)} {\1J35\2}
or simply give capDesignUtil::replaceText J32 J35

---

For replacing *J32*K1* to *J35*K2*, e.g. SN_J32_45_K1_20 to SN_J35_45_K2_20, please give the
following command-
capDesignUtil::replaceText {(.*)J32(.*)K1(.*)} {\1J35\2K2\3}
9.2.1 TCL Script Source for searching and replacing text globally in design in
the currently active Capture session
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: capDesignUtil.tcl
# contains OrCAD Capture Design utlities
#
# You can run the script either in the Capture TCL command window .
#
# Steps for running the script in Capture TCL shell
# 1. source <script path>
# e.g. source d:/workdata/capture/dbcheck/Published/capDesignUtil.tcl
#2. capDesignUtil::searchText <text>
# e.g. capDesignUtil::searchText "USB1.0"
#3. capDesignUtil::replaceText <text to search> <text to replace with>
# e.g. capDesignUtil::replaceText "USB1.0" "USB2.0"
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package require DboTclWriteBasic 16.3.0
package provide capDesignUtil 1.0
namespace eval ::capDesignUtil {
namespace export searchText
namespace export replaceText
}
# pTextToSearch can be a regular expression as understood by regexp
proc ::capDesignUtil::searchText { pTextToSearch } {
set lNullObj NULL
if { $pTextToSearch == $lNullObj ||
$pTextToSearch == "" } {
puts "Incorrect usage"
return
}
searchAndReplaceCommentText Search $pTextToSearch ""
}
# pTextToSearch and pTextToReplaceWith can be regular expressions as understood by regexp and regsub
proc ::capDesignUtil::replaceText { pTextToSearch pTextToReplaceWith } {
set lNullObj NULL
if { $pTextToSearch == $lNullObj ||
$pTextToSearch == "" ||
$pTextToReplaceWith == $lNullObj ||

---

$pTextToReplaceWith == "" } {
puts "Incorrect usage"
return
}
searchAndReplaceCommentText Replace $pTextToSearch $pTextToReplaceWith
}
proc ::capDesignUtil::capVisitPageCommentTexts { pPage pMode pTextToSearch pTextToReplaceWith } {
set lStatus [DboState]
set lNullObj NULL
set lPageName [DboTclHelper_sMakeCString]
$pPage GetName $lPageName
set lPageNameStr [DboTclHelper_sGetConstCharPtr $lPageName]
set lSchematicName [DboTclHelper_sMakeCString]
set lSchematic [$pPage GetOwner]
$lSchematic GetName $lSchematicName
set lSchematicNameStr [DboTclHelper_sGetConstCharPtr $lSchematicName]
set lGraphicIter [$pPage NewCommentGraphicsIter $lStatus]
set lGraphic [$lGraphicIter NextCommentGraphic $lStatus]
while {$lGraphic!=$lNullObj} {
set lComment [DboGraphicInstanceToDboGraphicCommentTextInst $lGraphic]
if {$lComment!=$lNullObj} {
set lDef [$lComment GetDboCommentText]
if { $lDef != $lNullObj} {
set lText [DboTclHelper_sMakeCString]
set lStatus1 [$lDef GetText $lText]
set lTextStr [DboTclHelper_sGetConstCharPtr $lText]
$lStatus1 -delete
set lSearchResult [regexp $pTextToSearch $lTextStr]
if { $lSearchResult == 1 } {
set lMessage [concat "Found text : " $pTextToSearch " as
" $lTextStr " on schematic : " $lSchematicNameStr " on page :
" $lPageNameStr]
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
if { $pMode == "Replace"} {
regsub -all $pTextToSearch $lTextStr $pTextToReplaceWith pReplacedText
set lMessage [concat ". .Replaced text :
" $pTextToSearch " found as " $lTextStr " replaced with
" $pReplacedText "on schematic : " $lSchematicNameStr
" on page : " $lPageNameStr]
set lMessageStr [DboTclHelper_sMakeCString $lMessage]
DboState_WriteToSessionLog $lMessageStr
set pReplacedTextCStr [DboTclHelper_sMakeCString $pReplacedText]
$lDef SetText $pReplacedTextCStr
$pPage MarkModified
}
}
}

---

}
set lGraphic [$lGraphicIter NextCommentGraphic $lStatus]
}
delete_DboPageCommentGraphicsIter $lGraphicIter
$lStatus -delete
return
}
proc ::capDesignUtil::capVisitPagesForCommentTexts { pSchematic pMode pTextToSearch pTextToReplaceWith }
{
set lStatus [DboState]
set lPagesIter [$pSchematic NewPagesIter $lStatus]
set lPage [$lPagesIter NextPage $lStatus]
set lNullObj NULL
while {$lPage!=$lNullObj} {
capVisitPageCommentTexts $lPage $pMode $pTextToSearch $pTextToReplaceWith
set lPage [$lPagesIter NextPage $lStatus]
}
delete_DboSchematicPagesIter $lPagesIter
$lStatus -delete
return
}
proc ::capDesignUtil::capVisitSchematicsForCommentTexts { pDesign pMode pTextToSearch pTextToReplaceWith
} {
set lStatus [DboState]
set lSchematicIter [$pDesign NewViewsIter $lStatus $::IterDefs_SCHEMATICS]
set lSchematic [$lSchematicIter NextView $lStatus]
set lNullObj NULL
while { $lSchematic!= $lNullObj} {
set lObj [DboViewToDboSchematic $lSchematic]
capVisitPagesForCommentTexts $lObj $pMode $pTextToSearch $pTextToReplaceWith
set lSchematic [$lSchematicIter NextView $lStatus]
}
delete_DboLibViewsIter $lSchematicIter
$lStatus -delete
return
}
# pMode = Search | Replace
proc ::capDesignUtil::searchAndReplaceCommentText { pMode pTextToSearch pTextToReplaceWith} {
set lSession $::DboSession_s_pDboSession
DboSession -this $lSession
set lNullObj NULL
set lDesign [$lSession GetActiveDesign]
if { $lDesign == $lNullObj} {
set lError [DboTclHelper_sMakeCString "Active design not found"]
DboState_WriteToSessionLog $lError
return
}

---

set lName [DboTclHelper_sMakeCString]
set lStatus [$lDesign GetRootName $lName]
$lStatus -delete
capVisitSchematicsForCommentTexts $lDesign $pMode $pTextToSearch $pTextToReplaceWith
DboTclHelper_sReleaseAllCreatedPtrs
return
}