<!--
source: algroskill/03dbcre8.md
part: 2/2
estimated_tokens: 3750
-->

### axlDBCreateText

`axlDBCreateText( t_text l_anchorPoint r_textOrientation [t_layer] [o_attach] ) => l_result/nil`

#### Description

Creates a text string in the layout using the arguments described.

#### Arguments

| Name | Description |
|---|---|
| `t_text` | Text string to add. `axlDBCreateText` accepts newlines embedded in the text. Each newline causes the function to create a new text line as a separate database object. The function returns the `dbids` of all text lines it creates. The textBlock parameter block specified in the `axlTextOrientation` structure specifies spacing between multiple text lines. |
| `l_anchorPoint` | Layout coordinates of the location to add the text. |
| `r_textOrientation` | `axlTextOrientation` structure: `defstruct axlTextOrientation ;;(r_textOrientation) - description of ;; the orientation of text textBlock ;string - text block name rotation ;rotation in floatnum degrees mirrored ;t-->mirrored, nil --> not mirrored, 'GEOMETRY --> only geometry is mirrored justify) ;"left", "center", "right"` Note: As with all SKILL defstructs, use the constructor function `make_axlTextOrientation` to create instances of `axlTextOrientation`. Use the copy function `copy_axlTextOrientation` to copy instances of `axlTextOrientation`. |
| `t_layer` | Name of the layer on which the text is to be added. |
| `o_attach` | `DBID` of the object to which the text must be attached, or use `nil` for the design. |

#### Value Returns

| Name | Description |
|---|---|
| `l_result` | Otherwise the function returns a list:
 (`car`) list of text `DBIDs` created, one for each line of text input
 (`cadr`) `t` if DRCs are created. Otherwise the function returns `nil`. |
| `nil` | Nothing is created. |

#### Examples

The following example adds the e text string "Chamfer both sides" center justified, mirrored and rotated 60 degrees.

`myorient = make_axlTextOrientation(?textBlock "8", ?rotation 60.0, ?mirrored t, ?justify "center") ret = axlDBCreateText( "Chamfer both sides", 7600:4600, myorient, "board geometry/plating_bar", nil) ==> (dbid:526743 nil)` Adds the  text string "`Chamfer both sides`" center justified, mirrored and rotated 60°.

#### See Also

axlTextOrientationCopy, axlDBChangeText

### axlDBCreateVia

`axlDBCreateVia( t_padstack/o_padstackDbid l_anchorPoint [t_netName] [g_mirror] [f_rotation] [o_parent] ) => l_result/nil`

#### Description

Creates a via in the layout as specified by the arguments described below.

#### Arguments

