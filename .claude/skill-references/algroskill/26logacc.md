### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

30
==

Logic Access Functions
======================

Overview
--------

This chapter describes the AXL-SKILL functions related to schematic capture or the logical definition of the design.

### axlDBAssignNet

`axlDBAssignNet(o_object/lo_objecto_net/t_net[g_ripup])⇒ t/nil`

#### Description

Assigns an object or a list of objects to a new net. Supports pins, vias, and shapes. Vias may not stay on net assigned if they do not connect to an object on the new net. This is not applicable if the new net has RETAIN\_NET\_ON\_VIAS property.

#### Arguments

|  |
| --- | ---
| `o_object` | `dbid`, or list of `dbids` of objects to change net.
| `o_net` | `dbid` of destination net, or `nil` if assigning to a dummy net.
| `t_net` | Net name can be used as an alternative to a dbid net.
| `g_ripup` | An optional flag to ripup clines and vias connected to modified objects. possible values are:  `t` = ripup clines connected to modified objects.  `nil` = do not ripup clines connected to modified objects. The default is `nil`.
| `g_ignoreFixed` | By default, won't allow net assignment if FIXED property is present on the object(s) in question. Setting this argument to`t`ignores the FIXED property.  If`g_ripup`is `t`, and connected clines have the FIXED property then the clines will remain and an error message thrown.
#### Value Returned

|  |
| --- | ---
| `t` | At least one object changed net.
| `nil` | No object changed net.
#### See Also

