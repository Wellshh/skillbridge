### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

Preface
=======

The*Cadence SKILL Language User Guide* introduces the SKILL language to new users and encourages sound SKILL programming methods. It also introduces the Cadence® SKILL++ Language, the second-generation extension language for CAD software from Cadence. It is aimed at the following users:

* People learning to program

* Software users who want to know some of the basics of SKILL

* Programmers beginning to program in SKILL

* CAD developers (internal users and customers) who have experience programming inSKILL

* CAD integrators

You can find companion information in the[*Cadence SKILL Language Reference*](../sklangref/sklangrefTOC.md).

Licensing in Cadence SKILL Language
-----------------------------------

Product license 111 is checked out at`skill` executable startup or at workbench startup.

For information on licensing in the Cadence SKILL Language, see*Virtuoso Software* [*Licensing and Configuration Guide*](../dfIIconfig/dfIIconfig.md)*.*

About the SKILL Language
------------------------

The SKILL programming language lets you customize and extend your design environment.SKILL provides a safe, high-level programming environment that automatically handles many traditional system programming operations, such as memory management. SKILL programs can be immediately executed in the Cadence environment.

SKILL is ideal for rapid prototyping. You can incrementally validate the steps of your algorithmbefore incorporating them in a larger program.

Storage management errors are persistently the most common reason cited for scheduledelays in traditional software development. SKILL's automatic storage management relieves your program of the burden of explicit storage management. You gain control of your software development schedule.

SKILL also controls notoriously error-prone system programming tasks like list managementand complex exception handling, allowing you to focus on the relevant details of your algorithm or user interface design. Your programs will be more maintainable because they will be more concise.

The Cadence environment allows SKILL program development such as user interfacecustomization. The SKILL Development Environment contains powerful tracing, debugging, and profiling tools for more ambitious projects.

SKILL leverages your investment in Cadence technology because you can combine existingfunctionality and add new capabilities.

SKILL allows you to access and control all the components of your tool environment: the UserInterface Management System, the Design Database, and the commands of any integrated design tool. You can even loosely couple proprietary design tools as separate processes with SKILL's interprocess communication facilities.

SKILL Development Helpful Hints
-------------------------------

Here are some helpful hints:

* You can click*Help* in the SKILL IDE window to access [*Cadence SKILL IDE User Guide*](../skillide/skillideTOC.md) for information about SKILL development tools. The [Walkthrough](../skillide/skillideTOC.md) can guide you through the tasks you perform when you develop SKILL programs using the SKILL development tools. You can also find information about [SKILL lint messages](../skillide/skillideTOC.md), and [message groups](../skillide/skillideTOC.md) in the SKILL IDE user guide.

* You can use the[SKILL Finder](../skillide/skillideTOC.md) to access syntax and abstracts for SKILL language functions and application procedural interfaces (APIs).

* You can copy examples from windows and paste the code directly into the CommandInterpreter Window (CIW) or use the code in non graphics SKILL mode. To select text

* Use`Control`+drag to select a text segment of any size.

* Use`Control`+double-click to select a word.

* Use`Control`+triple-click to select an entire section.

For more information about Cadence SKILL language and other related products, see

* [*Cadence SKILL IDE User Guide*](../skillide/skillideTOC.md)

* [*Cadence SKILL Development Reference*](../skdevref/skdevrefTOC.md)

* [*Cadence SKILL Language Reference*](../sklangref/sklangrefTOC.md)

* [*Cadence Interprocess Communication SKILL Reference*](../skipcref/skipcrefTOC.md)

* [*Cadence SKILL++ Object System Reference*](../skoopref/skooprefTOC.md)

**Note:** The[*Cadence Installation Guide*](../install/installTOC.md) tells you how to install the product.

Related Documents
-----------------

The following documents provide more information about SKILL and other topics discussedin this guide.

### Installation, Environment, and Infrastructure

