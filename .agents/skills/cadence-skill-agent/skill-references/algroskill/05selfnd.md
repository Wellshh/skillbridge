### axlSingleSelectPoint

`axlSingleSelectPoint( [l_point] [g_trapSize] ) => t/nil`

#### Description

Clears the select set, finds a figure at `l_point` according to the Find Filter, and puts the selected figure `dbid` in the select set. If `l_point` is `nil`, the function requests a single pick from the user.

`axlSingleSelectPoint` selects a single object and adds it to the select set, unless `EQUIVLOGIC` is on. In that case, it may select multiple objects, for example, if it finds a qualified figure (such as a pin, connect line, or via) that is part of a net. `axlSingleSelectPoint` adds all the qualified figures that belong to the net to the select set. (See the Find Filter Options.)

This finds objects within the current trapsize (`axlGetTrapBox`), which varies based upon the zoom factor.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | Point in database coordinates at which to look for figures. |
| `g_trapSize` | Enables a a trap box, which is based on the zoom level of the canvas. Objects that are found can be effected based on the current zoom level. When this option is set to `nil` the trap size gets disabled. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more `dbids` put in the select set. |
| `nil` | No `dbids` put in the select set. |

#### Examples

`axlSetFindFilter(?enabled "pins" ?onButtons "pins") axlSingleSelectPoint( 6325:3575 ) axlDBAddProp(axlGetSelSet() list( "MYPROP" 23.5)) ⇒` t
 
 Adds a previously defined user property `MYPROP` to a pin at X6325 Y3575.

To check

| Name | Description |
|---|---|
| 1. | From Allegro PCB Editor, choose Display - Element. |

| Name | Description |
|---|---|
| 2. | Select the pin to display its properties. |

The Show Element window displays MYPROP with value 23.500000 level

### axlAddSelectPoint

`axlAddSelectPoint( [l_point] ) => t/nil`

#### Description

Finds a figure at `l_point` according to the Find Filter and adds its `dbid` to the select set in cumulated mode. If `l_point` is `nil`, requests a single pick from the user.

Selects a single object and adds it to the select set, unless `EQUIVLOGIC` is on. In that case, selects multiple objects, for example, if it finds a qualified figure (such as a pin, connect line, or via) that is part of a net. Adds all the qualified figures that belong to the net to the select set. (See the Find Filter Options.)

This finds objects within the current trapsize (`axlGetTrapBox`), which varies based upon the zoom factor.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | Point in the layout at which to find figures. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more `dbids` put in the select set. |
| `nil` | No `dbids` put in the select set. |

#### Examples

See axlSingleSelectPoint for an example. `axlSingleSelectPoint` has the same behavior except that it selects only one object.

### axlSubSelectPoint

`axlSubSelectPoint( [l_point] ) => t/nil`

#### Description

Finds a figure at `l_point` according to the Find Filter and deletes its `dbid` from the select set in cumulated mode. That is, it deletes that `dbid` while leaving any others currently in the select set. If `l_point` is `nil`, requests a single pick from the user.

Removes a single object from the select set, unless `EQUIVLOGIC` is on. In that case, finds multiple objects, for example, if it finds a qualified figure (such as a pin, connect line, or via) that is part of a net. Deletes all the qualified figures that belong to the net from the select set. (See the Find Filter Options.)

This finds objects within the current trapsize (`axlGetTrapBox`), which varies based upon the zoom factor.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | Point in the layout at which to find figures to deselect. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more `dbids` removed from the select set |
| `nil` | No `dbids` removed from the select set. |

#### Examples

`axlSetFindFilter(?enabled "pins" ?onButtons "pins")``axlSingleSelectBox( list(6200:3700 6500:3300))``axlSubSelectPoint( 6325:3575 )``axlDBAddProp(axlGetSelSet() list("MYPROP" 23.5))``⇒ t`

Adds a previously defined user property, `MYPROP`

| Name | Description |
|---|---|
| 1. | Selects four pins in a box in order. |

| Name | Description |
|---|---|
| 2. | Before adding the property, subtracts the pin at `6325:3575` from the list, then adds as shown. |

To check

| Name | Description |
|---|---|
| 1. | Select Edit - Properties. |