[axlDBCreateNet](#1092110 "30"), [axlDBIgnoreFixed](14dsnctl.html#715890 "14")

#### Example:

* Simple re-assignment

> `pin_id->net->name => ""`

> `net_id->name => "GND"`

> `axlDBAssignNet(pin_id net_id t)=> t`

> `pin_id->net->name => "GND"`

* Interactive exploration; use the ashOne shareware provided in examples area of cdsroot.

> `;select an object`

> `item = ashOne()`

> `new net`

> `net = "net1"`

> `axlDBAssignNet(item net t t)`

### axlDBCreateConceptComponent

`axlDBCreateConceptComponent(s_refdess_partPaths_logNames_primName[s_pptRowName]`

`)`

`⇒ r_dbid/nil`

#### Description

Given the Concept information needed to describe an Allegro PCB Editor device, create the Allegro PCB Editor component and return its`dbid`. If the component definition already exists, use the existing definition to create the new component. If the component definition does not exist, create a new definition and then create the component instance. Concept information comes from a `chips_prt` file and from a physical parts table (PPT). Determine the location of this information using the `cptList``XXX` family of routines, which allow browsing through a Concept library.

#### Arguments

|  |
| --- | ---
| `s_refDes` | Reference designator for the new component.
| `s_partPath` | Full path to the`chips_ptr` file containing the description of the desired logical part. Determine using the `cptListComponentLibraries` function.
| `s_logName` | Name of the desired logical part. You can determine this using the`cptListComponentPrimitives` function.
| `s_primName` | Name of the desired primitive. You can determine this using the`cptListComponentPrimitives` function.
| `s_pptRowName` | Name of the desired PPT part. Concept data may not include specific device information which would be contained in a PPT. Indicates a specific row in a PPT from which to create the component. You can determine this using the`cptListComponentDevices()` function.
#### Value Returned

|  |
| --- | ---
| `r_dbid` | `dbid` of the new Allegro PCB Editor component instance.
| `nil` | Unable to create component instance.
**Note:** The actual name of the resulting Allegro PCB Editor device is generated automatically. If using the`cptListComponentDevices()` function, then the name should have been created already and is included in the return values of that function. Name is determined by the Concept library data you use to create the part.

This function is meant to be called from SKILL.

### axlDBCreateComponent

```
axlDBCreateComponent(s_refDess_deviceName[s_package][s_value][s_tolerance])==> r_dbid/nil
```

#### Description

Given the information needed to describe a Allegro PCB Editor device, create the Allegro PCB Editor component and return its`dbid`. If the component definition already exists, use the existing definition to create the new component. If the component definition does not exist, create a new definition using the device file and create the new component.

#### Arguments

|  |
| --- | ---
| `s_refDes` | The reference designator for the new component.
| `s_deviceName` | Name of Allegro PCB Editor device file.
| `s_package` | Package name to be used for the component. This overrides the value found in the device file (can be nil).
| `s_value` | "Value" attribute value. This will override the value found in the device file (can be nil).
| `s_tolerance` | "Tolerance" attribute value. This will override the value found in the device file (can be nil).
#### Value Returned

|  |
| --- | ---
| `r_dbid` | `dbid` of new Allegro PCB Editor component.
| `nil` | If unable to create component.
**Note:** If you change an existing component definition by specifying a new value for package, value, or tolerance, you need a device file.

#### Example

Create a new empty comp from an existing one, ashOne can be found at:

> `<cdsroot>/share/pcb/examples/skill/examples/ash-fxf/ashone.il`

> `syminst = ashOne()`

> `ci = syminst->component`

> `nci = axlDBCreateComponent("C1_NEW" ci->deviceType ci->package`

> `ci->compdef->prop->VALUE ci->compdef->prop->TOL)`

If your component is not a discrete component, you do not need the fourth and fifth arguments, but the above example will work for all components.

**See Also**

[axlComponentChangeClass](sipapd.html#1099342 "9")

### axlDBCreateManyModuleInstances

`axlDBCreateManyModuleInstances(`

`t_name`

`t_moddefName`

`x_tileStartNum`

`l_origin`

`l_offset`

`x_num_tiles`

`f_rotation`

`x_logicMethod`

`[l_netExcept]        [g_mirror]`

`)`

`==> o_result/nil`

#### Description

Creates multiple module instances in the design. By reducing the number of times the module definition file opens, this function optimizes performance when creating several instances of the same module.

#### Arguments

|  |
| --- | ---
| `t_name` | Prefix of the names of the module instances.
| `t_moddefName` | Name of the module definition/
| `x_tileStartNum` | Tile numbering start number and increment by 1 for each tile.
| `l_origin` | First location of first module.
| `l_offset` | List containing the offset wanted between module origins.
| `x_numTiles` | The number of module instances to be place.
| `f_rotation` | Angle of rotation for the module instance.
| `x_logicMethod` | Flag to indicate where the logic for the module comes from.
| `0` | No logic.
| `1` | Logic from schematic.
| `2` | Logic from module definition.
| `l_netExcept` | Optional list of net names to add to the net exception list.
| `g_mirror` | Optional if modules should be mirrored
#### Value Returned

|  |
| --- | ---
| `lo_result` | If successful, returns the list of database objects that belong to the module instances created.
| `nil` | Creation of module instance could not be completed.
#### See Also

[axlDBCreateModuleDef](#1075174 "30"), [axlDBCreateModuleInstance](#1075221 "30")

#### Example

Add five module instances based on the module definition file`mod.mdd`, starting at point (`10,10`) and offsetting by (`5,0`) every time:

> `modinsts = axlDBCreateManyModuleInstances(`

> `"Num" "mod" 2 10:10 '(5 0) 5 0 2 '("GND" "+5"))`

Creates five module instances named`Num2`, `Num3`, `Num4`, `Num5`, `Num6`.

### axlDBCreateModuleDef

`axlDBCreateModuleDef(t_namel_originl_objects`

`)`

`⇒ t/nil`

#### Description

Creates a module based on existing database objects.

#### Arguments

|  |
| --- | ---
| `t_name` | String providing the name of the module definition. File name is the module definition name appended with`.mdd`.
| `l_origin` | Coordinate serving as the origin of the module definition.
| `l_objects` | List of objects to add to the module.
#### Value Returned

|  |
| --- | ---
| `t` | Module definition successfully created.
| `nil` | No module definition created.
#### Example

```
axlSetFindFilter(?enabled '("noall" "components") ?onButtons '("noall"    "components"))
```

`axlSingleSelectName("COMPONENT" "U1")`

`comp1 = car(axlGetSelSet())`

`axlSingleSelectName("COMPONENT" "U2")`

`comp2 = car(axlGetSelSet())`

`axlDBCreateModuleDef("comps" '(0 0) '(comp1 comp2))`

`⇒ A module definition file named comps.mdd is created.`

Creates a module definition file containing two components.

### axlDBCreateModuleInstance

```
axlDBCreateModuleInstance(t_namet_moddef_namel_originr_rotationi_logic_methodl_net_except
```

`)`

`⇒ o_result/nil`

#### Description

Allows you to use or place a previously defined module.

#### Arguments

|  |
| --- | ---
| `t_name` | String providing name of the module instance.
| `t_moddef_name` | String providing name of the module definition to base the instance on.
| `l_origin` | Coordinate location to place the origin of the module definition.
| `r_rotation` | Angle of rotation for the module instance.
| `i_logic_method` | Flag indicating where the logic for the module comes from:  0 - no logic  1 - logic from schematic  2 - logic from module definition.
| `l_net_except` | Optional list of net names to add to net exception list.
#### Value Returned

|  |
| --- | ---
| `o_result` | Database object that is the group used to represent the module instance.
| `nil` | Module instance not created.
#### Example

`modinst = axlDBCreateModuleInstance("inst" "mod" '(500 1500) 2 '("GND" "+5"))`

Adds a module instance based on the module definition file`mod.mdd`.

### axlDBCreateNet

`axlDBCreateNet(t_netName)==> o_dbid/nil`

#### Description

Creates a net in database if does not exist or returns`dbid` of net if it exists.

#### Arguments

|  |
| --- | ---
| `t_netName` | Net name to create, or find.
#### Value Returned

`nil` if not created, or a axl `dbid` of net

#### See Also

[axlDBAssignNet](#1092015 "30")

#### Example

`net = axlDBNetCreate("gnd")`

> `=> dbid:123456`

`net->name`

> `=> "GND"`

### axlDBCreateSymDefSkeleton

`axlDBCreateSymDefSkeleton(l_symbolDatal_extents[l_pinData])==> axlDBID/nil`

#### Description

Creates a "minimal" symbol definition. While the symbol name and type must be provided, the instance is created only with pins. Once this "skeleton" definition has been created, you add the rest of the symbol geometry with additional`axlDBCreate` calls. This provides the ability to create symbols that do not exist in the library.

Shape symbol:

* You may only attach a single shape to a shape symbol, no voids.

* Layer required is "ETCH/TOP".

* Extents should be larger than the shape but there is no adverse impact if they are significantly larger.

Flash symbol:

* You may attach multiple shapes, but none may contain voids.

* Layer required is "ETCH/TOP".

* Extents should be larger than the shape but there is no adverse impact if they are significantly larger.

#### Arguments

|  |
| --- | ---
| `l_symbolData` | A list of (`t_symbolName` `[t_symbolType]`).  `t_symbolName``:` Name of the symbol.  `t_symbolType`: Package (default), mechanical, or format.
| `l_extents` | The lower left and upper right corners of the symbol def extents.
| `l_pinData` | List of`axlPinData` defstructs for the pins.
#### Value Returned

|  |
| --- | ---
| `axlDBCreateSymDefSkeleton` | `nil` if not created, or `axlDBID` of the symbol definition.
#### Examples

```
symdef = axlDBCreateSymDefSkeleton('("shape_pad" "shape") list(-100:-100 100:100))
```

`p = axlPathStart( list(-4:10 4:10 8:0 4:-10 -4:-10 -4:10))`

`s = axlDBCreateShape(p t "ETCH/TOP" nil symdef)`

Creates a shape symbol.

```
symdef = axlDBCreateSymDefSkeleton('("flash_pad" "flash") list(-100:-100 100:100))
```

`p = axlPathStart( list(-4:10 4:10 8:0 4:-10 -4:-10 -4:10))`

`ps = axlPathStart( list(-4:10 4:10 4:-10 -4:-10 -4:10))`

`s = axlDBCreateShape(p t "ETCH/TOP" nil symdef)`

`s = axlDBCreateShape(ps t "ETCH/TOP" nil symdef)`

Creates a flash symbol.

### axlDBDummyNet

`axlDBDummyNet (g_mode)-> lo_dbid/nil`

#### Description

This command returns all dummy nets in design. Two courtesy options provided are:

* `'pin` for any dummy net that has a pin return the first pin of the dummy net

* `'shape` for any dummy net that has a shape return the first shape of the dummy net

Typically each dummy net in design will only have a single pin or shape but this may not always be the case. Clines or vias cannot, by themselves exist on a dummy. Symbols (`dra`) do not have dummy nets

#### Arguments

* Can have following two values:
* `'shape` - returns list of first shapes on dummy nets
* `'pin` - returns a list of first pins on dummy nets

#### Value Returned

* `t` - indicates success

* `nil` - failed due to incorrect arguments

#### See Also

[axlIsDummyNet](07dbaccs.html#719568 "6"), [axlDbidName](#1076610 "30")

#### Examples

* Print all 1st pins on dummy nets

> > `foreach( mapc x axlDBDummyNet('pin) printf("%s\n" axlDbidName(x)))`

* Get all dummy nets on design

> > `p = axlDBDummyNet(nil)`

### axlDbidName

`axlDbidName(`

`o_dbid`

`) -> t_name/nil`

#### Description

Provides the standard Allegro PCB Editor name of a database object. Many of the named Allegro PCB Editor objects ( for example, nets) have names defined in the name attribute (for example,`dbid->name`) but other objects (for example, clines and pins) either do not have the desired reporting name or are unnamed.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A Allegro PCB Editor database id.
**Note:** Some Allegro PCB Editor database ids are pseudo ids (for example,`axlDBGetDesign`and pads) and generate a `nil` return.

#### Value Returned

Allegro PCB Editor name of object, or`nil` if not a `dbid` or true Allegro PCB Editor database object.

#### Examples

This uses the ashOne selection function found in:

`<cdsroot>/share/pcb/examples/skill/examples/ash-fxf/ashone.il`

Pin name:

> `pin = ashOne()`

> `axlDbidName(pin)`

> `-> "U1.1"`

Cline name:

> `cline = ashOne()`

> `axlDbidName(cline)`

> `-> "Net3, Etch/Top"`

### axlDiffPair

* Add DiffPair

`axlDiffPair(t_diffpairo_net1/t_net1o_net2/t_net2`

`)`

`⇒ o_diffpair/nil`

* Modify DiffPair

`axlDiffPair(o_diffpair/t_diffpairo_net1/t_net1o_net2/t_net2`

`)`

`⇒ o_diffpair/nil`

* Delete DiffPair

`axlDiffPair(o_diffpair/t_diffpair`

`)`

`⇒ t/nil`

#### Description

Creates, modifies, or deletes a differential pair. In all cases you can pass names or a`dbid`.

**Note:** If the differential pair was created due to Signoise models, you cannot modify or delete it. Consequently, you cannot modify or delete the differential pair if the following is true:

`diffpair_dbid->prop->DIFFP_ELECTRICAL ==t.`

#### Arguments

|  |
| --- | ---
| `o_diffpair` | Diffpair`dbid`
| `t_diffpair` | Diffpair name.
| `o_net` | Net`dbid`.
| `t_net` | Net name.
#### Value Returned

Values returned depend on whether adding, modifying, or deleting.

|  |
| --- | ---
| `o_diffpair` | `dbid` of new or modified diffpair
| `t` | Diffpair deleted.
| `nil` | Error due to incorrect arguments.
**Example 1**

`DPdbid = axlDiffPair("DP" "NET1+" "NET2-")`

Creates a differential pair and names it DP1.

**Example 2**

`DPdbid = axlDiffPair(DPdbid "NET1+" "NET1-")`

Modifies a differential pair.

**Example 3**

`axlDiffPair(DPdbid)`

Deletes a differential pair.

**Example 4**

`axlDiffPair(axlDBGetDesign()->diffpair)`

Delete all differential pairs in design.

### axlDiffPairAuto

```
axlDiffPairAuto(t_diffPairPrefixt_posNetPostfixt_negNetPostfix[g_returnDiffPairList]
```

`)`

`⇒ x_cnt/(xcnt lo_diffpair)/nil`

#### Description

Allows automatic generation of the diffpair. Generates the set of diffpairs based on the provided positive (`t_posNetPostfix`) and negative (`t_negNetPostfix`) postfixes used in your net naming.

You may provide a prefix (`t_diffPairPrefix`) used in generating the diffpair names of the form: <`t_diffPairPrefix`> + `netname` - `postfix`.

If nets are part of busses and end the bitfield syntax (`<1>`), the syntax portion is ignored when performing suffix matching. If a diffpair is created the bit number is added to the base net name used in forming a diffpair. For example, given two nets; `DATA_P<1>` and `DATA_N<1>` will result in a diffpair called `DP_DATA1` with this call:

`axlDiffPairAuto("DP_" "_P" "_N")`

#### Arguments

|  |
| --- | ---
| `t_diffPairPrefix` | String to prefix diffpair names. Use`""` if no prefix is desired.
| `t_posNetPostfix` | Postfixes used to identify`+` diffpair members.
| `t_negNetPostfix` | Postfixes used to identify`-` diffpair members.
| `g_returnDiffPairList` | Controls return.
#### Value Returned

Returns depend on value of`g_returnDiffPairList` as shown:

|  |  |
| --- | --- | ---
| ****g\_returnDiffPairList**** | **Value Returned** | **Description**
| `nil` | `x_cnt` | Number of diffpairs created.
| `t` | (`x_cnt`, `lo_diffpair`) | List of diffpairs created
#### Examples

**Example nets**

Two nets called`NET1+` and `NET1-` are passed to this function.

**Example 1**

> `axlDiffPairAuto("DP_" "+" "-")`

Shows diffpair creation and name generation. Results in one diffpair called`DP_NET1` with members `NET1+` and `NET1-`.

**Example 2**

> `axlDiffPairAuto("" "+" "-")`

Gives the same result as the previous example, but names the diffpair`NET1`.

### axlDiffPairDBID

`axlDiffPairDBID(t_name)⇒ o_dbid/nil`

#### Description

Returns the`dbid` of the named diffpair (`t_name`) if it exists in the database.

#### Arguments

|  |
| --- | ---
| `t_name` | Diffpair name.
#### Value Returned

|  |
| --- | ---
| `o_dbid` | `dbid` of diffpair if it exists.
| `nil` | Diffpair does not exist.
### axlMatchGroupAdd

`axlMatchGroupAdd(o_mgdbid/t_mgNameo_dbid/lo_dbid)==> t/nil`

#### Description

Adds members to a matched group. Eligible members are:

* nets (if a net is part of an xnet the xnet is added to the group)

* xnets

* pinpairs

See discussion in`axlDBMatchGroupCreate`.

Command fails in product tiers that do not support electrical constraints or the symbol editor.

* Using`dbids` is faster than using names.

#### Arguments

|  |
| --- | ---
| `o_mgdbid` | `dbid` of a match group.
| `t_mgName` | Name of a match group.
| `o_dbid` | Legal database`dbid` to add to match group.
| `lo_dbid` | List of legal database`dbids` to add to match group.
#### Value Returned

|  |
| --- | ---
| `t` | Added elements.
| `nil` | Failed one or more element additions.
#### See Also

[axlMatchGroupCreate](#1077223 "30")

#### Example

Add two nets to match group created in`axlMatchGroupCreate`:

> `mg = car(axlSelectByName("MATCH_GROUP" "MG1"))`

> `nets = axlSelectByName("NET" '("B1_OUT" "B2_OUT"))`

> `axlMatchGroupAdd(mg nets)`

### axlMatchGroupCreate

`axlMatchGroupCreate(t_name)==> o_mgdbid`

#### Description

Creates a new match group. If a match group already exists with the same name,`nil` is returned. Match groups need to be populated, or they are deleted when saving. Use the [axlMatchGroupAdd](#1076859 "30") command to populate the match groups.

**Note:** The axlMatchGroupCreate command fails in product tiers that do not support electrical constraints or the symbol editor.

If the match group was partially or completely created from an ECset, you can delete it, but it reappears when ECset flattening is required due to modifications in the design. SKILL functions do not indicate ECset-derived match groups.

You can access list of match groups in database by:

> `axlDBGetDesign()->matchgroup`

***RELATIVE\_PROPAGATION\_DELAY***

The RELATIVE\_PROPAGATION\_DELAY property can be added to match groups, xnets, and pinpairs. If you add it to the match group then any match group member that does not have that property inherits it from the match group.

Match groups contain the following elements: xnets, nets, and pinpairs. If a net is part of an xnet, the xnet is added to the match group.

Xnets and pinpairs can belong to multiple match groups, so an RPD property exists on the`dbid` for nets, xnets and pinpairs. This property is a list of lists where each sub-list contains a match group `dbid` and the RELATIVE\_PROPAGATION\_DELAY value:

`rpd = ( (o_mgDbid t_rpdValue) ....)`

Thus if a pinpair belongs to 2 match groups, you see two lists that are the inherited. A pinpair in a single match group has a single list of list. For example, a pinpair in MG3 with global scope and an override of delta/tolerance of`10ns:5%` reports:

> `rpd = ((dbid:61315360 "MG3:G:::10 ns:5 %"))`

The same pinpair without an override will report default match group value as

> `rpd = ((dbid:61315360 "MG3:G:AD:AR:0 ns:5 %"))`

In both the examples, the dbid references the match group id (MG3).

The RELATIVE\_PROPAGATION\_DELAY syntax is discussed in the Allegro Property Reference Manual. In general the syntax is:

`<Match group name>:<scope>:<pinpair>:<value>`

You can add and delete properties to a match group or pinpair`dbid` using [axlMatchGroupProp](#1078079 "30"). When creating the property value, you must include the match group name but not an explicit pinpair. For example, the following adds an RPD property to a match group named `MG2`:

`axlMatchGroupProp.(mg '("RELATIVE_PROPAGATION_DELAY" "MG2:G:::0 ns:5 %"))`

Additional restrictions for this property are:

* Pinpairs should leave the pinpair section empty (`"::"`).

> Example:`"MG2:G:::0 ns:5 %"`

* Match groups should not reference an explicit pinpair but, if not empty, should use a pinpair type (for example, "AD:AR","D:R" etc.)

For nets and xnets, if you access the RELATIVE\_PROPAGATION\_DELAY property, you may see the flattened version. This implies that if nets and xnets are part of multiple Match Groups, they all appear concatenated in the RELATIVE\_PROPAGATION\_DELAY property.

Any pinpairs that are part of the net appear as part of the property at the net or xnet level. This is present to support legacy applications like netlisters. The RPD property that is`dbids` for pinpairs, net and xnets breaks this concatentation. Using `axlDBAddProp` and `axlDBDeleteProp` commands to modify the property may effect all match groups and pinpairs. It is recommended that [axlMatchGroupProp](#1078079 "30") is used for modification of the RELATIVE\_PROPAGATION\_DELAY property for all objects.

#### Arguments

|  |
| --- | ---
| `t_name` | Name of match group (changed to upper case).
#### Value Returned

|  |
| --- | ---
| `nil` | Error or match group with same name already exists.
| `o_mgdbid`: | `dbid` of match group.
#### See Also

[axlPinPairSeek](#1078813 "30") , [axlPinsOfNet](#1078733 "30") , [axlMatchGroupCreate](#1077223 "30"), [axlMatchGroupDelete](#1077449 "30"), [axlMatchGroupAdd](#1076859 "30"), [axlMatchGroupRemove](#1080542 "30"), [axlMatchGroupProp](#1078079 "30")

#### Example

Create a match group called`MG1:`

> `mg = axlMatchGroupCreate("mg1")`

### axlMatchGroupDelete

`axlMatchGroupDelete(`

`o_mgdbid/t_mgName`

`) -> t/nil`

#### Description

This deletes a match group. The command fails in product tiers that do not support electrical constraints or the symbol editor.

* Using`dbids` is faster than using names.

#### Arguments

|  |
| --- | ---
| `o_mgdbid` | `dbid` of a match group.
| `t_mgName` | Name of a match group.
#### Value Returned

|  |
| --- | ---
| `t` | Match group deleted.
| `nil` | Failed.
#### See Also

[axlMatchGroupCreate](#1077223 "30")

#### Examples

Delete match group created in`axlMatchGroupCreate:`

> `mg = car(axlSelectByName("MATCH_GROUP" "MG1"))`

> `axlMatchGroupDelete(mg)`

or

> `axlMatchGroupDelete("MG1")`

### axlMatchGroupProp

`axlMatchGroupProp(`

`o_mgdbid/t_mgName`

`o_dbid`

`t_value/nil`

`)==> t/nil`

#### Description

Adds or removes the RELATIVE\_PROPAGATION\_DELAY property from a member of a match group. Property must be a legal RPD syntax that includes the RPD name.

The command fails in product tiers that do not support electrical constraints or the symbol editor.

See discussion in`axlDBMatchGroupCreate`.

* Using`dbids` is faster than using names.

#### Arguments

|  |
| --- | ---
| `o_mgdbid` | `dbid` of a match group
| `t_mgName` | Name of a match group
| `o_dbid` | Legal database dbid to of a member of the match group
| `t_value` | RELATIVE\_PROPAGATION\_DELAY value in legal syntax. If value is`nil;` removes the property.
#### Value Returned

|  |
| --- | ---
| `t` | Added elements.
| `nil` | Failed one or more element additions.
#### See Also

[axlMatchGroupCreate](#1077223 "30")

#### Examples

Add two nets to match group created in`axlMatchGroupCreate:`

> `mg = car(axlSelectByName("MATCH_GROUP" "MG1"))`

> `nets = axlSelectByName("NET" '("B1_OUT" "B2_OUT"))`

> `n1 = car(nets)`

> `n2 = cadr(nets)`

> `axlMatchGroupAdd(mg nets)`

Add properties:

> `axlMatchGroupProp(mg n1 "MG1:G:::100 ns:5 %")`

> `axlMatchGroupProp(mg n2 "MG1:G:AD:AR:0 ns:5 %")`

Remove property from`n2:`

> `axlMatchGroupProp(mg n2 nil`

### axlMatchGroupRemove

`axlMatchGroupRemove(`

`o_mgdbid/t_mgName`

`o_dbid/lo_dbid`

`)==> t/nil`

#### Description

Removes elements from an existing match group. Elements must be members (attribute groupMembers) of the match group.

The command fails in product tiers that do not support electrical constraints or the symbol editor.

* Using`dbids` is faster than using names.

#### Arguments

|  |
| --- | ---
| `o_mgdbid` | `dbid` of a match group.
| `t_mgName` | Name of a match group.
| `o_dbid` | Legal database`dbid` to remove from match group.
| `lo_dbid` | List of legal database`dbids` to remove from match group.
#### Value Returned

|  |
| --- | ---
| `t` | Removed elements.
| `nil` | Failed one or more element removals.
#### See Also

[axlMatchGroupCreate](#1077223 "30")

#### Example

To match group in example`axlMatchGroupAdd` remove one of the nets:

> `axlMatchGroupRemove(mg car(nets))`

### axlNetSched

`axlNetSched()`

`==> t`

#### Description

This is the main routine that the command processor calls for the`net schedule` command.

#### Arguments

None

#### Value Returned

`t`

### axlPinPair

Add

`axlPinPair(`

`o_pin1/t_pin1`

`o_pin2/t_pin2`

`)==> o_pinpair`

Delete

`axlPinPair(`

`o_pinpair/lo_pinpair`

`)==> t/nil`

#### Description

This creates or deletes a pinpair. A pinpair consists of two un-ordered pins or ratTs on the same net. For example, pinpair`u1.2:r1.2` is the same pinpair as `r1.2:u1.2`. If the pinpair already exists then the existing pinpair is returned. The command fails in product tiers that do not support electrical constraints or the symbol editor.

**Note:** You cannot create a pinpair if both pins (or ratT) do not belong to the same xnet.

If the pinpair was created in an ECset, the ECsetDerived attribute will be`t`andcannot delete it. You must modify the pinpair in the associated ECset.

At database save, a pinpair must be part of a match group or have a legal electrical constraint property assigned to it. Legal electrical properties are:

* PROPAGATION\_DELAY

* MIN\_FIRST\_SWITCH

* MAX\_FINAL\_SETTLE

* IMPEDANCE\_RULE

* TIMING\_DELAY\_OVERRIDE

* RELATIVE\_SKEW

RELATIVE\_PROPAGATION\_DELAY is stored on the RPD attrbiute as a list of lists.

See`axlMatchGroupCreate` for more infomation.

* Using`dbids` is faster than using names.

#### Arguments

|  |
| --- | ---
| `o_pin1/o_pin2` | `dbid` of a pin or ratT
| `t_pin1/t_pin2` | A pin name (`<refdes>.<pin#>`); ratT names are not supported.
| `o_pinpair` | Pinpair`dbid.`
| `lo_pinpair` | List of pinpair`dbids` (delete mode only).
#### Value Returned

Returns depending upon the mode.

`nil`: error

|  |
| --- | ---
| `t` | Deletion was successful.
| `o_pinpair` | `dbid` of added or modified differential pair.
#### See Also

[axlPinPairSeek](#1078813 "30"), [axlPinsOfNet](#1078733 "30"), [axlMatchGroupCreate](#1077223 "30")

#### Examples

Example 1: Xnet having two nets;`NET1` and `NET1A`. This demonstrates that pinpairs are stored on the xnet.

Create pinpair using name:

> `pp = axlPinPair("U2.13" "R1.2")`

Create pinpair with ratT of net`NET1A:`

> `ratTs = axlPinsOfNet("NET1A" 'ratT)`

> `pp = axlPinPair("U2.13" car(ratTs))`

Verify pinpairs are both on`NET1A:`

> `n = car(axlSelectByName("NET" "NET1A"))`

> `n->pinpair RETURNS nil`

Examine the xnet (`NET1`):

> `xn = car(axlSelectByName("XNET" "NET1"))`

> `xn->pinpair RETURNS (dbid:21697512 dbid:21697232)`

Delete all pinpairs of Example 1:

`axlPinPair(xn->pinpair)`

### axlPinPairSeek

`axlPinPairSeek(`

`o_pin1`

`o_pin2`

`)==> o_pinpair/nil`

#### Description

Given two pins or ratTs reports if they are part of a pinpair.

#### Arguments

|  |
| --- | ---
| `o_pin1/o_pin2` | `dbid` of a pin or ratT.
| `t_pin1/t_pin2` | A pin name (`<refdes>.<pin#>`); ratT names not supported.
#### Value Returned

|  |
| --- | ---
| `o_pinpair` | Pinpair`dbid.`
| `nil` | Pinpair for given pins does not exist.
#### See Also

[axlPinPair](#1078535 "30")

#### Example

See if a pinpair for these two pins exists:

> `pp = axlPinPair("U2.13" "R1.2")`

### axlPinsOfNet

`axlPinsOfNet(`

`o_net/t_net`

`g_mode`

`) -> lo_pins/nil`

#### Description

Returns list of pins and ratTs on a net or xnet. First argument can be either a net, xnet`dbid` or a net name (xnet names are not supported). Second option, `g_mode`, can be `'pin` to return only the pins, `'ratT` to return list of ratTs or nil to return both pins and ratTs. There is no meaning conveyed in the list of items returned.

#### Arguments

|  |
| --- | ---
| `o_net` | `dbid` of a net or xnet.
| `t_net` | Name of a net (does not support xnet names).
| `g_mode` | `nil` return both pins and ratTs of a net.
| `'pin` | Return only pins.
| `'ratT` | Return only the ratT's.
#### Value Returned

|  |
| --- | ---
| `lo_pins` | List of pins and/or ratTs on net or xnet.
| `nil` | Nothing meeting criteria (or error,`dbid` not net or xnet).
#### Examples

All pins on GND:

> `net = car(axlSelectByName("NET" "GND"))`

> `lpins = axlPinsOfNet(net, 'pins)`

All pins and ratTs on first xnet in design root (could be a net):

> `xnet = car( axlDBGetDesign()->xnet )`

> `lpins = axlPinsOfNet(xnet, nil)`

### axlRemoveNet

`axlRemoveNet(t_name/o_dbid[g_ripup])⇒ t/nil`

#### Description

Removes a net. May either give a string with the net name to be renamed or`dbid` of an object on that net.

* ***The net name may be used in properties. This function does not update these values.***

#### Arguments

|  |
| --- | ---
| `t_name` | Net name.
| `o_dbid` | `dbid` of a net.
| `g_ripup` | Optional argument. Ripup associated etch when a net is deleted.
#### Value Returned

|  |
| --- | ---
| `t` | Net successfully removed.
| `nil` | No net is removed.
#### Example

`axlRemoveNet("GND")`

### axlRenameNet

`axlRenameNet(t_old_namet_new_name)⇒ t/nil`

`axlRenameNet(o_dbidt_new_name)⇒ t/nil`

#### Description

Renames a net. For the old object, may either give a string with the net name to be renamed, or`dbid` of an object on that net. Fails if the new net name already exists in the database.

> `dbid = axlSingleSelectName("NET" '("NET"))`

**Note:** This function does not refresh any`axl` `dbids` to reflect the new net name.

* ***The net name may be used in properties. This function does not update net names in property values.***

#### Arguments

|  |
| --- | ---
| `t_old_name` | Existing net name.
| `o_dbid` | `dbid` of an object on a net.
| `t_new_name` | New net name (should not exist in the database.)
#### Value Returned

|  |
| --- | ---
| `t` | Net successfully renamed.
| `nil` | Net name already exists in the database.
#### Example

`axlRenameNet("GND" "NEWGND")`

`; first verify the new net name doesn't exist`

`axlSetFindFilter(?enabled '("noall" "nets"))`

`if(axlSingleSelectName("NET" '("NEWGND") ) then`

`axlRenameNet(dbid "NEWGND")`

### axlRenameRefdes

`axlRenameRefdes(t_old_name/o_oldCompDbidt_new_name/o_newCompDbid`

`)`

`⇒ t/nil`

#### Description

Renames a refdes. For either argument, may use a refdes name or a component instance.

If both refdes exist, a swap is done.

#### Arguments

|  |
| --- | ---
| `t_oldName` | Existing refdes name.
| `o_oldCompDbid` | Component`dbid`.
| `t_newName` | New refdes name.
| `o_newCompDbid` | Component`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Refdes successfully renamed or swapped.
| `nil` | No refdes renamed or swapped due to incorrect arguments.
#### Example 1

`axlRenameRefdes("U1" "X1")`

Changes refdes by name.

**Example 2**

`axlSetFindFilter(?enabled '("noall" "components") ?onButtons '(all))`

`axlSingleSelectName("COMPONENT" "U1")`

`firstComp = car(axlGetSelSet())`

`axlSingleSelectName("COMPONENT" "U2")`

`secondComp = car(axlGetSelSet())`

`axlRenameRefdes(firstComp secondComp)`

Swaps with starting point of two component`dbids`.

### axlSchedule

`axlSchedule(`

`o_net/t_net                                [g_userSchedule]`

`)`

`==> t_schedule/nil`

#### Description

Gets net schedule. When`g_userSchedule` is`t,`this fetches the `a` user schedule or a partial user schedule from a net. Returns nil if the net is completely algorithm scheduled. Using`t` is recommended. When `g_userSchedule` is nil, returns the schedule of the complete net even if the net is completely algorithm scheduled.

The format of`t_schedule`is a string in the $SCHEDULE netin (3rd party) format. See `netin` documentation for more info about the syntax.

#### Arguments

|  |
| --- | ---
| `o_net` | `dbid` of net
| `t_net` | Name of net
|  |
| --- | ---
| `g_userSchedule`(optional) | If t returns the schdule if the net is user schedule or partial userschedule. Other nets in this netin format if nil remove
#### Values Returned

|  |
| --- | ---
| `t_schedule` | Schedule or partial user schedule.
| `nil` | Failed or net is not user schedule or partial user schedule. Use axlDebug to obtain more data.
#### See Also

[axlScheduleNet](#1081172 "30")

#### Examples

Net2 has the following pins and rat-Ts:

P1.7 U1.4 U1.10 U2.6 T.1

It is partially user schedule such as P1.7, U1.4, and U1.10 should be connected to rat-T, T.1. Pin U2.6 is algorithm scheduled but the sub-schedule (partial) indicates it should connected to U1.10 (indicated by a star '\*' in the schedule string).

Fetch partial schedule (note no U2.6)

q = axlSchedule("NET2" t)

==> "P1.7 T.1 U1.4 ; T.1 \*U1.10 "

Same net but complete schedule

q = axlSchedule("NET2" t)

==> "P1.7 T.1 U1.4 ; T.1 \*U1.10 U2.6 "

### axlScheduleNet

`axlScheduleNet(`

`o_net/t_net`

`t_schedule/nil`

`)`

`==> t/nil`

#### Description

This applies a user schedule or a partial user schedule to a net. Format of`t_schedule` is a string in the $SCHEDULE netin (3rd party) format.

**Note:** See`netin` documentation for more info about the syntax.

When`t_schedule` is`nil` it removes any user schedule or partial user schedule from the net and restores its default schedule algorithm (NET\_SCHEDULE property).

#### Arguments

|  |
| --- | ---
| `o_net` | `dbid` of net
| `t_net` | Name of net
| `t_schedule` | Schedule or partial schedule using $SCHEDULE netin format; if`nil,` remove
#### Value Returned

|  |
| --- | ---
| `t` | Schedule applied.
| `nil` | Failed or arguments are incorrect (use`axlDebug`) for more info.
#### See Also

[axlSchedule](#1083124 "30")

### axlWriteDeviceFile

`axlWriteDeviceFile(o_compDefDbid[t_output_dir]`

`)`

`⇒ t/nil`

#### Description

Given a component definition, writes out a third party device file. Writes to the directory specified, or if no directory or`nil` is given, writes to the current directory.

Name of the file is compDef->deviceType in lower case with a .txt file extension. For example, if component definition (compDef) device type is`CAP1`, then the device file name is `cap1.txt`.

Also creates a`devices.map` file which is empty unless the device name has characters that are not legal as a filename.

See`netin` documentation for device file syntax.

**Note:** Do not use this function if you use Cadence Front-End Schematic packages.

* ***This function overwrites existing <`device`> and `devices.map` files in the directory.***

#### Arguments

|  |
| --- | ---
| `o_compDefDbid` | Component definition of the device file to write out.
| `t_output_dir` | Directory in which to write the files. If not provided, the current directory is used.
#### Value Returned

|  |
| --- | ---
| `t` | Device file successfully written.
| `nil` | Failed to write device file due to incorrect`dbid` or directory.
#### Example

`axlWriteDeviceFile( car(axlDBGetDesign()->components)->compdef)`

Writes device file of the definition for the first component instance off the design root.

### axlWritePackageFile

`axlWritePackageFile(o_symDefDbid[t_output_dir]`

`)`

`⇒ t/nil`

#### Description

Given a symbol definition, writes out symbol`.dra`, `.psm` and associated padstack files. Works like `dump_libraries` on a single symbol definition.

The file name root is the symbol definition name. For example, if the symbol definition (symDef) name is`CAPCK05`, the output files created are named `capck05.psm` and `capck05.dra`, plus any padstacks (in lower case) that are part of the symbol.

* ***This function overwrites existing files in the target directory.***

#### Arguments

|  |
| --- | ---
| `o_symDefDbid` | Symbol definition to store on disk.
| `t_output_dir` | Directory in which to store the files. If not provided, the current directory is used.
#### Value Returned

|  |
| --- | ---
| `t` | Files successfully written.
| `nil` | Failed to write files due to incorrect`dbid` or directory.
#### Example

`symDef = car(axlDBGetDesign()->components)->symbol->definition`

`axlWritePackageFile( symDef)`

Writes symbol files of the definition for the first component instance off the design root.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
