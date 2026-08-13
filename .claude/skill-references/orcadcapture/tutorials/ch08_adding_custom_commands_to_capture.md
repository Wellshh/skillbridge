# Chapter 8: Adding Custom Commands to Capture

8.1 Introduction
In the OrCAD Capture 16.3 release, you can add your own custom commands to the application and
make these commands available on the Right-Mouse-Button (RMB) pop-up menu. In this section we will
see how a simple command is added on the RMB pop-up menu in the OrCAD Capture Schematic Editor.
8.2 Requirement
When you add a custom functionality to OrCAD Capture through a TCL script, it is likely that you would
require that the functionality to be available through a GUI element. To help achieve this, the OrCAD
Capture TCL extension provides additional commands. The generic use-case of a custom operation can
be defined as:
i. You select an object.
ii. On RMB click, a pop-up menu appears with custom menu-items listed on it.
iii. These menu-items are enabled or disabled based on specific criteria;
a. For example, when you select a Part the “Assign Power Pins” command is enabled on
the pop-up menu, whereas if you select a Port the “Assign Power Pins” command is
disabled.
iv. You click on the desired menu-item and the requested operation is performed.

---

8.3 Context Aware Rotation
In this section we present a sample functionality that you might want to add to the UI through the TCL
scripting interface.
8.3.1 Problem Statement
In OrCAD Capture, when a part is rotated, the display-properties associated with the part are not
rotated. This is the default application behavior. This behavior causes the dimensions of the part’s
bounding-box to change, thereby displacing other manually placed elements, which is not desirable.
In OrCAD Capture 16.3 a TCL command is provided that modifies this default behavior such that the
display-properties are also rotated when a rotation is performed on a part, thus preserving the part’s
bounding-box dimensions. To enable this behavior, you need to invoke the following command in the
OrCAD Capture command window:
SetOptionBool RotateInstPropInContext TRUE
Once this option is set, rotation on a part also rotates the properties as illustrated below:
In the next section we will see how you can make this functionality available on the RMB pop-up menu
in the OrCAD Capture Schematic Editor.

---

8.3.2 Making a Custom Command Available in the UI
In OrCAD Capture 16.3, the following TCL extension is provided to add custom functionality to RMB pop-
up menus:
RegisterAction <Label> <Enabler> <Accel> <Callback> <ViewType>
Label Label on the pop-up menu
Enabler TCL procedure based on which this menu-item will appear
enabled or disabled
Accel Keyboard Accelerator; currently not used
Callback TCL Procedure that will be invoked when the user clicks on
this menu-item
ViewType The Application View type for which this command is
available. Valid view types are: Schematic, PM, Empty Value
for NULL
In this example we would use the following command:
RegisterAction "Context-Aware Rotate" "::capGUIUtils::capCARotateEnabler" "Ctrl+R"
"::capGUIUtils::capCARotate" "Schematic"
Once this command is registered, the following menu-item starts appearing on RMB pop-up menu as
follows:
Now, to make the functionality available in the application you will have to define the enabler -
“capCARotateEnabler” and the callback - “capCARotate” TCL procedures. The enabler TCL

---

procedure should return 1 if the menu-item needs to appear enabled for a particular selection and
should return 0 if the menu-item should be disabled. The callback TCL procedure is the one which will
actually perform the operation.
8.3.3 TCL Script Source for Context Aware Rotation
#/////////////////////////////////////////////////////////////////////////////////
# WARRANTY: NONE. THIS PROGRAM WAS WRITTEN AS "SHAREWARE" AND IS AVAILABLE AS IS
# AND MAY NOT WORK AS ADVERTISED IN ALL ENVIRONMENTS. THERE IS NO
# SUPPORT FOR THIS PROGRAM
# NOTE: YOU ARE STRONGLY ADVISED TO BACKUP YOUR DESIGN
# BEFORE RUNNING THIS PROGRAM
# TCL file: capCARotate.tcl
# contains OrCAD Capture Context Aware Rotation procedures
#/////////////////////////////////////////////////////////////////////////////////
package require TCL 8.4
package require DboTclWriteBasic 16.3.0
package provide capGUIUtils 1.0
namespace eval ::capGUIUtils {
namespace export capCARotateEnabler
namespace export capCARotate
}
proc ::capGUIUtils::capCARotateEnabler {} {
set lEnableRotate 0
# Get the selected objects
set lSelObjs [GetSelectedObjects]
# Enable only for single object selection
if { [llength $lSelObjs] == 1 } {
# Enable only if a part or a hierarchical block is selected
set lObj [lindex $lSelObjs 0]
set lObjType [DboBaseObject_GetObjectType $lObj]
if { $lObjType == 12 || $lObjType == 13 } {
set lEnableRotate 1
}
}
return $lEnableRotate
}
proc ::capGUIUtils::capCARotate {} {
# Note: this command will override the
# currently selected global rotation mode
SetOptionBool RotateInstPropInContext ON
Rotate
SetOptionBool RotateInstPropInContext OFF
}
# source c:/temp/capCARotate.tcl