| Name | Description |
|---|---|
| 2. | Select a window around all four pins. |

| Name | Description |
|---|---|
| 3. | Select MYPROP from the Available Properties list in the Edit Property window. |

The command displays the pins that have properties in the Show Properties window. Only the three pins not subtracted from the select set have the property, MYPROP.

### axlSingleSelectBox

`axlSingleSelectBox( [l_bBox] ) => t/nil`

#### Description

Clears the select set, finds all figures inside the rectangle `l_bBox` according to the Find Filter, and adds the selected figure `dbids` in single mode to the select set.

#### Arguments

| Name | Description |
|---|---|
| `l_bBox` | List containing one or two coordinates defining the bounding box to be used to select the figures. If `l_bBox` is `nil`, requests two picks from the user. If `l_bBox` has only one point, asks for a second point from the user. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the select set. |
| `nil` | No objects added to the select set. |

#### Examples

`axlSetFindFilter(?enabled "pins" ?onButtons "pins")``axlSingleSelectBox( list(6200:3700 6500:3300))``axlDBAddProp(axlGetSelSet() list( "MYPROP" 23.5))``⇒ t`

Adds a previously defined user property `MYPROP` to four pins by selecting a box around them with corners (`6200:3700 6500:3300`).

To check

| Name | Description |
|---|---|
| 1. | Select Edit - Properties. |

| Name | Description |
|---|---|
| 2. | Select the four pins. |

| Name | Description |
|---|---|
| 3. | Select MYPROP from the Available Properties list in the Edit Property window. |

The command displays the four pins in the Show Properties window as having MYPROP with value 23.500000 level

### axlAddSelectBox

`axlAddSelectBox( [l_bBox] ) => t/nil`

#### Description

Finds one or more figures inside the rectangle `l_bBox` according to the current Find Filter, and adds the selected figure `dbids` in cumulated mode for the select set.

#### Arguments

| Name | Description |
|---|---|
| `l_bBox` | List containing one or two coordinates defining the bounding box to be used to the select figures. If `l_bBox` is `nil`, requests two picks from the user. If `l_bBox` has only one point, asks for a second point from the user. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the select set. |
| `nil` | No objects added to the select set. |

#### Examples

See the example for axlSingleSelectBox. That function behaves exactly as `axlAddSelectBox`, except that `axlSingleSelectBox` does not clear the select set.

### axlSubSelectBox

`axlSubSelectBox( [l_bBox] ) => t/nil`

#### Description

Finds one or more figures inside the rectangle `l_bBox` according to the Find Filter, and deletes their `dbids` from the select set in cumulated mode. Deletes those `dbids` while leaving any others currently in the select set.

#### Arguments

| Name | Description |
|---|---|
| `l_bBox` | List containing one or two coordinates defining the bounding box to be used to the select figures. If `l_bBox` is `nil`, requests two picks from the user. If `l_bBox` has only one point, asks for a second point from the user. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects deleted from select set. |
| `nil` | No objects deleted from select set. |

#### Examples

See axlSubSelectPoint for an example of subtracting from the select set, and axlAddSelectPoint for an example of using a box for selection.

### axlAddSelectAll

`axlAddSelectAll() => t/nil`

#### Description

Finds all the figures in the database that pass the current Find Filter and adds their `dbids` to the select set.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more object `dbids` added to the select set. |
| `nil` | No object `dbids` added to the select set. |

#### Examples

`axlSetFindFilter(?enabled list( "noall" "vias")``?onButtons list( "noall" "vias"))``axlAddSelectAll()``axlDeleteObject(axlGetSelSet())``⇒ t`

Selects all vias in a layout and deletes them.

### axlSubSelectAll

`axlSubSelectAll() => t/nil`

#### Description

Finds all figures in the database that pass the current Find Filter and deletes their `dbids` from the select set. Use `axlSubSelectAll` to subtract all of a given type of figure from a larger set of selected objects.

Note: Use `axlClearSelSet` to deselect all figures in the current select set, regardless of the current Find Filter.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more `dbids` deleted from select set. |
| `nil` | No `dbids` deleted from select set. |

Note: Dependent on find filter ?enabled settings.

### axlSingleSelectName

`axlSingleSelectName( t_nameType l_names [g_wildcard] ) => t/nil`

