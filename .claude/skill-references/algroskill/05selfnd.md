### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

4
=

Selection and Find Functions
============================

Overview
--------

AXL edit functions such as move or delete operate on database object`dbids` contained in the *select* set. The select set is a list of one or more object `dbids` you have previously selected. You add `dbids` to the select set with the `axlSelect` functions described in this chapter. You use the select set as an argument in any edit function calls. This differs from interactive Allegro PCB Editor edit commands, where you first start a command, then select the objects to be edited. One advantage of a select set is that selected object `dbids` stay in the select set from function to function until you explicitly change it. You can perform multiple edits on the same set of objects without reselecting. Remember, however, that edit functions might cause `dbids` to go out of scope. This chapter also describes functions for managing the select set and controlling the selection filter.

AXL supports one active select set. The contents of the select set becomes invalid when you exit Allegro PCB Editor.

The interactive select functions find objects only on visible layers.

You can do the following with the selection functions:

* Set the Find Filter to control the types of objects selected

* Select objects at a single point, over an area, or by name

* Select parts of objects, such as individual pins of a package symbol

* Add or remove`dbids` from the select set

A select set can contain`dbids` of parts of a figure without containing the figure itself. For example, you can select one or more pins of a symbol or individual segments of a path figure. See [Chapter 2, "The Allegro PCB Editor Database User Model,"](02dbdesc.html#462876 "2") for a list of Allegro PCB Editor figure types.

You can add figure`dbids` to the select set interactively with a mouse click on the figure (point selection) or by drawing a box that includes the figure (box selection). The **Find Filter** controls filtering for specific object types. This chapter describes AXL-SKILL functions to set the filter for any object type.

All coordinates are in user units unless otherwise noted.

Select Set Highlighting
-----------------------

Objects in the select set are displayed as highlighted when control passes from SKILL to you for interactive input (for selection) or when SKILL returns control to the Allegro PCB Editor shell. You can select and modify objects using AXL-SKILL functions. To keep these objects from displaying as highlighted, remove them from the select set before returning SKILL control to you for interactive input or to the Allegro PCB Editor shell.

Select Modes
------------

AXL provides two select modes:

|  |
| --- | ---
| single | Selects one or a group of objects that match the selection criteria. When you select an object in this mode, AXL deselects any objects previously in the select set.
| cumulated | Adds to or subtracts from the select set one or a group of objects that match the selection criteria. Add cumulated mode never adds an object already in the set, so you do not have duplicate entries if you mistakenly select the same object twice. Subsequent selects of the same object are ignored.
Finding Objects by Name
-----------------------

The`axlSingleSelectName`, `axlAddSelectName`, and `axlSubSelectName` functions find objects by using their names. You can search for the following Allegro PCB Editor object types by name:

|  |
| --- | ---
| NET | List of net names for net selection.
| COMPONENT | List of reference designators for component instance selection.
| SYMBOL | List of reference designators for symbol instance selection.
| FUNCTION | List of function designators for function instance selection.
| DEVTYPE | List of device type for component or symbol instance selection. \*\*
| SYMTYPE | List of symbol types for symbol instance selection.
| REFDES | List of reference designators for component or symbol instance selection. \*\*
| DEVSYM | List of device type for symbol instance selection.
| GROUP | List of group names for group or group member selection.
| PROPERTY | List of property names or property value) lists for selection of database object that have the property/value. If no value is provided, the value will be ignored for the database property comparison. The find filter enabled and onButtons control the type of elements that will be selection.
\*\* For DEVTYPE and REFDES, a component instance is selected if COMPONENTS are in the find filter ?enabled list. Otherwise, if SYMBOLS are enabled, a symbol instance is selected.

See the descriptions of the`SelectName` functions for how to set up the arguments.

Point Selection
---------------

These functions select objects at a single geometric point. They prompt you for the point if that argument is missing from the function call.

> `axlSingleSelectPoint`

> `axlAddSelectPoint`

> `axlSubSelectPoint`

Area Selection
--------------

These functions select objects over an area. They prompt you for the area (`Bbox`) if that argument is missing from the function call.

> `axlSingleSelectBox`

> `axlAddSelectBox`

> `axlSubSelectBox`

Miscellaneous Select Functions
------------------------------

These functions select by other means as shown in each function description later in this chapter:

> `axlAddSelectAll`

> `axlSubSelectAll`

> `axlSingleSelectName`

> `axlAddSelectName`

> `axlSubSelectName`

> `axlSingleSelectObject`

> `axlAddSelectObject`

> `axlSubSelectObject`

axlSelect-The General Select Function
-------------------------------------

One function,`axlSelect`, combines the capabilities of the `axlAddSelect` functions. Use `axlSelect` as you write interactive commands to give the user the same select capabilities available in Allegro PCB Editor commands move or delete.

Select Set Management
---------------------

These functions manage the select set:

> `axlGetSelSet`

> `axlGetSelSetCount`

> `axlClearSelSet`

Find Filter Control
-------------------

These functions control the selection filter:

* `axlGetFindFilter`

* `axlSetFindFilter`

#### Find Filter Options

You can restrict selection in a given window to a subset of all possible figure types by using the**Find Filter** or the `FindFilter` functions described in this chapter. `FindFilter` functions also control whether the **Find Filter** is immediately visible to you.

