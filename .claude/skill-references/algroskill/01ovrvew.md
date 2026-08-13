### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

1
=

Introduction to Allegro PCB Editor SKILL Functions
==================================================

Overview
--------

This chapter is a brief overview of the following:

* Allegro PCB Editor AXL-SKILL

* AXL-SKILL functions

* How to initialize and run AXL-SKILL

* The AXL Allegro PCB Editor database

Later chapters describe in detail the AXL database objects and all AXL-SKILL functions.

AXL-SKILL in Allegro PCB Editor
-------------------------------

AXL-SKILL is a language processor contained in Allegro PCB Editor, as shown in the following figure.

AXL-SKILL contains and is an extension of the core Cadence SKILL language. You use
AXL-SKILL functions to access the Allegro PCB Editor database and its display and user interfaces. Once you have accessed the Allegro PCB Editor database, you can process the data using the core SKILL functions. The*SKILL Language Functions Reference* describes core SKILL and its available functions.

You access AXL-SKILL by entering the command`skill` on the Allegro PCB Editor command line.

AXL-SKILL initializes automatically when you start Allegro PCB Editor. As Allegro PCB Editor starts, it reads the Allegro PCB Editor`env` file, then the AXL `ilinit` file (as described below) then any script you may have specified with the `-s` option in the UNIX command starting Allegro PCB Editor.

Allegro PCB Editor looks for the`ilinit` file in the following way:

* For the locations specified below, Allegro PCB Editor reads one of the following files:

> `<``program_name``>.ilinit`

> `allegro.ilinit`

> From the locations:

> `<``cdsroot``>/share/pcb/etc/skill`

> `<``cdssite``>/pcb/skill`

> **Note:** `<``cdssite``>` defaults to `<``cdsroot``>/share/local/pcb/skill`, otherwise you can set the `CDS_SITE` variable to point to another location, the directory where your program started:

> `$HOME/pcbenv`

If you have multiple`ilinit` files in the locations listed above, *each* of the `ilinit` files will be read. If you wish only the *first* found `ilinit` file to be read (the methodology employed in pre-14.2 releases), set the environment variable `skill_old_ilinit`.

**Note:** You cannot insert SKILL commands in the`env` file.

#### Running AXL-SKILL from the Command Line

You run AXL-SKILL by typing`skill` on the Allegro PCB Editor command line. The AXL-SKILL interpreter appears with the *skill>* prompt in place of the Allegro PCB Editor command line.

You can also run AXL-SKILL functions from the Allegro PCB Editor command line with the following syntax:

> `skill (<function> <arguments>)`

Type`exit` to close the AXL-SKILL interpreter and return to the Allegro PCB Editor command line.

#### Running AXL-SKILL in Batch Mode

You can run AXL-SKILL in batch mode using an X terminal window without displaying Allegro PCB Editor, by typing the following command:

> `.allegro -nographic`

If your system is not running the X window system, verify that it has its DISPLAY environment variable set to a system running an X-server.

**Note:** The`-nographic` switch is valid for all Allegro PCB Editor graphic executables, such as `allegro_layout`, `allegro_engineer`, `allegro_prep`, `allegro_interactive`, and `allegro_layout`.

You can also program the Allegro PCB Editor and AXL-SKILL startup and command entry in a shell script, allowing full batch capability.

#### Debugging AXL-SKILL Programs

If you have a SKILL ACCESS development license, you can debug AXL-SKILL programs in Allegro PCB Editor using the same tools offered by other Cadence SKILL programs. See*SKILL Language Functions Reference* for a description of those tools, which are primarily available on Unix.

#### AXL-SKILL Grammar

AXL-SKILL functions follow SKILL grammar rules. In addition, the following characteristics apply to most AXL-SKILL functions:

* All Allegro PCB Editor AXL function names begin with`axl`.

* AXL functions are classified into families that typically have similar calling sequences and share a common part of their names, for example the`axlDBCreate` family, with members such as `axlDBCreateShape` and `axlDBCreateSymbol`.

#### SKILL Development Window

You can get a larger SKILL-only window by setting the Allegro PCB Editor environment variable,`TELSKILL`.

**Note:** All Allegro PCB Editor console output is directed to the SKILL window when the`TELSKILL` variable is set.

AXL-SKILL Database
------------------

Allegro PCB Editor stores design data as various types of objects in a proprietary database format. These object types can create a complete representation of an electronic layout. You can create, operate on, and extract information from this database using AXL-SKILL programs.

The AXL-SKILL database stores both physical and logical information about your design. Physical information is objects such as geometrical shapes (connecting etch, for example). Logical information is objects such as nets and logical components.

#### Object dbids (database identifiers)

Every Allegro PCB Editor database object has a unique`dbid` (database identifier) associated with it. When you call a function to operate on a database object, you identify the object to the function by giving the object's `dbid` as an argument.

Only AXL routines can create`dbids`. You cannot alter `dbids` directly, except for parameter record ids.

