# Chapter 11: OrCAD Capture TCL/Tk Applications Dashboard

11.1 Introduction
A facility to enumerate and launch TCL/Tk applications from the OrCAD Capture GUI is now
available. This section presents how this mechanism works and what needs to be done to add new
applications to this launcher.
11.2 Use-Model and Customization
The TCL/Tk Applications Dashboard is available only when a design is open in OrCAD Capture. To
launch the dashboard select the Accessories->Cadence TCL/Tk Utilities->Utilities menu, as shown in the
following figure:

---

This brings up the TCL/Tk applications dashboard:
Launches the selected
application
Shows the code in the
CodeViewer
Shows the description
string associated with
the application
The applications listed in this dashboard are controlled by the TCL script capApps.tcl in
<Cadence Installation Root>\tools\capture\tclscripts\capForms directory. This
file contains a TCL procedure capApps::getApps that returns a list of applications that would
be displayed in the dashboard. The TCL list returned by this procedure is structured as follows:
# Structure of a section:
{
<section1 name>
{
<app1_name> <app1 title> <app1 callback> <app1 description> <app1 source code file>
<app2_name> <app2 title> <app2 callback> <app2 description> <app2 source code file>
...
}
<section2 name>
{
<app1_name> <app1 title> <app1 callback> <app1 description> <app1 source code file>

---

<app2_name> <app2 title> <app2 callback> <app2 description> <app2 source code file>
...
}
...
}
For example, the applications listed in the default dashboard are configured through the following
list:
proc capApps::getApps {} {
set lAppList {
{
"Application Utilities"
{
{ "ExtPrefs"
"Extended Preferences"
"capExtPrefs::launchForm"
"Extended application preferences settings."
"capForms/capExtPrefs.tcl"
}
}
}
{
"Design Utilities"
{
{
"PDFExport"
"PDF Export"
"capPdfLaunch::init"
"Exports the selected design to PDF format with cross-references and
properties"
"./capUtils/capPdfLaunch.tcl"
}
}
}
{
"Scripting Documentation"
{
{"HelpPDF"
"Help on Scripting"
"capAppLaunch::appLaunchFormHelp"
"Launches the application notes PDF document. This contains installation steps,
samples and other useful information."
""
}
}
}
}
return $lAppList
}
Please note these points while adding applications:
 The application name must not contain spaces.
 The callback is the name of the TCL procedure that will be invoked when the application is
selected.
 The description string is displayed in the description area of the dashboard when the application
is selected.

---

 The location of the file containing the source code should be specified relative to the <Cadence
Installation Root>\tools\capture\tclscripts directory. This information is not
mandatory.
When the “Show Code” button is clicked, the associated script file (if any) is displayed in the
CodeViewer (a read-only viewer).