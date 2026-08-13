### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

9
=

SiP/APD Commands
================

This functions listed in this chapter are available only in Cadence IC Packaging tools; Allegro Package Designer (APD) and SiP Layout (CDNSIP).

### axlChangeLayer

```
axlChangeLayer(lo_dbid/o_dbidt_newLayer[o_padStackDbid]/[t_padstackname])==> t/nil
```

#### Description

Changes layer for lines, clines or segments, shapes, and text. Functionality offered, at the global level, matches the Allegro PCB Editor`change` command, but can differ in certain areas.

If moving clines or cline segments across layers, you should provide a via to be used to maintain connections. Via must meet constraint rules. For via to be accepted it must have:

* pads on start and destination layers

* be in the constraint via list for the net and location

If the provided padstack is not acceptable, system will select an acceptable padstack based upon the via list for net and location.

**Note:** If you need to change the layer of multiple etch objects, it is more efficient to pass them as a list of dbids then to call this function for each dbid.

#### Arguments

|  |
| --- | ---
| `lo_dbid/o_dbid` | a single dbid or list of dbids
| `t_newLayer` | new layer for placing dbid
| `o_padStackDbid` | if moving clines across layers, allegro will add a via to maintain connection. This is that via. If this argument is not provided the system default via is used.
| `t_padStackName` | name of padstack to be used
#### Value Returned

`t` if succeeded, `nil` if failure

#### *Failures*

For debug purposes set axlDebug(t) to see additional messages.

* dbid is of a unsupported type

* illegal option types

* target layer matches object current layer

#### Examples

* Move an object to ETCH/BOTTOM

> ```
> ; ashOne is a selection utility found at <cdsroot>/pcb/examples/skill/ash-fxf/ashone.il
> ```

> `dbid = ashOne()`

> `; pick an object (set find filter)`

> `result = axlChangeLayer(dbid "ETCH/BOTTOM")`

> `; or if moving clines`

> `result = axlChangeLayer(dbid "ETCH/BOTTOM" "PAD60SQ36D")`

#### See Also

