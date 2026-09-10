<!--
source: algroskill/18consmgt.md
part: 2/2
estimated_tokens: 5862
-->

### axlCNSSpacingMax

`axlCNSSpacingMax( [s_spacingType] [t_layer] ) => f_maxSpacing`

#### Description

Returns maximum spacing in design. This can be worst case spacing of entire design or base upon the object filtering.

Maximum spacing is calculated from all spacings in the domains of spacing, same net, and assembly (APD or SIP). The state of the check (on/off) is ignored (this is different from the minimum spacing API).

#### Arguments

| Name | Description |
|---|---|
| `s_spacingType` | Symbol representing the spacing constraint type. The supported values are: `'line`, `'shape`, `'via`, `'pin` |
| `t_subclassname` | A subclass name of the class ETCH or CONDUCTOR or `nil` for all layers |

#### Value Returns

| Name | Description |
|---|---|
| `f_maxSpacing` | Maximum spacing on entire design or sub-filtered setting. |

#### Examples

- Get maximum spacing on entire design

`axlCNSSpacingMax(nil)`

- Get maximum spacing on lines (clines) layer TOP

`axlCNSSpacingMax('line "TOP")`

- Get maximum spacing on lines (clines) all layers

`axlCNSSpacingMax('line nil)`

#### See Also

axlCNSSpacingMin

### axlCNSSpacingMin

`axlCNSSpacingMin( [s_spacingType] [t_layer] ) => f_minSpacing`

#### Description

Returns minimum spacing value in the design. This can be the minimum spacing of entire design or based upon the object filtering.

Maximum spacing is calculated from spacings in the domains of spacing, same net, and assembly (APD or SIP). The spacing check must be enabled (on) to be possibly included as a mimimum.

#### Arguments

| Name | Description |
|---|---|
| `s_spacingType` | Symbol representing the spacing constraint type. The supported values are: `'line`, `'shape`, `'via`, `'pin` |
| `t_subclassname` | A subclass name of the class ETCH or CONDUCTOR or `nil` for all layers |

#### Value Returns

| Name | Description |
|---|---|
| `f_minSpacing` | Minimum spacing on entire design or sub-filtered setting. |

#### Examples

See Examples section of axlCNSSpacingMax

#### See Also

axlCNSSpacingMax

### axlCNSSpacingModeGet

`axlCNSSpacingModeGet( nil ) => ls_constraints`

or

`axlCNSSpacingModeGet( 'all ) => lls_constraintNModes`

or

`axlCNSSpacingModeGet( s_name/t_name ) => s_mode/nil`

#### Description

This fetches the current spacing drc mode(s). Modes determine if a particular constraint is on or off. These modes apply to the entire board. To determine the set currently supported spacing modes do a axlCNSSpacingModeGet(nil).

The spacing mode set may be a subset of spacing values since the implementation may associate certain values under a master mode.

Note: Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