#### Description

Finds figures by their names. Clears the current contents of the select set and adds named figure `dbids` to the select set in single mode using the arguments as described below. The function selects any figures completely, regardless of the selection mode. If the function selects a figure already partially selected, the figure becomes fully selected.

Note: The on buttons are used for selecting Properties by name only. Both `axlSubSelectName` and `axlAddSelectName` always operate in wildcard mode. Both take the optional wildcard argument but ignore it. In the future, if passed `nil`, they may obey the argument.

#### Arguments

| Name | Description |
|---|---|
| `t_nameType` | Indicates the type of name string being provided. Also implies the type of object to be selected. (see Finding Objects by Name ). |
| `l_names` | List of item name names or for properties a name value. This varies with the nameType. Supports a single name item outside of a list. Therefore, supported values can be:
 - a name
 - a list of names
 - a list of name/value pairs |
| `g_wildcard` | A `t` means that `*` or `?` performs regular expression matching. Default is `nil` where `*` and `?` are treated as normal characters. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the select set. |
| `nil` | No objects added to the select set. |

### axlAddSelectName

`axlAddSelectName( t_nameType l_names ) => t/nil`

#### Description

Adds the named figure `dbids` to the select set in cumulated mode according to the arguments described below. Adds the found figures to the select set if not already there. Selects figures completely regardless of the selection mode. If the function selects a figure already partially selected, the figure becomes fully selected.

#### Arguments

| Name | Description |
|---|---|
| `t_nameType` | String denoting the name type to be selected (see Finding Objects by Name ). Also implies the type of object to be selected. |
| `l_names` | List of item name names or for properties a name value. This varies with the nameType. Supports a single name item outside of a list. Therefore, supported values can be:
 - a name
 - a list of names
 - a list of name/value pairs |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the select set. |
| `nil` | No objects added to the select set. |

The on buttons matter for select Properties by name, but don't for other name types. Both `axlSubSelectName` and `axlAddSelectName` always operate in wildcard mode. Both take the optional wildcard argument, but ignore it. In the future, if passed `nil`they may obey the argument.

#### Examples

See examples for axlSingleSelectName. The only difference is that `axlSingleSelectName` clears the select set, while `axlAddSelectName` adds the selected `dbids` into the select set without removing any already in it. The arguments for `axlAddSelectName` are the same as for `axlSingleSelectName`.

### axlSubSelectName

`axlSubSelectName( t_nameType l_names ) => t/nil`

#### Description

Removes `dbids` of the named figure from the select set using the arguments described. Removes figures completely regardless of the selection mode. If the function finds a figure already partially selected, it removes all of its `dbids` from the select set.

#### Arguments

| Name | Description |
|---|---|
| `t_nameType` | String denoting name type to be selected (see Finding Objects by Name ). Also implies the type of object to be selected. |
| `l_names` | List of item name names or for properties a name value. This varies with the nameType. Supports a single name item outside of a list. Therefore, supported values can be:
 - a name
 - a list of names
 - a list of name/value pairs |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects deleted from select set. |
| `nil` | No objects deleted from select set. |

Note: The on buttons matter for select Properties by name, but not for other name types. Both `axlSubSelectName` and `axlAddSelectName` always operate in wildcard mode. Both take the optional wildcard argument, but ignore it. In the future, if passed `nil,` they may obey the argument.

#### Examples

See examples for axlSingleSelectName. The only difference is that `axlSingleSelectName` clears the select set and then puts the `dbids` it finds into the select set, while `axlSubSelectName` removes the `dbids` of the elements it selects from the select set. The arguments are the same as `axlSingleSelectName`.

### axlSingleSelectObject

`axlSingleSelectObject( lo_dbid ) => t/nil`

#### Description

Clears contents of the select set and adds the `dbids` in `lo_dbid` to the select set in single mode. `lo_dbid` is either a single `dbid` or a list of `dbids`. Selects figures completely regardless of the selection mode. If the `dbid` of any part of a figure is in `lo_dbid`, the function adds the entire figure.

