# Chapter 1: Scripting Capability in OrCAD Capture

As part of the Cadence® 16.3 release, OrCAD® Capture was enhanced to include support for TCL/TK
scripting capability; greatly extending users’ ability to develop custom applications and scripts for their
design environment. This provides users with immense power to interact with both the Capture UI and
the design database.
Productivity improvements and tool efficiency drive the need for scripting and customization in a user’s
design environment. With scripting and customization, designers can apply automation to manual
processes and complete projects faster. Manual, often tedious, tasks can be automated, difficult
operations can be streamlined, and custom features that don’t exist natively can be created; further
enhancing and extending the Capture environment.
Capture’s new scripting functionality provides the ability for users to execute TCL/TK commands as well
as custom scripts through a command window or GUI customizations. The integrated TCL interpreter
also allows execution of any standard TCL/TK command as well as numerous Capture specific TCL/TK
commands.
The Capture Command Window can be displayed (if not already available) by selecting
View->Toolbar->Command Window Menu.

---

TCL/TK provides an extensive set of scripting functionality. The core TCL/TK functionality includes
procedures and commands for data manipulation, control constructs, mathematical expressions, file I/O
routines, system calls, registry handling, GUI designing, and many more. The always growing additional
packages of TCL/TK are just making almost everything possible that can be done using any procedural
language. Refer to Learn Basic TCL for learning basic TCL syntax.
The integrated TCL interpreter in OrCAD Capture allows any commands from these TCL/TK packages to
run seamlessly. On top of that, OrCAD Capture provides a rich set of its own TCL commands that gives
immense power to the users to interact with both Capture UI and database through the scripting
interface.
Capture TCL Communication Server-Client
OrCAD OrCAD Capture Other S t a
n
Capture Command Window OrCAD Capture Standalone d a
Database (.dsn/.olb) Applications r d
UI
T
C
L
c
o
m
m
a
n
d
User action TCL commands Database TCL Commands s
TCL installation
Capture provides two sets of its own TCL commands:
 User action TCL commands
 Database TCL commands
1.1 User action TCL commands
User-action TCL commands correspond to the operations within the GUI performed by the user. Every
user action performed in Capture is logged in the form of a TCL command. Journaling provides the
facility to store and later replay the command or copy for use in an external script.

---

The Journaling option is set through a TCL command “SetOptionBool Journaling TRUE” and allows
manual actions to display the corresponding TCL commands. All these TCL commands can be replayed
in individually or Capture automatically stores these commands in a TCL script file that can be replayed
to repeat the steps.
For example, if the following action is performed – click the “Place Wire” icon and then draw a wire at
co-ordinates (4.00, 1.00) to (6.00, 1.00) – the action is captured as a TCL command in the command
window as “PlaceWire 4.00 1.00 6.00 1.00”. Executing this TCL command would have the exact same
effect as placing the wire manually with the “Place Wire” command.
These commands allow users to perform a large set of operations automatically for specific needs and
provide a lot of customization capabilities. This capability also helps in debugging custom scripts as it
provides a definite mechanism for step-by-step re-creation.

---