| Name | Description |
|---|---|
| `nil:` | returns all modes that are in spacing domain |
| `'all:` | returns all checks and current mode |
| `s_name:` | symbol name of check. |
| `t_name:` | string name of check |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names:` | list of checks (s_name ...) |
| `lls_names:` | list of checks and their mode ((s_name s_mode) ...) |
| `s_mode:` | mode 'on, or 'off |

#### Examples

Get current list of design constraints

`axlCNSSpacingModeGet(nil)`

Get list of settings for all design constraints

`axlCNSSpacingModeGet('all)`

Get current setting of line to line

`axlCNSSpacingModeGet('line_line)`

Get current setting of line to shape using a string

`axlCNSSpacingModeGet("line_shape")`

#### See Also

axlCNSSpacingModeSet, axlCNSGetSpacing

### axlCNSSpacingModeSet

`axlCNSSpacingModeSet( t_name/s_name t_mode/s_mode ) => t/nil`

or

`axlCNSSpacingModeSet( 'all t_mode/smode ) => t/nil`

or

`axlCNSSpacingModeSet( l_constraintNModes t_mode/smode ) => t/nil`

or

`axlCNSSpacingModeSet( ll_constraintNModes ) => t/nil`

#### Description

This sets the current drc modes (on/off) for checks in the area of spacing constraints. These modes are global. To determine the constraints modes currently supported do a `axlCNSSpacingModeGet`(nil). We support several interfaces. All checks may be set ('all), individual checks, (t_name), list of checks with a same mode '(s_name ...) t_mode/s_mode '(t_name ...) t_mode/s_mode and sets of checks via a list of: '((s_name/t_name s_mode/t_mode) ....) The constraints names may be passed as a symbol or a string. For performance reasons, you should either do all your updates in a single call or wrap individual changes in the map API (see axlCNSMapUpdate).

Note: Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name:` | symbol name of check. |
| `t_name:` | string name of check. |
| `s_mode:` | mode setting; may be 'on or 'off. |
| `t_mode:` | string mode setting "on or "off" |
| `'all:` | set all checks for given tier of Allegro. |

#### Value Returns

Returns `t` if succeeds or `nil` if failure.

#### Examples

Turn off all spacing constraints

`axlCNSSpacingModeSet('all 'off)`

Turn on line to line check

`axlCNSSpacingModeSet('line_line 'on)`

Turn two constraints to on

`axlCNSSpacingModeSet('(line_shape thrupin_line) 'on)`

Set several constraints to different modes

`axlCNSSpacingModeSet( '((line_line off)`

`(thrupin_shape on)) )`

#### See Also

axlCNSSpacingModeGet, axlCNSMapUpdate

### axlCnsPurgeAll

`axlCnsPurgeAll( ) => x_purgeCount`

#### Description

Removes all unused constraint objects and constraint sets. Process all netclasses, regions, physical constraint sets and spacing constraint sets. Deletes all empty netclasses and regions.

#### Arguments

None

#### Value Returns

The count of the deleted items.

#### See Also

axlCnsPurgeCsets

### axlCnsPurgeCsets

`axlCnsPurgeCsets( list l_type ) => x_purgeCount`

#### Description

`axlCnsPurgeAll()` Process all constraint sets of the specified domain and delete those without references.

This class of functions is design to help migrate designs to take advantage of the 16.0 constraint model. These functions do have to be used when migrating designs. Before using these functions you need to evaluate your constraint usage.

#### Arguments

Domain of interest 'physical or 'spacing

#### Value Returns

Count of the csets deleted.

#### Examples

`axlCnsPurgeCsets('physical)`

`axlCnsPurgeCsets('spacing)`

#### See Also

axlCnsPurgeObjects, axlCnsPurgeAll(), axlCnsDeleteClassClassObjects, axlCnsDeleteRegionClassClassObjects, axlCnsDeleteRegionClassObjects

### axlCnsPurgeObjects

`axlCnsPurgeObjects( list l_type ) => x_purgeCount`

#### Description

Process the database and delete all group_type objects that have no members; a netclass with no nets, or a region with no shapes.

#### Arguments

Domain of interest 'physical or 'spacing.

#### Value Returns

Count of the objects deleted.

#### Examples

`axlCnsPurgeObjects('netclass)`

`axlCnsPurgeObjects('region)`

#### See Also

axlCnsPurgeCsets

### axlViaZLength

`axlViaZLength( t_layer1 t_layer2 [g_inclusion] ) => f_length`

#### Description

Returns the via length from layer1 to layer2. The layer names can either be given as the ETCH subclass name (TOP) or given as the formal skill layer name ("ETCH/TOP").

This is the length used in the ViaZ option to several DRC checks.

By default, does not use the thickness of the layer1 or layer2 in its calculation.

#### Arguments

| Name | Description |
|---|---|
| `t_layer1` | start layer name |
| `t_layer2` | end layer name |
| `g_inclusion` | Optional inclusion in calculation. `first:`include thickness of t_layer1 `'second:`include thickness of t_layer2 `'both:`include both layers `'nil:`do not include either |

#### Value Returns

| Name | Description |
|---|---|
| `f_length` | via length in design units |

#### Examples

Get length from top to bottom (exluding top and bottom thickness)

`axlViaZLength("TOP" "BOTTOM")`

#### See Also

axlCNSGetViaZPVF

### axlNetEcsetValueGet

`axlNetEcsetValueGet( o_itemDbid/t_netName t_cnsName/s_name ) => t_cnsValue/nil`

#### Description

Returns the value of a specific electrical constraint that has been assigned to a given net. Both fixed and user defined constraints may be accessed. This will not return a "flattened" net view of constraints applied to pinpairs. Use `axlCnsNetFlattened` to obtain this constraint view.

- If requesting multiple constraints from the same net it is faster to get the `dbid` of the net and pass that as first argument instead of using the net name.

#### Arguments

| Name | Description |
|---|---|
| `o_itemDbid` | `dbid` of any item that is assigned to a net or Xnet. |
| `t_cnsName` | Property name for the constraint to be fetched. This can be either a fixed constraint or a user-defined constraint. |
| `s_name` | Symbol name of DRC check (values returned by `axlCNSEcsetModeGet(nil`). These names may not exactly match the property name. They do not exist for user-defined properties in the ECset. |

#### Value Returns

| Name | Description |
|---|---|
| `t_cnsValue` | Value returned as a string. |
| `nil` | No value defined for the net. |

#### Examples

Net is part of an ECset (electrical constraint set) which has a MAX_EXPOSED_LENGTH constraint:

`net = car(axlSelectByName("NET" "NET2")`

`rule = axlNetEcsetValueGet(net "MAX_EXPOSED_LENGTH")`

Net has an override constraint for MAX_VIA_COUNT:

`rule = axlNetEcsetValueGet("NET2" "MAX_VIA_COUNT")`

Same as above example but uses the DRC check name:

`rule = axlNetEcsetValueGet("NET2" 'Maximum_Via_Count)`

#### See Also

axlCnsNetFlattened

### axlCNSEcsetValueSet

`axlCNSEcsetValueSet( o_ecsetDbid/t_ecsetName t_name/s_name f_value ) => t/nil`

or

`axlCNSEcsetValueSet( o_ecsetDbid/t_ecsetName ll_constraintNValues ) => t/nil`

#### Description

Sets the value of the ECset DRC. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

To determine the list of supported values, use the following command:

`axlCNSEcsetValueGet(nil)`

You may set single values or a list of values. `ll_constraintNValues` represents a list of values as shown:

`'((``s_name``/``t_name``f_value``/``t_value``) ...)`

Passing a `nil` or empty string " " as a value deletes the constraint from the ECset.

For performance reasons, changing a value does not invoke DRC. You must manually invoke DRC. See axlCNSMapUpdate for a set of interfaces that you use in order to mark changes to perform fewer DRC updates.

Note: Constraint checks may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `o_ecsetDbid` | `dbid` of the ECset. |
| `t_ecsetName` | Name of the ECset. |
| `s_name` | Symbol name of constraint. |
| `t_name` | String name of constraint. |
| `f_value` | Floating point value provided is assumed to be in the default user unit for the constraint. Value may be rounded. |
| `t_value` | If given as a string with MKS type, the value is converted to current user units for the constraint. Rounding may result. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Set value of ECset DRC. |
| `nil` | Failed to set value of ECset DRC due to incorrect argument(s). |

#### Examples

Sets impedance:

`axlCNSEcsetValueSet("UPREVED_DEFAULT"``'Impedance ALL:ALL:100.0:2)`

Sets multi-value:

`axlCNSEcsetValueSet("UPREVED_DEFAULT"`

`'((Impedance "ALL:ALL:100.0:2") (Maximum_Via_Count 5)))`

### axlCnsGetViaList

`axlCnsGetViaList( t_csetName ) => lt_padstacks/nil`

#### Description

Returns padstacks defined in a physical constraint set. If the cset name is provided then returns only vias assigned for that cset. Otherwise the function returns vias for all csets. The same vias may appear more than once when using the `nil` option.

If a cset name is given, order of vias in list effects the via selection behavior of the etch editing's working layer model (see this documentation for more information).

Note that padstacks in via list may not currently be loaded in database or may not exist on disk (via that cannot be found is shown by a `"*"` indicators in cns physical set dialog).

#### Arguments

| Name | Description |
|---|---|
| `t_csetName` | Name of physical cset. |
| `nil` | Process all csets. |

#### Value Returns

| Name | Description |
|---|---|
| `lt_padstacks` | List of padstacks defined in a cset or all csets. |
| `nil` | If no padstacks found or cset not found. |

#### Examples

Report vias in default physical constraint set

`axlCnsGetViaList("DEFAULT")`

Report vias in all physical constraint sets

`axlCnsGetViaList(nil )`

#### See Also

axlCnsAddVia`,`axlCnsDeleteVia, and axlCNSGetPhysical

### axlGetAllViaList

`axlGetAllViaList( [g_attrVias] ) => lo_padstack_dbid`

#### Description

Returns a list of all padstacks included in via lists in the design. This is a compilation of all via lists from all constraint sets. Optionally it provides padstacks from net VIA_LIST properties.

The order of padstack `dbids` depends on the order of constraint sets, VIA_LIST properties and the associated via lists.

- This interface will result in the via padstacks being loaded into the design if they are not already loaded.

#### Arguments

| Name | Description |
|---|---|
| `[g_attrVias]` | Optional argument to add padstacks that are not included in constraint sets but are provided in some net VIA_LIST attributes. |

#### Value Returns

| Name | Description |
|---|---|
| `lo_padstack_dbid` | List of padstack `dbids.` |
| `nil` | The design has empty via lists. |

### axlDRCUpdate

`axlDRCUpdate( g_mode ) => x_cnt/nil`

#### Description

Performs a DRC check on entire design.

Has two return options controled via `g_mode` option:

- `nil`: interactive (on) checks; similar to `drcupdate` command

- `t`: on and batch checks;similar to `dbdoctor drc` option

Will enable On-Line DRC if it is disabled. Obeys current DRC mode settings.

- Batch mode is being phased out.

#### Arguments

| Name | Description |
|---|---|
| `g_mode` | `t` do all checks plus batch only checks, `nil` do only interactive checks |

#### Value Returns

| Name | Description |
|---|---|
| `x_cnt` | Returns number of errors |

#### Examples

Run a drc check on a net named "GND"

#### See Also

axlDRCGetCount`,`axlDBControl`,`axlDRCWaive`,`axlDBCheck

### axlDRCWaive

`axlDRCWaive( g_mode o_DrcDbid/lo_DrcDbid [t_comment] ) => t/nil`

#### Description

`db = axlDBFindByName('net "GND") cnt = axlDRCItem(nil p)` Manages waive DRC state and access to the waive DRC functionality. It supports both waiving and restoring (unwaive) DRC markers. The interface supports both a single and a list of DRC `dbids`. If restoring a DRC marker, it will reappear but it may no longer reflect an actual DRC error. This may be due to:

- Change in the constraint expected value

- Change in the object(s) causing DRC

- Different DRC mode settings

The only way of determining if a DRC still should exist is to perform an `axlDRCItem` on the first item in the DRC's `dbid` violation attribute. The exception to this rule is external DRCs where the tool that created the DRC must be re-run. Note: Comment can also be added by adding the comment property to the DRC by:

`axlDBAddProp(drcDbid '("COMMENT" "This drc is OK"))`

#### Arguments

| Name | Description |
|---|---|
| `g_mode` | t: waive DRC. 
 nil: unwaive DRC. |
| `o_DrcDbid` | A single DRC marker. |
| `lo_DrcDbid` | A list of DRC markers. |
| `t_comment` | Optional, add a comment to waived DRC. Only applies in waive mode. |

#### See Also

axlDBControl`,`axlDRCWaiveGetCount

### axlDRCGetCount

`axlDRCGetCount( ) => x_count`

#### Description

Returns the total number of DRCs in the design. Note the design DRC may be out of date.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `x_count` | DRC count. |

### axlDRCItem

`axlDRCItem( g_mode o_dbid/lo_dbid ) => x_cnt/lo_drcDbid/nil`

#### Description

Performs a DRC check on the indicated item(s). The `dbid` may be any `dbid` type (except the design). If the same item appears multiple times in the list, then the same DRC error(s) are returned, and the count is the sum of errors created by each `dbid`. The `g_mode` option controls two return options:

| Name | Description |
|---|---|
| `nil` | Returns DRC error count. |
| `t` | Returns list of DRC errors. |

This obeys current DRC mode settings, which includes the master DRC on/off switch.

Due to waive and duplicate DRC suppression processing, the list of DRCs returned using `g_mode=t` may be less then the count returned by `g_mode=nil`.

- This is not an efficient way to run batch DRC or "what if" checks.

#### Arguments

| Name | Description |
|---|---|
| `g_mode` | `nil`: Returns DRC error count. `t:`Returns list of DRC errors. |
| `o_dbid` | A single. |

#### Value Returns

| Name | Description |
|---|---|
| `x_cnt` | Returns number of errors associated with list of items. |
| `lo_drcDBid` | List of DRC `dbids.` |
| `nil` | No `dbids` (if `g_mode` = `t`) or error in arguments. |

#### Examples

Run a DRC check on a net named "GND":

#### See Also

axlDRCGetCount`,`axlDBControl`,`axlDRCWaive`,`axlDRCUpdate

### axlDRCWaiveGetCount

`axlDRCWaiveGetCount() => x_count`

#### Description

`db = axlDBFindByName ('net "GND") cnt = axlDRCItem(nil p)` Returns total number of waived DRCs in the design.

#### Arguments

None.

#### Value Returns

`x_count` Returns waived DRC count.

### axlLayerSet

`axlLayerSet( o_dbid ) => o_dbid/nil`

#### Description

Updates changes to layer parameters. You can only update the color and visibility attributes of a parameter. This is a wrapper for `axlSetParam`. After completing color or visibility changes, call `axlVisibleUpdate` to update the display.

#### Arguments

| Name | Description |
|---|---|
| `o_dbid` | Layer parameter `dbid.` |

#### Value Returns

| Name | Description |
|---|---|
| `o_dbid` | Layer parameter `dbid.` |
| `nil` | If error. |

#### Examples

| Name | Description |
|---|---|
| 1. | Change color of top etch layer: |

`q = axlLayerGet("ETCH/TOP")``q->color = 7``q->pattern = 0 ; solid pattern``q->visibility = nil``axlLayerSet(q)``; if setting multiple layer colors/visisbility only call``; visible update after last change``axlVisibleUpdate(t)`

| Name | Description |
|---|---|
| 2. | To set all items to the same color on a class do |

`q = axlGetParam("paramLayerGroup:ETCH")``q->color = 7``axlSetParam(q)``axlVisibleUpdate(t)`

#### See Also

axlSetParam and axlLayerGet

### axlCnsList

`axlCnsList( s_csetDomain/nil ) => lt_csetNames/ls_csetsDomain`

#### Description

Returns the list of cset names of the domain specified. See `axlDBGetDesign()->ecsets` for a list of electrical csets.

#### Arguments

| Name | Description |
|---|---|
| `s_csetDomain` | Domains supported: spacing, physical, sameNet, and electrical. |
| `nil` | Lists all supported domains. |

#### See Also

axlPurgePadstacks`,` axlCnsDeleteVia, axlCnsAddVia, and axlCnsGetViaList

axlCNSCreate

### axlCNSMapClear

`axlCNSMapClear( ) => t`

#### Description

See `axlCNSMapUpdate`.

#### Arguments

none

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See axlCNSMapUpdate for an example.

### axlCNSMapUpdate

`axlCNSMapUpdate( ) => x_drcCount/nil`

#### Description

This function and `axlCNSMapClear`, which do not support nesting, batch and tune DRC updates from constraint changes made by `axlCNS<``xxx``>` functions. No `axlCNS<``xxx``>` functions perform a DRC update. Rather, they set the DRC system out-of-date.

You can run DRC system once on a set of constraint changes, which is more efficient than running it as part of each change. You may notice the increased efficiency on large boards.

#### Arguments

none

#### Value Returns

| Name | Description |
|---|---|
| `nil` | There is no matching `axlCNSMapClear`. |
| `x_drcCount` | Number of DRCs caused by batch changes. |

#### Examples

- Turns off electrical max via check, turns all design checks on, and sets the island tolerance to 10. The Clear/Update calls batch up and optimize the drc update required by these changes.

`axlCNSMapClear()`

`axlCNSEcsetModeSet('Maximum_Via_Count 'off)`

`axlCNSDesignModeSet('all 'on)`

`axlCNSDesignValueSet('Negative_Plane_Islands 10.0)`

`axlCNSMapUpdate()`

- Doing one change.

`axlCNSMapClear()`

`axlCNSEcsetModeSet('Maximum_Via_Count 'on)`

`xlCNSMapUpdate()`

For other real examples, see `<cdsroot>/share/pcb/examples/cmds files cns-design.il` and `acns_design.form`.

### axlCnsNetFlattened

`axlCnsNetFlattened( o_netDbid/t_netName t_cnsName/s_name ) => t_cnsValue/nil`

#### Description

Permits a view of constraints where explicit pinpair rules are promoted to the net. The information reported by the function is the same as in `show element` under the Properties attached to net heading. It is also in a format used by the third party netlist (`netin`) and in the `pstxnet.dat` file used by `netrev`.

If pinpairs are constrained by an electrical rule (for example, PROPAGATION_DELAY), Allegro PCB Editor stores the constraints on the pinpair, not on the net. The electrical constraints stored on the net are those applied to dynamic pinpairs (the use of the `AD:AR`, `L:S`, syntax) or where the rule applies to the net (for example, MAX_VIAS).

This does not return all constraint values applied to the net, if the constraint is obtained via the electrical constraint set (ECset) or overrides exist at the bus or diffpair level. This information is reported in `show element` under the heading, Electrical constraints assigned to net. Allegro PCB Editor maps electrical constraints from xnets, matched groups, and pin pairs to nets by promoting or flattening the electrical property to present a traditional net view of the constraints and to provide compatibility with schematic netlisters. Additional constraints may effect the net because of the ECset assigned to the net, xnet, differential pair or bus level. Additional override properties may exist at the differential pair or bus level. You can use `axlNetECsetValueGet`, but it will not flatten constraints.

- When requesting multiple constraints from the same net, use the `dbid` of the net as first argument instead of the net name.

#### Arguments

| Name | Description |
|---|---|
| `o_netDbid/t_netName` | `dbid` or name (string) of the net. |
| `t_cnsName` | Property name for the constraint. |
| `s_name` | Symbol name of DRC check (values returned by `axlCNSEcsetModeGet(nil).`These names may not exactly match the property name. |

#### Value Returns

| Name | Description |
|---|---|
| `t_cnsValue` | Value returned as a string exactall. |
| `nil` | No value defined for the net. |

#### Examples

Get impedance rule by name on `net1:`

`rule = axlCnsNetFlattened("NET1" "IMPEDANCE_RULE")`

Get impedance rule by DRC check name on `net1:`

`rule = axlCnsNetFlattened("NET1" 'Impedance)`

Get PROPAGATION_DELAY on MEM_DATA8 using the `dbid` of net:

`net = car(axlSelectByName("NET" "MEM_DATA8"))`

`rule = axlCnsNetFlattened(net "PROPAGATION_DELAY")`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

