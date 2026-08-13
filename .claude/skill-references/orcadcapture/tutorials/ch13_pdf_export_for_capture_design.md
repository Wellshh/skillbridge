# Chapter 13: PDF Export for Capture Design

13.1 Introduction
Sometimes, you are interested in exporting the PDF for Capture designs. This section presents
the information about a shareware utility built with TCL/Tk which lets you exporting PDF from Capture
design.
13.2 Architecture
Capture provides the facility of exporting the design to PDF, subject to the
availability of Postscript (PS) driver and Postscript-to-PDF converter software on
user’s machine. The following diagram shows the architecture of PDF Export

---

13.3 Use Model
The use-model of PDF export is as follows-
1. User installs a suitable Postscript driver in any of the following ways-
a) Install a suitable postscript driver through “Add Printer” wizard-
Click on “Add a printer” RMB option under Printers and Faxes
Add a local printer

---

Create a new “Local Port”
Name the port anything, e.g. “PS”
Choose “Generic” -> “MS Publisher Color Printer”

---

If the following window comes, choose “Replace the current driver”
Give the Printer name, e.g. “OrCADPSPrinter”

---

Do not share the printer
Do not set the printer as default
You will see a OrCADPSPrinter installed

---

b) Alternatively, download a suitable Postscript driver installer -
An example is Adobe Universal Postscript Driver installer for
Windows (Acrobat Distiller PostScript Printer driver) that can be
downloaded and installed from
http://www.adobe.com/support/downloads/product.jsp?platform=
win&product=pdrv). In case of installing this driver, the following
two files need to be downloaded from this location:
 PPD Files: Adobe
(http://www.adobe.com/support/downloads/detail.jsp?ftpI
D=204)
After downloading this file, extract the *.PPD files to any
location (e.g. c:/temp/Adobe)
 Adobe Universal PostScript Windows Driver Installer - English
(http://www.adobe.com/support/downloads/detail.jsp?ftpI
D=1500)
After downloading this file (winsteng.exe), run the
executable and select the following installation options as
shown in the diagrams below
Select Local printer

---

Select “FILE : Local Port”
Select “Browse”
Select the location where *.PPD files were extracted in the first step
and press OK

---

Select “Acrobat Distiller”
Select “Not Shared”
Select “No” in print test page

---

c) A postscript printer (on the network or attached to the machine)
can also be used as a postscript driver. Output will vary depending
on the selected postscript driver.
2. User acquires a suitable Postscript-to-PDF converter - User can acquire any
third party Postscript to PDF converter tool and use the tool for generating
the PDF output from the postscript file.
Examples are Distiller from Acrobat Professional (commercial and can be
acquired from http://www.adobe.com/products/acrobatpro ) or Ghostscript
(free and can be acquired from
http://sourceforge.net/projects/ghostscript). There are many other
commercial and free tools available. User needs to acquire or purchase any
of these tools and install the software at their end.
3. User runs the PDF Export command in Capture by performing the following
steps-
a) Opens a design in Capture
b) Select the design the Project (PM) view. Make sure that only the
design is selected
c) Open the “PDF Export” dialog from the TCL/Tk Application
Dashboard
d) Feed the data in the form and press OK
e) The PDF Export exports the PDF file with progress messages in the
session log
f) Open the PDF file for viewing using any PDF file viewer.

---

The following diagram depicts the use model of Export PDF -
13.4 Output PDF File Features
There are two PDF files generated-
4. Design PDF file
5. Design object properties PDF file (optional) - This is useful for property
values searching etc
The Design PDF file generated is rich with the following features present-
6. The design hierarchy tree (under bookmarks)
7. The reference designators list (under bookmarks)
8. The nets and connected component pins (under bookmarks)
9. The descend-ability for hierarchical blocks
10. In-place properties for all types of design objects on clicking the object
11. Bidirectional cross-probing of the object with properties PDF file

---

The following two diagrams show the features of the generated design PDF file -
Design Hierarchy, Reference Designators and Nets with connect components in
the Bookmark section
Descend option, Object properties and cross-probing option with Properties PDF
file

---

13.5 The PDF Export Form
2. Press Launch
1. Select “PDF Export” under
Design Utilities
The PDF Export
form is launched
from the TCL/Tk
Application
Dashboard
The following
PDF Export form
comes up on
pressing
“Launch”, if the
Project (PM) view
is active and the
design is selected
in it:

---

13.5.1 PDF Export form field descriptions
This section describes the user options available while performing PDF export.
Output Directory – Intermediate postscript files and output PDF files are generated
in this folder. The user must have write permission in this
directory.
Default value – Design directory
Output PDF File – Name of the output PDF file.
Default value – Design name suffixed with .pdf
Postscript Driver – Name of the postscript driver to generate postscript files from
the design file.
For local postscript drivers or printers, only the name of the
driver or printer will be required (e.g. “Acrobat Distiller”). For
network postscript printer, fully qualified path will be
required, e.g. \\srv-comp\printer01
Depending on the postscript driver used, the output will be
colored or black-and-white.
Default value – “Acrobat Distiller”
PS to PDF Converter – This specifies the name and the corresponding command for
the Postscript-to-PDF converter tool.
In case of using the “Custom” command, user needs to specify
the command in terms of two variables
$::capPdfUtil::mPdfFilePath and $::capPdfUtil::mPSFilePath
which correspond to output PDF file path and intermediate
postscript file path respectively.
User needs to ensure that either the fully qualified path of the
PS-to-PDF tool is specified in the command or they are
accessible through environment’s PATH variable.
Users can change the default PS-to-PDF Converter option list
by modifying the TCL procedure

