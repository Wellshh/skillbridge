# Chapter 10: Adding custom menus/submenus under Accessories and

associating TCL callbacks
10.1 Introduction
Sometimes, you are interested in adding menus/submenus and define your custom actions for
them. This section presents a TCL script which lets you adding menus and submenus under Accessories
and associating TCL callbacks with them.
10.2 Script and Usage
The TCL script in TCL Script Source for adding menus/submenus and define their TCL callbacks
can be used to you adding menus and submenus under Accessories and associating TCL callbacks with
them. This script can be run only from within the Capture command window.
Step 1. Source the TCL script
This step is required for running the utility from the TCL command window within the Capture
application. Copy the contents of the TCL script shown in TCL Script Source for adding
menus/submenus and define their TCL callbacks to a file and name it capMenuUtil.tcl. Load this file
in your TCL command window by typing the following command:
# the <file_path_to_capMenuUtil.tcl> in the following line \
# should be replaced with the actual path where capMenuUtil.tcl resides
# e.g. source [file normalize {c:\capMenuUtil.tcl}]
source [file normalize {<file_path_to_capMenuUtil.tcl>}]
Step 2. Run the utility
Upon sourcing the script itself, menus/submenus get added under the Accessories menu.
Menus can be added either at the schematic page level or at the design level.
For adding a schematic page level menu, an action named “cdnCapTclAddPageCustomMenu”
needs be registered in the TCL script. For adding a design level menu, an action named
“cdnCapTclAddDesignCustomMenu” needs to be registered in TCL script.
The TCL procedures associated with these actions are called for menu/submenu creation data.
For every submenu added, TCL script needs to define one TCL callback function that gets called
when submenu is selected. In the TCL callback procedure, as per the need, the design data can be
accessed/manipulated or any external program can be invoked or any other task can be performed

---

Registering an action with an associated procedure
RegisterAction "_cdnCapTclAddPageCustomMenu" "::capMenuUtil::capTrue" ""
"::capMenuUtil::addPageAccessoryMenu" ""
Action – cdnCapTclAddPageCustomMenu
Associated procedure – ::capMenuUtil::addPageAccessoryMenu
Adding menu/submenu information in the associated procedure
proc ::capMenuUtil::addPageAccessoryMenu { } {
AddAccessoryMenu "Text Editors" "Notepad" "::capMenuUtil::OpenPageNotepad"
AddAccessoryMenu "Text Editors" "Scite" "::capMenuUtil::OpenPageScite"
}
Handling submenu selection in TCL callback
proc ::capMenuUtil::OpenPageNotepad { pPage pOcc } {
exec "C:/WINDOWS/system32/notepad.exe"
}
Schematic page-level menu

---

Design level menu

---

10.2.1 TCL Script Source for adding menus/submenus and define their
TCL callbacks
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: capMenuUtil.tcl
# contains OrCAD Capture Menu utlities
#
# You can run the script in the Capture TCL command window .
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package provide capMenuUtil 1.0
namespace eval ::capMenuUtil {
}
proc ::capMenuUtil::addPageAccessoryMenu { } {
# AddAccessoryMenu <User menu under Accessories> <SubMenu under user menu> <TCL callback
#handler with 2 parameters pPage and pOcc>
AddAccessoryMenu "Text Editors" "Notepad" "::capMenuUtil::OpenPageNotepad"
AddAccessoryMenu "Text Editors" "Scite" "::capMenuUtil::OpenPageScite"
}
proc ::capMenuUtil::addDesignAccessoryMenu { } {
# AddAccessoryMenu <User menu under Accessories> <SubMenu under user menu> <TCL callback
#handler with 1 parameter pLib>
AddAccessoryMenu "Text Editors" "Design in Notepad" "::capMenuUtil::OpenDesignNotepad"
AddAccessoryMenu "Text Editors" "Design in Scite" "::capMenuUtil::OpenDesignScite"
AddAccessoryMenu "Process Viewer" "Process Explorer" "::capMenuUtil::OpenDesignProcessExplorer"
}
proc ::capMenuUtil::OpenPageNotepad { pPage pOcc } {
exec "C:/WINDOWS/system32/notepad.exe"
}
proc ::capMenuUtil::OpenPageScite { pPage pOcc } {
exec "d:/apps/wscite/SciTE.exe"
}
proc ::capMenuUtil::OpenDesignNotepad { pLib } {
exec "C:/WINDOWS/system32/notepad.exe"
}
proc ::capMenuUtil::OpenDesignScite { pLib } {
exec "d:/apps/wscite/SciTE.exe"
}
proc ::capMenuUtil::OpenDesignProcessExplorer { pLib } {
exec "d:/apps/ProcessExplorer/procexp.exe"
}
proc ::capMenuUtil::capTrue { } {
return 1
}
RegisterAction "_cdnCapTclAddPageCustomMenu" "::capMenuUtil::capTrue" ""
"::capMenuUtil::addPageAccessoryMenu" ""
RegisterAction "_cdnCapTclAddDesignCustomMenu" "::capMenuUtil::capTrue" ""
"::capMenuUtil::addDesignAccessoryMenu" ""