1.2 Database TCL commands
Capture also provides rich set of TCL commands that allow users to interact with design and library
databases directly. These database TCL commands allow for both querying and manipulation of the
design and library objects. All types of design and library objects, e.g. schematics, pages, parts, pins,
nets, wires, globals, off-pages, ports, library packages, graphic objects, etc. and their properties can be
queried, iterated and manipulated using TCL commands.
The database TCL commands provide the same power as Capture SDK APIs. Due to its power of directly
interacting with the database objects, engineering organizations and end users can build large sets of
customized design verification and manipulation procedures using these TCL commands. Refer to Learn
Capture Database TCL for learning how to use Capture database TCL commands.
As an example, if a user wants to simultaneously manipulate all the parts on a schematic page and add a
custom property “PartVersion” with a value of “1.1”, the following custom TCL procedure can be utilized
for this.
proc addPropertyToAllPartsOnPage { pPage } {
set lNullObj NULL
set lStatus [DboState]
set pPartInstsIter [$pPage NewPartInstsIter $lStatus]
set pInst [$pPartInstsIter NextPartInst $lStatus]
# iterate over all parts
while {$pInst!=$lNullObj} {
set lPropNameCStr [DboTclHelper_sMakeCString "PartVersion"]
set lPropValueCStr [DboTclHelper_sMakeCString "1.1"]
#add the property to part
set lStatus [$pInst SetEffectivePropStringValue $lPropNameCStr $lPropValueCStr]
set pInst [$pPartInstsIter NextPartInst $lStatus]
}
delete_DboPagePartInstsIter $pPartInstsIter
$lStatus -delete
}
These database TCL commands can be run within the Capture command window as well as in a
standalone TCL shell. Any TCL-aware application can also use these commands directly within its
process space. TCL commands are available to get active session, create new session, get active
design/schematic/page, open any design or library in the session and then perform the iterations to
retrieve and manipulate the desired set of database objects.
The command window in Capture also allows users to modify their custom TCL procedures as needed
within a session. The modified script can be sourced again in the command window to display the
changed behavior.

---

1.3 Automatic script load and procedure calls
The scripting framework in Capture provides various mechanisms for automatic script loading and
automatic calling of TCL procedures. This framework allows users to have customized sets of operations
and behaviors automatically available upon starting a Capture session and for various types of trigger
events.
For example, if user wants to always place a set of custom title blocks on a new page, he can use this
feature to run a custom TCL procedure automatically whenever a new page is created.
The framework includes the following functionality:
1.3.1 Automatic scripts loading at Capture startup
Capture automatically sources capture\tclscripts\capinit.tcl file at startup. Also, all the *.tcl files present
inside capture\tclscripts\capAutoLoad folder are sourced automatically during Capture startup. Using
this method, users can make their custom scripts and procedures available in Capture by default. These
files are searched using Cadence standard CSF search technology.
1.3.1.1 Recommendation to TCL application providers
The TCL/TK application providers for Capture are recommended to use the following methodology for
making their TCL applications available to their Capture end-users:
 Install a sub-folder inside <Cadence_Installation_Root>\tools\capture\tclscripts
For example, an application provider “XYZ” will install a sub-folder as
<Cadence_Installation_Root>\tools\capture\tclscripts\XYZ
 This sub-folder (XYZ) must contain all the custom TCL scripts along with a special TCL script file
“pkgIndex.tcl”. The content of the pkgIndex.tcl file contains the mapping of provider specific
packages with the TCL script file names, e.g.
package ifneeded xyzApps 1.0 [list source [file join $dir xyzApps.tcl]]

---

Capture automatically sources all pkgIndex.tcl files present inside sub-folders of tclscripts folder.
This ensures that these custom TCL packages automatically become available in the Capture
session.
For more details and example, please refer to Cadence sample sub-folders, e.g. capForms,
capUtils, capDB etc., inside the tclscripts folder.
 For providing the entry-point to the end-users for the custom TCL functionality, create
menu/sub-menus under top-level “Accessories” menu. Each sub-menu will be associated with a
TCL callback procedure. For creating custom menus/sub-menus under “Accessories”, create a
TCL script, e.g. xyzInit.tcl, by following the instructions as given in chapter Adding custom
menus/submenus under Accessories and associating TCL callbacks. This script file contains the
association of sub-menus with TCL callback procedures.
 Place the xyzInit.tcl script in the folder
