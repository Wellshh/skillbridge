### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

Before You Start
================

About This Manual
-----------------

This manual is for designers and engineers who use the Allegro PCB Editor SKILL functions to customize existing Allegro PCB Editor interactive commands or create new ones. It describes the AXL (Allegro eXtension Language) user model, how to start AXL, and how to use each AXL function.

This manual assumes that you are familiar with the development and design of printed circuit boards (PCBs). It also assumes you are familiar withAllegro PCB Editor for the physical design of PCBs and analysis of reliability, testability, and manufacturability.

If you are reading this manual for a general understanding of AXL capabilities, but do not actually intend to program in AXL, read[Chapter 1, "Introduction to Allegro PCB Editor SKILL Functions."](01ovrvew.html#103136 "1")

You should also be familiar with the Cadence SKILL language. The following manuals describe SKILL:

* *SKILL Language User Guide*

* *SKILL Language Reference*

* Cadence SKILL Functions Quick Reference

Prerequisites
-------------

Before you begin using Allegro PCB Editor to design boards, you should be familiar with the Allegro PCB Editor environment.

The[*Allegro PCB Editor User Guide: Getting Started with Physical Design*](../algrostart/algrostartTOC.md) explains how to:

* Start Allegro PCB Editor

* Navigate in the Allegro PCB Editor software

* Get help on a command

* Use the mouse, menus and forms

* Start a design session

Command Syntax Conventions
--------------------------

AXL-SKILL descriptions adhere to the conventions described in the*SKILL Language Basics*. In addition, this manual uses the conventions described below.

|  |
| --- | ---
| *italics* | Data type name.
| *nil* | Standard SKILL for empty list; as a return value, may indicate failure.
| *t* | Standard SKILL for "true;" return value for success.
| *[name]* | Optional argument "name."
| *<name>* | Argument of type "name" required.
| *dbid* | Instance of an Allegro PCB Editor database object (means "database id")
| *figure* | Geometric Allegro PCB Editor database object--for example, line, shape, or symbol are all Allegro PCB Editor figures. This is not to be confused with the Allegro PCB Editor's database object "figure", a special graphic denoting DRC markers and drill holes. To ensure clear distinction in this manual, "Allegro PCB Editor figure" denotes this special object.
| *l\_bBox* | A list of the coordinates of a bounding box. Coordinate pairs are lower left and upper right. For example,
|  | (list( 100:100 200:200 ))
| *t\_layer* | A pair of names separated by a slash "/" denoting the name of an Allegro PCB Editor class-subclass. For example, "PACKAGE GEOMETRY/SILKSCREEN\_TOP."
| *lo\_dbid* | Function that takes or returns a dbid or list of dbids.
| *o\_dbid* | Function that takes or returns a single dbid.
Referencing Objects by Name
---------------------------

When programming AXL, you can select or refer to a named object by using the unique name of that object. The table shows Allegro PCB Editor object types and their associated names:

****Table 2-1****
**Allegro PCB Editor Object Types and Names**

| **Allegro PCB Editor Object Type** | **Name**
| NET | netname
| COMPONENT | refdes
| SYMBOL | refdes or symbol pin: <refdes>.<pin number>
| FUNCTION | function designator
| DEVTYPE | device type
| SYMTYPE | symbol type, for example, "DIP 14"
| PROPERTY | property name, for example, "MAX\_OVERSHOOT"
You can select objects using the`axlName` functions in [Chapter 4, "Selection and Find Functions"](05selfnd.html#580309 "4").

Finding Information in This Manual
----------------------------------

The following table summarizes the topics described in this manual.

* **Read . . .**
* [Chapter 1, "Introduction to Allegro PCB Editor SKILL Functions"](01ovrvew.html#103136 "1")
* AXL functions
* AXL initialization, environment
* Starting and stopping AXL
* Debugging AXL programs
* *dbids* and object persistence
* Selecting Allegro PCB Editor database objects
* AXL-SKILL database object types
* [Chapter 2, "The Allegro PCB Editor Database User Model"](02dbdesc.html#462876 "2")
* Database rules
* Attribute types
* Figure (geometric) database types
* Logical database types
* Property database types
* Full attribute listing for all Allegro PCB Editor database objects
* [Chapter 15, "Database Create Functions"](03dbcre8.html#854400 "15")
* Path create functions
* Create shape and rectangle functions
* Create functions for line, pin, symbol, text, and via
* [Chapter 3, "Parameter Management Functions"](04parmgt.html#1069532 "3")
* [Chapter 4, "Selection and Find Functions"](05selfnd.html#580309 "4")
* Point selection
* Box selection
* Selection by name and object*dbid*
* Find filter management
* Selection set management
* [Chapter 5, "Interactive Edit Functions"](06intedt.html#822268 "5")
* Delete objects
* Show objects
* [Chapter 6, "Database Read Functions"](07dbaccs.html#718825 "6")
* Opening an Allegro PCB Editor design
* Accessing standalone branch figures, properties, pads, and text
* [Chapter 7, "Allegro PCB Editor Interface Functions"](08intprm.html#571929 "7")
* Highlighting and displaying database objects
* Loading the cursor buffer and dynamic rubberband displays for interactive commands
* Accepting single and multiple user coordinate picks
* Callback functions for completing and cancelling commands
* [Chapter 8, "Allegro PCB Editor Command Shell Functions"](09cmdshl.html#883012 "8")
* Setting Allegro PCB Editor shell variables
* Sending a command string to the Allegro PCB Editor shell.
* [Chapter 10, "User Interface Functions"](10usrint.html#101740 "10")
* Prompting and getting confirmation from the user, displaying text files
* Displaying and printing ASCII files
* [Chapter 11, "Form Interface Functions"](11frmint.html#414284 "11")
* Creating forms, including the various types of form fields
* Setting up callbacks for response to input to individual fields
* [Chapter 12, "Simple Graphics Drawing Functions"](12draw.html#1037521 "12")
* [Chapter 13, "Message Handler Functions"](13msghnd.html#673512 "13")
* Setting up for user messages
* Displaying messages to users
* [Chapter 14, "Design Control Functions"](14dsnctl.html#688730 "14")
* Opening a design
* Compiling, running edit check, and saving the current (symbol) design
* Getting the type of the active design
* Setting the Allegro PCB Editor symbol type
* Getting or setting the value for a specified database control, sector, and obstacle
* Changing the extents, origin, units and accuracy of the design
* Setting, deleting, and getting information about locks on the database
* Setting, clearing, and printing information about triggers, which register interest in events that occur in Allegro PCB Editor
* Getting the active class and subclass, active text block, type of design technology in use, and the full path of the drawing
* Saving the design
* Saving a board padstack out to a library
* Creating a new padstack by copying from an existing padstack
* Running dbdoctor on the current database
* [Chapter 16, "Database Group Functions"](15dbgrp.html#1037521 "16")
* Creating and removing database groups.
* Adding and removing database objects from database groups.
* [Chapter 17, "Database Attachment Functions"](16dbatt.html#1037521 "17")
* Creating, changing, and deleting database attachments
* Checking whether an object is a database attachment
* Getting the ids of all database attachments
* Getting a database attachment
* [Chapter 18, "Database Transaction Functions"](17dbtran.html#1037521 "18")
* Improving the performance and program memory use while updating many etch or package symbols in batch mode
* Marking the start of a database transaction and returning the mark to the calling function
* Writing a mark in the database to allow future rollback or commitment
* Commiting and undoing a database transaction
* [Chapter 19, "Constraint Management Functions"](18consmgt.html#1037521 "19")
* Getting and setting current DRC modes and values for design constraints and ECset members
* Creating, deleting, and getting the dbid of an ECset
* Checking the syntax of a given value against the allowed syntax for a given constraint
* Batching and tuning DRC updates from constraint changes made using axlCNS<xxx> functions
* [Chapter 20, "Command Control Functions"](19cmdctl.html#978462 "20")
* Registering and unregistering SKILL commands with the command interpreter
* Getting and setting the controls for line lock, active layer
* Defining popups
* Getting user data
* [Chapter 21, "Polygon Operation Functions"](20plyopr.html#1037521 "21")
* [Chapter 22, "Allegro PCB Editor File Access Functions"](21filacc.html#38804 "22")
* [Chapter 23, "AXL-SKILL Data Extract Functions"](22extrct.html#665474 "23")
* SKILL access to the extract command
* Selecting sets of database objects as members of a view and applying an AXL function to each
* [Chapter 24, "Utility Functions"](23utils.html#756635 "24")
* Calculating an arc center given various data
* Converting quantities to various units
* [Chapter 25, "Math Utility Functions"](24mthutl.html#1037521 "25")
* [Chapter 26, "Database Miscellaneous Functions"](25dbmisc.html#1037521 "26")
* [Chapter 30, "Logic Access Functions"](26logacc.html#1037521 "30")

Other Sources of Information
----------------------------

For more information about Allegro PCB Editor and other related products, consult the sources listed below.

#### Product Installation

The*Cadence Installation Guide* tells you how to install Cadence products.

#### Related Manuals

The following manuals comprise the Allegro PCB Editor documentation set for your workbench of PCB design tools:

|  |
| --- | ---
| **For Information About...** | **Read...**
| The Allegro PCB Editor user interface. An overview of the design process using Allegro PCB Editor, starting and exiting, controlling the graphic display, graphic and text elements, design information, and system information. | [*Allegro PCB Editor User Guide: Getting Started with Physical Design*](../algrostart/algrostartTOC.md)
| Building and managing libraries, including defining padstacks, custom pads, packages, electrical attributes, and formats. | [*Allegro PCB Editor User Guide: Defining and Developing Libraries*](../algrolibdev/algrolibdevTOC.md)
| Loading logical design data and converting third-party mechanical data, including loading data from Concept™, netlists, and board mechanical data. | [*Allegro PCB Editor User Guide: Transferring Logic Design Data*](../algrologic/algrologicTOC.md)
| Setting up the design and specifying design rules and controls, including instructions for specifying properties and constraints. | [*Allegro PCB Editor User Guide:Preparing the Layout*](../algrolay/algrolayTOC.md)
| Placing components using Allegro PCB Editor, including automatic and interactive placement. | [*Allegro PCB Editor User Guide: Placing the Elements*](../algroplace/algroplaceTOC.md)
| Routing using Allegro PCB Editor, including interactive and automatic routing. | [*Allegro PCB Editor User Guide: Routing the Design*](../algroroute/algrorouteTOC.md)
| Design output, including renaming reference designators, creating drill and silkscreen data, and generating penplots. | [*Allegro PCB Editor User Guide: Preparing Manufacturing Data*](../algroman/algromanTOC.md)
| Optional Allegro PCB Editor interfaces, including Cadnetix-E, CBDS, Racal Visula, IGES, Greenfield, Computervision CADDS, SDRC I-DEAS, AutoCAD DXF, PTC, CATIA, IPC-D\_350C, GDSII, Fluke Defect Analyzer, and HP3070 Tester. | [*Converting Third Party Designs and Mechanical Data*](../algrologic/chap3.md)
| Allegro PCB Editor commands, listed alphabetically. | [*Allegro PCB and Package Physical Layout Command Reference*](../cmdrefmast/cmdrefmast.md)
| Allegro PCB Editor properties, extracts (examples), and reports. | [*Allegro PCB Editor User Guide: Design Rules*](../algrodesrls/algrodesrlsTOC.md)*,* [*Extract Data Dictionary*](../algrodescmp/chap4.md), and [*Viewing Reports On Screen in HTML Format*](../rcoms/rchap.html#reportsprocedure)
| A comprehensive glossary for the Allegro PCB Editor user guides and reference manuals. | [*Allegro PCB Editor User Guide Glossary*](../algrostart/glossary.md)
#### Customer Support

Cadence offers many customer education services. Ask your sales representative for more information.

[Cadence Online Support (COS)](http://support.cadence.com) is available for customers who have a maintenance agreement with Cadence.

Here, you can also find technical information, including SKILL documentation and shareware code, online. COS provides the latest in Quarterly Incremental Releases (QIRs), case and product change release (CCR) information, technical documentation, solutions, software updates and more.

#### Allegro PCB Editor Users Mailing List Subscription

You can use electronic mail (email) to subscribe to the Allegro PCB Editor users mailing list. You will receive periodic newsletters containing up-to-date information on the Allegro PCB Editor product family.

#### To subscribe to the Allegro PCB Editor mailing list

* Send an email message to*majordomo@cadence.com*, and include the phrase "subscribe allegro\_users" in the body of the message.

> You will receive an acceptance notification.

#### AXL-SKILL Example Files

You can find AXL-SKILL example files in this location:

`<install_dir>``/share/pcb/examples/skill`

#### User Discussion Forums

You can find discussion groups for users of Cadence products at[Cadence Community](http://community.cadence.com) site.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