Note: You need to "BOUNDARY_SHAPES" to the axlSetFindFilter "?enabled" option if you wish to select a duynamic. We do not allow the generated shape of dynamics shapes to be selected via the SelectObject APIs since the generated shapes cannot be edited.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | `dbid`, or list of `dbids` to be added to the select set. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the select set. |
| `nil` | No objects added to the select set. |

#### Examples

`axlClearSelSet()``axlSetFindFilter(``?enabled list( "all" "equivlogic")``?onButtons list( "all"))``mysym = axlDBCreateSymbol(``list( "dip14" "package"), 5600:4600)``axlSingleSelectObject(car(mysym))``⇒ t`

Creates a symbol and add its `dbid` to the select set.

### axlAddSelectObject

`axlAddSelectObject( lo_dbid ) => t/nil`

#### Description

Adds the `dbids` in `lo_dbid` to the select set in cumulated mode, that is, without removing already selected objects. `lo_dbid` is either a single `dbid` or a list of `dbids`. Adds `dbids` in the select set only if they are not already there. Selects figures completely regardless of the selection mode. If the `dbid` of any part of a figure is in `lo_dbid`, adds the entire figure.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | `dbid`, or list of `dbids` to be added to the select set. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the select set. |
| `nil` | No objects added to the select set. |

#### Examples

`axlSetFindFilter(``?enabled list( "all")``?onButtons list( "all"))``mysym = axlDBCreateSymbol(``list("dip14" "package") 2600:2600 ) axlAddSelectObject(car(mysym))``⇒ t`

Creates a symbol instance and adds its `dbid` to the select set.

### axlSubSelectObject

`axlSubSelectObject( lo_dbid ) => t/nil`

#### Description

Removes the `dbids` in `lo_dbid` from the select set in cumulated mode. `lo_dbid` is either a single `dbid` or a list of `dbids`. Removes figures completely regardless of the selection mode.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | `dbid`, or list of `dbids` to be removed from select set. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects deleted from select set. |
| `nil` | No objects deleted from select set. |

#### Examples

`axlClearSelSet()``axlSetFindFilter(?enabled list("noall" "vias")``?onButtons list( "vias"))``myvia = axlDBCreateVia( "pad1", 3025:3450)``axlAddSelectBox( list( 3000:3100 3200:3600))``axlSubSelectObject( car( myvia))``⇒ t`

Creates a via, then selects all the vias in a surrounding region for deletion, but saves the one just created by subtracting its `dbid` from the selection set.

The resulting select set contains the `dbids` of all vias in the box except `myvia`, the one just created.

### axlSelect

`axlSelect( ?firstEventCallback s_callback ?groupMode t/nil ?prompt t_prompt ) => t/nil`

#### Description

General tool for AXL programs to solicit interactive object selections from the user. `axlSelect` automatically sets up the pop-up to provide any of the possible Allegro PCB Editor selection methods:

- Single point select

- Window select

- Group select

You can set up the pop-up to display other options such as Done and Cancel, but the function also displays the find options. See the example.

Before `axlSelect` returns, it puts in the select set a list of the `dbids` of the objects the user selected.

Use `axlSelect` when you create interactive commands that allow the user to select objects in the same way as existing Allegro PCB Editor interactive commands such as move or delete. `axlSelect` allows the user to select objects using the standard methods of mouse pick, window, and group. It returns when the user has selected one or more objects or picks Done or Cancel, depending on the pop-up selections you set up. The default mode for `axlSelect` is selecting a single object by point--equivalent to `axlSingleSelectPoint`.

`axlSelect` removes any previously selected `dbids` in the selection set when the user first selects one or more objects.

You must set up the find filter to meet your requirements before calling `axlSelect`.

#### Arguments

| Name | Description |
|---|---|
| `firstEventCallback` | Procedure to be called once the first user event occurs. The callback takes no arguments. |
| `groupMode` | Default is for `axlSelect` to return when the user makes a selection. If groupMode is `'t`, `axlSelect` won't return until you do an `axlCancelEnterFun` or `axlFinishEnterFun`. You perform all of your activity in popup callbacks instead of when `axlSelect` returns. In `groupMode`, `axlSelect` does not clear existing selections. To clear existing selections after the first event, clear them in your `firstEventCallback`. |
| `prompt` | Prompt to the user. The default prompt is:
 "`Enter selection point`" |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more object `dbids` put into the select set during the call. The select set is a list of the `dbids` of the objects the user selected. |