#### Out of Scope dbids

When a dbid is separated from its object, the dbid is considered out-of-scope. A dbid can become separated from its object for any of the following reasons:

* You delete an object.

* You add a connect line that touches an existing connect line. This causes the existing line to break in to two objects, each with a separate dbid, so the original dbid of the line no longer denotes the same object.

* You return to Allegro PCB Editor from AXL.

* You run an Allegro PCB Editor command while in SKILL, using the AXL shell function. To minimize out-of-scope issues with AXL shell, isolate AXL shell functions and if necessary refresh dbids after AXL shell calls with the function axlDBRefreshID.

* You open a new layout.

Out of scope`dbids` have no attributes, so they have no object type. If you try to evaluate a `dbid` that is out of scope, SKILL displays the message:

`dbid: removed`

Using an out of scope`dbid` in a function causes unexpected results.

#### Object Types

Each Allegro PCB Editor object has an associated*type* and a set of *attributes* that describe the object. For example, all `symbol` objects are of type `symbol`. All `symbols` have the `isMirrored` attribute, among others, and this attribute has the value `t` if the symbol is mirrored or `nil` if it is not. You can use an AXL-SKILL function with "`->"` (the access operator) to access any object attribute. If the attribute does not exist for that object the function returns `nil`.

You use the SKILL special attributes`?` (question mark) and `??` to see all attributes and all attribute/value pairs of an object. See [Chapter 2, "The Allegro PCB Editor Database User Model,"](02dbdesc.html#462876 "2") for more information about object types.

#### Object Classes

An*object* class is a data-type abstraction used to group related object types. When a number of distinct object types share enough attributes, you can discuss them as a single class. The start of each section describing a class of object types lists all attributes common to that class.

The different types and classes of objects form a class hierarchy. At the top of the hierarchy is a class containing all types. At the bottom of the hierarchy, each leaf (terminal node) represents an object type that you can create, delete, and save on disk. Each intermediate node in the hierarchy has attributes that are common to all of its children. AXL-SKILL figures, for example, have common attributes of`layer` and `bBox` (bounding box). These higher level classes do not exist as objects.

#### Select Sets and Find Functions

AXL-SKILL edit functions obtain the identities of the objects on which they operate from a list of`dbids` called the *select set.* You accumulate `dbids` in the select set by selecting one or several objects using AXL select functions. You then apply edit functions to the objects by passing the select set as an argument to the functions.

AXL-SKILL has functions to do the following:

* Set the Find Filter to control the types of objects selected and select options

* Select objects at a single point, over an area, or by name

* Select parts of objects (for example, pins, which are parts of symbols)

* Add or remove objects from the select set (the set of selected objects)

* Get`dbids` and return the count of `dbids` in the select set

* Add`dbids` to and remove them from the select set before using it.

See[Chapter 4, "Selection and Find Functions,"](05selfnd.html#580309 "4") for information about select set functions.

**Note:** Allegro PCB Editor highlights selected objects whenever it refreshes the display.

#### Design Files

Design files are containers for Allegro PCB Editor database objects. AXL-SKILL has two major design file types:

|  |
| --- | ---
| `Layout` | Contains printed circuit or MCM layout data.
| `Symbol` | Contains the definition drawing of a symbol. The compiled output of a symbol file can be added to layouts. Symbol files can define any of package, mechanical, format, and shape symbols.
#### Logical Objects

Logical objects are the objects in the netlist that Allegro PCB Editor loads from a schematic or third-party netlist file:

|  |
| --- | ---
| Component | Contains the electrical functions, such as nand gates, and pins that define the electrical behavior of an object. A component's reference designator is its name.
| Net | Is the set of all the etch objects--ppins, etch paths, shapes, and vias--associated with a particular signal name. Every net has a name which is its signal name. A net contains one or more branches. Each branch is a list of the etch objects that are physically connected among themselves. A branch can include ppins, etch paths, shapes, and vias. The number of branches in a net varies as Allegro PCB Editor connects or disconnects parts of the net. A completely connected net consists of one and only one branch.
#### Layer Attributes

Each Allegro PCB Editor figure exists on a class/subclass in the database. For example, a c-line might be on class ETCH, subclass TOP. AXL-SKILL represents this class/subclass combination with a layer attribute. Each AXL-SKILL layer is in one-to-one correspondence with an Allegro PCB Editor class/subclass combination. A later section describes this structure in detail.

#### Allegro PCB Editor Properties

Although they are a class of Allegro PCB Editor objects, you do not create or access Allegro PCB Editor properties directly. Rather, you use AXL-SKILL commands to attach, delete, and read the values of properties on Allegro PCB Editor database objects. You can also use AXL-SKILL commands to read, create and delete definitions of your own properties.

#### Property Definitions

AXL-SKILL stores each property definition for an object indirectly associated with that object. You can access any property definition on an object to find its value and you can create new, user-defined properties using AXL-SKILL functions.

You can use an AXL-SKILL function to attach a property to an object if the object accepts that property type. The property must be defined in the property dictionary of that database. A property definition is an object that contains the property name, value type, and a list specifying to what object types it can be attached.

#### Figures

The following AXL-SKILL figures are Allegro PCB Editor geometry types.

|  |
| --- | ---
| Arc | Is a figure that is either an arc or a circle. You can specify arcs to AXL-SKILL with start and end points, and either radius or center point. (Allegro PCB Editor figure:`arc segment`).
| Branch | Is a collection of etch figures that make up one physically connected part of a net. Nets are made up of branches, and branches are made up of pins, vias, tees and etch figures, as described later in this chapter.
| DRC | Is a design rule violation marker with one or more object identities and a violation type and location.
| Line | An object defined by the coordinates of its center line and a width (Allegro PCB Editor figure:`line segment`).
| Path | Is a sequence of end-to-end lines and arcs on the same layer. Each segment can have a different width (Allegro PCB Editor figures:`lines and clines`).
| PPin | Is a physical instance of a pin with associated padstack.
| Polygon | Is an unfilled, closed path (Allegro PCB Editor figure:`unfilled shape`).
| Shape | Is a filled shape. It can optionally contain voids.
| Pad | Is a geometric shape (circle, oblong, rectangle) defining the shape of one type of pad on one layer. Pads are always owned by padstacks.
| Symbol | Is a collection of geometries and text with a type name, location, rotation and mirroring.
| Tee | Is the single point where the endpoints of three or more etch paths connect.
| Text | Is a string of characters with associated size, mirror, rotation, and location.
| Via | Is a connecting drill path between layers with associated padstack.
The following types are not figures but contain geometry that defines figure instances:

|  |
| --- | ---
| Padstack | (Pin/Via Definition) Contains the definition data for all ppins or vias of a named type.
| Symdef | Contains the definition data for all symbols of a named type.
#### Accessing Allegro PCB Editor Colors with AXL-SKILL

You can access predefined colors and Allegro PCB Editor database colors using AXL-SKILL. Only graphics editors support access to Allegro PCB Editor database colors.

#### Forms

You set and access pre-defined colors by their symbols. The pre-defined colors include the following:

* `black