---

::capPdfUtil::populateDefaultPSToPDFConverterList inside
tclscripts/capUtils/capPdfUtil.tcl file.
Default value – “Acrobat Distiller”
Default command - {acrodist.exe} /N /q /o
$::capPdfUtil::mPdfFilePath $::capPdfUtil::mPSFilePath
Options:
Printing Mode – Two modes of exporting the design into PDF are supported
– Occurrence mode and Instance mode.
Default value – “Occurrence mode”
Orientation – Two orientations of exporting the design into PDF are
supported – Landscape and Portrait
Default value – “Landscape”
Create Properties PDF File – If this option is turned ON, a separate
Properties PDF file (Name is Prop<Design>.pdf) is also created
for all the design objects. A cross-probing between the Design
PDF file and properties PDF file is also in-built. The generation
of this file usually takes more time because of extensive data.
Default value – “OFF”
Create Net and Part Bookmarks – If this option is turned ON, the bookmark
section in the design PDF file shows two additional
information trees – one for all the reference designators and
another for all the nets with their connected components.
Default value – “ON”
Output Paper Size - The user can choose the size of the output paper size in the PDF
file. The option shows a list of all possible values that are
supported by various Postscript drivers though some Postscript
drivers may support only the commonly used paper sizes.

---

13.6 More Customization capabilities
13.6.1 Object and properties filtering for PDF annotation
User can apply his own filters inside the TCL procedures present in the TCL file to
control the PDF annotations for different type of objects. For example, if he wants
to not print the properties of graphical objects such as rectangles, arcs etc, he can
do those customizations in the TCL file easily.
The user can do such customizations in the tclscripts/capUtils/capPdfUtil.tcl file
13.7 Minimum software requirement
1) OrCAD Capture release 16.3, hotfix-s013
2) Third party Postscript driver
3) Third party Postscript-to-PDF converter
13.8 Handling Error Code in PDF Export
On exporting very large designs, e.g. while printing more than 300-400 pages, user
may experience error message like “Failed to create empty document” and some
pages may not be exported when this error comes. The reason behind this can be
the resource crunch of any of the following types-
1) Desktop Heap (
http://blogs.msdn.com/ntdebugging/archive/2007/01/04/desktop-heap-
overview.aspx )
2) User Objects ( http://msdn.microsoft.com/en-us/library/ms725486(VS.85).aspx )
3) GDI objects ( http://msdn.microsoft.com/en-us/library/ms724291(VS.85).aspx )
The default limits for these are as follows-
1) Desktop Heap - per desktop default heap size is 3072 (governed by registry key
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session
Manager\SubSystems\Windows
2) User Object - per process default user object is 10000 (governed by registry key
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
NT\CurrentVersion\Windows\USERProcessHandleQuota

---

3) GDI Objects - per process default GDI object is 10000 (governed by registry key
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
NT\CurrentVersion\Windows\GDIProcessHandleQuota
When any application attempts to consumes these resources beyond their limits that
may result in the exception thrown to the user something like "Failed to create
empty document".
There are ways to measure the values currently used by the system at any point in
time -
1) Desktop Heap - Desktop Heap Monitor (dheapmon ) -
http://www.microsoft.com/downloads/details.aspx?familyid=5cfc9b74-97aa-4510-
b4b9-b2dc98c8ed8b&displaylang=en
After installation, the following procedure needs to be done
a) dheapinst.exe -y srv*http://msdl.microsoft.com/download/symbols (make sure
you are on internet)
b) dheapmon -l (to load the driver)
c) dheapmon (to see the stats)
d) dheapmon -u (to unload the driver)
2) User Object - In the Windows task manager Processes tab, Select Menu View ->
Select Columns -> Select User Objects
3) GDI Objects - In the Windows task manager Processes tab, Select Menu View ->
Select Columns -> Select GDI Objects
To overcome the issue of resource crunch, the user needs to set these keys with
higher values in the registry (and reboot the system), so that Capture is able to
acquire required amount of resources without fail. The higher values can be set as
follows-
1) Desktop Heap - change the default value 3072 to 8192
a) Go to registry key -
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session
Manager\SubSystems\Windows
b) The value will look something like - %SystemRoot%\system32\csrss.exe
ObjectDirectory=\Windows SharedSection=1024,3072,512 Windows=On

---

SubSystemType=Windows ServerDll=basesrv,1
ServerDll=winsrv:UserServerDllInitialization,3
ServerDll=winsrv:ConServerDllInitialization,2 ProfileControl=Off
MaxRequestThreads=16
c) In the value, SharedSection specifies the System and desktop heaps using the
following format: SharedSection=xxxx,yyyy,zzz where xxxx defines the
maximum size of the system-wide heap (in kilobytes), yyyy defines the size of
the per desktop heap, and zzz defines the size of the desktop heap for a
"noninteractive" window station.
d) Change ONLY the yyyy value to 8192 (or larger) and press OK.
(Refer to http://stackoverflow.com/questions/507853/system-error-code-8-not-
enough-storage-is-available-to-process-this-command for more details)
2) User Object -change the default user object from 10000 to 16384
a) Go to registry key - HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
NT\CurrentVersion\Windows\USERProcessHandleQuota
b) Change the value from 10000 to 16384 and press OK
3) GDI Object -change the default GDI object from 10000 to 16384
a) Go to registry key - HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
NT\CurrentVersion\Windows\GDIProcessHandleQuota
b) Change the value from 10000 to 16384 and press OK
After any or all of these changes, make sure to REBOOT the system before running
the tool.