| `nil` | No object `dbids` put into the select set. |

#### Examples

`(defun showElement ()``mypopup = axlUIPopupDefine( nil``(list (list "Done" 'axlFinishEnterFun)``(list "Cancel" 'axlCancelEnterFun)))``axlUIPopupSet( mypopup)``axlSetFindFilter( ?enabled list( "NOALL" "ALLTYPES" "NAMEFORM")``?onButtons "ALLTYPES")``while( axlSelect()``axlShowObject( axlGetSelSet()))`

Function loops, performing the `Show Element` command on each object selected by the user.

Although you explicitly set Done and Cancel for this command, AXL also adds Group, Window Select, and FindFilter to the pop-up.

### axlGetSelSet

`axlGetSelSet() => lo_dbid/nil`

#### Description

Gets the list of object `dbids` in the select set.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `lo_dbid` | List of figure `dbids`. |
| `nil` | Select set is empty. |

#### Examples

`axlClearSelSet()``axlSetFindFilter(?enabled list("noall" "vias")``?onButtons list("vias"))``axlAddSelectBox(list(3000:3100 3200:3600))``axlShowObject(axlGetSelSet())``⇒ t`

Selects all vias in a box area and shows the contents of the select set.

The Show Element window is displayed, with the via selected.

### axlGetSelSetCount

`axlGetSelSetCount() => x_selCount`

#### Description

Returns the number of figure `dbids` in the select set.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `x_selCount` | Number of objects selected. Returns `0` if nothing is selected. |

#### Examples

`axlClearSelSet()``axlSetFindFilter(?enabled list("noall"))``axlSetFindFilter(?enabled list("pins")``?onButtons list("pins"))``axlAddSelectBox()``axlGetSelSetCount()``⇒ 14`

Sets the Find Filter to find pins, selects a box around a 14 pin dip and prints the number of `dbids` in the select set. It is 14, as expected.

### axlClearSelSet

`axlClearSelSet() => t/nil`

#### Description

Removes all `dbids` from select set.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more `dbids` removed in order to empty the select set. |
| `nil` | Select set already empty. |

#### Examples

`axlClearSelSet()``axlSetFindFilter(?enabled list("noall"))``axlSetFindFilter(?enabled list("pins")``?onButtons list("pins"))``axlAddSelectBox()``axlGetSelSetCount()``⇒ 14`

Ensures the select set does not have any leftover `dbids` in it, as in the example for `axlGetSelSetCount`.

### axlGetFindFilter

`axlGetFindFilter( [onEnabledF] ) => lt_filters/nil`

#### Description

Returns the current Find Filter settings as a list `pf` keyword strings. The return find filters settings (onButton or enabled) is controlled by the boolean `onEnabledF`

#### Arguments

| Name | Description |
|---|---|
| `onEnabledF` | If `onEnabledF` is `t`, returns the enabled list.<br><br>If `onEnabledF` is `nil`, returns the `onButton` list. 
 Default is nil. |

#### Value Returns

| Name | Description |
|---|---|
| `lt_filters` | List of element types in the Find Filter 
 OR 
 list of current onButton settings. |
| `nil` | If list would be empty. |

#### Examples

`axlSetFindFilter ?enabled (list "vias" "pins" "nets" "clinesegs" "nameform") ?onButtons (list "vias" "pins" "clinesegs"))`

`ret =axlGetFindFilter()`

Returns the following:

`("NAMEFORM" "NETS" "CLINESEGS" "VIAS" "PINS"``<plus default items that may change from release to release> )`

`ret = axlGetFindFilter(t)`

Returns:

`("CLINESEGS" "VIAS" "PINS")`

### axlSetFindFilter

`axlSetFindFilter( ?enabled lt_enabled ?onButtons lt_filterOn ) => t/nil`

#### Description

Sets up both the object types to be displayed in the Find Filter, and which types among those are set to on in the Find Filter.

The first argument, `lt_enabled`, is a list of the object types to be displayed in the Find Filter and of the select options described. The second argument, `lt_onButons`, lists the object types whose buttons are to be on (and therefore selectable) when the filter displays. The table lists the keywords that can be included in the enabled and `onButtons` lists for setting up the Find Filter. The diagrams show the keywords and the buttons they cause `axlSetFindFilter` to display.

