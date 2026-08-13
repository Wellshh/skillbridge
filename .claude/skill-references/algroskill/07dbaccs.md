### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

6
=

Database Read Functions
=======================

AXL-SKILL Database Read Functions
---------------------------------

The chapter describes the AXL-SKILL functions that read the Allegro PCB Editor database.

### axlAltSymbolList

`axlAltSymbolList(t_name/o_dbidg_layer) lt_symbols/nil`

#### Description

This queries the provided object and returns a list of alternative symbol names.

#### Arguments

|  |
| --- | ---
| `t_name` | Component definition or a refdesname
| `o_dbid` | a symbol instance, component instance or compdef dbid
| `g_layer` | `top, 'bottom, or'internal
#### Value Returns

|  |
| --- | ---
|  | list of alternate symbols for the layer provided
|  | nil, in case of error or if the symbol does not have a alternate symbol set
#### Examples

> `strings = axlAltSymbolList("U1" top)`

#### See Also

[axlAltSymbolReplace](#739374 "6"), [axlAltSymbolOK](#739294 "6"), ALT\_SYMBOL property

### axlAltSymbolOK

`axlAltSymbolOK(t_name/o_dbidg_layert_symbol) => t/nil`

#### Description

This verifies that symbol is legal for component. Must be in the ALT\_SYMBOL list with the correct layer.

#### Arguments

|  |
| --- | ---
| `t_name` | may be compdef or a refdes name
| `o_dbid` | a symbol instance, component instance or compdef dbid
| `g_layer` | `top, 'bottom, or'internal
| `t_symbol` | name of symbol
#### Value Returns

|  |
| --- | ---
| `t` | is legal
| `nil` | error or symbol is not legal for component
#### Examples

> `result = axlAltSymbolOK("R1" 'top "res400")`

#### See Also