<Cadence_Installation_Root>\tools\capture\tclscripts\capAutoLoad. On doing this, the custom
menus/sub-menus automatically get loaded in Capture. The TCL callback procedures for these
sub-menus will call appropriate TCL procedures in the custom packages available inside
<Cadence_Installation_Root>\tools\capture\tclscripts\XYZ sub-folder. This is done by calling
“package require <package name>” command before calling the corresponding TCL procedures.
As an example, you can refer to
<Cadence_Installation_Root>\tools\capture\tclscripts\capAutoLoad\capAppLaunchMenu.tcl
script that adds an accessories submenu for “"Cadence TCL/Tk Utilities -> Utilities" for launching
the TCL/TK Application Dashboard, the required package for which is “capAppLaunch” present
inside <Cadence_Installation_Root>\tools\capture\tclscripts\capForms\capAppLaunch.tcl script
file.
Note:- Do not place a TCL script inside the capAutoLoad folder that does some heavy
computation or does some blocking calls, as it will have an adverse impact on Capture startup.
1.3.2 TCL procedure callback on various events
Capture provides TCL procedure hooks to execute scripts upon event triggers. User needs to register the
custom TCL callback procedure using the “RegisterAction” TCL command. Details are presented in
section “Making a Custom Command Available in the UI”. Any number of TCL callback procedures can
be registered against an event. They all are called in sequence when the particular event is triggered.

---

For the custom title blocks on a new page example, the addition a new page could call a custom TCL
procedure ‘AddPageCustomTitleblocks’ automatically at every new page creation. The registration of
the TCL procedure would be performed with the following command.
RegisterAction "_cdnOrOnNewSchematicPage" "capTrue" "" "::xyzPageUtil::AddPageCustomTitleblocks"
""
where, New page creation hook unique name = _cdnOrOnNewSchematicPage
Custom TCL procedure to call on new page creation = ::xyzPageUtil::AddPageCustomTitleblocks
1.4 Capture TCL/Tk Advanced Environment Setup
Capture TCL/Tk framework works with the default TCL/TK installation that is part of the standard
Cadence installation.
If application developers use advanced TCL features (packages) or Tk GUI extensions (ttk, BWidgets, etc),
the environment needs additional setup. This section shows you how to setup your environment to be
able to create scripts using additional packages available in the ActiveState TCL 8.4.
1.4.1 Installation instructions
Cadence OrCAD Capture recommends ActiveState ActiveTCL version 8.4 for developing TCL/Tk
extensions that require packages not supplied with the default installation. ActiveState ActiveTCL 8.4 is
available for download at:
https://www.activestate.com/activetcl/downloads
Download and install ActiveTCL. In order to develop TCL/Tk GUIs the environment needs to be setup as
follows:
1. If you have write-permissions in the Cadence root installation folder, you should modify the
capinit.tcl file within <Cadence Installation Root>\tools\capture\tclscripts
folder. Locate the procedure capGetTclTkHome in this file and uncomment the line
# return [file normalize {TCL/Tk_install_root}]
to point to the location where you have installed ActiveTcl. For example (assuming TCL is
installed at C:/TCL):

---

proc capGetTclTkHome {} {
# Replace the string <TCL/Tk_install_root> in the following line
# with the TCL/Tk installation path on your machine
# and uncomment the following line
return [file normalize {C:/TCL}]
}
Note: This change will affect all users who use Cadence tools this machine.
2. If you do not have write-permissions in the Cadence root installation folder, you should locate
the directory corresponding to the %HOME% environment variable. Within this directory create
the following subdirectory structure if not already present:
%HOME%\cdssetup\capture
3. Once you have created the above directory structure, you should copy the capinit.tcl file
from <Cadence Installation Root>\tools\capture\tclscripts to the newly
created directory and make changes to the capinit.tcl file as described in step 1.
This will ensure that TCL/Tk is automatically loaded and ready for use when Capture starts up.
You can put other initialization procedures in this file. It is important that the name of this file is
capinit.tcl. Capture will load initialization commands only from this file. You can source
multiple TCL/Tk files from within this file. You can also automatically load other packages by
appending to the auto_path TCL variable. Consult the TCL/Tk help files available with your
third party TCL/Tk installation for more details on how to use the auto_path variable to
automatically load packages.
4. Launch Capture and verify setup by issuing the following commands on the Capture Command
Window:
package require Tk
toplevel .new
A Tk window should appear with the title “new”.