[axlTransformObject](06intedt.html#821370 "5"), [axlDBChangeText](06intedt.html#832157 "5"), [axlChangeWidth](06intedt.html#823183 "5")

### axlCNSAssemblyModeGet

`axlCNSAssemblyModeGet(nil) => ls_constraints`

`axlCNSAssemblyModeGet('all) => lls_constraintNModes`

`axlCNSAssemblyModeGet(s_name/t_name) => s_mode/nil`

`axlCNSAssemblyModeGet(s_name/t_name'print) => t_name/nil`

#### Description

This retrieves the current assembly DRC mode(s). Modes determine if a particular constraint is on or off. These DRC modes apply to the entire design. Use`axlCNSAssemblyModeGet(nil)` to determine the set currently supported assembly modes.The `'print` mode offers the name shown in reports like show element.

* ***Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.***

#### Arguments

|  |
| --- | ---
| `nil` | returns all modes that are in the spacing domain
| `'all` | returns all checks and current mode
| `s_name` | symbol name of check.
| `t_name` | string name of check
| `'print` | printable constraint name option
#### Value Returned

|  |
| --- | ---
| `ls_names` | list of checks`(s_name ...)`
| `lls_names` | list of checks and their mode`((s_name s_mode) ...)`
| `s_mode` | mode`'on`, or `'off`
| `t_name` | the printable constraint name
#### Examples

* Get current list of assembly constraints

> `axlCNSAssemblyModeGet(nil)`

* Get list of settings for all assembly constraints

> `axlCNSAssemblyModeGet('all)`

* Get current mode of Die to Finger Spacing check

> `axlCNSAssemblyModeGet('die_to_finger)`

#### See Also

axlCNSAssemblyModeSet, axlCNSGetAssembly

### **axlCNSAssemblyModeSet**

`axlCNSAssemblyModeSet(t_name/s_namet_mode/s_mode)=> t/nil`

`axlCNSAssemblyModeSet('allt_mode/smode)=> t/nil`

`axlCNSAssemblyModeSet(l_constraintNModest_mode/smode)=> t/nil`

`axlCNSAssemblyModeSet(ll_constraintNModes)=> t/nil`

#### Description

This command sets the current DRC modes (on/off) for checks in the area of assembly constraints. These modes are global.

To determine the constraints modes currently supported, use`axlCNSAssemblyModeGet(nil)`.

Several interfaces are supported for this command, all checks`('all)`, individual checks (`t_name`), list of checks within a mode `'(s_name ...) t_mode/s_mode'(t_name ...) t_mode/s_mode`, and sets of checks via a list of:`'((s_name/t_name s_mode/t_mode) ....).`

The constraints names may be passed as a symbol or a string. For performance reasons, either do all your updates in a single call or wrap individual changes in the map API (see[axlCNSMapUpdate](18consmgt.html#1074801 "19")).

* ***Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.***

#### Arguments

|  |
| --- | ---
| `s_name` | symbol name of check.
| `t_name` | string name of check.
| `s_mode` | mode setting; may be 'on or 'off.
| `t_mode` | string mode setting "on or "off".
| `'all` | set all checks for assembly design rule checks (including online wire rules)
#### Value Returned

|  |
| --- | ---
| `t` | if succeeds
| `nil` | if failed
#### Examples

* Turn all constraints off

> `axlCNSAssemblyModeSet('all 'off)`

* Turn Die to Finger Spacing check on

> `axlCNSAssemblyModeSet('die_to_finger 'on)`

* Turn two constraint to on

> `axlCNSAssemblyModeSet('(via_to_package_edge die_to_finger) 'on)`

* Set various constraints to different modes

> `axlCNSAssemblyModeSet( '((die_to_finger off) (via_to_package_edge 'on)) )`

#### See Also

[axlCNSAssemblyModeGet](#1105112 "9"), [axlCNSGetAssembly](#1105625 "9"), [axlCNSMapUpdate](18consmgt.html#1074801 "19")

### axlCNSGetAssembly

`axlCNSGetAssembly(t_csett_layers_constraint[g_string])=> g_value/nil`

`axlCNSGetAssembly(t_csett_layernil[g_string])=> ll_nameValue/nil`

`axlCNSGetAssembly(nilnilnil)=> ls_cnsTypes`

#### Description

Obtains an Assembly cset values. In the first operational mode, the command obtains the value of an assembly constraint given a cset and a layer. In second mode of operation, it obtains all assembly constraint as name-value pairs for a cset on a layer. For the last mode, a list of all supported assembly constraints is obtained by passing three`nil` values to the interface:`axlCNSGetAssembly(nil nil nil)`

DATA TYPES -- Unless otherwise specified constraints are in current design units.

#### Arguments

|  |
| --- | ---
| `t_cset` | Name of a assembly cset. Use "" for design-level constraints.
| `t_layer` | ETCH layer name (e.g "ETCH/TOP" or "TOP"). If`nil` is specified, gets constraints on all layers.
| `s_constraint` | Name of constraint. If`nil`, returns a set of symbol/value pairs of all constraints.
| `g_string` | By default, returns value in the native units of the constraint. If`g_string` is set to `t`, the data is returned as a string.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value of constraint in design units
| `ll_nameValue` | Mame value pairs of assembly constraint symbol and constraint value for all assembly`(s_constraint g_value)`. `'((wire_len_min 10.0) (wire_len_max 50.0) ...)`
| `ls_cnsTypes` | List of supported assembly constraint names
| `nil` | Indicates an error
#### Examples

* Get min wire length in design cset

> `axlCNSGetAssembly("" nil 'wire_len_min)`

* Get all assembly constraints for "V" cset, bottom layer

> `axlCNSGetAssembly("V" "BOTTOM" nil)`

* Get min shape constraint list for "V" cset, top layer

> `axlCNSGetAssembly("V" "TOP" 'min_shape_check)`

* Get supported Assembly constraint symbols

> `axlCNSGetAssembly(nil nil nil)`

* Fetch all layers and constraints of Assembly cset V

> ```
> cset = "V"       ;; Dforeach(subclass axlSubclassRoute()layer = axlCNSGetAssembly(cset subclass nil)printf("\nLAYER=%s\n\tconstraints=%L\n" subclass, layer))
> ```

#### See Also

[axlCNSSetAssembly](#1106263 "9")

### axlCNSSetAssembly

```
axlCNSSetAssembly(t_object/nilt_layer/nils_constraintg_value[s_object_type] )==> t/nil
```

```
axlCNSSetAssembly(t_object/nilt_layer/nilll_constraintValuesnil[s_object_type] )==> t/nil
```

#### Description

Updates assembly cset, wire profile or symbol constraint values. By passing`nil` at the appropriate argument, values for all csets and all layers may be changed.

By default, object type is a cset. To update values on wire profile, use wire profile as an object name and pass fifth argument as`'PROFILE`. To update values on symbols (dies, spacers or interposers) use refdes as an object name, and specify the fifth argument as `'SYMBOL`.

DATA TYPES -- See[axlCNSGetAssembly](#1105625 "9") for the data type of each constraint.

Design Units:

* A number (integer or floating point) where units is current design units. Must not exceed accuracy of the design.

* Unitless string where accuracy cannot exceed db accuracy.

* String with units, data converted to current design units.

Boolean: Use`t/nil` or "true"/"false".

* For list of Assembly constraints see[axlCNSGetAssembly](#1105625 "9").

* ***This does NOT change override values. For example, you can set wire\_len\_min value in all csets but if the user has applied it to a wire profile as an override, it will still be used for those items.***

#### Arguments

|  |
| --- | ---
| `t_object` | cset name, use`""` for design level constraint. Use `nil` to apply change to all cset.  wire profile name  die refdes
| `t_layer` | ETCH layer name (e.g "ETCH/TOP" or "TOP"). If nil apply change to all layers - applicable to by layer constraints only. Use nil for constraints that cannot be set by layer.
| `s_contraint` | Constraint symbol to change. Use`axlCNSGetAssembly(nil nil nil)` for list of permissible values.
| `g_value` | Value to update. For data type see above for "DATA TYPES".
| `ll_constraintValues` | Multiple values may be updated by passing a list of lists for the third argument.  `'((s_contraint g_value) ... )`
| `s_object_type` | By default, object type is cset. Use`'SYMBOL` for die, `'PROFILE` for wire profile
#### Value Returned

* `t` if succeeds

* `nil`, in case of an error. This value is returned if:

* cset name does not exit

* layer does not exist

* constraint does not exist

* illegal value for constraint

#### Examples

* Set min shape check on all constraint sets and layers

> `axlCNSSetAssembly(nil nil 'min_shape_check 50)`

* Set min void check on all layers on design level

> `axlCNSSetAssembly("" nil 'min_void_check 60)`

* Set min wire length on wire profile PROFILE1

> `axlCNSSetAssembly("PROFILE1" nil 'wire_len_min 75 'profile)`

* Set die overhang x on die U1

> `axlCNSSetAssembly("U1" nil 'die_overhang_x 50 'symbol)`

#### See Also

[axlCNSGetAssembly](#1105625 "9")

### axlCreateDeviceFileTemplate

`axlCreateDeviceFileTemplate(t_deviceNamet_CLASSl_pinList) -> t/nil`

#### Description

This creates a template device file providing same functionality as the create device command in the symbol editor. Normally you would use[axlDBCreateComponent](26logacc.html#1076090 "30") to create a device file if in the board.

#### Arguments

|  |
| --- | ---
| `t_deviceName` | Name of device file (no file extension or path)
| `t_CLASS` | Class of device (e.g. IC, IO, etc.)
| `l_pinList` | List of pins. Can be any combination of either pin dbid or pin numbers. If a pin dbid will filter out mechanical pins
#### Value Returned

`t` - file created

`nil` - an issue

#### See Also

[axlDBCreateComponent](26logacc.html#1076090 "30")

### axlCompAddPin

`axlCompAddPin(o_compg_absLoco_pin/lo_pins) => t/nil`

#### Description

This function adds one or more pins to the specified component. Pins are added to the corresponding component and symbol definition, with changes being reflected in all instances of those definitions.

#### Arguments

|  |
| --- | ---
| `o_comp` | Dbid of component instance to which pins should be added.
| `g_absLoc` | If true, locations and rotations for pins are absolute values in the design space. If`nil`, these values are relative to the origin of the unmirrored, unrotated symbol definition.
| `o_pin/lo_pins` | Structure, or list of structures, defining the pins to be added. These objects are defstructs as defined below.
Defstruct used to define a pin. Use`make_axlCompPinRecord`.

Required Elements are:

* `s_pinUse` - Pin use code for this pin. Must be one of the following symbols:

|  |  |
| --- | --- | ---
|  |  | UNSPEC
|  |  |
| --- | --- | ---
|  |  | POWER
|  |  |
| --- | --- | ---
|  |  | GROUND
|  |  |
| --- | --- | ---
|  |  | NC
|  |  |
| --- | --- | ---
|  |  | LOADIN
|  |  |
| --- | --- | ---
|  |  | LOADOUT
|  |  |
| --- | --- | ---
|  |  | BI
|  |  |
| --- | --- | ---
|  |  | TRI
|  |  |
| --- | --- | ---
|  |  | OCA
|  |  |
| --- | --- | ---
|  |  | OCL.
* `n_swapCode` - Swap group code for this pin. A swap code of `0` means this pin is not swappable. Otherwise, all pins with the same swap code are swappable. This value is not used for co-design components, as all co-design comp pins are considered swappable.

* `l_location` - X/Y coordinate location for the pin. Absolute or relative to the symbol def origin, as specified by `g_absLoc`.

* `n_rotation` - Angular rotation of this pin. Absolute or relative to the symbol definition origin, as specified by `g_absLoc`.

Optional Elements are:

* `pinNumber` - Physical pin number to assign to this pin. Must be unique across all pins of the component. If no pin number is provided, the pin number will be computed based on the pin numbering scheme for the component. If the numbering scheme is 'Customized', as is the default for co-design objects, then the tool will assign the first unused integer as the pin's number (1, 2...).

* `pinName` - Logical pin name for the pin. Not used for power/ground pins. If not provided, the pin name for signal pins will be the same as the physical pin number.

* `verilogPort` - Verilog port name for the pin. Not used for power/ground pins. If not provided, there is no verilog port name for the pin and the function pin name is used.

* `net` - Net name or dbid to assign this pin to when created. If nil, pin will be created on a dummy net and can be assigned later.

* `padstack` - Padstack name or dbid to use for this pin. If no padstack is supplied, the padstack already in use for pins of this component will be used for this pin as well.

Co-design Elements are:

* `codesignNet` - Net name for this pin in the secondary design space. For example:

* For a co-design die in a package, this is the pin's net in the IC design.

* For a co-design package in a board, this is the pin's net in the package.

* `codesignPad` - Pad/Cell name for this pin in the secondary design space. For example:

* For a co-design die in a package, this is the pin's LEF bump macro.

* For a co-design package in a board, this is the pin's padstack in the package.

#### Value Returned

* `t` if the pin(s) were added.

* `nil` if there was an error adding any of the pins, e.g. if a pin would be placed outside the extents of the symbol or drawing.

* If many pins are to be added, it is more efficient to pass the entire list to this function to process them in one call than to call axlCompAddPin with each individual pin.

#### See Also

[axlCompDeletePin](#1085880 "9"), [axlCompMovePin](#1085881 "9")

### axlCompDeletePin

`axlCompDeletePin(o_pin/lo_pins) => t/nil`

#### Description

This function deletes the specified pin(s) from the parent component and symbol definition. As a result, the pin will also be deleted from all instances of these definitions and not just the instance the pin passed in belongs to.

#### Arguments

|  |
| --- | ---
| `o_pin/lo_pins` | skill dbid of the pin to be deleted, or a list of pins to be deleted.
#### Value Returned

* `t` if the pin(s) were deleted.

* `nil` if there was an error deleting any of the pins, e.g. if a pin had the fixed property.

**Note:** If many pins are to be delete, it is more efficient to pass the entire list to this function to process them in one call than to call[axlCompDeletePin](#1085880 "9") with each individual pin.

#### See Also

[axlCompAddPin](#1091129 "9"), [axlCompMovePin](#1085881 "9")

### axlCompMovePin

```
axlCompMovePin(o_pin/lo_pins?move            l_deltaPoint?groupMirror     t/nil?groupRotation   f_angle?rotOrigin       l_rotatePoint?pinRotation     f_deltaAngle) => t/nil
```

**Description**

This function moves the specified pin(s) by the specified delta x/y, rotation, and mirror. Rotation and mirror, if provided, are applied around the`rotatePoint` (defaults to 0,0 if not provided). A rotation to apply to each individual pin may also be provided.

#### Arguments

|  |
| --- | ---
| `o_pin/lo_pins` | skill dbid of the pin to be moved, or a list of pins to be moved.
| `move` | X/Y delta to move each pin in the set by.
| `groupMirror` | `t` if the position of each pin in the group should be mirrored around the supplied rotOrigin.
| `groupRotation` | angle of rotation that should be applied to each pin in the group to determine its new final location. Applied around rotOrigin.
| `rotOrigin` | X/Y origin for group mirror and rotation application.
| `pinRotation` | Rotation to apply to individual pins once placed at new location.  For example, if you are moving a pin from the north side to west side, and the pin is rectangular, you may wish to specify a rotation of 90 degrees to keep the same orientation of the pin rectangle relative to the nearest die edge.
|
#### Value Returned

`t` if the pin(s) were moved.

`nil` if there was an error moving any of the pins, e.g. if a pin had the fixed property or would be placed outside the extents.

**Notes**:

* If many pins are to be moved, it is more efficient to pass the entire list to this function to process them in one call than to call axlCompMovePin with each individual pin.

* When applying multiple transforms at once to the set of pins, the operations are performed in the following order:

|
| ---
|
 **a.** | group mirror is performed for the group about the specified rotOrigin.
|
| ---
|
 **b.** | group rotation is then applied, also around the rotOrigin.
|
| ---
|
 **c.** | move delta is then applied.
This is important to keep in mind so that you achieve the desired end position for all pins being moved, and so that you use the correct rotOrigin point.

#### See Also

[axlCompAddPin](#1091129 "9"), [axlCompDeletePin](#1085880 "9")

### axlComponentChangeClass

`axlComponentChangeClass(s_devType/o_compDefs_class) -> t_oldClass/nil`

#### Description

This command changes the component class of a component definition.

Do not change class for the component definitions with component class as MECHANICAL, PLATING\_BAR or DRIVER\_CELL. Also you may not change an object to those classes.

To get the dbid of a component definition,

* For symbol instance,`cd = syminst->component->compdef`

> **Note:** A symbol may not have a component instance (e.g. mechanical)

* For component instance,`cd = component->compdef`

* ***Running a Cadence or 3rd party ECO restores the original component class.***

#### Arguments

|  |
| --- | ---
| `s_devType` | Name of the device.
| `o_compDef` | dbdid of a component definition.
| `s_class` | Name of the new component class.  Possible values are IC, IO, DISCRETE
#### Value Returned

|  |
| --- | ---
| `t_oldClass` | Old component class name is returned in case of success.
| `nil` | Returned in case of an error.
#### Example

`axlComponentChangeClass("DIP14" "DISCRETE")`

#### See Also

[axlDBCreateComponent](26logacc.html#1076090 "30")

### axlCompSetPinAttributes

```
axlCompSetPinAttributes(o_pin/lo_pins?number     t_pinNumber?name       t_pinName?use        t_pinUse?padstack   t_padstack/g_padstack?rotation   f_rotation?swapCode   n_swapCode) => t/nil
```

#### Description

This function modifies attributes of the specified pin(s) at the symbol and component definition level. Things like the padstack, pin number, and swap code (see below for full list of supported attributes). All update items, if not set, will be left at the pin's existing value.

#### Arguments

|  |
| --- | ---
| `o_pin/lo_pins` | Skill dbid of the pin to be modified, or a list of pins to be modified.
| `number` | New pin number for pin.  It is recommended that this parameter must be used only with single pins sent in, as pin numbers MUST be unique.
| `name` | Function pin name for the pin.  Since the actual database function,`pinname`, is a key for the function pin definition, this must be unique within the function definition. However, if a non-unique value is supplied, or the string is not valid for a function pin name (such as it contains lower case characters), the name supplied here is stored as the Verilog\_Port\_Name for the pin and a legal unique PinName is derived from this name to generate a unique key for the database.
| `use` | New pin use for the pin.  If changing the pin use from power/ground to a signal pin, function pins are created. In the reverse scenario -- changing pinuse from signal to power/ground -- function pins are removed.
| `padstack` | New padstack to be used for the specified pin.
| `rotation` | New rotation of pin (on the specific symbol instance as currently placed in the design). Symbol definition pin is updated to compensate for final instance rotation.
| `swapCode` | New swap code group index for pin.
#### Value Returned

|  |
| --- | ---
| `t` | Returned when at least one pin is modified.
| `nil` | Returned in case there is an an error modifying any of the pins.
#### See Also

[axlCompAddPin](#1091129 "9")`,`[axlCompDeletePin](#1085880 "9")`,`[axlCompMovePin](#1085881 "9")

### axlDBIsBondingWireLayer

`axlDBIsBondingWireLayer(t_layerName)⇒ t/nil`

#### Description

This is an obsolete function. Bonding wire layers have been replaced by die stack layers. Use`axlDBIsDieStackLayer` to check whether a layer is a die stack layer.

Verifies if a layer is a bonding layer. This means that attribute of the "paramLayer" parameter`dbid` called "type" has a value of "`BONDING _WIRE`".

This is normally used in the APD product.

#### Arguments

|  |
| --- | ---
| `t_layerName` | Layer name, for example, "CONDUCTOR/<`subclass`>"  **Note:** CONDUCTOR is ETCH in Allegro PCB Editor.
#### Value Returned

|  |
| --- | ---
| `t` | Layer is a bonding layer.
| `nil` | Layer is not a bonding layer.
#### See Also

[axlDBIsBondwire](#1092539 "9")

#### Example

`axlDBIsBondingWireLayer("CONDUCTOR/TOP_COND")-> nil`

### axlDBIsBondpad

`axlDBIsBondpad(o_dbid)⇒ t/nil`

#### Description

Verifies whether or not the given element is a*bondpad*.

A*bondpad* (or *bondfinger*) is a `"via"` with the `BOND_PAD` property.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of the element to be checked.
#### Value Returned

|  |
| --- | ---
| `t` | `o_dbid` is a bondpad.
| `nil` | `o_dbid` is not a bondpad.
### axlDBIsBondwire

`axlDBIsBondwire(o_dbid)⇒ t/nil`

#### Description

Verifies whether or not the given element is a*bonding wire*.

A*bonding wire* (or *bondingfinger*) is a`"via"` (can be through hole or blind/buried) with either the`"beginning"` or `"ending"` (if the via has been mirrored) layer type set to the `BondingWire` property.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of the element to check.
#### Value Returned

|  |
| --- | ---
| `t` | `o_dbid` is a bonding wire.
| `nil` | `o_dbid` is not a bonding wire.
### axlDBIsDiePad

`axlDBIsDiePad(rd_dbid)⇒ t/nil`

#### Description

Verifies whether or not the given element is a*die pad*.

A*die pad* is a pin with a component class of `IC`.

#### Arguments

|  |
| --- | ---
| `rd_dbid` | `dbid` of the element to check.
#### Value Returned

|  |
| --- | ---
| `t` | `rd_dbid` is a die pad.
| `nil` | `rd_dbid` is not a die pad.
### axlDBIsPlatingbarPin

`axlDBIsPlatingbarPin(rd_dbid)⇒ t/nil`

#### Description

Verifies whether or not the given element is a*plating bar pin*.

A*plating bar pin* is a pin with a component class of `DISCRETE` or `PLATING_BAR`.

#### Arguments

|  |
| --- | ---
| `rd_dbid` | `dbid` of the element to check.
#### Value Returned

|  |
| --- | ---
| `t` | `rd_dbid` is a plating bar pin.
| `nil` | `rd_dbid` is not a plating bar pin.
### axlGetDieType

`axlGetDieType(o_componentDBID)==> t_dieType`

#### Description

Returns the die attachment type for a given die component in a Cadence packaging tool (APD/SIP). A die is considered to be an IC class component in the database. Currently, the supported attachment types include the following:

* WIREBOND

* FLIP CHIP

#### Arguments

|  |
| --- | ---
| `Component DBID` | `dbid` handle of the die component to query.
#### Value Returned

|  |
| --- | ---
| `t_dieType` | If successful.
| `nil` | If failed (non-die object passed or not a packaging product).
#### Examples

`axlGetDieType(myComp)`

`==> "FLIP CHIP"`

### axlGetMetalUsageForLayer

`axlGetMetalUsageForLayer(l_layers [l_extents][g_positive])==> resultStruct/nil`

#### Description

Computes the percentage metal coverage on the layers specified in l\_layer(s) (combination of all layers listed) in the area specified in`l_extents`. If no extents are provided, then the geometry outline extents of the design are used.

Negative layer metal coverage can be computed by passing nil for g\_positive, if processing negative artwork layers such as solder mask layers.

#### Arguments

|  |
| --- | ---
| `l_layers` | A single layer or list of layers to compute the (combined) metal usage on. For example, passing list("CONDUCTOR/TOP" "PIN/TOP") will compute the coverage of all conductor + pin objects on the top layer. It will not compute the two individually.
| `l_extents` | BBox region to compute metal coverage in. If not supplied, the tool will compute based on the substrate geometry outline's extents or, if no outline is present, the database extents.
| `g_positive` | Whether the layer(s) being processed are positive or negative layers. Defaults to true.
#### Value Returned

* `resultStruct/nil` - resultStruct is a defstruct containing for elements:

* `areaUnits` - Units in which the area was computed and returned.

* `regionArea` - The area of the extents region the tool used (user supplied or drawing extents).

* `metalArea` - The total metal area in the region checked on the layers indicated.

* `percentMetalCoverage` - The percentage of the extents region covered by metal. Calculated as `((metalArea / regionArea) * 100.0)`

* `nil` is returned if there is an error, with error printed to command line.

### axlGetWireProfileDefinition

`list axlGetWireProfileDefinition(profileName)`

#### Description

Given a bonding wire profile name, this will returns its definition information.

#### Arguments

|  |
| --- | ---
| `profileName` | Name of the profile definition being queried. If this argument is`nil`, definitions of all profiles in design are retrieved.
#### Value Returned

Structure of information describing the profile definition (material, 3d points list, etc).

In case of failure, an error string is returned.

### axlAddAutoAssignNetAlgorithm

`axlAddAutoAssignNetAlgorithm(t_algorithm t_displayName)==> t/nil`

#### Description

This function allows the user to add custom auto net assignment algorithms to the list in the Logic -> Auto Assign Net command's algorithms list in the APD and SIP IC Packaging tools. This list will always contain the Cadence standard algorithms (Router-Based, Nearest Match, and Constraint-Driven).

These names cannot be duplicate or overwritten by the customer.

Specifying a pair with either a duplicate algorithm or display name will cause the currently-existing (user) entry to be replaced.

#### Arguments

|  |
| --- | ---
| `t_algorithm` | Text string (case sensitive) containing the name of the skill function to be called for this algorithm. The function must take two parameters:  First parameter: List of source pins.  Second parameter: List of destination pins.  The function should return "FAIL" if it was unable to complete due to some manner of code failure, or else should return a list of source pins that are still unassigned.
| `t_displayName` | Text string (also case sensitive) that will be used as the name of this algorithm in the auto assign net command's pull-down menu for selecting the algorithm to use.
#### Value Returned

`t` if algorithm successfully registered.

`nil` if registration failed (function not defined, name in use, etc).

### axlGetWireProfileDirection

`axlGetWireProfileDirection(profileName)==> "FORWARD"/"REVERSE"/nil`

#### Description

This function returns the direction of a wire profile definition defined in the database. Profiles may be either forward or reverse. If the profile definition name provided does not exist in the design, the return value will be`nil`.

#### Arguments

|  |
| --- | ---
| `profileName` | The name of the wire profile to query the direction of.
#### Value Returned

* `"FORWARD"` for forward-bond wire profile definitions.

* `"REVERSE"` for reverse-bond wire profile definitions.

* `nil` if the wire profile definition does not exist in the database.

### axlGetAllVisibleProfiles

`axlGetAllVisibleProfiles()==> list of profiles / nil`

#### Description

Returns a list of all the bond wire profiles currently visible in the design.

#### Arguments

Nothing.

#### Value Returned

* list of profile names.

* `nil` if error or no profiles visible.

### axlSetAllProfilesVisible

`axlSetAllProfilesVisible(visible)==> t / nil`

#### Description

Turns all wire profiles in the design on or off.

#### Arguments

|  |
| --- | ---
| `visible` | `t` to turn all profiles on, `nil` to turn them off.
#### Value Returned

`t`/`nil` to indicate success or failure.

### axlSetBondWireProfile

`axlSetBondWireProfile(bondWiresprofileName)==> t/nil`

#### Description

This command allows you to change the bond wire profile on one or more bond wires in the design. The bond wire profile definition must already exist in the design.

> **Note:** Changing a wire's profile changes not just the profile name, but also the wire's material and its diameter or width to match the new profile definition.

#### Argument

|  |
| --- | ---
| `bondWires` | either a dbid or a list of dbids representing the bond wires to be modified.
| `profileName` | the name of the new bond wire profile to assign to the bond wire(s).
#### Value Returned

|  |
| --- | ---
| `t` | if profile is defined and one or more bond wires were modified.
| `nil` | if an error occurred or no bond wires were modified.
**Note:** It is much more efficient to assign a wire profile to all bond wires, which should be set to that profile, in a single call to this function, than to call the function on each individual bond wire.

### axlImportWireProfileDefinitions

`axlImportWireProfileDefinitions(xmlFileNamesetAsMaster)==> x/nil`

#### Description

This function will import the bond wire profiles defined in the xml file specified. If a profile is defined both in the XML file and in the current design, the design's definition will be updated to match the new definition being imported.

#### Argument

|  |
| --- | ---
| `xmlFileName` | The name of the XML file on disk which includes the bond wire profile definitions to be read. If not in the current working directory, this should include the absolute or relative path to the XML file.
| `setAsMaster` | If true, this XML file will be set as the master profile definitions file for this database. The master file is where the user can refresh profile definitions from if they are changed. Only one file is allowed to be the master.
#### Value Returned

* `x`, the number of profile definitions successfully imported.

* `nil` if an error occurred (message printed to status window).

### axlSetBondWireProfile

`axlSetBondWireProfile(`

`bondWires`

`profileName`

`)`

`==> t/nil`

#### Description

This command allows you to change the bond wire profile on one or more bond wires in the design. The bond wire profile definition must already exist in the design. Note that changing a wire's profile will change not just the profile name, but also the wire's material and its diameter or width to match the new profile definition.

**Note:** It is much more efficient to assign a wire profile to ALL bond wires which should be set to that profile in a single call to this function, than to call the function on each individual bond wire.

#### Argument

|  |
| --- | ---
| `bondWires` | either a dbid or a list of dbids representing the bond wires to be modified.
| `profileName` | the name of the new bond wire profile to assign to the bond wire(s).
#### Value Returned

* `t`, if profile is defined and one or more bond wires was modified.

`nil` if an error occurred or no bond wires were modified.

### axlSetDieStackData

`axlSetDieData (g_stackIds_dataTypeg_newValue)==> t/nil`

#### Description

This function sets the given data for the specified die.

**Note:** The command is available only in SIP products.

#### Arguments

|  |
| --- | ---
| `g_stackId` | Name or dbid of the die stack to get the data for.
| `s_dataType` | Data type of the given value, one of the following:  `'(DSA_CAVITY_DEPTH`  `DSA_CAVITY_LAYER`  `DSA_CAVITY_DIMENSION``)`
|
|
|
| `g_newValue` | New value for the specified data type.
#### Value Returned

`t` on success, otherwise `nil`

### axlDBIsDieStackLayer

`axlDBIsDieStackLayer (t_layerName)==> t or nil`

#### Description

Verifies if layer is a die stack layer. This means that the attribute of the`"paramLayer"` parameter `dbid` called `"type"` has a value of `"DIESTACK"`. This is normally used in the APD product.

#### Arguments

`t_layerName` Layer name `"CONDUCTOR/<subclass>"`

**Note:** CONDUCTOR is ETCH in Allegro PCB Editor

#### Value Returned

`t` If die stack layer.

`nil` If not.

#### See Also

[axlDBIsBondwire](#1092539 "9")

#### Examples

`axlDBIsDieStackLayer("CONDUCTOR/TOP_COND") -> nil`

### axlGetDieData

`axlGetDieData (g_dieId)==> die-data defstruct/nil`

#### Description

Gets the data for the given die and loads it into the a defstruct.

Only available in SIP products.

#### Arguments

`g_dieName` `refdes` or `dbid` of the given die.

#### Value Returned

|  |
| --- | ---
| `dieData` | defstruct with data for the given die.
| `nil` | Die does not exist or there was an error.
defstruct fields:

`dbid` dbid of die

`refId` die refdes

`memberType` DSA\_DIE

`stackName` parent die-stack name

`stackPosition` integer position of member in stack

`layerName` die pad layer

`dieThickness` die thickness (flipchip bumps not included)

`totalThickness` die thickness (flipchip bumps included)

`stackHeightMin` starting height within stack

`stackHeightMax` ending height within stack

`origin` die symbol x/y location

`rotation` rotation angle in degrees

`extents` unioned extents of all members in stack

`type` one of DSA\_DIE\_STANDARD or DSA\_DIE\_CODESIGN

`attachType` one of DSA\_DIE\_FLIPCHIP or DSA\_DIE\_WIREBOND

`orientation` one of DSA\_DIE\_CHIPUP or DSA\_DIE\_CHIPDOWN

`bumpDiamAtPkg` flipchip bump diameter at package

`bumpDiamAtDie` flipchip bump diameter at die

`bumpDiamMax` flipchip bump diameter maximum

`bumpHeight` flipchip bump height

`bumpEcond` flipchip electrical conductivity w/units

#### Example

`data = axlGetDieData("FLIPCHIP_1")`

`printf("stack-pos = %L, layer-name = %L, attach-type = %L\n"`

`data->stackPosition data->layerName data->attachType)`

`==> stack-pos = 1, layer-name = "TOP_COND", attach-type = DSA_DIE_FLIPCHIP`

### axlGetDieStackData

`axlGetDieStackData (g_stackArg)==> stack-data defstruct/nil`

#### Description

Gets the data for the given die-stack and loads it into a defstruct.

Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_stackArg` | name or`dbid` of the given die-stack
#### Value Returned

|  |
| --- | ---
| `stackData` | defstruct with data for the given die stack.
| `nil` | Die stack does not exist or there was an error.
defstruct fields:

|  |
| --- | ---
| `dbid` | dbid of member
| `refId` | member name
| `surface` | one of DSA\_SUBSTRATE\_CAVITY\_TOP, DSA\_SUBSTRATE\_CAVITY\_BOTTOM  DSA\_SUBSTRATE\_TOP, DSA\_SUBSTRATE\_BOTTOM,
| `depth` | for cavity-placed dies, gives the number of layers below the surface the stack is placed
| `cavityClearance` | For cavity-placed stacks, the clearance from the stack extents to the edge of the cavity on the lowest layer.
| `cavityExpansion` | For cavity-placed stacks, the amount by which the cavity grows on each subsequent layer (the "width" of the stadium step).
| `stackHeightMin` | starting height within stack
| `stackHeightMax` | ending height within stack
| `rotation` | rotation angle in degrees
| `extents` | unioned extents of all members in stack
#### Example

`data = axlGetDieStackData("DIESTACK1")`

`printf("name = %L, minHeight = %L, maxheight = %L\n"`

`data->name data->stackHeightMin data->stackHeightMax)`

`==> name = "DIESTACK1", minHeight = 0.0, maxheight = 496.0`

### axlGetDieStackMemberSet

`axlGetDieStackMemberSet()==> list of die-stack member defstructs/nil`

#### Description

Returns a list of defstructs - one for each member of the given die stack.

Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_stackArg` | name or`dbid` of the die stack
#### Value Returned

|  |
| --- | ---
| `l_data` | List of die-stack member data defstructs
| `nil` | in case of an error
#### defstruct fields:

|  |
| --- | ---
| `dbid` | `dbid` of member
| `refId` | member name
| `memberType` | one of DSA\_DIE, DSA\_SPACER, DSA\_INTERPOSER
| `stackPosition` | integer position of member in stack
| `layerName` | etch object subclass of member
| `nextMemberOnSameLayer` | flag indicating next member on same layer
| `prevMemberOnSameLayer` | flag indicating previous member on same layer
#### Example

`data = axlGetDieStackMemberSet("DIESTACK1")`

`foreach(member data`

`printf("refId = %L, memberType = %L\n" member->refId`

`member->memberType)`

`)`

`==> refId = "FC1", memberType = DSA_DIE`

`refId = "IPOSER_1", memberType = DSA_INTERPOSER`

`refId = "WB1", memberType = DSA_DIE`

`refId = "SPACER_1", memberType = DSA_SPACER`

`refId = "WB2", memberType = DSA_DIE`

### axlGetDieStackNames

`axlGetDieStackNames() ==> list of die-stack names/nil`

#### Description

Returns a list of the names of all die stacks in the current design.

Only available in ICP products.

#### Arguments

None

#### Value Returned

List of die-stack names or`nil` if none exist

### axlGetIposerData

`axlGetIposerData(g_iposerId)==> iposer-data defstruct/nil`

#### Description

This function fetches the data for the given iposer and loads it into a defstruct.

* Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_iposerName` | name or`dbid` of the given interposer
#### Value Returned

|  |
| --- | ---
| `iposerData` | defstruct with data for the given iposer.
| `nil` | iposer does not exist or there was an error.
defstruct fields:

|  |
| --- | ---
| `dbid` | `dbid` of interposer
| `refId` | interposer ref-id
| `memberType` | DSA\_INTERPOSER
| `stackName` | parent die-stack name
| `stackPosition` | integer position of member in stack
| `layerName` | etch-object layer (vias/clines/shapes)
| `totalThickness` | dielectric + conductor thickness
| `stackHeightMin` | starting height within stack
| `stackHeightMax` | ending height within stack
| `origin` | interposer symbol x/y location
| `rotation` | rotation angle in degrees
| `extents` | unioned extents of all members in stack
| `dielMatl` | name of dielectric material used for substrate
| `dielThickness` | thickness of dielectric material
| `condMatl` | name of conductor material used for etch objects
| `condThickness` | thickness of conductor material
#### Example

`data = axlGetDieData("IPOSER_1")`

`printf("stack-pos = %L, layer-name = %L, thickness = %L\n"`

`data->stackPosition data->layerName data->totalThickness)`

`==> stack-pos = 4, layer-name = "IP1", thickness = 106.0`

### axlGetSpacerData

`axlGetSpacerData(g_spacerId)==> spacer-data defstruct/nil`

#### Description

Gets the data for the given spacer and loads it into a defstruct.

* Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_spacerName` | name or*dbid* of the given spacer
#### Value Returned

|  |
| --- | ---
| `spacerData` | defstruct with data for the given spacer.
| `nil` | Spacer does not exist or there was an error.
defstruct fields:

|  |
| --- | ---
| `dbid` | `dbid` of spacer
| `refId` | spacer ref-id
| `memberType` | DSA\_INTERPOSER
| `stackName` | parent die-stack name
| `stackPosition` | integer position of member in stack
| `layerName` | etch-object layer (vias/clines/shapes)
| `totalThickness` | dielectric + conductor thickness
| `stackHeightMin` | starting height within stack
| `stackHeightMax` | ending height within stack
| `origin` | spacer symbol x/y location
| `rotation` | rotation angle in degrees
| `extents` | unioned extents of all members in stack
| `dielMatl` | name of dielectric material used for substrate
| `dielThickness` | thickness of dielectric material
#### Example

`data = axlGetDieData("SPACER_1")`

`printf("stack-pos = %L, layer-name = %L, diel-matl = %L\n"`

`data->stackPosition data->layerName data->dielMatl)`

`==> stack-pos = 4, layer-name = "SP1", diel-matl = "PHENOLIC"`

### axlGetWireProfileColor

`axlGetWireProfileColor(t_profile)==> color index / nil`

#### Description

This function will retrieve the color index associated with a bond wire profile. If no profile matching the name supplied is found in the database, nil is returned.

#### Arguments

|  |
| --- | ---
| `t_profile` | Name of profile to retrieve color for.
#### Value Returned

Color number assigned to profile if the profile is found.

`nil` if an error occurred or profile not found.

### axlGetWireProfileVisible

`axlGetWireProfileVisible(t_profile)==> t / nil`

#### Description

This function will retrieve the visibility status of a bond wire profile. If no profile matching the name supplied is found in the database, nil is returned.

#### Arguments

|  |
| --- | ---
| `t_profile` | Name of profile to retrieve color for.
#### Value Returned

`t:` if wire profile exists and is visible.

`nil:` if profile is invisible or does not exist.

### axlPackageDesignCheckAddCategory

```
axlPackageDesignCheckAddCategory(t_namet_bitmapt_description)==> g_category / nil
```

#### Description

This function will register a new category inside the IC Packaging tools' "package integrity" command check tree.

You must define a category before adding checks to it. So, this function should always be called prior to[axlPackageDesignCheckAddCheck](#1085976 "9").

A newly added category will be inserted into the tree in alphabetically sorted order. Therefore, you do not need to manage the order categories are added by yourself.

**Note:** If the category name already exists, it will not be redefined.

#### Arguments

|  |
| --- | ---
| `t_name` | Name of the category of checks as it should appear in the user interface. This name should be used when calling[axlPackageDesignCheckAddCheck](#1085976 "9") to add specific checks.
| `t_bitmap` | Name of the bitmap file which should be shown when this check category is active in the user interface. This should be a full path to the bitmap or else the bitmap must be resolvable through BMPPATH.
| `t_description` | The description to be displayed in the GUI when this category is highlighted.
#### Value Returned

|  |
| --- | ---
| g\_category | Skill defstruct defining the category.
#### See Also

[axlPackageDesignCheckAddCheck](#1085976 "9")

#### Example

The following example add a new integrity check category for subsequent addition of usr-defined rules:

```
axlPackageDesignCheckAddCategory("User-Defined Rules" "user_defined.bmp" "Descriptive Text")==> g_category
```

The next time the Package Integrity Check tool is run, a new category will be shown, named "User-Defined Rules".

### axlPackageDesignCheckAddCheck

```
axlPackageDesignCheckAddCheck(t_category t_name t_bitmap t_descriptions_runCommand g_fixable) ==> defstruct defining check.
```

#### Description

This function will register a new check in the specified category of the IC Packaging tools' "package integrity" command check tree.

You must define a category before adding checks to it. So, this function should always be called after[axlPackageDesignCheckAddCategory](#1085975 "9").

A newly added check will be inserted into the tree in alphabetically sorted order. Therefore, you do not need to manage the order checks are added by yourself.

`s_runCommand` is the skill function which should be called if this check is selected to run. This function MUST adhere to the following guidelines:

* It must take exactly one argument, which is whether to fix errors it encounters or not.

* It must return an integer value for how many errors were found in the database.

* It must call the following functions:

> `axlPackageDesignCheckLogError(<error string> <fixed>)`

> and

> `axlPackageDesignCheckDrcError(<error location> <dbids>)`

> to report any errors it finds.

These restrictions are imposed to ensure that output is consistent across all checks run by this command.

#### Arguments

|  |
| --- | ---
| `t_category` | Name of the category this check should be placed under in the user interface tree. This should be the same name as sent to[axlPackageDesignCheckAddCategory](#1085975 "9").
| `t_name` | Name of the check as it should appear in the user interface. This will be the name given to the check in the resulting log file, and will be the description for any external DRCs created.
| `t_bitmap` | Name of the bitmap file that should be shown when this check is active in the user interface. This should be a full path to the bitmap or else the bitmap must be resolvable through`BMPPATH`.
| `t_description` | The description to be displayed in the GUI when this check is highlighted. This description will also be printed to the log file ahead of any violations found for this check. As a result, the description should be as descriptive as possible in order to maximize its usefulness.
| `s_runCommand` | A symbol representing the function to be called to check this rule. See FUNCTION description for details about the required format and return value of this function.
| `g_fixable` | Boolean flag to tell the user on the interface whether problems found by this check can be automatically fixed or not.
#### Value Returned

|  |
| --- | ---
| `g_check` | Skill defstruct defining the check.
#### Example

The following example adds a new integrity check to the "User-Defined Rules" category in the Package Integrity Check user interface.

```
axlPackageDesignCheckAddCheck("User-Defined Rules" "My First Rule" "user_defined.bmp" "Descriptive Text" 'myCheckFunction t))==> g_check
```

The next time the Package Integrity Check tool is run, "My First Rule" will be available under the "User-Defined Rules" category.

#### See Also

[axlPackageDesignCheckAddCategory](#1085975 "9"), [axlPackageDesignCheckLogError](#1077751 "9"), [axlPackageDesignCheckDrcError](#1085977 "9")

### axlPackageDesignCheckDrcError

`axlPackageDesignCheckDrcError(l_location o_dbids)==> nil`

#### Description

This function will create an external DRC marker for an error found by the currently running package integrity check. The tool itself will track the check being run so that it knows the name to use for the rule violation.

#### Arguments

|  |
| --- | ---
| `l_location` | Location at which to place the DRC marker.
| `o_dbids` | Optional list of database object ids that are associated with this error. Usually 0-2 objects are affected.
#### Value Returned

`nil`

#### Example

The following example creates a DRC marker about a missing via found with a fictional rule. In this case, since the via is missing, no dbids for objects are passed in:

`axlPackageDesignCheckDrcError((0.0 0.0) nil)==> nil`

In the canvas, an external DRC marker is created at (0.0 0.0) with the name of the user-defined rule that generated the error.

#### See Also

[axlPackageDesignCheckAddCheck](#1085976 "9"), [axlPackageDesignCheckLogError](#1077751 "9")

### axlPackageDesignCheckLogError

`axlPackageDesignCheckLogError(t_errorStringg_fixedg_location)==> nil`

#### Description

This function will log an error found by this function to the log file if the log file is enabled. By using this interface, you are ensuring that the API will format your message consistently.

#### Arguments

|  |
| --- | ---
| `t_errorString` | String to be printed to the log file. This should have all variable substitutions already done and be a simple string. This function will take care of any formatting necessary.
| `g_fixed` | Boolean indicating whether the error was fixed by the tool.
| `g_location` | Location where the error occurred, if applicable. This is appended to your log entry for you, and is used to let the user zoom to the error location in the design. If the location is unknown or not applicable, pass nil for the location.
#### Value Returned

`nil`

#### Example

The following example logs an error about a missing via found with a fictional rule. The error was not fixed by the caller:

`axlPackageDesignCheckLogError("Missing via" nil (0.0 0.0))==> nil`

In the log file, the following is printed under the heading of the user-defined rule that found it:

> `"- Missing via at (0.0 0.0)"`

#### See Also

[axlPackageDesignCheckAddCheck](#1085976 "9"), [axlPackageDesignCheckDrcError](#1085977 "9")

### axlSetDieData

`axlSetDieData(g_dieIds_dataTypeg_newValue)==> t/nil`

#### Description

Sets the given data for the given die.

* Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_dieName` | name or`dbid` of the die to get the data for
| `s_dataType` | data type of the given value, one of:  `'(DSA_BUMP_PACKAGE_DIAM_DBREP`  `DSA_BUMP_PACKAGE_DIAM_STRING`  `DSA_BUMP_DIE_DIAM_DBREP`  `DSA_BUMP_DIE_DIAM_STRING`  `DSA_BUMP_MAX_DIAM_DBREP`  `DSA_BUMP_MAX_DIAM_STRING`  `DSA_BUMP_HEIGHT_DBREP`  `DSA_BUMP_HEIGHT_STRING`  `DSA_BUMP_ECOND_STRING`  `DSA_DIE_THICKNESS_DBREP`  `DSA_DIE_THICKNESS_STRING)`
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
| `g_newValue` | new value for the specified data type.
#### Value Returned

`t` on success, otherwise `nil`

### axlSetDieType

`axlSetDieType(o_componentDBIDt_dieType)==> t/nil`

#### Description

This function sets the attachment type for a die component to one of the available types. Currently, the supported attachment types are:

|  |  |
| --- | --- | ---
|  |  | WIREBOND
|  |  |
| --- | --- | ---
|  |  | FLIP CHIP
#### Arguments

|  |
| --- | ---
| `o_componentDBID` | dbid handle of the die component to be configured.
| `t_dieType` | Attachment type to configure this component as. Supported values are "WIREBOND" and "FLIP CHIP".
#### Value Returned

|  |
| --- | ---
| `t` | if successful.
| `nil` | if failed (non-die object passed or not packaging product).
#### Example

`axlSetDieType(myComp "WIREBOND")`

`==> t`

### axlSetIposerData

`axlSetIposerData(g_iposerIds_dataTypeg_newValue)==> t/nil`

#### Description

Sets the given data for the given iposer.

Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_iposerName` | name or`dbid` of the given iposer
| `s_dataType` | data type of the given value, one of:  `'(DSA_CONDUCTOR_MATERIAL`  `DSA_CONDUCTOR_THICKNESS_DBREP`  `DSA_CONDUCTOR_THICKNESS_STRING`  `DSA_DIELECTRIC_MATERIAL`  `DSA_DIELECTRIC_THICKNESS_DBREP`  `DSA_DIELECTRIC_THICKNESS_STRING`  `DSA_PART_NUMBER)`
|
|
|
|
|
|
|
| `g_newValue` | new value for the specified data type
#### Value Returned

`t` on success, otherwise `nil`

### axlSetSpacerData

`axlSetSpacerData(g_spacerIds_dataTypeg_newValue)==> t/nil`

#### Description

This function sets the given data for the given spacer.

* Only available in SIP products.

#### Arguments

|  |
| --- | ---
| `g_spacerName` | name or dbid of the spacer to get the data for
| `s_dataType` | data type of the given value, one of:  `'(DSA_DIELECTRIC_MATERIAL`  `DSA_DIELECTRIC_THICKNESS_DBREP`  `DSA_DIELECTRIC_THICKNESS_STRING`  `DSA_PART_NUMBER)`
|
|
|
|
| `g_newValue` | new value for the specified data type.
#### Value Returned

`t` on success, otherwise `nil`

### axlSetWireProfileColor

`axlSetWireProfileColor(t_profile n_color)==> t / nil`

#### Description

This function will set the color of a wire profile to the given value.

#### Arguments

|  |
| --- | ---
| `t_profile` | Name of profile to retrieve color for.
| `n_color` | Color index to assign to the profile.
#### Value Returned

t, if successful.

`nil`, if error (profile does not exist).

### axlSetWireProfileVisible

`axlSetWireProfileVisible(t_profile g_visible)==> t / nil`

Description

This function will make the identified wire profile visible or invisible.

#### Arguments

|  |
| --- | ---
| `t_profile` | Name of profile to retrieve color for.
| `g_visible` | t for visible, nil for invisible.
#### Value Returned

* `t`, if successful.

* `nil`, if error (profile does not exist).




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
