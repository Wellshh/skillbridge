<!--
source: algroskill/18consmgt.md
part: 2/2
estimated_tokens: 8013
-->

For a list of physical constraints, see`axlCNSGetPhysical`. If adding/deleting individual vias, you may find it easier to use `axlCnsAddVia` and `axlCnsDeleteVia`.

* ***Same\_net behavior will change in 16.2. This does not change override values. For example, you can set width\_min value in all csets, but if the you applied it to a net or constraint area as an override, it will still be used for those items.***

#### Arguments

|  |
| --- | ---
| `t_cset` | Cset name. You can use "" for the DEFAULT cset. Use`nil` to apply changes to all csets.
| `t_layer` | ETCH layer name (for example, "ETCH/TOP" or "TOP"). If nil, applies changes to all layers.
| `s_constraint` | Constraint symbol to change. Use`axlCNSGetPhysical(nil nil nil)` for list of permissible values.
| `g_value` | Value to update. For data types, see Data Types above.
| `ll_constraintValues` | Multiple values may be updated by passing a list of lists for the third argument.  '((s\_constraint g\_value) ... )
|
#### Value Returned

|  |
| --- | ---
| `t` | Success.
| `nil` | An error occurs when the ECset name does not exist; the layer does not exist; the constraint does not exist; the value for the constraint is illegal; or the cset is locked.
#### Example 1

> `axlCNSSetPhysical(nil nil 'width_min 5)`

Sets minimum line width on all constraints and layers

**Example 2**

> `axlCNSSetPhysical("" nil 'allow_etch t)`

Sets`allow_etch` on all layers in default cset.

**Example 3**

> `axlCNSSetPhysical("VOLTAGE" "top" 'allow_ts "NOT_ALLOWED")`

Doesn't allow Ts on top layer of VOLTAGE cset.

**Example 4**

> `axlCNSSetPhysical("VOLTAGE" "top" 'allow_ts 'NOT_ALLOWED)`

Uses the same value.

#### See Also