* `white

* `red

* `green

* `yellow

* `blue

* `button

Button means grey, the color of buttons in the application.

**Note:** You can use only pre-defined colors in Allegro PCB Editor forms.

#### Design Object

Graphics editors support access to the colors used for Allegro PCB Editor layers. These are represented by integers.

AXL API calls, including`axlLayerGet` ("class/subclass") or its primitive form `axlGetParm`(`paramLayerGroup`:<`class/paramLayer:`<`subclass`>), return the current color setting of a layer via the color attribute call, as shown.

> `p = axlLayerGet("etch/top")`

> `p->color    ->2`

These color settings range between 1 and 24 with 0 reserved for the background color.

Form based interfaces supporting color include the following:

* axlFormDoc

* axlFormColorize

* axlFormGridDoc

* axlGRPDoc

**Notes:**

* AXL does not allow you to change the red/green/blue (RGB) of Allegro PCB Editor database colors.

* Pre-defined colors are restricted to minimize problems with 8 bit color graphics on UNIX.

#### Database Objects

A design is made of various database objects that you can combine to make other database objects. This section describes the relationships among database objects.

**Parts of a Design**

A design can include any of the following database objects:

* Property Dictionary

* Lines

* Text

* Polygons

* Shapes

* Property Definitions

* DRCs

* Vias that are Padstack object types

* Symbols that are Symdef object types

* Components

* Nets

**Parts of a Symbol**

Symbols that are Symdef objects types can include any of the following database objects:

* PPins that are Padstack object types

* Vias that are Padstack object types

* Lines

* Arcs

* Text

* Polygons

* Shapes

**Parts of a Branch**

Branches can include any of the following database objects:

* Tees

* Vias that are Padstack object types

* PPins that are Padstack object types

* Paths

* Shapes

**Parts of a Path**

A path can include any of the following database objects:

* Lines

* Arcs

**Parts of a Symdef**

A symdef can include any of the following database objects:

* PPins that are Padstack object types

* Vias that are Padstack object types

* Lines

* Arcs

* Text

* Polygons

* Shapes

**Types of Parameters**

Allegro PCB Editor parameters store feature or board level options to the Allegro PCB Editor database. You can modify parameters using a SKILL program. The parameter types include the following:

* Design

* Display

* Layer Group

* Textblock Group

****Table 1-1****
**Other Database Object Relationships**

| **Object Name** | **Object Parts**
| Property Dictionary | Property Entries
| Net | Branches
| Padstack | Pads
| Polygon | Paths
| Shape | Paths
| Void | Polygons
| Polygon | Paths
| PPin | Pin Number Text
| Layer Group | Layers
| Textblock Group | Textblocks
For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