Each change is additive and processed in the order that they appear in the list. For example, you type the following to enable all object types except for pins.

`'("ALLTYPES" "NOPINS")`

Each of the following keywords may be preceded with a `"NO"` to disable the particular option or object type. For example, `"NOPINS"`. The initial default is `"NOALL"`.

`axlSetFindFilter` Keywords

| Name | Description |
|---|---|
| Keyword | Description |
| `"PINS"` | Enable pins |
| `"VIAS"` | Enable vias |
| `"CLINES"` | Enable clines |
| `"CLINESEGS"` | Enable cline (arc or line) segs |
| `"LINES"` | Enable lines |
| `"LINESEGS"` | Enable line (arc or line) segs |
| `"DRCS"` | Enable drc errors |
| `"TEXT"` | Enable text |
| `"SHAPES"` | Enable shapes, rects and frects |
| `"SHAPESEGS"` | Enable shape segments |
| `"BOUNDARY_SHAPES"` | Enable promotion to boundary shape if auto-shape is selected (see dynamic shape discussion) |
| `"VOIDS"` | Enable shape voids |
| `"VOIDSEGS"` | Enable shape void segments |
| `"SYMBOLS"` | Enable symbol instances |
| `"FIGURES"` | Enable figures |
| `"COMPONENTS"` | Enable component instances |
| `"FUNCTIONS"` | Enable function instances |
| `"NETS"` | Enable nets |
| `"AUTOFORM"` | Option - OBSOLETE |
| `"EQUIVLOGIC"` | Option - For logic object types (nets and components), causes the physical equivalent to be selected. Physical objects must be enabled in both "`enabled`" and "`onButton`" lists. |
| `"INVISIBLE"` | Option - Allows selection of objects that are not visible due to color `class/subclass` form setting. |
| `"NAMEFORM"` | Option - Enables the Find by Name/property fields in the Find Filter form. |
| `"ALLTYPES"` | Enables all object types `("PINS" ... "NETS")`. |
| `"ALL"` | Enables all object types and options. |
| `"DYNTHEMALS"` | Enable selection of thermal reliefs generated by dynamic shapes. Only applicable to `?enabled`. By default, you should not select these if you plan on modifying the objects since the dynamic shape will just re-generate them. You should only access them for read-only purposes. |
| `"GROUPS" "GROUPMEMBERS"` | `"GROUPS"` and `"GROUPMEMBERS"` operate together to produce four possible selection states:
 
 
 State 1: Legacy. This supports code that predates the group implementation. This is the same as State 3.
 
 
 State 2: Group only. By only setting the group bitfield, any selected group is returned to the application as a group.
 
 
 State 3: Members only. By only setting the group_members bitfield, group members are returned to the application when a group is selected.
 
 
 State 4: Hierarchical. By setting both the group and group_members bitfields, a group is returned for any hierarchical group that is selected (such as a Module instance), and group members are returned for all other selected group types. |
| `"AUTOFORM"` | OBSOLETE |
| `"EQUIVLOGIC"` | Option - For logic object types (nets and components), causes the physical equivalent to be selected. Physical objects must be enabled in both "enabled" an "onButton" lists. |
| `"INVISIBLE"` | Option - Allows selection of objects that are not visible due to color class/subclass form setting. |
| `"NAMEFORM"` | Option - enables the find by name/property fields in the find filter form. |
| `"DYNTHEMALS"` | Option - Enable selection of thermal reliefs generated by dynamic shapes. Only applicable to ?enabled. By default, you should not select these if you plan on modifying the objects since the dynamic shape will just re-generate them. You should only access them from read-only purposes.
 If in the partition editor or the design has partitions active then this option is used to selections of read-only objects.
 This option should also be used to select shape base fillets. The system will not allow shape based fillets to be modified it the dynamic fillet option is enabled. |
| `"BONDSMART"` | Option - Application has been updated to differentiate bond wires and/or fingers (APD/SIP). 
 For more information, see Bond Objects. |
| `"ALLTYPES"` | Enable all object types ("PINS" ... "NETS"). |
| `"ALL"` | Enable all object types and options. |