[axlCNSGetPhysical](#1083339 "19")`,`[axlCNSMapClear](#1076663 "19")`,`[axlCNSMapUpdate](#1074801 "19")[axlCnsAddVia](#1104370 "19")`,` and [axlCnsDeleteVia](#1092387 "19")

### axlCNSSetSpacing

`axlCNSSetSpacing(t_cset/nilt_layer/nils_constraintg_value)==> t/nil`

`axlCNSSetSpacing(t_cset/nilt_layer/nilll_constraintValuesnil)==> t/nil`

#### Description

Allows updating spacing constraint values. By passing`nil`at the appropriate argument, values for all csets and all layers may be changed.

#### Data types

See[axlCNSGetSpacing](#1093423 "19") for the data type of each constraint.

Allowed Design Units:

* A number (integer or floating point) where units is current design units. Must not exceed accuracy of the design.

* Unitless string where accuracy cannot exceed database accuracy.

* String with units, data converted to current design units.

Allowed Data Values:

* Boolean: Use`t/nil` or `"true"/"false"`.

* 1) For best performance, when calling multiple`axlCNS`interfaces to update constraint values, wrap them in the `axlCnsMap` interfaces as shown below:

`axlCNSMapClear()`

`axlCNSSetSpacing(nil nil 'line_shape 10.0)`

`axlCNSSetSpacing("" nil 'line_line 5)`

`...`

`axlCNSMapUpdate()`

> 2) Single change calls do not require this. For a list of current spacing constraints, see[axlCNSGetSpacing](#1093423 "19")`.`

* ***Same\_net constraint has been moved to the same net spacing domain. An idiosyncrasy when values sent as strings requires the number of decimal points to be no more than the current database accuracy, or the change will be rejected. This does NOT change override values. For example, you can change the line to line value in all csets but if you have applied a net or constraint area override, it will still be used for those items.***

#### Arguments

|  |
| --- | ---
| `t_cset` | The cset name. You can use "" for DEFAULT cset. Use`nil`to apply the changes to all csets.
| `t_layer` | The ETCH layer name (e.g "ETCH/TOP" or "TOP"). If`nil,` applies the changes to all layers.
| `s_constraint` | Constraint symbol to change. Use`axlCNSGetPhysical(nil nil nil)` for a list of permissible values.
| `g_value` | Value to update. For data types, see[Data types](#1084427 "19") above.
| `ll_constraintValues` | Multiple values may be updated by passing a list of lists for the third argument.  '((s\_constraint g\_value) ... )
|
#### Value Returned

|  |
| --- | ---
| `t` | Success.
| `nil` | Indicates an error. An error occurs when the ECset name does not exist; the layer does not exist; the constraint does not exist; the value for the constraint is illegal; or the cset is locked.
#### Examples

* Set line to shape spacing in all csets, all layers

> `axlCNSSetSpacing(nil nil 'line_shape 5)`

* Set line to line spacing to 5 on DEFAULT cset, all layers

> `axlCNSSetSpacing("" nil 'line_line 5)`

* Value of DEFAULT cset

> `axlCNSSetSpacing("25_MIL_SPACE" "top" 'line_line 5)`

* Set a single spacing for all ids for all layers

> `cnsIds = axlCNSGetSpacing(nil nil nil)`

> `values = nil`

> `defaultSpace = 10.0`

> `foreach( id cnsIds`

> `values = cons(list(id defaultSpace) values)`

> `)`

> `axlCNSSetSpacing("10_MIL_SPACE" nil values)`

#### See Also

[axlCNSGetSpacing](#1093423 "19")`,`[axlCNSMapClear](#1076663 "19")`,`and [axlCNSMapUpdate](#1074801 "19")

### axlCNSSetPinDelayEnabled

`axlCNSSetPinDelayEnabled(g_value) => t`

#### Description

Enables or disables Pin Delay.

#### Argument

|  |
| --- | ---
| `g_value:` | `t` or `nil` to indicate if Pin Delay is turned on or off.
#### Value Returned

`t`

### axlCNSSetPinDelayPVF

`axlCNSSetPinDelayPVF(g_value) => t/nil`

#### Description

Sets a value for pin delay propagation velocity.

#### Arguments

|  |
| --- | ---
| `g_value:` | a string to define the new pin delay propagation velocity factor. A`nil` value indicates that the value is to be deleted.
Value Returned

|  |
| --- | ---
| `t:` | no errors
| `nil:` | error detected
### axlCNSSetSameNet

`axlCNSSetSameNet(t_cset/nilt_layer/nils_constraintg_value)==> t/nil`

`axlCNSSetSameNet(t_cset/nilt_layer/nilll_constraintValuesnil)==> t/nil`

#### Description

Documentation same as[axlCNSSetSpacing](#1111453 "19").

#### Arguments

|  |
| --- | ---
| `t_cset:` | cset name, can use "" for DEFAULT cset. Use`nil` to apply change to all cset.
| `t_layer:` | ETCH layer name ( "ETCH/TOP" or "TOP"). If`nil` apply change to all layers.
| `s_contraint:` | Constraint symbol to change. Use`axlCNSGetSameNet`(`nil nil nil`) for list of permissible values.
| `g_value:` | Value to update. For data type, see above for "DATA TYPES".
| `ll_constraintValues:` | Multiple values may be updated by passing a list of lists for the third argument. '((s\_contraint g\_value) ... )
#### Value Returned

|  |
| --- | ---
| `t` | if succeeds
| `nil` | an error  - ecset name does not exit  - layer does not exist  - contraint does not exist  - illegal value for constraint  - cset is locked
|
|
|
|
|
#### See Also

[axlCNSGetSameNet](#1092689 "19"), [axlCNSSetSpacing](#1111453 "19")

#### Examples

Set line to same net spacing in all csets, all layers

> `axlCNSSetSameNet(nil nil 'line_shape 5)`

Set line to line same net to 5 on DEFAULT cset, all layers

> `axlCNSSetSameNet("" nil 'line_line 5)`

Value of DEFAULT cset

> `axlCNSSetSameNet("25_MIL_SPACE" "top" 'line_line 5)`

### axlCNSSetSameNetXtalkEnabled

`axlCNSSetSameNetXtalkEnabled(g_value)=> t`

#### Description

Enables or disables Same Net Xtalk.

#### Arguments

|  |
| --- | ---
| `g_value:` | `t` or `nil` to indicate if same net Xnet is turned on or off.
#### Value Returned

`t`

### axlCNSSetViaZEnabled

`axlCNSSetViaZEnabledenabled(g_value) => t`

#### Description

Enables or disables Via Z.

#### Arguments

|  |
| --- | ---
| `g_value:` | `t` or `nil` to indicate if Via Z is turned on or off.
#### Value Returned

`t`

### axlCNSSetViaZPVF

`axlCNSSetViaZPVF(g_value)=> t/nil`

#### Description

Sets a value for Via Z propagation velocity factor.

#### Arguments

|  |
| --- | ---
| `g_value:` | a string to define the new via Z propagation velocity factor. A`nil` value indicates that the value is to be deleted.
#### Value Returned

|  |
| --- | ---
| `t:` | no errors
| `nil:` | error detected
### axlCNSSpacingMax

`axlCNSSpacingMax([s_spacingType][t_layer])=> f_maxSpacing`

#### Description

Returns maximum spacing in design. This can be worst case spacing of entire design or base upon the object filtering.

Maximum spacing is calculated from all spacings in the domains of spacing, same net, and assembly (APD or SIP). The state of the check (on/off) is ignored (this is different from the minimum spacing API).

#### Arguments

|  |
| --- | ---
| `s_spacingType` | Symbol representing the spacing constraint type. The supported values are:  `'line`, `'shape`, `'via`, `'pin`
| `t_subclassname` | A subclass name of the class ETCH or CONDUCTOR or`nil` for all layers
#### Value Returned

|  |
| --- | ---
| `f_maxSpacing` | Maximum spacing on entire design or sub-filtered setting.
#### Examples

* Get maximum spacing on entire design

> `axlCNSSpacingMax(nil)`

* Get maximum spacing on lines (clines) layer TOP

> `axlCNSSpacingMax('line "TOP")`

* Get maximum spacing on lines (clines) all layers

> `axlCNSSpacingMax('line nil)`

#### See Also

[axlCNSSpacingMin](#1131466 "19")

### axlCNSSpacingMin

`axlCNSSpacingMin([s_spacingType][t_layer])=> f_minSpacing`

#### Description

Returns minimum spacing value in the design. This can be the minimum spacing of entire design or based upon the object filtering.

Maximum spacing is calculated from spacings in the domains of spacing, same net, and assembly (APD or SIP). The spacing check must be enabled (on) to be possibly included as a mimimum.

#### Arguments

|  |
| --- | ---
| `s_spacingType` | Symbol representing the spacing constraint type. The supported values are:  `'line`, `'shape`, `'via`, `'pin`
| `t_subclassname` | A subclass name of the class ETCH or CONDUCTOR or`nil` for all layers
#### Value Returned

|  |
| --- | ---
| `f_minSpacing` | Minimum spacing on entire design or sub-filtered setting.
#### Examples

See Examples section of[axlCNSSpacingMax](#1131567 "19")

#### See Also

[axlCNSSpacingMax](#1131567 "19")

### axlCNSSpacingModeGet

`axlCNSSpacingModeGet(nil) ==> ls_constraints`

`axlCNSSpacingModeGet('all) ==> lls_constraintNModes`

`axlCNSSpacingModeGet(s_name/t_name) ==> s_mode/nil`

#### Description

This fetches the current spacing drc mode(s). Modes determine if a particular constraint is on or off. These modes apply to the entire board. To determine the set currently supported spacing modes do a axlCNSSpacingModeGet(nil).

The spacing mode set may be a subset of spacing values since the implementation may associate certain values under a master mode.

**Note:** Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

|  |
| --- | ---
| `nil:` | returns all modes that are in spacing domain
| `'all:` | returns all checks and current mode
| `s_name:` | symbol name of check.
| `t_name:` | string name of check
#### Value Returned

|  |
| --- | ---
| `ls_names:` | list of checks (s\_name ...)
| `lls_names:` | list of checks and their mode ((s\_name s\_mode) ...)
| `s_mode:` | mode 'on, or 'off
#### See Also

[axlCNSSpacingModeSet](#1096534 "19"), [axlCNSGetSpacing](#1093423 "19")

#### Examples

Get current list of design constraints

> `axlCNSSpacingModeGet(nil)`

Get list of settings for all design constraints

> `axlCNSSpacingModeGet('all)`

Get current setting of line to line

> `axlCNSSpacingModeGet('line_line)`

Get current setting of line to shape using a string

> `axlCNSSpacingModeGet("line_shape")`

### axlCNSSpacingModeSet

`axlCNSSpacingModeSet(t_name/s_namet_mode/s_mode)==> t/nil`

`axlCNSSpacingModeSet('allt_mode/smode)==> t/nil`

`axlCNSSpacingModeSet(l_constraintNModest_mode/smode)==> t/nil`

`axlCNSSpacingModeSet(ll_constraintNModes)==> t/nil`

#### Description

This sets the current drc modes (on/off) for checks in the area of spacing constraints. These modes are global. To determine the constraints modes currently supported do a`axlCNSSpacingModeGet`(nil). We support several interfaces. All checks may be set ('all), individual checks, (t\_name), list of checks with a same mode '(s\_name ...) t\_mode/s\_mode '(t\_name ...) t\_mode/s\_mode and sets of checks via a list of: '((s\_name/t\_name s\_mode/t\_mode) ....) The constraints names may be passed as a symbol or a string. For performance reasons, you should either do all your updates in a single call or wrap individual changes in the map API (see [axlCNSMapUpdate](#1074801 "19")).

**Note:** Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

|  |
| --- | ---
| `s_name:` | symbol name of check.
| `t_name:` | string name of check.
| `s_mode:` | mode setting; may be 'on or 'off.
| `t_mode:` | string mode setting "on or "off"
| `'all:` | set all checks for given tier of Allegro.
#### Value Returned

Returns`t` if succeeds or `nil` if failure.

#### See Also

[axlCNSSpacingModeGet](#1096197 "19"), [axlCNSMapUpdate](#1074801 "19")

#### Examples

Turn off all spacing constraints

> `axlCNSSpacingModeSet('all 'off)`

Turn on line to line check

> `axlCNSSpacingModeSet('line_line 'on)`

Turn two constraints to on

> `axlCNSSpacingModeSet('(line_shape thrupin_line) 'on)`

Set several constraints to different modes

> `axlCNSSpacingModeSet( '((line_line off)`

> `(thrupin_shape on)) )`

### axlCnsPurgeAll()

`axlCnsPurgeAll() -> x_purgeCount`

#### Description

Removes all unused constraint objects and constraint sets. Process all netclasses, regions, physical constraint sets and spacing constraint sets. Deletes all empty netclasses and regions.

#### Arguments

None

#### Value Returned

The count of the deleted items.

#### See Also

[axlCnsPurgeCsets](#1096942 "19")

#### Examples

`axlCnsPurgeAll()`

### axlCnsPurgeCsets

`axlCnsPurgeCsets(list l_type) -> x_purgeCount`

#### Description

Process all constraint sets of the specified domain and delete those without references.

This class of functions is design to help migrate designs to take advantage of the 16.0 constraint model. These functions do have to be used when migrating designs. Before using these functions you need to evaluate your constraint usage.

#### Arguments

Domain of interest 'physical or 'spacing

#### Value Returned

Count of the csets deleted.

#### Examples

> `axlCnsPurgeCsets('physical)`

> `axlCnsPurgeCsets('spacing)`

#### See Also

[axlCnsPurgeObjects](#1097092 "19"), [axlCnsPurgeAll()](#1096928 "19"), [axlCnsDeleteClassClassObjects](#1092356 "19"), [axlCnsDeleteRegionClassClassObjects](#1092421 "19"), [axlCnsDeleteRegionClassObjects](#1092487 "19")

### axlCnsPurgeObjects

`axlCnsPurgeObjects(list l_type) -> x_purgeCount`

#### Description

Process the database and delete all group\_type objects that have no members; a netclass with no nets, or a region with no shapes.

#### Arguments

Domain of interest 'physical or 'spacing.

#### Value Returned

Count of the objects deleted.

#### Examples

> `axlCnsPurgeObjects('netclass)`

> `axlCnsPurgeObjects('region)`

#### See Also

[axlCnsPurgeCsets](#1096942 "19")

### axlViaZLength

`axlViaZLength(t_layer1t_layer2[g_inclusion]) -> f_length`

#### Description

Returns the via length from layer1 to layer2. The layer names can either be given as the ETCH subclass name (TOP) or given as the formal skill layer name ("ETCH/TOP").

This is the length used in the ViaZ option to several DRC checks.

By default, does not use the thickness of the layer1 or layer2 in its calculation.

#### Arguments

* start layer name
* end layer name
* `'nil:`do not include either
* `first:`include thickness of t\_layer1
* `'second:`include thickness of t\_layer2
* `'both:`include both layers

#### Value Returned

|  |
| --- | ---
| `f_length` | via length in design units
#### Examples

Get length from top to bottom (exluding top and bottom thickness)

> `axlViaZLength("TOP" "BOTTOM")`

#### See Also

[axlCNSGetViaZPVF](#1093618 "19")

### axlNetEcsetValueGet

`axlNetEcsetValueGet(o_itemDbid/t_netNamet_cnsName/s_name)==> t_cnsValue/nil`

#### Description

Returns the value of a specific electrical constraint that has been assigned to a given net. Both fixed and user defined constraints may be accessed. This will not return a "flattened" net view of constraints applied to pinpairs. Use`axlCnsNetFlattened` to obtain this constraint view.

* If requesting multiple constraints from the same net it is faster to get the`dbid` of the net and pass that as first argument instead of using the net name.

#### Arguments

|  |
| --- | ---
| `o_itemDbid` | `dbid` of any item that is assigned to a net or Xnet.
| `t_cnsName` | Property name for the constraint to be fetched. This can be either a fixed constraint or a user-defined constraint.
| `s_name` | Symbol name of DRC check (values returned by`axlCNSEcsetModeGet(nil`). These names may not exactly match the property name. They do not exist for user-defined properties in the ECset.
#### Value Returned

|  |
| --- | ---
| `t_cnsValue` | Value returned as a string.
| `nil` | No value defined for the net.
#### See Also

[axlCnsNetFlattened](#1133015 "19")

#### Examples:

Net is part of an ECset (electrical constraint set) which has a MAX\_EXPOSED\_LENGTH constraint:

> `net = car(axlSelectByName("NET" "NET2")`

> `rule = axlNetEcsetValueGet(net "MAX_EXPOSED_LENGTH")`

Net has an override constraint for MAX\_VIA\_COUNT:

> `rule = axlNetEcsetValueGet("NET2" "MAX_VIA_COUNT")`

Same as above example but uses the DRC check name:

> `rule = axlNetEcsetValueGet("NET2" 'Maximum_Via_Count)`

### axlCNSEcsetValueSet

`axlCNSEcsetValueSet(o_ecsetDbid/t_ecsetNamet_name/s_namef_value)⇒ t/nil`

`axlCNSEcsetValueSet(o_ecsetDbid/t_ecsetNamell_constraintNValues)⇒ t/nil`

#### Description

Sets the value of the ECset DRC. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

To determine the list of supported values, use the following command:

`axlCNSEcsetValueGet(nil)`

You may set single values or a list of values.`ll_constraintNValues` represents a list of values as shown:

`'((s_name/t_name f_value/t_value) ...)`

Passing a`nil` or empty string " " as a value deletes the constraint from the ECset.

For performance reasons, changing a value does not invoke DRC. You must manually invoke DRC. See[axlCNSMapUpdate](#1074801 "19") for a set of interfaces that you use in order to mark changes to perform fewer DRC updates.

**Note:** Constraint checks may change from release to release.

#### Arguments

|  |
| --- | ---
| `o_ecsetDbid` | `dbid` of the ECset.
| `t_ecsetName` | Name of the ECset.
| `s_name` | Symbol name of constraint.
| `t_name` | String name of constraint.
| `f_value` | Floating point value provided is assumed to be in the default user unit for the constraint. Value may be rounded.
| `t_value` | If given as a string with MKS type, the value is converted to current user units for the constraint. Rounding may result.
#### Value Returned

|  |
| --- | ---
| `t` | Set value of ECset DRC.
| `nil` | Failed to set value of ECset DRC due to incorrect argument(s).
#### Examples

Sets impedance:

```
axlCNSEcsetValueSet("UPREVED_DEFAULT"                    'Impedance ALL:ALL:100.0:2)
```

Sets multi-value:

`axlCNSEcsetValueSet("UPREVED_DEFAULT"`

`'((Impedance "ALL:ALL:100.0:2") (Maximum_Via_Count 5)))`

### axlCnsGetViaList

`axlCnsGetViaList(t_csetName)==>lt_padstacks/nil`

#### Description

Returns padstacks defined in a physical constraint set. If the cset name is provided then returns only vias assigned for that cset. Otherwise the function returns vias for all csets. The same vias may appear more than once when using the`nil` option.

If a cset name is given, order of vias in list effects the via selection behavior of the etch editing's working layer model (see this documentation for more information).

Note that padstacks in via list may not currently be loaded in database or may not exist on disk (via that cannot be found is shown by a`"*"` indicators in cns physical set dialog).

#### Arguments

|  |
| --- | ---
| `t_csetName` | Name of physical cset.
| `nil` | Process all csets.
#### Value Returned

|  |
| --- | ---
| `lt_padstacks` | List of padstacks defined in a cset or all csets.
| `nil` | If no padstacks found or cset not found.
#### See Also

[axlCnsAddVia](#1104370 "19")`,`[axlCnsDeleteVia](#1092387 "19"), and [axlCNSGetPhysical](#1083339 "19")

#### Examples

Report vias in default physical constraint set

> `axlCnsGetViaList("DEFAULT")`

Report vias in all physical constraint sets

> `axlCnsGetViaList(nil )`

### axlGetAllViaList

`axlGetAllViaList([g_attrVias])==> lo_padstack_dbid`

#### Description

Returns a list of all padstacks included in via lists in the design. This is a compilation of all via lists from all constraint sets. Optionally it provides padstacks from net VIA\_LIST properties.

The order of padstack`dbids` depends on the order of constraint sets, VIA\_LIST properties and the associated via lists.

* ***This interface will result in the via padstacks being loaded into the design if they are not already loaded.***

#### Arguments

|  |
| --- | ---
| `[g_attrVias]` | Optional argument to add padstacks that are not included in constraint sets but are provided in some net VIA\_LIST attributes.
#### Value Returned

|  |
| --- | ---
| `lo_padstack_dbid` | List of padstack`dbids.`
| `nil` | The design has empty via lists.
### axlDRCUpdate

`axlDRCUpdate(g_mode) -> x_cnt/nil`

#### Description

Performs a DRC check on entire design.

Has two return options controled via`g_mode` option:

* `nil`: interactive (on) checks; similar to `drcupdate` command

* `t`: on and batch checks;similar to `dbdoctor drc` option

Will enable On-Line DRC if it is disabled. Obeys current DRC mode settings.

* ***Batch mode is being phased out.***

#### Arguments

|  |
| --- | ---
| `g_mode` | `t` do all checks plus batch only checks, `nil` do only interactive checks
#### Value Returned

|  |
| --- | ---
| `x_cnt` | Returns number of errors
#### See Also

[axlDRCGetCount](#1079214 "19")`,`[axlDBControl](14dsnctl.html#690074 "14")`,`[axlDRCWaive](#1079924 "19")`,`[axlDBCheck](14dsnctl.html#706276 "14")

#### Example

Run a drc check on a net named "GND"

`db = axlDBFindByName('net "GND")`

`cnt = axlDRCItem(nil p)`

### axlDRCWaive

`axlDRCWaive(g_modeo_DrcDbid/lo_DrcDbid[t_comment])==> t/nil`

#### Description

Manages waive DRC state and access to the waive DRC functionality. It supports both waiving and restoring (unwaive) DRC markers. The interface supports both a single and a list of DRC`dbids`. If restoring a DRC marker, it will reappear but it may no longer reflect an actual DRC error. This may be due to:

* Change in the constraint expected value

* Change in the object(s) causing DRC

* Different DRC mode settings

The only way of determining if a DRC still should exist is to perform an`axlDRCItem` on the first item in the DRC's `dbid` violation attribute. The exception to this rule is external DRCs where the tool that created the DRC must be re-run. Note: Comment can also be added by adding the comment property to the DRC by:

> `axlDBAddProp(drcDbid '("COMMENT" "This drc is OK"))`

#### Arguments

|  |
| --- | ---
| `g_mode` | t: waive DRC.  nil: unwaive DRC.
| `o_DrcDbid` | A single DRC marker.
| `lo_DrcDbid` | A list of DRC markers.
| `t_comment` | Optional, add a comment to waived DRC. Only applies in waive mode.
#### Values Returned

|  |
| --- | ---
| `t` | Success.
| `nil` | Failed due to incorrect arguments.
#### See Also

[axlDBControl](14dsnctl.html#690074 "14")`,`[axlDRCWaiveGetCount](#1079288 "19")

#### Example 1 Waive 1st DRC in drc list

`p = axlDBGetDesign()->drcs`

`axlDRCWaive(t car(p) "This DRC is OK")`

#### Example 2 Waive all drcs in design

`p = axlDBGetDesign()->drcs`

`axlDBGetWaive(t p)`

#### Example 3 Restore all waived DRCs

`p = axlDBGetDesign()->waived`

`axlDBGetWaive(nil p)`

### axlDRCGetCount

`axlDRCGetCount()⇒ x_count`

#### Description

Returns the total number of DRCs in the design. Note the design DRC may be out of date.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `x_count` | DRC count.
### axlDRCItem

`axlDRCItem(g_modeo_dbid/lo_dbid)⇒ x_cnt/lo_drcDbid/nil`

#### Description

Performs a DRC check on the indicated item(s). The`dbid` may be any `dbid` type (except the design). If the same item appears multiple times in the list, then the same DRC error(s) are returned, and the count is the sum of errors created by each `dbid`. The `g_mode` option controls two return options:

|       |                             |
| -------| -----------------------------|
| `nil` | Returns DRC error count.    |
| `t`   | Returns list of DRC errors. |
This obeys current DRC mode settings, which includes the master DRC on/off switch.

Due to waive and duplicate DRC suppression processing, the list of DRCs returned using`g_mode=t` may be less then the count returned by `g_mode=nil`.

* ***This is not an efficient way to run batch DRC or "what if" checks.***

#### Arguments

|  |
| --- | ---
| `g_mode` | `nil`: Returns DRC error count.  `t:`Returns list of DRC errors.
| `o_dbid` | A single.
#### Value Returned

|  |
| --- | ---
| `x_cnt` | Returns number of errors associated with list of items.
| `lo_drcDBid` | List of DRC`dbids.`
| `nil` | No`dbids` (if `g_mode` = `t`) or error in arguments.
#### See Also

[axlDRCGetCount](#1079214 "19")`,`[axlDBControl](14dsnctl.html#690074 "14")`,`[axlDRCWaive](#1079924 "19")`,`[axlDRCUpdate](#1081297 "19")

#### Examples

Run a DRC check on a net named "GND":

`db = axlDBFindByName ('net "GND")`

`cnt = axlDRCItem(nil p)`

### axlDRCWaiveGetCount

`axlDRCWaiveGetCount()⇒ x_count`

#### Description

Returns total number of waived DRCs in the design.

#### Arguments

None.

#### Value Returned

`x_count` Returns waived DRC count.

### axlLayerSet

`axlLayerSet(o_dbid)==>o_dbid/nil`

#### Description

Updates changes to layer parameters. You can only update the color and visibility attributes of a parameter. This is a wrapper for`axlSetParam`. After completing color or visibility changes, call `axlVisibleUpdate` to update the display.

#### Arguments

|  |
| --- | ---
| `o_dbid` | Layer parameter`dbid.`
#### Value Returned

|  |
| --- | ---
| `o_dbid` | Layer parameter`dbid.`
| `nil` | If error.
#### See Also

[axlSetParam](04parmgt.html#1109729 "3") and [axlLayerGet](04parmgt.html#1173865 "3")

#### Examples

* Change color of top etch layer:

> ```
> q = axlLayerGet("ETCH/TOP")q->color = 7q->pattern = 0          ; solid patternq->visibility = nilaxlLayerSet(q); if setting multiple layer colors/visisbility only call; visible update after last changeaxlVisibleUpdate(t)
> ```

* To set all items to the same color on a class do

> ```
> q = axlGetParam("paramLayerGroup:ETCH")q->color = 7axlSetParam(q)axlVisibleUpdate(t)
> ```

### axlCnsList

`axlCnsList(s_csetDomain/nil)==> lt_csetNames/ls_csetsDomain`

#### Description

Returns the list of cset names of the domain specified. See`axlDBGetDesign()->ecsets` for a list of electrical csets.

#### See Also

[axlPurgePadstacks](06intedt.html#821249 "5")`,` [axlCnsDeleteVia](#1092387 "19"), [axlCnsAddVia](#1104370 "19"), and [axlCnsGetViaList](#1076043 "19")

#### Arguments

|  |
| --- | ---
| `s_csetDomain` | Domains supported: spacing, physical, sameNet, and electrical.
| `nil` | Lists all supported domains.
#### Values Returned

|  |
| --- | ---
| `lt_csetNames` | Lists csets in specified domain.
| `ls_csetDomains` | List of supported domains.
#### See Also

[axlCNSCreate](#1106245 "19")

#### Example 1

> `axlCnsList('spacing)`

Returns all spacing cset names.

#### Example 2

> `axlCnsList(nil)`

Returns supported domains.

### axlCNSMapClear

`axlCNSMapClear()⇒ t`

#### Description

See`axlCNSMapUpdate`.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
**Examples**

See[axlCNSMapUpdate](#1074801 "19") for an example.

### axlCNSMapUpdate

`axlCNSMapUpdate()⇒ x_drcCount/nil`

#### Description

This function and`axlCNSMapClear`, which do not support nesting, batch and tune DRC updates from constraint changes made by `axlCNS<``xxx``>` functions. No `axlCNS<``xxx``>` functions perform a DRC update. Rather, they set the DRC system out-of-date.

You can run DRC system once on a*set* of constraint changes, which is more efficient than running it as part of each change. You may notice the increased efficiency on large boards.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `nil` | There is no matching`axlCNSMapClear`.
| `x_drcCount` | Number of DRCs caused by batch changes.
#### Examples

* Turns off electrical max via check, turns all design checks on, and sets the island tolerance to 10. The Clear/Update calls batch up and optimize the drc update required by these changes.

> `axlCNSMapClear()`

> `axlCNSEcsetModeSet('Maximum_Via_Count 'off)`

> `axlCNSDesignModeSet('all 'on)`

> `axlCNSDesignValueSet('Negative_Plane_Islands 10.0)`

> `axlCNSMapUpdate()`

* Doing one change.

> `axlCNSMapClear()`

> `axlCNSEcsetModeSet('Maximum_Via_Count 'on)`

> `xlCNSMapUpdate()`

For other real examples, see`<cdsroot>/share/pcb/examples/cmds files cns-design.il` and `acns_design.form`.

### axlCnsNetFlattened

`axlCnsNetFlattened(o_netDbid/t_netNamet_cnsName/s_name)==> t_cnsValue/nil`

#### Description

Permits a view of constraints where explicit pinpair rules are promoted to the net. The information reported by the function is the same as in`show element` under the Properties attached to net heading. It is also in a format used by the third party netlist (`netin`) and in the `pstxnet.dat` file used by `netrev`.

If pinpairs are constrained by an electrical rule (for example, PROPAGATION\_DELAY), Allegro PCB Editor stores the constraints on the pinpair, not on the net. The electrical constraints stored on the net are those applied to dynamic pinpairs (the use of the`AD:AR`, `L:S`, syntax) or where the rule applies to the net (for example, MAX\_VIAS).

This does not return all constraint values applied to the net, if the constraint is obtained via the electrical constraint set (ECset) or overrides exist at the bus or diffpair level. This information is reported in`show element` under the heading, Electrical constraints assigned to net. Allegro PCB Editor maps electrical constraints from xnets, matched groups, and pin pairs to nets by promoting or flattening the electrical property to present a traditional net view of the constraints and to provide compatibility with schematic netlisters. Additional constraints may effect the net because of the ECset assigned to the net, xnet, differential pair or bus level. Additional override properties may exist at the differential pair or bus level. You can use `axlNetECsetValueGet`, but it will not flatten constraints.

* When requesting multiple constraints from the same net, use the`dbid` of the net as first argument instead of the net name.

#### Arguments

|  |
| --- | ---
| `o_netDbid/t_netName` | `dbid` or name (string) of the net.
| `t_cnsName` | Property name for the constraint.
| `s_name` | Symbol name of DRC check (values returned by`axlCNSEcsetModeGet(nil).`These names may not exactly match the property name.
#### Value Returned

|  |
| --- | ---
| `t_cnsValue` | Value returned as a string exactall.
| `nil` | No value defined for the net.
#### Examples

Get impedance rule by name on`net1:`

> `rule = axlCnsNetFlattened("NET1" "IMPEDANCE_RULE")`

Get impedance rule by DRC check name on`net1:`

> `rule = axlCnsNetFlattened("NET1" 'Impedance)`

Get PROPAGATION\_DELAY on MEM\_DATA8 using the`dbid` of net:

> `net = car(axlSelectByName("NET" "MEM_DATA8"))`

> `rule = axlCnsNetFlattened(net "PROPAGATION_DELAY")`

####




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