[axlAltSymbolList](#739212 "6")

### axlAltSymbolReplace

`axlAltSymbolOK(t_name/o_dbidt_symbol) => t/nil`

#### Description

This replaces a PLACED component with one of its allowed replacements (ALT\_SYMBOL). To be successful the following must be true

* symbol must already be placed

* provided symbol must be a legal alternative for the layer where the symbol is placed

* the replacement symbol, any of its padstacks and any shape or flash symbols referenced by the padstacks must be found and loaded into the design which this API will attempt to do.

**Note:** Text properties on the symbol instance, and attached text re-positioning are preserved.

#### Arguments

|  |
| --- | ---
| `t_name` | may be compdef or a refdes name
| `o_dbid` | a symbol instance, component instance or compdef dbid
| `t_symbol` | name of replacement symbol
#### Value Returns

|  |
| --- | ---
| `t` | replacement done
| `nil` | error or cannot replace
#### Examples

> `result = axlAltSymbolReplace("R1" "res400")`

#### See Also

[axlAltSymbolList](#739212 "6")

### axlBackdrillGet

`axlBackdrillGet(o_dbidPinOrVia) => lt_backdrillData/nil`

`axlBackdrillGet(status') => g_status`

#### Description

In one mode, when a pin or a via is provided, the command returns the backdrilling result on that pin or via.

In other mode, it returns status of design's backdrilling.

**Note:** Symbols do not support backdrilling.

#### Arguments

|  |
| --- | ---
| `o_dbidPinOrVia` | query for backdrill on pin or via
| `status'` | status of backdrill on design
#### Value Returns

|  |
| --- | ---
| `nil` | error or pin/via is not backdrilled
| `lt_backdrillData` | A disembodied property list having (all non strings are in user units):
|  |  |
| --- | --- | ---
|  | `holeSize` | finished hole size
|  | `backdrillSize` | backdrill hole size
|  | `electricalStub` | max electrical stub (from the`BACKDRILL_MAX_PTH_STUB` property on net)
|  | `mfgStub` | manufacturing stub from backdrill parameter dialog
|  | If pin or via is backdrilled from top, topStartLayer is non-nil and the following attributes are set: |
|  | `topStartLayer` | start layer of drill (string)
|  | `topMustCutLayer` | must cut layer (string)
|  | `topMustNotCutLayer` | must NOT cut layer (string)
|  | `topDrillDepth` | depth of backdrill from topStartLayer to immediatelybefore topMustNotCutLayer
|  | `topRemainingStub` | remaining stub after backdrill. This is fromtopRemainingStub to first layer with a connection(min value is manufacturing stub length)
|  | if pin/via is backdrilled from bottom, botStartLayer is non-nil and the following attributes are set. |
|  | `botStartLayer` | start layer of drill (string)
|  | `botMustCutLayer` | must cut layer (string)
|  | `botMustNotCutLayer` | must NOT cut layer (string)
|  | `botDrillDepth` | depth of backdrill from botStartLayer to immediatelybefore botMustNotCutLayer
|  | `botRemainingStub` | remaining stub after backdrill. This is frombotRemainingStub to first layer with a connection(min value is manufacturing stub length)
|  |
| --- | ---
| `g_status` | returns status about design's backdrill
| `nil` | error
| `'notStarted` | backdrill not performed on design
| `'t` | backdrill done and is up to date
| `'odd` | backdrill done but changes make it out-of-date
#### Examples

* Get status

> `axlViaZLength('status)`

* Get info on a pin or via

> ```
> ; ashOne is a selection utility found at;   <cdsroot>/pcb/examples/skill/ash-fxf/ashone.il; select a pin or via
> ```

> `pinvia = ashOne(("PINS""VIAS"))'backdrill = axlBackdrillGet(pinvia)`

#### See Also

axlViaZLength

### axlDBGetDesign

`axlDBGetDesign()⇒ o_design/nil`

#### Description

Returns the root design`dbid`. Use this `dbid` to get the design properties and to add properties to the design.

**Note:** You cannot edit the root design object. AXL-SKILL edit commands ignore this`dbid`.

This also allows access to lists of many types of dbid in the design, such as nets, components, and so on.

* If you need to access all dbids if the same type (all nets or all components), it is more efficient to use the appropriate attribute of this dbid than to use the Selection APIs to query all elements.

To flatten attributes in lists, use the "~>" reference. For example, to get names of all nets in the design do:

`netNames = axlDBGetDesign()->nets~>name`

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `o_design` | Root design`dbid`.
| `nil` | Error occurred.
#### Example

> > ```
> > mydesign = axlDBGetDesign()axlDBAddProp( mydesign, list("board_thickness", 0.350))
> > ```

Gets the root design and sets the`BOARD_THICKNESS` property to `0.350` inches.

To verify the property has the value specified:

* From the Allegro PCB Editor menu, select *Display - Element*.

* From the Find Filter, select*Drawing Select*.

> The**Show** window appears, listing the current properties attached to the design.

### axlDBGetDrillPlating

`axlDBGetDrillPlatingt_padstackname)⇒ "PLATED"/"NON PLATED"/nil`

#### Description

Retrieves the plating type of the padstack passed as an argument to this function.

#### Arguments

|  |
| --- | ---
| `t_padstackname` | Name of padstack.
#### Value Returned

|  |
| --- | ---
| `"Plated" or "Nonplated"` | Drillplating name.
| `nil` | Incorrect padstack name, or other error occurred.
### axlIsDBIDType

`axlIsDBIDType(g_dbid)⇒ t/nil`

#### Description

Determines if`g_dbid` is an Allegro PCB Editor database `dbid`. Returns `t` if so and `nil` otherwise.

#### Arguments

|  |
| --- | ---
| `g_dbid` | Variable to be checked whether a`dbid` or not.
#### Value Returned

|  |
| --- | ---
| `t` | `g_dbid` is a true Allegro PCB Editor `dbid`.
| `nil` | `g_dbid` is not a true Allegro PCB Editor `dbid`.
#### Example

Defines a function based on`axlIsDBIDType` to tell whether a symbol is an Allegro PCB Editor `dbid` or not. Then creates an `r_path` (which is not an Allegro PCB Editor `dbid`, because *paths* are only temporary building structures) and uses the `r_path` to create an Allegro PCB Editor line (which is an Allegro PCB Editor `dbid`). Shows whether each is a true `dbid`.

> ```
> defun( isItDBID (testDBID)    "Print whether testDBID is a true Allegro dbid"    if( axlIsDBIDType( testDBID)     then        println( "This is an Allegro DBID.")    else        println( "This is NOT an Allegro DBID.") ) )mypath = axlPathStart( list(100:500))axlPathLine( mypath, 0.0, 200:250)myline = axlDBCreatePath( mypath, "etch/top" nil)isItDBID(mypath)isItDBID(caar(myline))
> ```

The function prints the following:

> `"This is NOT an Allegro DBID.""This is an Allegro DBID."`

### axlDBGetAttachedText

`axlDBGetAttachedText(o_dbid)⇒ l_dbid/nil`

#### Description

Returns the list of`dbids` of text objects attached to the object whose `dbid` is `o_dbid`. If [axlDBGetDesign](#700317 "6") is used to retrieve the dbid, the function returns all text attached to root design.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of object from which attached text `dbids` are retrieved.
#### Value Returned

|  |
| --- | ---
| `l_dbid` | List of the text objects attached to`o_dbid`.
| `nil` | No attached text objects.
#### Example

> ```
> (defun showText ()    "Print text of selected objects"    mypopup = axlUIPopupDefine( nil        (list (list "Done" 'axlFinishEnterFun)        (list "Cancel" 'axlCancelEnterFun)))axlUIPopupSet( mypopup)axlSetFindFilter( ?enabled list("noall")    ?onButtons "noall")axlSetFindFilter( ?enabled list("symbols")    ?onButtons "symbols")axlOpenFindFilter()(while (axlSelect)    progn(    alltext =        axlDBGetAttachedText(car(axlGetSelSet()))        foreach(thistext alltext            printf( "Text on this symbol is : '%s'\n",            thistext->text))))axlCloseFindFilter())
> ```

Lets the user pick a symbol, then prints the text attributes of each text object attached to that symbol.

Run`showText()` and pick a symbol of device type `"74F74",` assigned as `refdes` `"T23".` The function prints the following:

> `Text on this symbol is : 'T23'Text on this symbol is : '74F74'`

### axlDBGetPad

`axlDBGetPad(o_dbidt_layert_type)⇒ o_pad/nil`

#### Description

For the pin or via specified by`o_dbid`, gets the pad of type `t_type` associated with layer `t_layer`.

**Note:** smd pads do not have a default internal layer.
 To obtain the adjacent layer keepout pad:`axlDBGetPad(dbid 'adjacent "KEEPOUT")`

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of the pin, via, or a padstack definition.
| `t_layer` | String or symbol of a layer desired.  Format for regular layers:
|
* Coverlay pads specify by`"COVERLAY_TOP"` or `"COVERLAY_BOTTOM"`
* `"ETCH/TOP"`
* `"TOP"`
* Mask layers must use class of pin or via class:
* `"PIN/SOLDERMASK_TOP"`
* `'backdrillSoldermask` - soldermask pad to substitute for drill start layer
* `'internal` - default internal layer (not present on SMD padstacks)
* `'composite` - sum of all the layers (worse case) this option ignores the t\_type argument
* `'adjacent` - adjacent layer keepout option
* `'backdrillStart`
* type="REGULAR" - larger pad for drill start layer (positive)
* type="ANTI" - larger pad for drill start layer (negative layers)
* `'backdrillClearance`
* type="ANTI" - pad size for internal backdrill layers for negative layers
* type="KEEPOUT" - generate a KEEPOUT for positive layers for backdrill layers.
* Type of pad to retrieve:`"REGULAR",` `"ANTI",` `"THERMAL"`, or `"KEEPOUT".`

#### Value Returned

|  |
| --- | ---
| `o_pad` | `dbid` of the pad of the type associated with `o_dbid` on the layer specified.
| `nil` | Cannot get the pad`dbid`.
#### Example

* Lets the user pick any pin or via and shows the figureName attribute of the selected pad.

```
(defun showPad () mypopup = axlUIPopupDefine( nil (list (list "Done" 'axlFinishEnterFun)                                 (list "Cancel" 'axlCancelEnterFun)))
```

> `axlUIPopupSet( mypopup)`

> ```
> axlSetFindFilter( ?enabled list("noall") ?onButtons "noall")                 axlSetFindFilter( ?enabled list("pins" "vias")?onButtons list("pins" "vias"))
> ```

> `(while axlSelect()`

> `progn(mypad = axlDBGetPad(car(axlGetSelSet()) "etch/top" "regular")`

> `printf( "Pad figure type : %s\n", mypad->figureName)))`

> To fetch default internal regular pad:

> `r = axlDBGetPad(car(axlGetSelSet() 'internal "REGULAR")`

> Run showPad() and pick a pin with a square pad on "etch/top", then a circular pad. The function prints the following:

> `Pad figure type : SQUARE`

> `Pad figure type : CIRCLE`

### axlDBGetPropDict

axlDBGetPropDict - return list of current define property dictionary entries

`axlDBGetPropDict(S_filter/nil) -> lt_propNames`

#### Description

Returns a list of property definitions in the current design. Several trivial filters are defined:

* `nil` - visible Allegro and user-defined properties

* `allegro` - visible Allegro properties. Product tiering results in filtering of these properties.

* `user` - visible user-defined properties.

* `invisible` - Invisible Allegro properties, these are application internal properties.

#### Arguments

|  |
| --- | ---
| `S_filter` | Symbol or string requesting a list of property types
#### Value Returned

|  |
| --- | ---
| `lt_propNames` | List of names (unsorted) or`nil`
**Examples**

`axlDBGetPropDict('user) -> list of names`

**See Also**

[axlDBGetPropDictEntry](#735236 "6")

### axlDBGetPropDictEntry

`axlDBGetPropDictEntry(t_name)⇒ o_propDictEntry/nil`

`axlDBGetPropDictEntry(nil)==> lt_validObjects`

#### Description

Gets the property dictionary entry for the property name given by the string`t_name`. Use [axlDBGetPropDictEntry](#735236 "6") to get the information about a property dictionary entry. If name is `nil`, the command returns a list of legal objects that can be used to create property dictionary entries. This is the `objects` attribute of the `o_propDictEntry` data type. You cannot create a property with the same name as an existing Allegro property.

#### Arguments

|  |
| --- | ---
| `t_name` | String specifying the name of the property whose dictionary entry is to be retrieved.
#### Value Returned

|  |
| --- | ---
| `o_propDictEntry` | `dbid` of the property dictionary entry for the property whose name is given by `t_name`. If could not get the entry, it returns nil.
| *lt\_validObjects* | List of valid objects to associate with a property
| `nil` | Could not get the entry.
#### See Also

[axlDBAddProp](03dbcre8.html#367701 "15")

#### Example

The following example gets the`"SIGNAL MODEL"` property, and dumps its attributes.

> `myprop = axlDBGetPropDictEntry("SIGNAL_MODEL")`

> `myprop->??`

> > ```
> > (write nil useCount 0 units nil     range nil objType "PropDict"     name "SIGNAL_MODEL"     dataType "STRING"     readOnly t)
> > ```

### axlDBGetProperties

`axlDBGetProperties(o_dbid[lt_type])⇒ l_result/nil`

#### Description

Gets the properties attached to a specified object. Returns the properties in an assoc list, that is, a list of lists, each of which contains a name and a value. The SKILL`assoc` function can operate using this list.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of the object from which to get the properties.
| `lt_type` | List of strings qualifying the types of properties to be retrieved from`o_dbid`. `"user"` means retrieve user-defined properties only. `"allegro"` means retrieve Allegro PCB Editor defined properties only. `nil` means retrieve both user and Allegro PCB Editor.
#### Value Returned

|  |
| --- | ---
| `l_result` | List of name-value pairs. For each name-value pair:  (`car`) is the property name  (`cadr`) is the property value, including units.
| `nil` | No properties found.
#### Example

The following example selects the component with refdes "U1," gets its properties using the axlDBGetProperties command, and prints the associated property list it returns. The properties are:

* ROOM with value D

* DFA\_DEV\_CLASS with value DIP

* LEAD\_DIAMETER with value 23 mil.

> `axlClearSelSet()`

> `axlSetFindFilter(?enabled '("noall" "alltypes") ?onButtons "alltypes")`

> `axlSingleSelectName("component" "U1")`

> `myprops = axlDBGetProperties(car(axlGetSelSet()) '("user" "allegro"))`

> `print myprops`

> `==> ((ROOM "D")`

> `(DFA_DEV_CLASS "DIP")`

> `(LEAD_DIAMETER "23 MIL"))`

### axlDBGetDesignUnits

`axlDBGetDesignUnits()⇒ l_value/nil`

#### Description

Returns the design units and accuracy number of the active design.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `l_value` | List containing the design units as a string and the accuracy number as an integer.
| `nil` | Failed to return the design units and accuracy number of the active design.
#### Example

`(axlDBGetDesignUnits)⇒("millimeters" 3)`

The design**Drawing Parameters** form shows *User Units* as `Millimeter` and *Accuracy* as `3`.

### axlDBRefreshId

`axlDBRefreshId(o_dbid/nil)⇒ o_dbid/nil`

#### Description

Updates the attributes of the object specified by`o_dbid`. Subsequent attribute retrieval requests access the updated information.

* This does NOT update the Allegro database. It updates the cached dbid view of objects in Skill.

**Note:** Because of performance considerations, refreshes only the object itself. If the object being refreshed has`dbids` in any of its attributes, those `dbids` are not refreshed. For example, a net branch has *children*, a list of paths, tees, vias, pins, and shapes. If another path is added to that list of paths due to connectivity change, `axlDBRefreshId` of the branch does not update the *children*. If you move a via that is a child of the branch, then doing `axlDBRefreshId` of the branch and accessing the via as child of branch may yield incorrect attributes of that child (via in this case).

#### Arguments

|  |
| --- | ---
| `o_dbid` | SKILL list of`dbids` of the objects whose attributes are to be refreshed.
| `nil` | All ids are refreshed.
**Note:** Refreshing all ids may cause performance problems if done indiscriminately.

#### Value Returned

|  |
| --- | ---
| `o_dbid` | Refreshed`dbid`.
| `nil` | Could not refresh.
#### Example

> ```
> axlSetFindFilter( ?enabled    '("noall" "alltypes"))axlSingleSelectName("net" "sclkl")mynet = car(axlGetSelSet())mybranch = car(mynet->branches)mychildren = mybranch->childrenforeach( thismember mychildren        if( (thismember->objType == "via")         then            axlDeleteObject(thismember)))axlDBRefreshId(mybranch)⇒ t
> ```

Finds`net` `"sclkl",` walks all members of its first branch, deleting any vias. Then refreshes the branch.

If the refresh was not done,`mybranch` would still report having vias following the operation that deleted its vias.

### axlDBGetLonelyBranches

`axlDBGetLonelyBranches()⇒ l_dbid/nil`

#### Description

Returns a list of the*standalone branch* `dbids` in the design. A *standalone branch* is a branch not associated with any net.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `l_dbid` | List of standalone branches.
| `nil` | No standalone branches found.
#### Example

> ```
> (axlDBGetLonelyBranches)⇒(dbid:12051156 dbid:11994768 dbid:12002292 dbid:12000892 dbid:11999396dbid:11996652 dbid:11996048 dbid:11994476 dbid:11992964 dbid:11991564dbid:11989672 dbid:11989344 dbid:12072172 dbid:11895392 dbid:11892048dbid:11888704 dbid:11888744 dbid:11888804 dbid:11888844 dbid:11888884dbid:12074948 dbid:11888984 dbid:11889064 dbid:11889204 dbid:11889224dbid:11889856 dbid:11890036 dbid:11890056 dbid:11890236 dbid:11890256dbid:11886180 dbid:12011360 dbid:11886760 dbid:11887140 dbid:11887916 )
> ```

Gets list of standalone branch`dbids`.

### axlDBGetConnect

`axlDBGetConnect(o_dbid[t_full])⇒ l_result/nil`

#### Description

Finds all the elements, including pads and shapes, that are connected to a given`dbid`. Input can be a PIN, VIA, T, CLINE/CARC or CLINE/CARC SEGMENT, and shapes.

If the second argument is`nil` or is not present:

* For pins, vias or Ts, the function returns a list of connected clines.

* For path (clines) or line/arc (segments) returns list of objects connected to either end.

* For shapes same as t\_full=t

If the second argument is set to`t`,:

* For pins, vias and T, the command returns full connectivity which includes clines, shapes, pins, vias or T's.

* For path (clines) or line/arc (segments) return value is same as`t_full=nil`

* For shapes list of connected objects which may be clines, shapes, pins, vias or T's.

**Note:** You should set`t_fill` to `t`. The `nil` option operates in its mode due to legacy considerations and is used by Allegro Package Designer applications.

If a segment is passed as an argument, the command does not report inter-path connectivity. Thus only the first and last segment of a path report any connectivity. Internal segments of a path always return nil. This is because the Allegro database connectivity model guarantees that internal segments are always connected to their adjacent segments. The list of segments reported in a path (cline) dbid is how the individual segments are connected.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A`dbid`, path(cline), line/arc (segment), shape, pin, via or T.
| `t_full` | `t`: For full connectivity of pins, vias, or Ts.  `nil`: Returns connectivity including any connected SHAPES. Also supports segments.
#### Value Returned

|  |
| --- | ---
| `l_result` | List of`dbids` connected to `o_dbid`.  ``` If o_dbid is a CLINE or SEGMENT, thenl_result = (list list1 list2)where list1 = nil or elements connected to the first end list2 = nil or elements connected to the second end. ```  For all other objects, returns a list of connections.
| `nil` | Nothing connected to`o_dbid`.
### axlDBIsFixed

```
axlDBIsFixed(o_dbid[g_showMessage])⇒ nil or [dbid of 1st element that makes the item fixed]
```

#### Description

Verifies whether or not the specified database object is fixed. When the FIXED property is present if can either be directly on the object, on a parent (e.g. a CLINE is fixed if the NET is fixed) or on a child (e.g. a symbol is fixed if its place bounds is fixed).

An object can be fixed by the following:

* Object has the`FIXED` property or its parent or child objects have the `FIXED` property. For example, group symbol

* The object (parent or child) has a private database fixed attribute

* Object is Read-only (typically due to partition enabled)

* Object is a symbol with test points and the`FIXED` test point flag is set.

* Object is a symbol and has one or more children with the`FIXED` property.

Returns the first item found that causes the element to be fixed (could be more then one).

**Note:** Using[axlDBCloak](17dbtran.html#1065349 "18") with its `'ignoreFixed` option is recommended.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of the element to check.
| `g_showMessage` | Use`t` to have Allegro PCB Editor display the message if the item is fixed or `nil` to have no message display.
#### Value Returned

|  |
| --- | ---
| `dbid` | `dbid` of the element causing the object to be fixed.
| `nil` | Object not fixed.
#### Example

> `p = axlSelectByname("SYMBOL" "U1")`

> `ret = axlDBIsFixed(p)`

#### See Also

[axlDBIgnoreFixed](14dsnctl.html#715890 "14"), axlDBIsReadOnly, [axlDBCloak](17dbtran.html#1065349 "18")

### axlDBIsPackagePin

`axlDBIsPackagePin(rd_dbid)⇒ t/nil`

#### Description

Verifies whether or not the given element is a*package pin*.

A*package pin* is a pin with a component class of `IO`.

#### Arguments

|  |
| --- | ---
| `rd_dbid` | `dbid` of element to check.
#### Value Returned

|  |
| --- | ---
| `t` | `rd_dbid` is a package pin.
| `nil` | `rd_dbid` is not a package pin.
### axlGetModuleInstanceDefinition

`axlGetModuleInstanceDefinition(o_modinst)⇒ t_moddef/nil`

#### Description

AXL interface to the C function that returns the name of the module definition used to create the module instance.

#### Arguments

|  |
| --- | ---
| `o_modinst` | AXL`dbid` of the module instance (the `dbid` returned by `axlDBCreateModuleInstance`.)
#### Value Returned

|  |
| --- | ---
| `t_moddef` | String containing the name of the module definition.
| `nil` | Could not access the information.
#### Example

> `axlSetFindFilter(?enabled '("noall" "groups") ?onButtons '("noall" "groups" ))`

> `axlSingleSelectName("GROUP" "inst")`

> `modinst = car(axlGetSelSet())`

> `axlGetModuleInstanceDefinition(modinst)`

> `= "mod"`

Gets the definition of a module instance named`inst`.

### axlGetModuleInstanceLocation

`axlGetModuleInstanceLocation(o_modinst)⇒ l_loc/nil`

#### Description

AXL interface to the C function that gets the current location of the module instance in the design.

#### Arguments

|  |
| --- | ---
| `o_modinst` | AXL`dbid` of the module instance (the `dbid` returned by `axlDBCreateModuleInstance`.)
#### Value Returned

* [g\_mirror]: Is a n optional parameter, which is set to `t` when mirrored
* l\_origin:origin of module
* x\_rotation:rotation in degress \* 1000

#### Example

> `axlSetFindFilter(?enabled '("noall" "groups") ?onButtons '("noall" "groups" ))`

> `axlSingleSelectName("GROUP" "inst")`

> `modinst = car(axlGetSelSet())`

> `axlGetModuleInstanceLocation(modinst)`

> `--> ((500 1500) 0)`

Gets the location of a module instance named`inst`.

### axlGetModuleInstanceLogicMethod

`axlGetModuleInstanceMethod(o_modinst)⇒ i_logic/nil`

#### Description

AXL interface to the C function that determines the logic method used by the module instance.

#### Arguments

|  |
| --- | ---
| `o_modinst` | AXL`dbid` of the module instance (the `dbid` returned by `axlDBCreateModuleInstance`.)
#### Value Returned

|  |
| --- | ---
| `i_logic` | Value of the logic method flag for the module instance. Legal values are:  `0` - no logic  `1` - logic from schematic  `2` - logic from module definition
| `nil` | Could not access the information.
#### Example

> `axlSetFindFilter(?enabled '("noall" "groups") ?onButtons '("noall" "groups" ))`

> `axlSingleSelectName("GROUP" "inst")`

> `modinst = car(axlGetSelSet())`

> `axlGetModuleInstanceLogicMethod(modinst)`

> `= 2`

Gets the logic method of a module instance named`inst`.

### axlGetModuleInstanceNetExceptions

`axlGetModuleInstanceNetExceptions(o_modinst)⇒ l_nets/nil`

#### Description

AXL interface to the C function that gets the net exception of the module instance in the design.

#### Arguments

|  |
| --- | ---
| `o_modinst` | AXL`dbid` of the module instance (the `dbid` returned by `axlDBCreateModuleInstance`.)
#### Value Returned

|  |
| --- | ---
| `l_nets` | List of names of the nets that are treated as exceptions in the module instance.
| `nil` | Could not access the information.
#### Example

> `axlSetFindFilter(?enabled '("noall" "groups") ?onButtons '("noall" "groups" ))`

> `axlSingleSelectName("GROUP" "inst")`

> `modinst = car(axlGetSelSet())`

> `axlGetModuleInstanceNetExceptions(modinst)`

> `= ("GND" "+5")`

Gets the list of net exceptions of a module instance named`inst`.

### axlIsDummyNet

`axlIsDummyNet(net_dbid)⇒ t/nil`

#### Description

Determines if a given net is a Dummy net. Name of net is an empty string ("").

#### Arguments

|  |
| --- | ---
| `net_dbid` | Net database object.
#### Value Returned

|  |
| --- | ---
| `t` | `net_dbid` is a Dummy Net.
| `nil` | `net_dbid` is not a Dummy Net.
#### See Also

[axlIsPinUnused](#719636 "6")

### axlIsLayerNegative

`axlIsLayerNegative(t_layerName)⇒ t/nil`

#### Description

Determines whether or not the given plane layer is negative.

#### Arguments

|  |
| --- | ---
| `t_layerName` | Name of the conductor layer to check.
#### Value Returned

|  |
| --- | ---
| `t` | Active layer is negative.
| `nil` | Active layer is not negative or is not an`ETCH` layer.
#### See Also

[axlXSectionGet](04parmgt.html#1169585 "3")

#### Examples

Tests if layer named GND is negative

`axlIsLayerNegative("GND")`

### axlIsPinUnused

`axlIsPinUnused(pin_dbid)⇒ t/nil`

#### Description

Determines if the given pin is unused, indicating that it is on a dummy net.

#### Arguments

|  |
| --- | ---
| `pin_dbid` | Pin database object.
#### Value Returned

|  |
| --- | ---
| `t` | Pin is unused.
| `nil` | Pin is used.
#### See Also

[axlIsDummyNet](#719568 "6")

### axlIsitFill

`axlIsitFill(t_layer)⇒ t/nil`

#### Description

Determines if fill shape is allowed for a given class subclass.

#### Arguments

|  |
| --- | ---
| `t_layer` | Layer name, for example,`ETCH/TOP`.
#### Value Returned

|  |
| --- | ---
| `t` | Fill shape is allowed.
| `nil` | Fill shape is not allowed.
### axlOK2Void

`axlOK2Void(t_layer)⇒ t/nil`

#### Description

Determines if voids are allowed for a given`class/subclass`. Determines if a layer supports voids for shapes.

#### Arguments

|  |
| --- | ---
| `t_layer` | Layer name, for example,`ETCH/TOP`.  or  just class name ("ETCH")
#### Value Returned

|  |
| --- | ---
| `t` | Voids are allowed.
| `nil` | Voids are not allowed.
#### Example

`axlOK2Void("ETH/TOP")`

### axlDBDynamicShapes

`axlDBDynamicShapes(g_value)⇒ x_count`

#### Description

Queries and updates dynamic shapes. When`g_value` is `t,` updates all out of date dynamic shapes on the board regardless of the dynamic shape updating setting in the **Drawing Options** dialog. When `g_value` is `nil`, returns a count of out of date shapes.

#### Arguments

|  |
| --- | ---
| `g_value` | `t` = update dynamic shapes  `nil` = return count of out of date shapes
#### Value Returned

|  |
| --- | ---
| `x_count` | Count of out of date shapes. If updating shapes,`x_count` is the number of out of date shapes before the update.
### axlDBGetShapes

`axlDBGetShapes(t_layer)⇒ l_dbid/nil`

#### Description

Provides quick access to shapes without access to visibility or find settings.

#### Arguments

|  |
| --- | ---
| `t_layer` | Layer name  `nil` = all layers  <`class`> = all subclasses of the class  <`class`>/<`subclass`> = specified layer
#### Value Returned

|  |
| --- | ---
| `l_dbid` | List of shapes.
| `nil` | Incorrect argument.
#### Examples:

* Returns all shapes on the design.

`axlDBGetShapes(nil)`

* Returns all shapes on the BOUNDARY layer.

`axlDBGetShapes("BOUNDARY")`

* Returns all shapes on ETCH GND.

`axlDBGetShapes("ETCH/GND")`

* Returns all shapes on ROUTE KEEPOUT.

`axlDBGetShapes("ROUTE KEEPOUT")`

### axlDBTextBlockCompact

`axlDBTextBlockCompact(t/nil)⇒ x_unusedBlocks`

#### Description

Reports and/or compresses unused database text blocks. If compacting text blocks, it always updates database text to reflect the new text block numbers.

The database, even if new, must have at least one text block.

**Note:** You must force a`dbid` refresh on any text parameters and text type `dbids` in order for them to reflect the new numbering.

#### Arguments

|  |
| --- | ---
| `t` | Compact the text blocks.
| `nil` | Report the number of text blocks that can be eliminated from the database.
#### Value Returned

|  |
| --- | ---
| `x_unusedBlocks` | Count of text blocks that are unused.
#### Example

`unused = axlDBTextBlockCompact(nil)`

`printf("This database has %d unused text blocks\n" unused)`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