`axlSetFindFilter` processes the keywords in each argument list in order and only makes the changes occurring in the list. Changes are incremental for each call to the function. To remove a selection, attach the string `"NO"` to the front of the keyword. For example, the list `("ALLTYPES" "NOPINS")` enables all object types except pins. The initial default setting of the Find Filter is `"NOALL"`, or, nothing enabled. Use `"NOALL"`, as shown, to clear the Find Filter before enabling particular types.

#### Arguments

| Name | Description |
|---|---|
| `lt_enabled` | List of keyword strings that describe object types that are to be selectable. Enabled object types will appear in the Find Filter form. Object types need the `onButton` set as well to fully enable selection. List may also include selection options.<br><br>Also supports a single keyword string instead of a list of strings. |
| `lt_onButtons` | List of keyword strings that describe object types that are to be enabled for selection. Enabled types will appear with the `onButton` depressed in the Find Filter form. `onButton` settings provide the default for controls which can be modified by the user when the Find Filter form is opened. An object type must be on in both the enabled and the `onButton` lists to be fully enabled for selection. Options are ignored when provided in the `onButton` list.<br><br>Also supports a single keyword string instead of a list of strings. |

Note: `axlSetFindFilter` does not display or select any types that are not enabled. That means that `?onButtons` keywords only effect enabled types. For example, to have all enabled buttons be on, use `?onButtons list("alltypes")`. In general, you need only set specific buttons on if you want those on and others off.

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more Find Filter changes were made. |
| `nil` | No valid keywords were provided. |

### axlAutoOpenFindFilter

`axlAutoOpenFindFilter() => t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Returns `t` always. |

### axlOpenFindFilter

`axlOpenFindFilter() => t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Returns `t` always. |

### axlCloseFindFilter