* For more information on installing Cadence products, see the[*Cadence Installation Guide.*](../install/installTOC.md).

* For information on database SKILL functions, including data access functions, see thesee the [*Virtuoso Design Environment SKILL Reference*](../skdfref/skdfrefTOC.md)*.* It contains APIs for the graphics editor, database access, design management, technology file administration, online environment, design flow, user entry, display lists, component description format, and graph browser.

* [*Cadence User Interface SKILL Reference*](../skuiref/skuirefTOC.md) contains APIs for management of windows and forms.

* [*Virtuoso Software Licensing and Configuration Guide*](../dfIIconfig/dfIIconfig.md) contains SKILL licensing functions.

Section Names and Meanings
--------------------------

Each function described in this book can have up to seven sections. Not every section isrequired for every function description.

|  |
| --- | ---
| `Syntax` | The syntax requirements for this function.
|  |
| --- | ---
| `Prerequisites` | Steps required before calling this function.
|  |
| --- | ---
| `Description` | A brief phrase identifying the purpose of the function and the textdescription of the operation performed by the function.
|  |
| --- | ---
| `Arguments` | An explanation of the arguments input to the function.
|  |
| --- | ---
| `Return Value` | An explanation of the value returned by the function.
|  |
| --- | ---
| `Example` | Actual SKILL code using this function.
|  |
| --- | ---
| `References` | Other functions that are relevant to the operation of this function:ones with partial or similar functionality or which could be called by or could call this function. Sections in this manual which explain how to use this function.
Typographic and Syntax Conventions
----------------------------------

The following typographic and syntax conventions are used in this document.

|  |
| --- | ---
| `literal (LITERAL)` | Nonitalic (UPPERCASE) words indicate keywords that you must enter literally. These keywords represent command (function, routine) or option names.
|  |
| --- | ---
| `argument (z_argument)` | Words in italics indicate text that you must replace with an appropriate argument. The prefix (in this case, z\_) indicates the data type that the argument can accept. Names are case sensitive. Do not type the data type or underscore before your arguments.
|  |
| --- | ---
| `|` | Vertical bars (OR-bars) separate the choice of options. They takeprecedence over any other character.
|  |
| --- | ---
| `[ ]` | Brackets denote optional arguments. When used with verticalbars, they enclose a list of choices from which you can choose one.
|  |
| --- | ---
| `{ }` | Braces are used with vertical bars and enclose a list of choicesfrom which you must choose one.
|  |
| --- | ---
| `...` | Three dots (`...`) indicate that you can repeat the previous argument. If you use them with brackets, you can specify zero or more arguments. If they are used without brackets, you must specify at least one argument, but you can specify more.
|  |
| --- | ---
|  | `argument...``;specify at``least``one,``;but more are possible`
|  |
| --- | ---
|  | `[argument]... ;specify zero or more`
|  |
| --- | ---
| `,...` | A comma and three dots together indicate that if you specifymore than one argument, you must separate those arguments by commas.
|  |
| --- | ---
| `=>` | A right arrow points to the return values of the function. Variablevalues returned by the software are shown in italics. Returned literals, such as `t` and `nil`, are in plain text. The right arrow is also used in code examples in SKILL manuals.
|  |
| --- | ---
| `/` | Separates the possible values that can be returned by aCadence SKILL language function.
|  |
| --- | ---
| `text` | Indicates names of manuals, menu commands, form buttons,and form fields.
### SKILL Syntax Examples

The following examples show typical syntax characters used in SKILL.

#### Example 1

> `list( g_arg1 [g_arg2] ...) => l_result`

This example illustrates the following syntax characters.

