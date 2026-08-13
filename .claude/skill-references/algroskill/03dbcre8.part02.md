<!--
source: algroskill/03dbcre8.md
part: 2/2
estimated_tokens: 4940
-->

**Note:** Do not use this function in the symbol editor.

* ***This function is intended for programmers with a high level of knowledge of the Allegro PCB Editor database model. It provides a powerful method for creating symbols within Allegro PCB Editor. Although you can use this command to create non-conventional symbols, the rest of Allegro PCB Editor may not behave as you expect. To ensure a symbol behaves as a conventional symbol, you must ensure that what you create abides by symbol rules. For example, you can create a symbol with no attached graphics. Allegro PCB Editor's Find utility will not be able to find it. Another programmer may use this feature to create a temporary symbol instance as a placeholder.

  Through interaction, the user changes this symbol into a conventional Allegro PCB Editor symbol.***

#### Arguments

The first argument may be either`t_refdes` or `l_symbolData`, as described here:

|  |
| --- | ---
| `t_refdes` | If this is the first argument, the function looks for a component in the layout with that refdes, finds the package symbol required for its component device type, adds a package symbol with the symbol name prescribed by the component definition, and assigns that refdes to the symbol (example, refdes`U1` requires a `DIP14` package symbol). Returns nil if it cannot find the given refdes.
| `l_symbolData` | If this is the first argument, the function looks for the symbol, symbol type, and refdes specified by this structure.  `l_symbolData` is a list  (`t_symbolName` [[`t_symbolType` [`t_refdes`]]), where:  `t_symbolName` is the name of the symbol (example: `DIP14`)  `t_symbolType` is a symbol type: "`PACKAGE`" (default), "`MECHANICAL`" or "`FORMAT`"  `t_refdes` is a refdes; if `t_refdes` is present, `t_symbolType` must be "`package`"  Example of a list: ("`DIP16`" "`package`" "`U6`").  To create a component with an alternate symbol, a symbol different from the one specified in the component library, use the`l_symbolData` structure.  For example, refdes`C7` is a capacitor requiring the top-mount package "`CAP1206F`". Your design requires the alternative package "`CAP1206B`" on the bottom side of the layout.  To create the component mirrored, use`axlDBCreateSymbol` with the `l_symbolData` argument:  `"CAP1206B" "package" "C7")`
| `l_anchorPoint` | Layout coordinates of the location to create the symbol. This will be the origin of the symbol.
| `g_mirror` | `nil` - create unmirrored (default).  `t` - create symbol mirrored.  `` `GEOMETRY `` - geometry is mirrored.
| `f_rotation` | Rotation angle of the symbol in degrees.  `nil` - 0.0.
| `l_pinData` | List of axlPinData defstructs for any pins you require to be different from their library definition, as shown below:  `(defstruct axlPinData;(r_pinData) - pin data`  `number ;pin number as a text string`  `padstack ;padstack for the pin (text string)`  `origin ;relative location (X Y) of the pin`  `rotation) ;relative rotation of pin in degrees`  **Note:** As with all SKILL defstructs, use the constructor function make\_axlPinData to create instances of axlPinData. Use the copy function copy\_axlPinData to copy instances of axlPinData.
| `t_embeddedLayer` | Place on embedded layer. Layer must be enabled for embedded. Mirror option is ignored. Layer may either be fully qualified ("ETCH/GND") or just the subclass ("GND"). May not use the top or bottom layer.
#### Value Returned

|  |
| --- | ---
| `l_result` | `nil` - Nothing is created.  List Containing the following:  (`car`) axl `DBID` of the symbol created  (`cadr`) `t` if DRCs are created. `nil` if DRCs are not created.
#### Example

> ```
> mypins = list( make_axlPinData( ?number "2",     ?padstack "pad1", ?origin -100:-100 ?rotation 45)make_axlPinData( ?number "4", ?padstack "pad1",    ?origin -100:-300 ?rotation 45)make_axlPinData( ?number "6", ?padstack "pad1",    ?origin -100:-500 ?rotation 45)make_axlPinData( ?number "9", ?padstack "pad1",    ?origin 200:-500 ?rotation 45)make_axlPinData( ?number "11", ?padstack "pad1",    ?origin 200:-300 ?rotation 45)make_axlPinData( ?number "13", ?padstack "pad1",    ?origin 200:-100 ?rotation 45))axlDBCreateSymbolSkeleton( list("dip14"),    5600:4600, nil, 0, mypins)            ﬁ (dbid:426743 nil)
> ```

Adds a DIP14 symbol with all even-numbered pins having the same padstack as pin 1, rotated 45 °, and offset -100 mils.

### axlDBCreateText

```
axlDBCreateText(t_textl_anchorPointr_textOrientation[t_layer][o_attach])⇒ l_result/nil
```

#### Description

Creates a text string in the layout using the arguments described.

#### Arguments

|  |
| --- | ---
| `t_text` | Text string to add.`axlDBCreateText` accepts newlines embedded in the text. Each newline causes the function to create a new text line as a separate database object. The function returns the `dbids` of all text lines it creates. The textBlock parameter block specified in the `axlTextOrientation` structure specifies spacing between multiple text lines.
| `l_anchorPoint` | Layout coordinates of the location to add the text.
| `r_textOrientation` | `axlTextOrientation` structure:  `defstruct axlTextOrientation`  `;;(r_textOrientation) - description of`  `;; the orientation of text`  `textBlock ;string - text block name`  `rotation ;rotation in floatnum degrees`  `mirrored ;t-->mirrored, nil --> not mirrored,`  `'GEOMETRY --> only geometry is mirrored`  `justify) ;"left", "center", "right"`  **Note:** As with all SKILL defstructs, use the constructor function `make_axlTextOrientation` to create instances of `axlTextOrientation`. Use the copy function `copy_axlTextOrientation` to copy instances of `axlTextOrientation`.
| `t_layer` | Name of the layer on which the text is to be added.
| `o_attach` | `DBID` of the object to which the text must be attached, or use `nil` for the design.
#### Value Returned

|  |
| --- | ---
| `l_result` | Otherwise the function returns a list:  (`car`) list of text `DBIDs` created, one for each line of text input  (`cadr`)`t`if DRCs are created. Otherwise the function returns `nil`.
| `nil` | Nothing is created.
#### Notes

* If`o_attach`is a symbol instance, then the text is "stand alone", but a child of the symbol instance.

* If the`t_text` string contains NEWLINEs, then multiple text records will be created (and multiple `DBIDs` returned).

#### See Also

[axlTextOrientationCopy](06intedt.html#847294 "5"), [axlDBChangeText](06intedt.html#832157 "5")

#### Example

The following example adds the e text string "Chamfer both sides" center justified, mirrored and rotated 60 degrees.

`myorient = make_axlTextOrientation(?textBlock "8", ?rotation 60.0,`

`?mirrored t, ?justify "center")`

`ret = axlDBCreateText( "Chamfer both sides", 7600:4600,`

`myorient, "board geometry/plating_bar", nil)`

`==> (dbid:526743 nil)`

Adds the  text string "`Chamfer both sides`" center justified, mirrored and rotated 60°.

### axlDBCreateVia

```
axlDBCreateVia(t_padstack/o_padstackDbidl_anchorPoint[t_netName][g_mirror][f_rotation][o_parent])⇒ l_result/nil
```

#### Description

Creates a via in the layout as specified by the arguments described below.

#### Arguments

|  |
| --- | ---
| `t_padstack` | Padstack name. If a padstack definition with this name is not already in the layout, the function searches in order the libraries specified by`PADPATH` and loads the definition into the database.
| `o_padstackDbid` | a padstack dbid
| `l_anchorPoint` | Layout coordinates of the location to create the via.
| `t_netName` | Name of the net to which the via is to belong;  `nil` → via is stand-alone.
| `g_mirror` | `t` → create via mirrored.  `nil` → create via unmirrored.  `` `GEOMETRY `` → only geometry is mirrored.
| `f_rotation` | Rotation of via in degrees.
| `o_parent` | `DBID`of the object to which to attach the via. Use a symbol instance or use `nil` to specify the design itself.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (`car`) `DBID`of the via created.  (`cadr`) `t`if DRCs are created. `nil`if DRCs are not created.
| nil | Nothing is created.
#### Note

`axlDBCreateVia` cannot create a test point. You have to create testpoints by using the `axlTestPoint` function.

#### Example

> ```
> myvia = axlDBCreateVia( "pad1", 5600:4200,    "sclkl", t, 45., nil)    ⇒ (dbid:526745 nil)
> ```

Adds a standalone via using padstack "`pad1`" at x5600 y4200 on net "`sclkl`", mirrored and rotated. Adds a via rotated at 45 degrees:

### axlDBCreateSymbolAutosilk

`axlDBCreateSymbolAutosilk(o_symbol)⇒ t/nil`

#### Description

Creates or updates the`AUTOSILK` information for the specified symbol, as required. Also updates, as required, any other `AUTOSILK` information near the symbol.

#### Arguments

|  |
| --- | ---
| `o_symbol` | `dbid` of the symbol.
#### Value Returned

|  |
| --- | ---
| `t` | A valid symbol`dbid` is provided.
| `nil` | The`dbid` provided is not for a valid symbol.
### axlCreateWirebondGuide

`axlCreateWirebondGuide(r_path)==> dbid/nil`

#### Description

This function adds a wirebond guide path into the design, which can then be used to snap fingers through the wirebond tools.

**Arguments**

|  |
| --- | ---
| `r_path` | Existing path consisting of the straight-line and arc segments previously created by axlPath functions
#### Value Returned

* dbid of newly created guide path if successful.

* nil if an error occurred (message printed to status window).

Property Functions
------------------

This section describes the`DBCreate` functions you use to create your own (user-defined) property definitions, and add properties to database objects.

### axlDBCreatePropDictEntry

```
axlDBCreatePropDictEntry(t_namet_typelt_objects/t[ln_range][t_units][g_hidden]))⇒ od_propDictEntry/nil
```

`axlDBCreatePropDictEntry(nil)==> lt_availbeObject`

#### Description

Creates an Allegro user-defined property dictionary entry with given attributes. Once a dictionary entry is created, the property can then be attached to objects.

STRING property values are limited to 1024. STRING\_ID allows property values up to 4096. STRING\_ID is not currently supported in "define property" dialog of Allegro PCB Editor.

If you need to store larger data within the database, use attachments ([axlCreateAttachment](16dbatt.html#1065349 "17")).

#### Arguments

|  |
| --- | ---
| `t_name` | Name of the property. Must be different from all other property names in the design, both Allegro PCB Editor pre-defined and user-defined property names.
| `t_type` | Data type of the property value.  Legal values are:  Typical: BOOLEAN, INTEGER, REAL, STRING, and DESIGN\_UNITS.  Other supported types are:  ALTITUDE  CAPACITANCE  DISTANCE  ELEC\_CONDUCTIVITY  FAILURE\_RATE  IMPEDANCE  INDUCTANCE  LAYER\_THICKNESS  NAME  NOISE\_VOLTAGE  PERCENTAGE  PROP\_DELAY  RESISTANCE  TEMPERATURE  THERM\_CONDUCTANCE  THERM\_CONDUCTIVITY  THERM\_RESISTANCE  VOLTAGE  VELOCITY  STRING\_ID
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
|
| `lt_objects` | List of strings representing the object types to which this property can be added. (Use`axlDBGetPropDictEntry`(`nil`) to get a list of valid objects). If only a single object type is allowed, then it may be specified as a string, rather than a list containing one string.  If this value is t then all allowed properties are allowed.
|
| `ln_range` | List of the lowest and highest legal values for the (numeric) property. If the first value is`nil`, it means negative infinitely. If the second value is `nil`, it means infinity.
| `t_units` | A text string so be used with data types (`t_type`) without units, such as `STRING`, `INTEGER`, or `REAL`.
| `g_hidden` | `t`property is hidden from the user. Hidden properties are not shown in any Allegro UI like Constraint Manager, Show Element or Property Edit. Hidden properties can be accessed via SKILL. Typically, properties are hidden if they are only meant to be changed outside of the SKILL program. Hidden properties are also visible via `extracta`.
#### Value Returned

|  |
| --- | ---
| `o_propDictEntry` | `DBID`of the property dictionary entry created.
| `nil` | Property not created.
#### See Also

[axlDBAddProp](#367701 "15"), [axlCreateAttachment](16dbatt.html#1065349 "17")

#### Example

* Add a new property of type string, supported on db objects

> `propDoct = axlDBCreatePropDictEntry("ACME" "STRING" t)`

* Create`MYPROP` as a real number property with range -50 to 100 units of `"level",` attachable to pins, nets, and symbols.

> ```
> axlDBCreatePropDictEntry( "myprop", "real", list( "pins" "nets" "symbols"),list( -50. 100), "level")
> ```

> `propDict:2421543`

To check

* From Allegro PCB Editor, select*Setup - Property Definitions*.

> The Define User Properties window appears.

* Select*MYPROP* from the Available Properties list.

### axlDBAddProp

`axlDBAddProp(lo_attachll_name_value)⇒ l_result/nil`

#### Description

Adds all the property/value pairs listed in`ll_name_value` to all the object `dbids` listed in `lrd_attach`. If a particular object does not accept a particular property name in `ll_name_value`, `axlDBAddProp` silently ignores that combination, and continues. If an object already has the specific property attached, `axlDBAddProp` silently replaces its original value with the one specified in `ll_name_value`.

If any errors occur or if`axlDBAddProp` has not added or changed any properties, the function returns `nil`.

#### Arguments

|  |
| --- | ---
| `lo_attach` | List of Allegro PCB Editor object dbids to which to add the property/value combinations listed in`ll_name_value`. A list of `nil` denotes attachment to the design *(*`list``nil`*)*. However, if `lo_attach` is `nil`, there are no objects for attachment, and `axlDBAddProp` does nothing, returning `nil`.
| `ll_name_value` | List of property-name/property-value pairs as lists. If the`car` of this list is not a list, then `axlDBAddProp` treats `ll_name_value` as a single name-value list. The `car` of each name-value pair is the property name as a string. The `cadr` of the name-value list is the property value. It is either a string with or without units included, or a simple value (fixed or floating). If the value does not include units explicitly, then `axlDBAddProp` uses the units specified in the system `units.dat` file.
|  | `axlDBAddProp` ignores the property-value if the property data type is BOOLEAN.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (`car`) list of `dbids` of objects that had at least one property successfully added  (`cadr`) always `nil`.
| `nil` | No properties are added.
#### See Also

[axlDBDeleteProp](06intedt.html#808739 "5"), [axlDBCreatePropDictEntry](#367783 "15")[axlDBGetPropDictEntry](07dbaccs.html#735236 "6")[axlDBGetProperties](07dbaccs.html#700383 "6")`,`[axlDBDeletePropAll](06intedt.html#827023 "5")`,` [axlDBDeletePropDictEntry](06intedt.html#827658 "5"), and axlDBGetPropDict

#### Example

see[axlDBDeleteProp](06intedt.html#808739 "5")

> The Show Element window appears with the MYPROP value at`23.500000 level`.

Load and Save Functions
-----------------------

This section describes theLoad functions that add external objects to the Allegro PCB Editor database.

### axlLoadPadstack

`axlLoadPadstack (t_padname)⇒ o_dbid`

#### Description

Loads a padstack by attempting to find the padstack by name in the existing database. Failing that, Allegro PCB Editor looks in the pad library on the disk.

#### Arguments

|  |
| --- | ---
| `t_padname` | Padstack name. If loaded from disk, Allegro PCB Editor uses the`PADLIB` path variable to find the pad. Pad name is limited to 20 characters.
#### Value Returned

|  |
| --- | ---
| `o_dbid` | `dbid`of padstack loaded.
| `nil` | Nothing is found.
#### Example

`pad = axlLoadPadstack (VIA)`

Loads the VIA padstack.

### axlLoadSymbol

`axlLoadSymbol(t_symKind t_symName) -> o_dbidSymDef/nil`

**Description**

Searches for indicated symbol in database. If not present, searches PSMPATH and loads the symbol into the database. In the symbol editor, this can only be used for shape and mechanical symbols for use with padstacks.

* ***If a symbol definition is not in use (dbid->instance is nil) then the definition is deleted. This deletion of unused symbols occurs during save drawing, refresh symbol, place manual among other place. This means the database is saved as part of axlRunBatchDBProgram then the unused symdefs will be deleted.***

FLASH and SHAPE symbols are loaded automatically when a padstack using those symbols is loaded. This interface allows loading of these symbol types to allow analsyis of the contents of these symbols types since you cannot use the extracta program.

NOTES:

* `axlDBCreateSymbol` also loads the symbol definition if required. You do not need this API to place symbols.

* You can delete unused symdefs via axlDeleteObject.

#### Arguments

|  |
| --- | ---
| `t_symkind` | "PACKAGE", "MECHANICAL", "FORMAT" , "SHAPE, or "FLASH" (case insensitive)
| `t_symName` | Name of symbol (lower case). This is the root name of the symbol, do not include an extension (for example,`.psm`) or a directory path.
#### Value Returned

|  |
| --- | ---
| `dbid` | Of symbol definition
| `nil` | Cannot find symbol, unknown symbol type, symbol type doesn't match symbol, can't find a padstack that is required for a sym pin, or symbol revision is too old.
#### See Also

[axlDBCreateSymbol](#439738 "15")

#### EXAMPLE

`symdef = axlLoadSymbol("package" "dip14")`

### axlPadstackToDisk

`axlPadstackToDisk([t_padName][t_outPadName])⇒ t/nil`

#### Description

Saves a board padstack out to a library.

#### Arguments

|  |
| --- | ---
| `t_padName` | Name of the pad to be saved to a library.
| `t_outPadName` | Name of the output pad.
#### Value Returned

|  |
| --- | ---
| `t` | Pad is created.
| `nil` | Failed to create pad.
#### Example

* Dump all the padstacks in the layout.

`axlPadstackToDisk()`

* Dump padstack "`pad60cir36d`" from the layout as "`pad60cir36d.pad`".

`axlPadstackToDisk("pad60cir36d")`

* Dump padstack "`pad60cir36d`" from the layout as "`mypadstack.pad`".

`axlPadstackToDisk("pad60cir36d" "mypadstack")`

### axlRefreshSymbol

`axlRefreshSymbol(t_symName/o_SymDef[g_options])==> t/nil`

#### Description

Refreshes a symbol from file on disk which is located by current PSMPATH. Works the same as the refresh\_symbol functionality except updates one symbol definition. Unlike refresh\_symbol this does not support the reset custom drill option since this is done at the padstack level not the symbol level.

* 1) If updating multiple symbols use[axlDBCloak](17dbtran.html#1065349 "18") for best performance and minimal memory use.
  2) To ignore the FIXED property see [axlDBIgnoreFixed](14dsnctl.html#715890 "14").

#### Arguments

* existing symbol name
* symbol definition dbid
* `'keepPadstack` - keep instance edited padstacks
* `'text` - reset text locations
* `'fanout` - reset fanouts (if design has fanouts delete them). Default is to only delete fanouts if disk symbol has them.

RETURNS

* `o_SymDef` - refreshed symdef

* `nil` - fails; typically if cannot find symbol on disk or if a FIXED property is present.

#### Example

* Update the DIP14 and reset text locations

> `axlRefreshSymbol("DIP14" 'text)`

* Update first symbol def off database root and set both the text and pin escape option

> `symdef = axlDBGetDesign()->symdefs`

> `axlRefreshSymbol(car(symdef) '(text fanout))`

#### See Also

[axlDBCloak](17dbtran.html#1065349 "18"), [axlDBIgnoreFixed](14dsnctl.html#715890 "14"), [axlReplacePadstack](06intedt.html#31833 "5")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