| Name | Description |
|---|---|
| `t_padstack` | Padstack name. If a padstack definition with this name is not already in the layout, the function searches in order the libraries specified by `PADPATH` and loads the definition into the database. |
| `o_padstackDbid` | a padstack dbid |
| `l_anchorPoint` | Layout coordinates of the location to create the via. |
| `t_netName` | Name of the net to which the via is to belong; `nil` → via is stand-alone. |
| `g_mirror` | `t` → create via mirrored. `nil` → create via unmirrored. ``GEOMETRY` → only geometry is mirrored. |
| `f_rotation` | Rotation of via in degrees. |
| `o_parent` | `DBID`of the object to which to attach the via. Use a symbol instance or use `nil` to specify the design itself. |

#### Value Returns

| Name | Description |
|---|---|
| `l_result` | List:
 (`car`) `DBID`of the via created.
 (`cadr`) `t` if DRCs are created. `nil` if DRCs are not created. |
| nil | Nothing is created. |

#### Examples

`myvia = axlDBCreateVia( "pad1", 5600:4200,``"sclkl", t, 45., nil)``⇒ (dbid:526745 nil)`

Adds a standalone via using padstack "`pad1`" at x5600 y4200 on net "`sclkl`", mirrored and rotated. Adds a via rotated at 45 degrees:

### axlDBCreateSymbolAutosilk

`axlDBCreateSymbolAutosilk( o_symbol ) => t/nil`

#### Description

Creates or updates the `AUTOSILK` information for the specified symbol, as required. Also updates, as required, any other `AUTOSILK` information near the symbol.

#### Arguments

| Name | Description |
|---|---|
| `o_symbol` | `dbid` of the symbol. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | A valid symbol `dbid` is provided. |
| `nil` | The `dbid` provided is not for a valid symbol. |

### axlCreateWirebondGuide

`axlCreateWirebondGuide( r_path ) => dbid/nil`

#### Description

This function adds a wirebond guide path into the design, which can then be used to snap fingers through the wirebond tools.

#### Arguments

| Name | Description |
|---|---|
| `r_path` | Existing path consisting of the straight-line and arc segments previously created by axlPath functions |

#### Value Returns

- dbid of newly created guide path if successful.

- nil if an error occurred (message printed to status window).

Property Functions

This section describes the `DBCreate` functions you use to create your own (user-defined) property definitions, and add properties to database objects.

### axlDBCreatePropDictEntry

`axlDBCreatePropDictEntry( t_name t_type lt_objects/t [ ln_range ] [ t_units ] [ g_hidden ] ) => o_propDictEntry/nil`

#### Description

Creates an Allegro user-defined property dictionary entry with given attributes. Once a dictionary entry is created, the property can then be attached to objects.

STRING property values are limited to 1024. STRING_ID allows property values up to 4096. STRING_ID is not currently supported in "define property" dialog of Allegro PCB Editor.

If you need to store larger data within the database, use attachments (axlCreateAttachment).

#### Arguments

| Name | Description |
|---|---|
| `t_name` | Name of the property. Must be different from all other property names in the design, both Allegro PCB Editor pre-defined and user-defined property names. |
| `t_type` | Data type of the property value. 
 Legal values are: 
 Typical: BOOLEAN, INTEGER, REAL, STRING, and DESIGN_UNITS. 
 Other supported types are:
 ALTITUDE
 CAPACITANCE
 DISTANCE
 ELEC_CONDUCTIVITY
 FAILURE_RATE
 IMPEDANCE
 INDUCTANCE
 LAYER_THICKNESS
 NAME
 NOISE_VOLTAGE
 PERCENTAGE
 PROP_DELAY
 RESISTANCE
 TEMPERATURE
 THERM_CONDUCTANCE
 THERM_CONDUCTIVITY
 THERM_RESISTANCE
 VOLTAGE
 VELOCITY
 STRING_ID |
| `lt_objects` | List of strings representing the object types to which this property can be added. (Use `axlDBGetPropDictEntry`(`nil`) to get a list of valid objects). If only a single object type is allowed, then it may be specified as a string, rather than a list containing one string.
 If this value is t then all allowed properties are allowed. |
| `ln_range` | List of the lowest and highest legal values for the (numeric) property. If the first value is `nil`, it means negative infinitely. If the second value is `nil`, it means infinity. |
| `t_units` | A text string so be used with data types (`t_type`) without units, such as `STRING`, `INTEGER`, or `REAL`. |
| `g_hidden` | `t`property is hidden from the user. Hidden properties are not shown in any Allegro UI like Constraint Manager, Show Element or Property Edit. Hidden properties can be accessed via SKILL. Typically, properties are hidden if they are only meant to be changed outside of the SKILL program. Hidden properties are also visible via `extracta`. |

#### Value Returns

| Name | Description |
|---|---|
| `o_propDictEntry` | `DBID`of the property dictionary entry created. |
| `nil` | Property not created. |

#### Examples

- Add a new property of type string, supported on db objects

`propDoct = axlDBCreatePropDictEntry("ACME" "STRING" t)`

- Create `MYPROP` as a real number property with range -50 to 100 units of `"level",` attachable to pins, nets, and symbols.

`axlDBCreatePropDictEntry( "myprop", "real", list( "pins" "nets" "symbols"),``list( -50. 100), "level")`

`propDict:2421543`

To check

| Name | Description |
|---|---|
| 1. | From Allegro PCB Editor, select Setup - Property Definitions. |

The Define User Properties window appears.

| Name | Description |
|---|---|
| 2. | Select MYPROP from the Available Properties list. |

#### See Also

axlDBAddProp, axlCreateAttachment

### axlDBAddProp

`axlDBAddProp( lo_attach ll_name_value ) => l_result/nil`

#### Description

Adds all the property/value pairs listed in `ll_name_value` to all the object `dbids` listed in `lrd_attach`. If a particular object does not accept a particular property name in `ll_name_value`, `axlDBAddProp` silently ignores that combination, and continues. If an object already has the specific property attached, `axlDBAddProp` silently replaces its original value with the one specified in `ll_name_value`.

If any errors occur or if `axlDBAddProp` has not added or changed any properties, the function returns `nil`.

#### Arguments

| Name | Description |
|---|---|
| `lo_attach` | List of Allegro PCB Editor object dbids to which to add the property/value combinations listed in `ll_name_value`. A list of `nil` denotes attachment to the design (`list nil`). However, if `lo_attach` is `nil`, there are no objects for attachment, and `axlDBAddProp` does nothing, returning `nil`. |
| `ll_name_value` | List of property-name/property-value pairs as lists. If the `car` of this list is not a list, then `axlDBAddProp` treats `ll_name_value` as a single name-value list. The `car` of each name-value pair is the property name as a string. The `cadr` of the name-value list is the property value. It is either a string with or without units included, or a simple value (fixed or floating). If the value does not include units explicitly, then `axlDBAddProp` uses the units specified in the system `units.dat` file.<br><br>`axlDBAddProp` ignores the property-value if the property data type is BOOLEAN. |

#### Value Returns

| Name | Description |
|---|---|
| `l_result` | List:
 (`car`) list of `dbids` of objects that had at least one property successfully added
 (`cadr`) always `nil`. |
| `nil` | No properties are added. |

#### Examples

see axlDBDeleteProp

The Show Element window appears with the MYPROP value at `23.500000 level`.

Load and Save Functions

This section describes the Load functions that add external objects to the Allegro PCB Editor database.

#### See Also

axlDBDeleteProp, axlDBCreatePropDictEntryaxlDBGetPropDictEntryaxlDBGetProperties`,`axlDBDeletePropAll`,` axlDBDeletePropDictEntry, and axlDBGetPropDict

### axlLoadPadstack

`axlLoadPadstack ( t_padname ) => o_dbid`

#### Description

Loads a padstack by attempting to find the padstack by name in the existing database. Failing that, Allegro PCB Editor looks in the pad library on the disk.

#### Arguments

| Name | Description |
|---|---|
| `t_padname` | Padstack name. If loaded from disk, Allegro PCB Editor uses the `PADLIB` path variable to find the pad. Pad name is limited to 20 characters. |

#### Value Returns

| Name | Description |
|---|---|
| `o_dbid` | `dbid` of padstack loaded. |
| `nil` | Nothing is found. |

#### Examples

`pad = axlLoadPadstack (VIA)`

Loads the VIA padstack.

### axlLoadSymbol

`axlLoadSymbol( t_symKind t_symName ) => o_dbidSymDef/nil`

#### Description

Searches for indicated symbol in database. If not present, searches PSMPATH and loads the symbol into the database. In the symbol editor, this can only be used for shape and mechanical symbols for use with padstacks.

- If a symbol definition is not in use (dbid->instance is nil) then the definition is deleted. This deletion of unused symbols occurs during save drawing, refresh symbol, place manual among other place. This means the database is saved as part of axlRunBatchDBProgram then the unused symdefs will be deleted.

FLASH and SHAPE symbols are loaded automatically when a padstack using those symbols is loaded. This interface allows loading of these symbol types to allow analsyis of the contents of these symbols types since you cannot use the extracta program.

NOTES:

- `axlDBCreateSymbol` also loads the symbol definition if required. You do not need this API to place symbols.

- You can delete unused symdefs via axlDeleteObject.

#### Arguments

| Name | Description |
|---|---|
| `t_symkind` | "PACKAGE", "MECHANICAL", "FORMAT" , "SHAPE, or "FLASH" (case insensitive) |
| `t_symName` | Name of symbol (lower case). This is the root name of the symbol, do not include an extension (for example, `.psm`) or a directory path. |

#### Value Returns

| Name | Description |
|---|---|
| `dbid` | Of symbol definition |
| `nil` | Cannot find symbol, unknown symbol type, symbol type doesn't match symbol, can't find a padstack that is required for a sym pin, or symbol revision is too old. |

#### Examples

`symdef = axlLoadSymbol("package" "dip14")`

#### See Also

axlDBCreateSymbol

### axlPadstackToDisk

`axlPadstackToDisk( [t_padName] [t_outPadName] ) => t/nil`

#### Description

Saves a board padstack out to a library.

#### Arguments

| Name | Description |
|---|---|
| `t_padName` | Name of the pad to be saved to a library. |
| `t_outPadName` | Name of the output pad. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Pad is created. |
| `nil` | Failed to create pad. |

#### Examples

- Dump all the padstacks in the layout.

`axlPadstackToDisk()`

- Dump padstack "`pad60cir36d`" from the layout as "`pad60cir36d.pad`".

`axlPadstackToDisk("pad60cir36d")`

- Dump padstack "`pad60cir36d`" from the layout as "`mypadstack.pad`".

`axlPadstackToDisk("pad60cir36d" "mypadstack")`

### axlRefreshSymbol

`axlRefreshSymbol( t_symName/o_SymDef [g_options] ) => t/nil`

#### Description

Refreshes a symbol from file on disk which is located by current PSMPATH. Works the same as the refresh_symbol functionality except updates one symbol definition. Unlike refresh_symbol this does not support the reset custom drill option since this is done at the padstack level not the symbol level.

- 1) If updating multiple symbols use axlDBCloak for best performance and minimal memory use.2) To ignore the FIXED property see axlDBIgnoreFixed.

#### Arguments

| Name | Description |
|---|---|
| `t_symName` | existing symbol name |
| `o_SymDef` | symbol definition dbid |
| `g_options` | The available options are: `'text` - reset text locations `'fanout` - reset fanouts (if design has fanouts delete them). Default is to only delete fanouts if disk symbol has them. `'keepPadstack` - keep instance edited padstacks |

RETURNS

- `o_SymDef` - refreshed symdef

- `nil` - fails; typically if cannot find symbol on disk or if a FIXED property is present.

#### Examples

| Name | Description |
|---|---|
| 1. | Update the DIP14 and reset text locations |

`axlRefreshSymbol("DIP14" 'text)`

| Name | Description |
|---|---|
| 2. | Update first symbol def off database root and set both the text and pin escape option |

`symdef = axlDBGetDesign()->symdefs`

`axlRefreshSymbol(car(symdef) '(text fanout))`

#### See Also

axlDBCloak, axlDBIgnoreFixed, axlReplacePadstack

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