|  |
| --- | ---
| `list` | Plain type indicates words that you must enter literally.
|  |
| --- | ---
| `g_arg1` | Words in italics indicate arguments for which you must substitutea name or a value.
|  |
| --- | ---
| `( )` | Parentheses separate names of functions from their arguments.
|  |
| --- | ---
| `_` | An underscore separates an argument type (left) from anargument name (right).
|  |
| --- | ---
| `[ ]` | Brackets indicate that the enclosed argument is optional.
|  |
| --- | ---
| `...` | Three dots indicate that the preceding item can appear anynumber of times.
|  |
| --- | ---
| `=>` | A right arrow points to the description of the return value of thefunction. Also used in code examples in SKILL manuals.
|  |
| --- | ---
| `l_result` | All SKILL functions compute a data value known as the returnvalue of the function.
#### Example 2

> `needNCells( s_cellType | st_userType x_cellCount) => t / nil`

This example illustrates two additional syntax characters.

|  |
| --- | ---
| `|` | Vertical bars separate a choice of required options.
|  |
| --- | ---
| `/` | Slashes separate possible return values.
Identifiers Used to Denote Data Types
-------------------------------------

The Cadence SKILL language supports several data types to identify the type of value youcan assign to an argument.

Data types are identified by a single letter followed by an underscore; for example,`t` is the data type in `t_viewNames`. Data types and the underscore are used as identifiers only; they should not be typed.

|  |  |
| --- | --- | ---
| ****Prefix**** | **Internal Name** | **Data Type**
| `a` | array | array
| `A` | amsobject | AMS object
| `b` | ddUserType | DDPI object
| `B` | ddCatUserType | DDPI category object
| `C` | opfcontext | OPF context
| `d` | dbobject | Cadence database object (CDBA)
| `e` | envobj | environment
| `f` | flonum | floating-point number
| `F` | opffile | OPF file ID
| `g` | general | any data type
| `G` | gdmSpecIlUserType | gdm spec
| `h` | hdbobject | hierarchical database configuration object
| `K` | mapiobject | MAPI object
| `l` | list | linked list
| `L` | tc | Technology file time stamp
| `m` | nmpIlUserType | nmpIl user type
| `M` | cdsEvalObject | --
| `n` | number | integer or floating-point number
| `o` | userType | user-defined type (other)
| `p` | port | I/O port
| `q` | gdmspecListIlUserType | gdm spec list
| `r` | defstruct | defstruct
| `R` | rodObj | relative object design (ROD) object
| `s` | symbol | symbol
| `S` | stringSymbol | symbol or character string
| `t` | string | character string (text)
| `T` | txobject | transient object
| `u` | function | function object, either the name of a function (symbol) ora lambda function body (list)
| `U` | funobj | function object
| `v` | hdbpath | --
| `w` | wtype | window type
| `x` | integer | integer number
| `y` | binary | binary function
| `&` | pointer | pointer type
For information on SKILL language, see[*Cadence SKILL Language User Guide*](../sklanguser/sklanguserTOC.md).

Additional Learning Resources
-----------------------------

Cadence offers the following training courses on the SKILL programming language:

* [SKILL Language Programming Introduction](http://www.cadence.com/Training/NA/Pages/coursedetails.aspx?componentID=ES_84508_IC6.1.6)

* [SKILL Language Programming](http://www.cadence.com/Training/NA/Pages/coursedetails.aspx?componentID=ES_83018_IC6.1.6)

* [Advanced SKILL Language Programming](http://www.cadence.com/Training/NA/Pages/coursedetails.aspx?componentID=ES_84401IA_IC6.1.6)

For further information on these and other related Virtuoso Layout Suite training coursesavailable in your region, visit the [Cadence Training](http://www.cadence.com/Training) portal. You can also write to training\_enroll@cadence.com.

**Note:** The links in this section open in a new browser. The course links initially display therequested training information for North America, but if required, you can navigate to the courses available in other regions.

How to Contact Technical Support
--------------------------------

Cadence Customer Support is region specific. To find out the e-mail address, phone number,or fax number for your region, select the *Contacts* button from the Cadence Online Support home page (<http://support.cadence.com>).

You can also useCadence Online Support to find out the latest information on Virtuoso Parasitic Aware Design.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