`axlCloseFindFilter() => t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Returns `t` always. |

### axlDBFindByName

`axlDBFindByName( s_type t_name ) => o_dbid/nil`

#### Description

Finds `dbid` of an object by name without involving the selection set. This means you can run this command any time without affecting what exists in the selection set. The following object lookup types are supported:

| Name | Description |
|---|---|
| type | t_name; return type |
| 'net | net name; `dbid` of a net |
| 'refdes | refdes; `dbid` of a component instance |
| 'padstack | padstack name; `dbid`of a padstack |

This is restricted to a single object. To find objects using wildcards, use `axlSelectByName`.

#### Arguments

| Name | Description |
|---|---|
| `s_type` | Type symbol; see above. |
| `t_name` | Object's name (this is case insensitive). |

#### Value Returns

| Name | Description |
|---|---|
| `o_dbid` | `dbid` of object or `nil.` |

#### Examples

`db = axlDBFindByName('net "GND")`

`db = axlDBFindByName('padstack "VIA")`

`db = axlDBFindByName('refdes "U1")`

#### See Also

axlSelectByName

### axlFindFilterIsOpen

`axlFindFilterIsOpen() => t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Returns `t` always. |

### axlSelectByName

`axlSelectByName ( t_objectType t_name/lt_name [g_wildcard] ) => lo_dbid/nil`

#### Description

Selects database objects by name.

Interface allows more than one name to be passed, but only one object type per call. For certain object types, a single name may return multiple objects. The supported object types and related items follow:

| Name | Description |
|---|---|
| Object Type | Item the function finds |
| `"NET"` | net name |
| `"COMPONENT"` | component name |
| `"FUNCTION"` | function name |
| `"DEVTYPE"` | device type name |
| `"SYMTYPE"` | symbol type name |
| `"PIN"` | refdes.pinname |
| `"REFDES"` | find symbol by refdes name |
| `"COMPREFDES"` | find component by refdes name |
| `"GROUP"` | find group by name |
| `"BUS"` | find bus by name |
| `"DIFF_PAIR"` | find differential pair by name |
| `"NETCLASS"` | find netclass by name |
| `"NET_GROUP"` | find a net group by name |
| `"REGION"` | find region by name |
| `"XNET"` | find xnet by name; Will return a Net if xnet is a single net xnet. See `<cdsroot>/share/pcb/examples/skill/select/ashfindxnet.il` |
| `"MATCH_GROUP"` | find matchgroup by name |
| `"MODULE"` | find module by name |

You can use wildcards with this function:

- `"*"` matches any sequence of zero or more characters.

- `"?"` matches any single character.

- `"\"` is used to send a special character, for example, `\x`.

Provided third argument `[g_wildcard]` is set to `TRUE`.

Note: This saves and restores the current find filter settings, but resets the selection set.

#### Arguments

| Name | Description |
|---|---|
| `t_objectType` | Type of database name. |
| `t_name` | Object to find. |
| `lt_name` | List of names to find. |
| `[g_wildcard]` | If `*` or `?` appear in name, use regular expression matching |

#### Value Returns

| Name | Description |
|---|---|
| `t` | List of objects found. |
| `nil` | No matching name or illegal `objectType` name. |

### axlSelectByProperty

`axlSelectByProperty( t_objectType t_property [t_value] [g_regularExpression] ) => lo_dbid/nil`

#### Description

Selects the `dbid` set of a particular Allegro PCB Editor database object with the indicated property.

Property can be a name or a name/value pair. Value may contain a regular expression (`*` or `?`), since certain select by name functions support wildcards. You can test for the presence of wildcards before you call this function.

Regular expressions used by Allegro PCB Editor differ from the Skill regular expressions. Allegro PCB Editor handles regular expressions such that they are more compatible with the character set allowed in Allegro PCB Editor object names. Do not use this function to test patterns sent to the Skill `regexp` family of functions.

For value, match the database formats into the value string to contain the units preference if applicable for the property. If the data type of the attribute is BOOLEAN, and if it exists on the element, the string is empty. If the data type is `INTEGER` or `REAL`, the user units string, if any, is appended to the value. If the data type is one of the `"units category"` types, for example, `ALTITUDE`, `PROP_DELAY`, the MKS package converts the value.

Properties must be upper case. The value is case insensitive if wildmatch match is `nil` while case sensitive for wildcard matching.

Note: Property names may change from release to release, or may be rendered obsolete. SKILL programs using property names may require modifications in future releases.

#### Arguments

| Name | Description |
|---|---|
| `t_objectType` | String for Allegro PCB Editor database object type. Must be: `compdef`, `component`, `drc`, `net`, `symdef`, `symbol`, or `group`. |
| `t_property` | Name of property. |
| `t_value` | Optional property value. |
| `g_regularExpression` | `t`if property value is to be treated as a regular expression, or `nil`, which is the default, to treat property value as a simple match. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more `dbids` added to the select set. |
| `nil` | No `dbids` added to the select set. |

### axlSnapToObject

`axlSnapToObject( g_mode xy ) => xy/nil`

#### Description

Supports snapping to a logic object's connect point. A logic object is a:

- Cline

- Clines segments (lines or arcs)

- Via

- Pin

For cline objects, the two end points are considered the connect points. For pad objects, the connect point is defined in the padstack. Snapping is based upon the trap size, which varies based upon the zoom factor (see `axlGetTrapBox`). The smaller the trap size, the higher the zoom. If no object is found within the original xy location is returned.

Note: Avoid using the grid snapping option with `axlEnterPoint` as it might move the user pick outside the trap size.

#### Arguments

| Name | Description |
|---|---|
| `g_mode` | `nil`: Use active sel set to determine snapping.<br><br>`t`: Snap based upon the visible layers in the database. |
| `xy` | Location in design units to snap (list of design units x:y). |

#### Value Returns

| Name | Description |
|---|---|
| `xy` | Object snapped point (list of design units x:y). |
| `nil` | If not object exists for snapping returns nil. |

Also nil if arguments are incorrect

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

#### See Also

axlGetSelSet`,`axlGetTrapBox`,`axlGetLastEnterPoint

### axlLastPickIsSnapped

`axlLastPickIsSnapped() => t/nil`

#### Description

Normally called after an `axlEnter` call to determine if the pick was snapped or unsnapped.

#### Arguments

none

#### Value Returns

`t` if last picked was snapped, `nil` if unsnapped

#### Examples

`snappedPoint = axlEnterPoint(?prompts list("Pick origin point") ?gridSnap t) state = axlLastPickIsSnapped()`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