The permissible keywords for the`lt_options` list are shown. These keywords are a subset of the Allegro PCB Editor Find Filter. You can prefix any of these keywords with `NO` to reverse the effect. See the description of [axlSetFindFilter](#580660 "4") for details on how to use these keywords:

|  |
| --- | ---
| `Global` | `ALL`, `ALLTYPES`, `EQUIVLOGIC`
| `Figures` | `PINS`, `VIAS`, `CLINES`, `CLINESEGS`, `LINES`, `LINESEGS`, `DRCS`, `TEXT`, `SHAPES` (includes rectangles), `SHAPESEGS`, `VOIDS`, `VOIDSEGS`, `TEXT`.  **Note:**The `xxx``SEG` keywords also select arc and circle segments
| `Logic` | `COMPONENTS`, `SYMBOLS`, `NETS`
Except for`EQUIVLOGIC`, the *Find Filter* functions take the keywords in the order found. For example, the list `(ALL NOPIN)` results in all objects except pins being selectable.

`EQUIVLOGIC` is a global find state. It instructs *find* to select the physically equivalent parts, as specified in the filter of the found logic object. For example, if the user picks any physical part of a net, the selection returns any physical parts of the (logical) net selected by the *find filter*. Both the logical and the physical objects must be enabled. For example, to select all pins of a net, both `NETS` and `PINS` must be enabled and set with `?onButton`.

Selection and Find Functions
----------------------------

This section lists selection and find functions.

### axlSingleSelectPoint

`axlSingleSelectPoint([l_point][g_trapSize])⇒ t/nil`

#### Description

Clears the select set, finds a figure at`l_point` according to the Find Filter, and puts the selected figure `dbid` in the select set. If `l_point` is `nil`, the function requests a single pick from the user.

`axlSingleSelectPoint` selects a single object and adds it to the select set, unless `EQUIVLOGIC` is on. In that case, it may select multiple objects, for example, if it finds a qualified figure (such as a pin, connect line, or via) that is part of a net. `axlSingleSelectPoint` adds all the qualified figures that belong to the net to the select set. (See the [Find Filter Options](#581761 "4").)

This finds objects within the current trapsize (`axlGetTrapBox`), which varies based upon the zoom factor.

#### Arguments

|  |
| --- | ---
| `l_point` | Point in database coordinates at which to look for figures.
| `g_trapSize` | Enables a a trap box, which is based on the zoom level of the canvas. Objects that are found can be effected based on the current zoom level. When this option is set to`nil` the trap size gets disabled.
#### Value Returned

|  |
| --- | ---
| `t` | One or more`dbids` put in the select set.
| `nil` | No`dbids` put in the select set.
#### Example

```
axlSetFindFilter(?enabled "pins" ?onButtons "pins")axlSingleSelectPoint( 6325:3575 )axlDBAddProp(axlGetSelSet() list( "MYPROP" 23.5))⇒ t
```

Adds a previously defined user property`MYPROP` to a pin at X6325 Y3575.

To check

* From Allegro PCB Editor, choose*Display - Element*.

* Select the pin to display its properties.

> The**Show Element** window displays *MYPROP* with value *23.500000 level*

### axlAddSelectPoint

`axlAddSelectPoint([l_point])⇒ t/nil`

#### Description

Finds a figure at`l_point` according to the Find Filter and adds its `dbid` to the select set in cumulated mode. If `l_point` is `nil`, requests a single pick from the user.

Selects a*single* object and adds it to the select set, unless `EQUIVLOGIC` is on. In that case, selects multiple objects, for example, if it finds a qualified figure (such as a pin, connect line, or via) that is part of a net. Adds all the qualified figures that belong to the net to the select set. (See the [Find Filter Options](#581761 "4").)

This finds objects within the current trapsize (`axlGetTrapBox`), which varies based upon the zoom factor.

#### Arguments

|  |
| --- | ---
| `l_point` | Point in the layout at which to find figures.
#### Value Returned

|  |
| --- | ---
| `t` | One or more`dbids` put in the select set.
| `nil` | No`dbids` put in the select set.
#### Example

See[axlSingleSelectPoint](#580413 "4") for an example. `axlSingleSelectPoint` has the same behavior except that it selects only one object.

### axlSubSelectPoint

`axlSubSelectPoint([l_point])⇒ t/nil`

#### Description

Finds a figure at`l_point` according to the Find Filter and deletes its `dbid` from the select set in cumulated mode. That is, it deletes that `dbid` while leaving any others currently in the select set. If `l_point` is `nil`, requests a single pick from the user.

Removes a*single* object from the select set, unless `EQUIVLOGIC` is on. In that case, finds multiple objects, for example, if it finds a qualified figure (such as a pin, connect line, or via) that is part of a net. Deletes all the qualified figures that belong to the net from the select set. (See the [Find Filter Options](#581761 "4").)

This finds objects within the current trapsize (`axlGetTrapBox`), which varies based upon the zoom factor.

#### Arguments

|  |
| --- | ---
| `l_point` | Point in the layout at which to find figures to deselect.
#### Value Returned

|  |
| --- | ---
| `t` | One or more`dbids` removed from the select set
| `nil` | No`dbids` removed from the select set.
#### Example

> > ```
> > axlSetFindFilter(?enabled "pins" ?onButtons "pins")axlSingleSelectBox( list(6200:3700 6500:3300))axlSubSelectPoint( 6325:3575 )axlDBAddProp(axlGetSelSet() list("MYPROP" 23.5))⇒ t
> > ```

Adds a previously defined user property,`MYPROP`

* Selects four pins in a box in order.

* Before adding the property, subtracts the pin at`6325:3575` from the list, then adds as shown.

To check

* Select*Edit - Properties*.

* Select a window around all four pins.

* Select*MYPROP* from the Available Properties list in the **Edit Property** window.

> The command displays the pins that have properties in the**Show Properties** window. Only the three pins not subtracted from the select set have the property, *MYPROP*.

### axlSingleSelectBox

`axlSingleSelectBox([l_bBox])⇒ t/nil`

#### Description

Clears the select set, finds all figures inside the rectangle`l_bBox` according to the
Find Filter, and adds the selected figure `dbids` in single mode to the select set.

#### Arguments

|  |
| --- | ---
| `l_bBox` | List containing one or two coordinates defining the bounding box to be used to select the figures. If`l_bBox` is `nil`, requests two picks from the user. If `l_bBox` has only one point, asks for a second point from the user.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the select set.
| `nil` | No objects added to the select set.
#### Example

```
axlSetFindFilter(?enabled "pins" ?onButtons "pins")axlSingleSelectBox( list(6200:3700 6500:3300))axlDBAddProp(axlGetSelSet() list( "MYPROP" 23.5))⇒ t
```

Adds a previously defined user property`MYPROP` to four pins by selecting a box around them with corners (`6200:3700 6500:3300`).

To check

* Select*Edit - Properties*.

* Select the four pins.

* Select*MYPROP* from the Available Properties list in the **Edit Property** window.

> The command displays the four pins in the**Show Properties** window as having *MYPROP* with value *23.500000 level*

### axlAddSelectBox

`axlAddSelectBox([l_bBox])⇒ t/nil`

#### Description

Finds one or more figures inside the rectangle`l_bBox` according to the current Find Filter, and adds the selected figure `dbids` in cumulated mode for the select set.

#### Arguments

|  |
| --- | ---
| `l_bBox` | List containing one or two coordinates defining the bounding box to be used to the select figures. If`l_bBox` is `nil`, requests two picks from the user. If `l_bBox` has only one point, asks for a second point from the user.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the select set.
| `nil` | No objects added to the select set.
#### Example

See the example for[axlSingleSelectBox](#580450 "4"). That function behaves exactly as `axlAddSelectBox`, except that `axlSingleSelectBox` does not clear the select set.

### axlSubSelectBox

`axlSubSelectBox([l_bBox])⇒ t/nil`

#### Description

Finds one or more figures inside the rectangle`l_bBox` according to the Find Filter, and deletes their `dbids` from the select set in *cumulated* mode. Deletes those `dbids` while leaving any others currently in the select set.

#### Arguments

|  |
| --- | ---
| `l_bBox` | List containing one or two coordinates defining the bounding box to be used to the select figures. If`l_bBox` is `nil`, requests two picks from the user. If `l_bBox` has only one point, asks for a second point from the user.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects deleted from select set.
| `nil` | No objects deleted from select set.
#### Example

See[axlSubSelectPoint](#580437 "4") for an example of subtracting from the select set, and [axlAddSelectPoint](#609263 "4")for an example of using a box for selection.

### axlAddSelectAll

`axlAddSelectAll()⇒ t/nil`

#### Description

Finds all the figures in the database that pass the current Find Filter and adds their`dbids` to the select set.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | One or more object`dbids` added to the select set.
| `nil` | No object`dbids` added to the select set.
#### Example

> ```
> axlSetFindFilter(?enabled list( "noall" "vias")    ?onButtons list( "noall" "vias"))    axlAddSelectAll()    axlDeleteObject(axlGetSelSet())    ⇒ t
> ```

Selects all vias in a layout and deletes them.

### axlSubSelectAll

`axlSubSelectAll()⇒ t/nil`

#### Description

Finds all figures in the database that pass the current Find Filter and deletes their`dbids` from the select set. Use `axlSubSelectAll` to subtract all of a given type of figure from a larger set of selected objects.

**Note:** Use`axlClearSelSet` to deselect all figures in the current select set, regardless of the current Find Filter.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | One or more`dbids` deleted from select set.
| `nil` | No`dbids` deleted from select set.
**Note:** Dependent on find filter ?enabled settings.

#### Example 1

The following example selects the nets GND and VCC by their names.

```
axlClearSelSet()axlSetFindFilter(?enabled    list( "noall" "equivlogic" "nets" "clines" "vias")    ?onButtons list( "all"))axlSingleSelectName( "NET" list( "GND" "VCC"))
```

`==> (dbid:234436 dbid:98723)`

`axlSingleSelectName("PROPERTY" list( list("BUS_NAME" "MEM") "FIXED"`

`)⇒ t`

Interactively selects all connect lines (clines) and vias on a net, subtracts the via`dbids` from the select set, and deletes the remaining `dbids` in the select set.

The prompt*Enter**selection**point*, is displayed. Only the connect lines on the net you select are deleted--not the vias of the net.

**Example 2**

The following example selects a set of nets--one set by the property name ELECTRICAL\_CONSTRAINT\_SET with value DEFAULT, and another set that has the name ROUTE\_PRIORITY.

`axlClearSelSet()`

`axlSetFindFilter( ?enabled list( "noall" "nets")`

`?onButtons list( "all"))`

`axlSingleSelectName("PROPERTY"`

`list( list( "ELECTRICAL_CONSTRAINT_SET" "DEFAULT")`

`"ROUTE_PRIORITY"))`

`==> (dbid:234436 dbid:98723 dbid:234437 dbid:98727`

`dbid:234438 dbid:98725 dbid:234439 dbid:98726)`

### axlSingleSelectName

`axlSingleSelectName(t_nameTypel_names[g_wildcard])⇒ t/nil`

#### Description

Finds figures by their names. Clears the current contents of the select set and adds named figure`dbids` to the select set in single mode using the arguments as described below. The function selects any figures completely, regardless of the selection mode. If the function selects a figure already partially selected, the figure becomes fully selected.

**Note:** The*on* buttons are used for selecting *Properties* by name only. Both `axlSubSelectName` and `axlAddSelectName` always operate in wildcard mode. Both take the optional wildcard argument but ignore it. In the future, if passed `nil`, they may obey the argument.

#### Arguments

|  |
| --- | ---
| `t_nameType` | Indicates the type of name string being provided. Also implies the type of object to be selected. (see[Finding Objects by Name](#581608 "4")).
| `l_names` | List of item name names or for properties a name value. This varies with the nameType. Supports a single name item outside of a list. Therefore, supported values can be:  - a name  - a list of names  - a list of name/value pairs
|
|
|
| `g_wildcard` | A`t` means that `*` or `?` performs regular expression matching. Default is `nil` where `*` and `?` are treated as normal characters.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the select set.
| `nil` | No objects added to the select set.
#### Example 1

```
axlClearSelSet()axlSetFindFilter(    ?enabled list( "noall" "nets")    ?onButtons list( "all"))axlSingleSelectName ("NET" (list ("GND" "VCC"))⇒ (dbid:234436 dbid:98723)
```

`axlSingleSelectName ("PROPERTY" (list (list "BUS_NAME" "MEM") "FIXED")`

Selects the nets`GND` and `VCC` by their names.

#### Example 2

```
axlClearSelSet()axlSetFindFilter(    ?enabled list( "noall" "nets")    ?onButtons list( "all"))axlSingleSelectName ("PROPERTY"    list(    list( "ELECTRICAL_CONSTRAINT_SET" "ECL_DEFAULT")    "ROUTE_PRIORITY"))⇒ (dbid:234436 dbid:98723 dbid:234437 dbid:98727    dbid:234438 dbid:98725 dbid:234439 dbid:98726)
```

Selects a set of nets--one set by the property name`ELECTRICAL_CONSTRAINT_SET` with value `ECL_DEFAULT`, and another set that has the name `ROUTE_PRIORITY`.

### axlAddSelectName

`axlAddSelectName(t_nameTypel_names)⇒ t/nil`

#### Description

Adds the named figure`dbids` to the select set in cumulated mode according to the arguments described below. Adds the found figures to the select set if not already there. Selects figures completely regardless of the selection mode. If the function selects a figure already partially selected, the figure becomes fully selected.

#### Arguments

|  |
| --- | ---
| `t_nameType` | String denoting the name type to be selected (see[Finding Objects by Name](#581608 "4")). Also implies the type of object to be selected.
| `l_names` | List of item name names or for properties a name value. This varies with the nameType. Supports a single name item outside of a list. Therefore, supported values can be:  - a name  - a list of names  - a list of name/value pairs
|
|
|
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the select set.
| `nil` | No objects added to the select set.
The on buttons matter for select Properties by name, but don't for other name types. Both`axlSubSelectName` and `axlAddSelectName` always operate in wildcard mode. Both take the optional wildcard argument, but ignore it. In the future, if passed `nil`they may obey the argument.

#### Example

See examples for[axlSingleSelectName](#580506 "4"). The only difference is that `axlSingleSelectName` clears the select set, while `axlAddSelectName` adds the selected `dbids` into the select set without removing any already in it. The arguments for `axlAddSelectName` are the same as for `axlSingleSelectName`.

### axlSubSelectName

`axlSubSelectName(t_nameTypel_names)⇒ t/nil`

#### Description

Removes`dbids` of the named figure from the select set using the arguments described. Removes figures completely regardless of the selection mode. If the function finds a figure already partially selected, it removes all of its `dbids` from the select set.

#### Arguments

|  |
| --- | ---
| `t_nameType` | String denoting name type to be selected (see[Finding Objects by Name](#581608 "4")). Also implies the type of object to be selected.
| `l_names` | List of item name names or for properties a name value. This varies with the nameType. Supports a single name item outside of a list. Therefore, supported values can be:  - a name  - a list of names  - a list of name/value pairs
|
|
|
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects deleted from select set.
| `nil` | No objects deleted from select set.
**Note:** The on buttons matter for select Properties by name, but not for other name types. Both`axlSubSelectName` and `axlAddSelectName` always operate in wildcard mode. Both take the optional wildcard argument, but ignore it. In the future, if passed `nil,` they may obey the argument.

#### Example

See examples for[axlSingleSelectName](#580506 "4"). The only difference is that `axlSingleSelectName` clears the select set and then puts the `dbids` it finds into the select set, while `axlSubSelectName` removes the `dbids` of the elements it selects from the select set. The arguments are the same as `axlSingleSelectName`.

### axlSingleSelectObject

`axlSingleSelectObject(lo_dbid)⇒ t/nil`

#### Description

Clears contents of the select set and adds the`dbids` in `lo_dbid` to the select set in single mode. `lo_dbid` is either a single `dbid` or a list of `dbids`. Selects figures completely regardless of the selection mode. If the `dbid` of any part of a figure is in `lo_dbid`, the function adds the entire figure.

**Note:** You need to "BOUNDARY\_SHAPES" to the axlSetFindFilter "?enabled" option if you wish to select a duynamic. We do not allow the generated shape of dynamics shapes to be selected via the SelectObject APIs since the generated shapes cannot be edited.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | `dbid`, or list of `dbids` to be added to the select set.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the select set.
| `nil` | No objects added to the select set.
#### Example

> ```
> axlClearSelSet()axlSetFindFilter(         ?enabled list( "all" "equivlogic")    ?onButtons list( "all"))mysym = axlDBCreateSymbol(    list( "dip14" "package"), 5600:4600)axlSingleSelectObject(car(mysym))⇒ t
> ```

Creates a symbol and add its`dbid` to the select set.

### axlAddSelectObject

`axlAddSelectObject(lo_dbid)⇒ t/nil`

#### Description

Adds the`dbids` in `lo_dbid` to the select set in cumulated mode, that is, without removing already selected objects. `lo_dbid` is either a single `dbid` or a list of `dbids`. Adds `dbids` in the select set only if they are not already there. Selects figures completely regardless of the selection mode. If the `dbid` of any part of a figure is in `lo_dbid`, adds the entire figure.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | `dbid`, or list of `dbids` to be added to the select set.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the select set.
| `nil` | No objects added to the select set.
#### Example

> ```
> axlSetFindFilter(    ?enabled list( "all")    ?onButtons list( "all"))mysym = axlDBCreateSymbol(    list("dip14" "package") 2600:2600 ) axlAddSelectObject(car(mysym))⇒ t
> ```

Creates a symbol instance and adds its`dbid` to the select set.

### axlSubSelectObject

`axlSubSelectObject(lo_dbid)⇒ t/nil`

#### Description

Removes the`dbids` in `lo_dbid` from the select set in cumulated mode. `lo_dbid` is either a single `dbid` or a list of `dbids`. Removes figures completely regardless of the selection mode.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | `dbid`, or list of `dbids` to be removed from select set.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects deleted from select set.
| `nil` | No objects deleted from select set.
#### Example

> ```
> axlClearSelSet()axlSetFindFilter(?enabled list("noall" "vias")    ?onButtons list( "vias"))myvia = axlDBCreateVia( "pad1", 3025:3450)axlAddSelectBox( list( 3000:3100 3200:3600))axlSubSelectObject( car( myvia))⇒ t
> ```

Creates a via, then selects all the vias in a surrounding region for deletion, but saves the one just created by subtracting its`dbid` from the selection set.

The resulting select set contains the`dbids` of all vias in the box except `myvia`, the one just created.

### axlSelect

```
axlSelect(?firstEventCallback    s_callback?groupMode    t/nil?prompt    t_prompt)⇒ t/nil
```

#### Description

General tool for AXL programs to solicit interactive object selections from the user.`axlSelect` automatically sets up the pop-up to provide any of the possible Allegro PCB Editor selection methods:

* Single point select

* Window select

* Group select

You can set up the pop-up to display other options such as*Done* and *Cancel*, but the function also displays the find options. See the example.

Before`axlSelect` returns, it puts in the select set a list of the `dbids` of the objects the user selected.

Use`axlSelect` when you create interactive commands that allow the user to select objects in the same way as existing Allegro PCB Editor interactive commands such as *move* or *delete*. `axlSelect` allows the user to select objects using the standard methods of mouse pick, window, and group. It returns when the user has selected one or more objects or picks *Done* or *Cancel*, depending on the pop-up selections you set up. The default mode for `axlSelect` is selecting a single object by point--equivalent to `axlSingleSelectPoint`.

`axlSelect` removes any previously selected `dbids` in the selection set when the user first selects one or more objects.

You must set up the find filter to meet your requirements before calling`axlSelect`.

#### Arguments

|  |
| --- | ---
| `firstEventCallback` | Procedure to be called once the first user event occurs. The callback takes no arguments.
| `groupMode` | Default is for`axlSelect` to return when the user makes a selection. If groupMode is `'t`, `axlSelect` won't return until you do an `axlCancelEnterFun` or `axlFinishEnterFun`. You perform all of your activity in popup callbacks instead of when `axlSelect` returns. In `groupMode`, `axlSelect` does not clear existing selections. To clear existing selections after the first event, clear them in your `firstEventCallback`.
| `prompt` | Prompt to the user. The default prompt is:  "`Enter selection point`"
|
#### Value Returned

|  |
| --- | ---
| `t` | One or more object`dbids`put into the select set during the call. The select set is a list of the `dbids` of the objects the user selected.
| `nil` | No object`dbids` put into the select set.
#### Example

> ```
> (defun showElement ()mypopup = axlUIPopupDefine( nil    (list (list "Done" 'axlFinishEnterFun)    (list "Cancel" 'axlCancelEnterFun)))axlUIPopupSet( mypopup)axlSetFindFilter( ?enabled list( "NOALL" "ALLTYPES" "NAMEFORM")    ?onButtons "ALLTYPES")while( axlSelect()    axlShowObject( axlGetSelSet()))
> ```

Function loops, performing the`Show Element` command on each object selected by the user.

Although you explicitly set*Done* and *Cancel* for this command, AXL also adds *Group**,* WindowSelect*,* and *FindFilter*to the pop-up.

### axlGetSelSet

`axlGetSelSet()⇒ lo_dbid/nil`

#### Description

Gets the list of object`dbids` in the select set.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `lo_dbid` | List of figure`dbids`.
| `nil` | Select set is empty.
#### Example

> ```
> axlClearSelSet()axlSetFindFilter(?enabled list("noall" "vias")    ?onButtons list("vias"))axlAddSelectBox(list(3000:3100 3200:3600))axlShowObject(axlGetSelSet())⇒ t
> ```

Selects all vias in a box area and shows the contents of the select set.

The**Show Element** window is displayed, with the via selected.

### axlGetSelSetCount

`axlGetSelSetCount()⇒ x_selCount`

#### Description

Returns the number of figure`dbids` in the select set.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `x_selCount` | Number of objects selected. Returns`0` if nothing is selected.
#### Example

> ```
> axlClearSelSet()axlSetFindFilter(?enabled list("noall"))axlSetFindFilter(?enabled list("pins")    ?onButtons list("pins"))axlAddSelectBox()axlGetSelSetCount()⇒ 14
> ```

Sets the Find Filter to find pins, selects a box around a 14 pin dip and prints the number of`dbids` in the select set. It is 14, as expected.

### axlClearSelSet

`axlClearSelSet()⇒ t/nil`

#### Description

Removes all`dbids` from select set.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | One or more`dbids` removed in order to empty the select set.
| `nil` | Select set already empty.
#### Example

> ```
> axlClearSelSet()axlSetFindFilter(?enabled list("noall"))axlSetFindFilter(?enabled list("pins")    ?onButtons list("pins"))axlAddSelectBox()axlGetSelSetCount()⇒ 14
> ```

Ensures the select set does not have any leftover`dbids` in it, as in the example for `axlGetSelSetCount`.

### axlGetFindFilter

`axlGetFindFilter([onEnabledF])⇒ lt_filters/nil`

#### Description

Returns the current Find Filter settings as a list`pf` keyword strings. The return find filters settings (onButton or enabled) is controlled by the boolean `onEnabledF`

#### Arguments

|  |
| --- | ---
| `onEnabledF` | If`onEnabledF` is `t`, returns the enabled list.
|  | If`onEnabledF` is `nil`, returns the `onButton` list.  Default is nil.
|
#### Value Returned

|  |
| --- | ---
| `lt_filters` | List of element types in the Find Filter  OR  list of current onButton settings.
|
|
| `nil` | If list would be empty.
#### Example

> ```
> axlSetFindFilter ?enabled (list "vias" "pins" "nets" "clinesegs" "nameform") ?onButtons (list "vias" "pins" "clinesegs"))
> ```

> `ret =axlGetFindFilter()`

> Returns the following:

> ```
> ("NAMEFORM" "NETS" "CLINESEGS" "VIAS" "PINS" <plus default items that may change from release to release> )
> ```

> `ret = axlGetFindFilter(t)`

> Returns:

> `("CLINESEGS" "VIAS" "PINS")`

### axlSetFindFilter

`axlSetFindFilter(?enabled    lt_enabled?onButtons    lt_filterOn)t/nil`

#### Description

Sets up both the object types to be displayed in the Find Filter, and which types among those are set to*on* in the **Find Filter**.

The first argument,`lt_enabled`, is a list of the object types to be displayed in the Find Filter and of the select options described. The second argument, `lt_onButons`, lists the object types whose buttons are to be *on* (and therefore selectable) when the filter displays. The table lists the keywords that can be included in the enabled and `onButtons` lists for setting up the Find Filter. The diagrams show the keywords and the buttons they cause `axlSetFindFilter` to display.

Each change is additive and processed in the order that they appear in the list. For example, you type the following to enable all object types except for pins.

> `'("ALLTYPES" "NOPINS")`

Each of the following keywords may be preceded with a`"NO"` to disable the particular option or object type. For example, `"NOPINS"`. The initial default is `"NOALL"`.

* **Description**
* Enable pins
* Enable vias
* Enable clines
* Enable cline (arc or line) segs
* Enable lines
* Enable line (arc or line) segs
* Enable drc errors
* Enable text
* Enable shapes, rects and frects
* Enable shape segments
* Enable promotion to boundary shape if auto-shape is selected (see dynamic shape discussion)
* Enable shape voids
* Enable shape void segments
* Enable symbol instances
* Enable figures
* Enable component instances
* Enable function instances
* Enable nets
* Option - OBSOLETE
* Option - For logic object types (nets and components), causes the physical equivalent to be selected. Physical objects must be enabled in both "`enabled`" and "`onButton`" lists.
* Option - Allows selection of objects that are not visible due to color`class/subclass` form setting.
* Option - Enables the*Find by Name/property* fields in the Find Filter form.
* Enables all object types`("PINS" ... "NETS")`.
* Enables all object types and options.
* Enable selection of thermal reliefs generated by dynamic shapes. Only applicable to`?enabled`. By default, you should not select these if you plan on modifying the objects since the dynamic shape will just re-generate them. You should only access them for read-only purposes.
* State 4: Hierarchical.
  By setting both the group and group\_members bitfields, a group is returned for any hierarchical group that is selected (such as a Module instance), and group members are returned for all other selected group types.
* State 1: Legacy.
  This supports code that predates the group implementation. This is the same as State 3.
* State 2: Group only.
  By only setting the group bitfield, any selected group is returned to the application as a group.
* State 3: Members only.
  By only setting the group\_members bitfield, group members are returned to the application when a group is selected.
* OBSOLETE
* Option - For logic object types (nets and components), causes the physical equivalent to be selected. Physical objects must be enabled in both "enabled" an "onButton" lists.
* Option - Allows selection of objects that are not visible due to color class/subclass form setting.
* Option - enables the find by name/property fields in the find filter form.
* Option - Enable selection of thermal reliefs generated by dynamic shapes. Only applicable to ?enabled. By default, you should not select these if you plan on modifying the objects since the dynamic shape will just re-generate them. You should only access them from read-only purposes.

  If in the partition editor or the design has partitions active then this option is used to selections of read-only objects.

  This option should also be used to select shape base fillets. The system will not allow shape based fillets to be modified it the dynamic fillet option is enabled.
* Option - Application has been updated to differentiate bond wires and/or fingers (APD/SIP).

  For more information, see[Bond Objects](#678803 "4").
* Enable all object types ("PINS" ... "NETS").
* Enable all object types and options.

`axlSetFindFilter` processes the keywords in each argument list in order and only makes the changes occurring in the list. Changes are incremental for each call to the function. To remove a selection, attach the string `"NO"` to the front of the keyword. For example, the list `("ALLTYPES" "NOPINS")` enables all object types except pins. The initial default setting of the Find Filter is `"NOALL"`*,* or, nothing enabled. Use `"NOALL"`, as shown, to clear the
Find Filter before enabling particular types.

#### ***Dynamic Shapes***

When writing an application and it needs to handle shapes, you need to decide how you want to handle dynamic shapes. If your SKILL program does not access shapes, read no further.

A shape on`ETCH` may be either static or dynamic. A static shape is similar to what existed in Allegro PCB Editor prior to PSD15.0. You add a shape to an etch layer and manually void objects that impact the shape. A dynamic shape is placed on the `BOUNDARY CLASS` and generates zero or more shapes on the `ETCH` layer based upon voiding.

If you want to modify a dynamic shape, then you should set`BOUNDARY_SHAPES`. This allows the user to select the generated shape, but selection will return its dynamic shape (e.g. a *move shape*). If you want to access information on the shape, then do not set the `BOUNDARY_SHAPES` option (e.g. *show element*).

**Note:** If you pass`"ALL"` or `"ALLTYPES"` to `setOptions`, then `BOUNDARY_SHAPES` will be enabled and user's selecting a `ETCH` layer generated shape will result in the selection returning its dynamic shape on the `"BOUNDARY CLASS"`. If you wish to select the generated shape, but want to use the `all` option, then use the following:

> `"(ALLTYPES" "NOBOUNDARY_SHAPES")`

You need only pass`BOUNDARY_SHAPES` to the enabled list. It will be ignored if passed to the `onButtons` list.

****Figure 4-1****
**Find Filter and Related Keywords**

The differences in effects of different combinations of keywords can be subtle.[Figure 4-2](#580670 "4") shows the relationship between the keywords.

****Figure 4-2****
**Relationship Among axlSetFindFilter Keywords (*See examples also*)**

#### *Bond Objects*

Bond objects (bond wires and fingers) are enabled only in SIP/APD. These options are ignored in the PCB products.

In SIP/APD, to maintain backward compatibility, an application is not considered to be "bond smart". This means if the Skill application enables VIAs then FINGERS are enabled and if CLINES is enabled, the BOND WIRES are automatically enabled.

To make an application BOND SMART, you either set the BONDSMART option or use the BONDWIRES, NOBONDWIRES, FINGERS or NOFINGERS options. An application that is bond smart can separately control the selection of bond objects (fingers or bond wires) from their base objects (vias or clines).

**Note:** You only need to make you Skill application bond smart if you wish to differentiate the disabling of one of these objects. By default, users in SIP/APD will be able to independently select:

|  |  |
| --- | --- | ---
|  |  | VIAS or FINGERS if the Skill application enables VIAS
|  |  |
| --- | --- | ---
|  |  | CLINES and WIRES if CLINES are enabled.
Ideally most applications will not need to be updated to be bond smart.

#### Arguments

|  |
| --- | ---
| `lt_enabled` | List of keyword strings that describe object types that are to be selectable. Enabled object types will appear in the**Find Filter** form. Object types need the `onButton` set as well to fully enable selection. List may also include selection options.
|  | Also supports a single keyword string instead of a list of strings.
| `lt_onButtons` | List of keyword strings that describe object types that are to be enabled for selection. Enabled types will appear with the`onButton` depressed in the Find Filter form. `onButton` settings provide the default for controls which can be modified by the user when the Find Filter form is opened. An object type must be *on* in both the enabled and the `onButton` lists to be fully enabled for selection. Options are ignored when provided in the `onButton` list.
|  | Also supports a single keyword string instead of a list of strings.
**Note:** `axlSetFindFilter` does not display or select any types that are not enabled. That means that `?onButtons` keywords only effect enabled types. For example, to have all enabled buttons be *on*, use `?onButtons list("alltypes")`. In general, you need only set specific buttons *on* if you want those on and others off.

#### Value Returned

|  |
| --- | ---
| `t` | One or more Find Filter changes were made.
| `nil` | No valid keywords were provided.
#### Application Programming Note

When you use`axlSetFindFilter` to implement an interactive command, make your
AXL-SKILL program restore the user's FindFilter settings from the previous time he or she used the same command. Find Filter settings are incremental. Clear any previous settings as you start, then set the ones you want. Call `axlSetFindFilter` with `"noall"` as the first member of the list for both the `?enabled` and `?onButtons` arguments the first time you call it.

To maintain the user's Find Filter settings between invocations of your command

* The first time the user invokes your program (when it loads), preset global variables to the list of`?enabled` and `?onButtons` settings you want as the initial default, as follows:

> > `myglobal_enabled = list("noall" "xxx" "yyy" ... "zzz")`

> > `myglobal_onButtons = list("xxx" ..."zzz")`

* Each time the user invokes your command, call`axlSetFindFilter` with the current global values of `?enabled` and `?onButtons`.

> ```
> axlGetFindfilter( ?enabled myglobal_enabled        ?onButtons myglobal_onButtons)
> ```

> Since users can set or clear any of the buttons on the Find Filter, you need to save the button settings as you exit the command.

* As you end the command, save the user's Find Filter`onButton` settings as shown:

> > `myglobal_onButtons = cons( "noall" axlGetFindFilter(t))`

> **Note:** The`cons - "noall"`ensures that when you call `axlSetFindFilter` again you clear any settings left over from any previous command, and set only the buttons set at the time you call `axlGetFindFilter`.

#### Example 1

> > ```
> > (axlSetFindFilter ?enabled (list "vias" "pins" "nets")     ?onButtons (list "vias" "pins"))
> > ```

Displays the Find Filter with a list of Nets, Pins, and Vias. The Pins and Vias boxes are turned on as shown:

#### Example 2

> > ```
> > (axlSetFindFilter ?enabled (list "noall" "vias" "pins"    "nets" "clinesegs" "nameform")    ?onButtons (list "vias" "pins" "clinesegs"))
> > ```

Displays the Find Filter with Pins, Vias, and Clinesegs turned on.

#### Example 3

> > ```
> > axlSetFindFilter(?enabled list("noall" "equivlogic" "nets" "pins" "vias")?onButtons list("all"))
> > ```

Sets to find all the pins and vias on a net when the user selects any part of the net.

### axlAutoOpenFindFilter

`axlAutoOpenFindFilter()⇒ t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` always.
### axlOpenFindFilter

`axlOpenFindFilter()⇒ t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` always.
### axlCloseFindFilter

`axlCloseFindFilter()⇒ t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` always.
### axlDBFindByName

`axlDBFindByName(s_typet_name) ⇒ o_dbid/nil`

#### Description

Finds`dbid` of an object by name without involving the selection set. This means you can run this command any time without affecting what exists in the selection set. The following object lookup types are supported:

|  |  |
| --- | --- | ---
| **type** | **t\_name** | **return type**
| 'net | net name | `dbid` of a net
| 'refdes | refdes | `dbid` of a component instance
| 'padstack | padstack name | `dbid`of a padstack
This is restricted to a single object. To find objects using wildcards, use`axlSelectByName`.

#### Arguments

|  |
| --- | ---
| `s_type` | Type symbol; see above.
| `t_name` | Object's name (this is case insensitive).
**Value Returned**

|  |
| --- | ---
| `o_dbid` | `dbid` of object or `nil.`
#### See Also

[axlSelectByName](#665244 "4")

#### Examples

> `db = axlDBFindByName('net "GND")`

> `db = axlDBFindByName('padstack "VIA")`

> `db = axlDBFindByName('refdes "U1")`

### axlFindFilterIsOpen

`axlFindFilterIsOpen()⇒ t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` always.
### axlSelectByName

`axlSelectByName (t_objectTypet_name/lt_name[g_wildcard])⇒ lo_dbid/nil`

#### Description

Selects database objects by name.

Interface allows more than one name to be passed, but only one object type per call. For certain object types, a single name may return multiple objects. The supported object types and related items follow:

|  |
| --- | ---
| **Object Type** | **Item the function finds**
| `"NET"` | net name
| `"COMPONENT"` | component name
| `"FUNCTION"` | function name
| `"DEVTYPE"` | device type name
| `"SYMTYPE"` | symbol type name
| `"PIN"` | refdes.pinname
| `"REFDES"` | find symbol by refdes name
| `"COMPREFDES"` | find component by refdes name
| `"GROUP"` | find group by name
| `"BUS"` | find bus by name
| `"DIFF_PAIR"` | find differential pair by name
| `"NETCLASS"` | find netclass by name
| `"NET_GROUP"` | find a net group by name
| `"REGION"` | find region by name
| `"XNET"` | find xnet by name; Will return a Net if xnet is a single net xnet. See`<cdsroot>/share/pcb/examples/skill/select/ashfindxnet.il`
| `"MATCH_GROUP"` | find matchgroup by name
| `"MODULE"` | find module by name
You can use wildcards with this function:

* `"*"` matches any sequence of zero or more characters.

* `"?"` matches any single character.

* `"\"` is used to send a special character, for example, `\x`.

Provided third argument`[g_wildcard]` is set to `TRUE`.

**Note:** This saves and restores the current find filter settings, but resets the selection set.

#### Arguments

|  |
| --- | ---
| `t_objectType` | Type of database name.
| `t_name` | Object to find.
| `lt_name` | List of names to find.
| `[g_wildcard]` | If`*` or `?` appear in name, use regular expression matching
#### Value Returned

|  |
| --- | ---
| `t` | List of objects found.
| `nil` | No matching name or illegal`objectType` name.
#### Example 1

> `Skill > p = axlSelectByName("NET" '("GND" "NET1"))`

> `(dbid:28622576 dbid:28639844)`

Finds two nets.

#### Example 2

> `Skill > p = axlSelectByName("NET" '("GND" "FOO"))`

> `(dbid:28622576)`

Finds two nets, but board only has`GND`.

#### Example 3

> `Skill > p = axlSelectByName("COMPONENT" "C1")`

> `(dbid:28590388)`

> `Skill > car(p)->objType`

> `"component"`

Finds Component`C1`.

#### Example 4

> `Skill > p = axlSelectByName("FUNCTION" "TF-326")`

> `(dbid:28661572)`

> `Skill > car(p)->objType`

> `"function"`

Finds function`TF-326.`

#### Example 5

> `Skill > p = axlSelectByName("DEVTYPE" "CAP1")`

> `(dbid:28591032 dbid:28590700 dbid:28590388)`

> `Skill > car(p)->objType`

> `"component"`

Finds devices of type`CAP1`.

#### Example 6

> `Skill > p = axlSelectByName("SYMTYPE" "dip14_3")`

> `(dbid:28688416 dbid:28686192)`

> `Skill > car(p)->objType`

> `"symbol"`

Finds symbols of type`DIP14_3`.

#### Example 7

> `Skill > p = axlSelectByName("PIN" "U1.1")`

> `(dbid:28630692)`

> `Skill > car(p)->objType`

> `"pin"`

Finds pin`U2.1`.

#### Example 8

> `Skill > p = axlSelectByName("REFDES" "U3")`

> `(dbid:28688416)`

> `Skill > car(p)->objType`

> `"symbol"`

Finds symbol by refdes`U3`.

#### Example 9

> `Skill > p = axlSelectByName("COMPREFDES" "U3")`

> `(dbid:28621208)`

> `Skill > car(p)->objType`

> `"component"`

Finds component by refdes`U3`.

#### Example 10

> `Skill > p = axlSelectByName("GROUP" "BAR")`

> `(dbid:28593776)`

> `Skill > car(p)->objType`

Finds a group`BAR` by name.

#### Example 11

> `Skill > p = axlSelectByName("PIN" "U1.*" t)`

> ```
> (dbid:28630856 dbid:28630784 dbid:28630692 dbid:28630572 dbid:28630400 dbid:28630228 dbid:28630076 dbid:28630004 dbid:28629912 dbid:28629800 dbid:28629728 dbid:28629656 dbid:28629484 dbid:28629372 dbid:28629280 dbid:28629208
> ```

> `)`

Finds all pins on`refdes U1`.

#### Example 12

> `Skill > p = axlSelectByName("PIN" "U1.?" t)`

> ```
> (dbid:28630856 dbid:28630692 dbid:28630572 dbid:28630400 dbid:28630228 dbid:28630076 dbid:28630004 dbid:28629912 dbid:28629800
> ```

> `)`

Finds pins with single digit number on`U1`.

#### Example 13

> `Skill > p = axlSelectByName("NET" "N*" t)`

> `(dbid:28630044 dbid:28634000 dbid:28638750)`

Finds nets starting with`N`.

### axlSelectByProperty

```
axlSelectByProperty(t_objectTypet_property[t_value][g_regularExpression])⇒ lo_dbid/nil
```

#### Description

Selects the`dbid` set of a particular Allegro PCB Editor database object with the indicated property.

Property can be a name or a name/value pair. Value may contain a regular expression (`*` or `?`), since certain select by name functions support wildcards. You can test for the presence of wildcards before you call this function.

Regular expressions used by Allegro PCB Editor differ from the Skill regular expressions. Allegro PCB Editor handles regular expressions such that they are more compatible with the character set allowed in Allegro PCB Editor object names. Do not use this function to test patterns sent to the Skill`regexp` family of functions.

For value, match the database formats into the value string to contain the units preference if applicable for the property. If the data type of the attribute is BOOLEAN, and if it exists on the element, the string is empty. If the data type is`INTEGER` or `REAL`, the user units string, if any, is appended to the value. If the data type is one of the `"units category"` types, for example, `ALTITUDE`, `PROP_DELAY`, the MKS package converts the value.

Properties must be upper case. The value is case insensitive if wildmatch match is`nil` while case sensitive for wildcard matching.

**Note:** Property names may change from release to release, or may be rendered obsolete. SKILL programs using property names may require modifications in future releases.

#### Arguments

|  |
| --- | ---
| `t_objectType` | String for Allegro PCB Editor database object type. Must be:`compdef`, `component`, `drc`, `net`, `symdef`, `symbol`, or `group`.
| `t_property` | Name of property.
| `t_value` | Optional property value.
| `g_regularExpression` | `t`if property value is to be treated as a regular expression, or `nil`, which is the default, to treat property value as a simple match.
#### Value Returned

|  |
| --- | ---
| `t` | One or more`dbids` added to the select set.
| `nil` | No`dbids` added to the select set.
#### Example 1

> `p = axlSelectByProperty("net" "ELECTRICAL_CONSTRAINT_SET")`

> `axlAddSelectObject(p)`

Selects all nets with an`ECset` property, then adds them to the current select set.

#### Example 2

> `p = axlSelectByProperty("net" "ELECTRICAL_CONSTRAINT_SET", "SPITFIRE_ADDRESS")`

Selects all nets with ECset property of value`SPITFIRE_ADDRESS`.

#### Example 3

> `p = axlSelectByProperty("net" "ELECTRICAL_CONSTRAINT_SET", "SPITFIRE*" t)`

Selects all nets with ECset property with any value matching`spitfire`.

### axlSnapToObject

`axlSnapToObject(g_modexy)⇒ xy/nil`

#### Description

Supports snapping to a logic object's connect point. A logic object is a:

* Cline

* Clines segments (lines or arcs)

* Via

* Pin

For cline objects, the two end points are considered the connect points. For pad objects, the connect point is defined in the padstack. Snapping is based upon the trap size, which varies based upon the zoom factor (see`axlGetTrapBox`). The smaller the trap size, the higher the zoom. If no object is found within the original xy location is returned.

**Note:** Avoid using the grid snapping option with`axlEnterPoint` as it might move the user pick outside the trap size.

#### Arguments

|  |
| --- | ---
| `g_mode` | `nil`: Use active sel set to determine snapping.
|  | `t`: Snap based upon the visible layers in the database.
| `xy` | Location in design units to snap (list of design units x:y).
#### Value Returned

|  |
| --- | ---
| `xy` | Object snapped point (list of design units x:y).
| `nil` | If not object exists for snapping returns nil.
Also nil if arguments are incorrect

#### See Also

[axlGetSelSet](#580611 "4")`,`[axlGetTrapBox](08intprm.html#616877 "7")`,`[axlGetLastEnterPoint](06intedt.html#861744 "5")

#### Examples

Pseudo code to move objects.

`; select object(s); do not do a axlClearSelSet`

`_clpSelect`

`; first snap to an object that is the selection list`

`gridSnap = axlEnterPoint(?prompts list("Pick origin point")`

`? gridSnap t)`

`; for better results use the unsnapped pick`

`origin = axlSnapToObject(nil axlLastPick(nil))`

`; if no object found fallback to the grid snapped pick`

`unless( origin origin = gridSnap)`

`; ok to do clear now`

`axlClearSelSet()`

`; now ask user for a destination`

`gridSnap = axlEnterPoint(?prompts list("Pick origin point")`

`? gridSnap t)`

`; Now snap the destination point based upon what can be found at that`

`; location`

`; for better results use the unsnapped pick`

`dest = axlSnapToObject(nil axlLastPick(nil))`

`; fallback to grid snapped location if nothing found`

`unless( origin dest = gridSnap)`

`; modify coordinates with dest location`

`axlTransformObject(....)`

### axlLastPickIsSnapped

`axlLastPickIsSnapped()-> t/nil`

#### Description

Normally called after an`axlEnter` call to determine if the pick was snapped or unsnapped.

#### Arguments

none

#### Value Returned

`t` if last picked was snapped, `nil` if unsnapped

#### Examples

`snappedPoint = axlEnterPoint(?prompts list("Pick origin point")`

`?gridSnap t)`

`state = axlLastPickIsSnapped()`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
