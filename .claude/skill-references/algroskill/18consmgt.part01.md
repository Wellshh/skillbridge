<!--
source: algroskill/18consmgt.md
part: 1/2
estimated_tokens: 13476
-->

### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

19
==

Constraint Management Functions
===============================

Overview
--------

This chapter describes the AXL-SKILL functions related to constraint management.

For a list of constraints, see Appendix B in the*Allegro Constraint Manager User Guide.*

### axlCnsAddVia

`axlCnsAddVia(t_csetNamet_padstackName)==> t/nil`

#### Description

Adds padstack to the constraint via list of a physical cset. Via is added to end of list (see[axlCnsGetViaList](#1076043 "19") of via ordering functionality in etch editing).

Padstack does not need to exist to be added to a constraint via list.

If`t_csetName` is `nil`, add padstack to all physical csets.

**Note:** If a via already exists in the via list, a`t` is returned. Locked csets return a `nil`.

#### Arguments

|  |
| --- | ---
| `t_csetName` | Name of physical cset or`nil` for all csets.
| `t_padstack` | Name of a via padstack.
#### Value Returned

|  |
| --- | ---
| `t` | If added.
| `nil` | Error in arguments; cset does not exist or illegal padstack name.
#### Examples

Add ALLPAD to all csets

> `axlCnsAddVia(nil "ALLPAD")`

Add ONEPAD to DEFAULT cset

> `axlCnsAddVia("DEFAULT" "ONEPAD")`

### axlCnsAssignPurge

`axlCnsAssignPurge(s_tableType) ==> x_delCount/ nil`

#### Description

Obsolete. Kept for backward compatibility

Purges either the physical or spacing assignment table of unused entries. Allegro PCB Editor supports two assignment tables: physical and spacing. This functionality duplicates that found in the Constraint Assignment Tables forms.

#### Arguments

|  |
| --- | ---
| `s_tableType`: | Spacing or Physical.
#### Value Returned

|  |
| --- | ---
| `nil` | Error.
| `x_delCount` | Number of entries deleted.
#### Example

> `axlCnsAssignPurge('spacing)`

#### See Also

[axlCnsList](#1110584 "19")

### axlCnsClassTableChange

```
axlCnsClassTableChange(o_dbidClassTables_csetType/ll_typeAndName[t_csetName]) -> o_dbidClassTable/nil
```

#### Description

This command changes the Csets associated with an existing net class table entry.

**Note:** See[axlCnsClassTableCreate](#1102983 "19") for complete family of functions.

You cannot change any table entries containing a region entry in Allegro PCB Designer or lower tiers.

#### Arguments

|  |
| --- | ---
| `o_dbidClassTable` | dbid of an existing classTable entry.
| `s_csetType` | symbol for cset type. spacing, 'physical or 'sameNet)
| `ll_typeAndName` | lists`s_csetType` and `t_csetName`
| `t_csetName` | cset name string
#### Value Returned

Updated classTable dbid or nil if failure

#### See Also

[axlCnsClassTableCreate](#1102983 "19")

#### Examples

Before running the sample skillcode for`axlCnsClassTableChange`, create a class table by running the example code in the [axlCnsClassTableCreate](#1102983 "19") command. Next, execute the following skill code and update the entry created in [axlCnsClassTableCreate](#1102983 "19") by adding it to the spacing.

`cset named 1, physical cset named 2 and a same net cset named 3.`

`prop = '((spacing "1") (physical "2") (sameNet "3"))`

`tbl = axlCnsClassTableChange(tbl prop)`

### axlCnsClassTableCreate

```
axlCnsClassTableCreate(g_class1g_class2g_regions_csetType/ll_typeAndName[t_csetName]) -> o_dbidClassTable/nil
```

#### Description

This command creates a class table entry that consists of any of the following:

* class to class (spacing only)

* region to class (spacing, same net and physical)

* region to class to class (spacing only)

Optionally, the command also associates a spacing cset, a physical cset, and same net cset with the table entry. If a class table entry already exists, it is modified with the provided csets.

Regions are not available in Allegro PCB Designer and lower products. Command will fail if you attempt to create a region-based table entry in these products. Class tables may not be created in symbol editor.

Points to remember:

* The order of class1 and class2 does not matter.

* If an entry already exists it will return the existing entry.

* Netclasses can be classified by domain (spacing and/or physical). If a netclass is restricted to one domain, it is possible to create a netclass to any entry that crosses domains. This table entry will be ignored by DRC. For example, you have a netclass,`ANY`, in both physical and spacing domains; and another netclass `PHYS`that is restricted to the physical domain. It is possible to create a `ANY` to `PHYS` relationship which is only appropriate in the spacing domain but the `PHYS` netclass is not legal in that domain.

> **Note:** This condition might be tested for and rejected in future releases.

* DRC is set out-of-date, you must manually update the DRC.

* Unlike Constraint Manager, you can add cset names that don't yet exist in the database. In these cases, we will automatically create a cset. Check via axlCnsList if your cset exists if you don't wish to create new csets.

* Class table entries may also have constraint overrides attached via property overrides (`axlDBAddProp`)

#### Arguments

|  |
| --- | ---
| `g_class1` | NETCLASS dbid or name of name class
| `g_class2` | NETCLASS dbid, name of name class or nil
| `g_region` | REGION dbid, name of region or nil
| `s_csetType` | symbol cset type one of 'spacing, 'physical or 'samenet
| `t_csetName` | string cset name for given type
| `ll_typeAndName` | option list of values where you have  `((s_csetType t_csetName) (s_csetType t_csetName) ...)`
#### Value Returned

returns`dbid` of type `classTable` for new or existing cset or nil if error

#### See Also

[axlCnsClassTableFind](#1102985 "19"), [axlCnsClassTableSeek](#1104268 "19"), [axlCnsClassTableChange](#1102955 "19"), [axlCnsClassTableDelete](#1103600 "19"), axlCnsList,

Also see classTable dbid object description.

#### Examples

* Create appropriate entries in design

> `region = axlRegionCreate("ANALOG")`

> `ncls = axlNetClassCreate("VOLTAGE" '(spacing physical))`

* Add new spacing region-class table entry and give it the spacing cset "25MILS"

> `tbl = axlCnsClassTableCreate("VOLTAGE" nil "ANALOG" 'spacing "25MILS")`

* Alternative method plus also add a physical voltage cset.

> `props = '((spacing "25MILS") (physical "VOLTAGE"))`

> `tbl = axlCnsClassTableCreate(ncls nil region props)`

### axlCnsClassTableDelete

`axlCnsClassTableDelete(o_dbidClassTable/lo_dbidClassTable) -> t/nil`

#### Description

Deletes one or more entries in the class table.

DRC is marked out of date.

#### Arguments

|  |
| --- | ---
| `o_dbidClassTable` | dbid of an existing classTable entry.
| `lo_dbidClassTable` | deletes list of classTable entries.
#### Value Returned

`t` if successful, `nil` if an error

#### See Also

[axlCnsClassTableCreate](#1102983 "19"), [axlCnsDeleteRegionClassClassObjects](#1092421 "19"), [axlCnsDeleteClassClassObjects](#1092356 "19")

#### Examples

Create a classTable entry by executing example code in[axlCnsClassTableCreate](#1102983 "19"). Delete entry just created by running the following command.

> `axlCnsClassTableDelete(tbl)`

### axlCnsClassTableFind

`axlCnsClassTableFind(s_type[o_dbid]) -> lo_dbidClassTable/nil`

#### Description

This command searches the class table for class table entries matching the search criteria.

#### Arguments

* `` `match `` - returns all entries that contain provided region or class dbid (`o_dbid`)
* `` `netclass `` - returns all class entries (all entries except for wire and component)
* `` `classClass `` - returns all class to class entries
* `` `classRegion `` - returns all class to region entries
* `` `classClassRegion `` - returns all class to class to region entries
* `` `wireProf `` - returns all wire profile entries (APD/SIP only)
* `` `component `` - returns all component entries (APD/SIP only)
* only applicable for the match option will return all class table entries containing the dbid.

#### Value Returned

List of class table dbids matching search criteria or`nil` if no match is found.

#### See Also

[axlCnsClassTableCreate](#1102983 "19"), [axlCnsClassTableSeek](#1104268 "19"), [axlSelectByName](05selfnd.html#665244 "4")

#### Examples

* Return all class entries that effect physical, spacing or same net DRC

> `` tbl = axlCnsClassTableFind(`netclass) ``

* Return all entries that contain Region "`ANALOG`" entry (assumes design has a region called "ANALOG")

> `region = car (axlSelectByName("REGION" "ANALOG"))`

> `` tbl = axlCnsClassTableFind(`match region) ``

### axlCnsClassTableSeek

`axlCnsClassTableSeek(g_class1g_class2g_region) -> o_dbidClassTable/nil`

#### Description

This command seeks a specific class table entry matching exactly the provided`dbids`. Order of class1 and class2 does not matter since C1/C2 is the same as C2/C1 and only one entry exists in the table.

* Constraint overrides may exist on a table entry via the`prop` attribute. While fetching multiple table entries, best performance is achieved by using dbids or using [axlCnsClassTableFind](#1102985 "19").

#### Arguments

|  |
| --- | ---
| `g_class1` | NETCLASS dbid, name of net class or nil
| `g_class2` | NETCLASS dbid, name of net class or nil
| `g_region` | REGION dbid, name of region or nil
#### Value Returned

Class table entry matching search criteria or`nil` if none found.

#### See Also

[axlCnsClassTableCreate](#1102983 "19")

#### Examples

Create a classTable entry by executing example code in[axlCnsClassTableCreate](#1102983 "19")

* Return class table entry for a netclass called VOLTAGE and region called ANALOG.

> `tbl = axlCnsClassTableSeek("VOLTAGE" nil "ANALOG")`

* Alternative method using dbids

> `region = car( axlSelectByName("REGION" "ANALOG"))`

> `netclass = car( axlSelectByName("NETCLASS" "VOLTAGE"))`

> `tbl = axlCnsClassTableSeek(netclass nil region)`

### axlCNSCreate

`axlCNSCreate(g_domaint_namet_copyName)==> t/nil`

#### Description

Creates a new constraint set in the specified domain. For spacing and physical csets, you must supply an existing cset as the copy cset. If the`copyName` is nil, the DEFAULT cset is used. Electrical csets (ECsets) are created empty for a nil `copyName` . By default, the ECset created is empty. If you provide a second argument, the ECset contents are copied.

To assign a cset to a logical object such as a net, bus, or a netclass, assign a PHYSICAL\_CONSTRAINT\_SET, SPACING\_CONSTRAINT\_SET, SAME\_NET\_SPACING\_CONSTRAINT\_SET or ELECTRICAL\_CONSTRAINT\_SET property to the logical object where the value of the property is the cset name.

**Note:** Electrical csets cannot be created in Allegro PCB Designer.

#### Arguments

|  |
| --- | ---
| `g_domain` | Specifies the domain of the Cset. Possible values are Physical, spacing, electrical, or `sameNet.
| `t_name` | Name of new cset. (Changed to upper case) string must pass allowed character set
| `t_copyName` | Name of cset to use as template. If this is`nil`, spacing and physical domains use DEFAULT as the template, while in case of electrical domain, an empty ECset is created.
#### Value Returned

|  |
| --- | ---
| `t` | Cset created.
| `nil` | Failed for the following reasons: domain name is illegal; name of cset is illegal; cset already exists; or`copyName` cset does not exist.
#### See Also

[axlCNSEcsetCreate](#1074235 "19") , [axlCNSDelete](#1110310 "19") , [axlCnsList](#1110584 "19"), [axlDBAddProp](03dbcre8.html#367701 "15"), [axlNetClassCreate](15dbgrp.html#1077736 "16")

#### Example

Create a new physical cset called`foo`.

> `axlCNSCreate('physical "foo" nil)`

### axlCNSCsetLock

`axlCNSCsetLock(g_domaint_csetNameg_mode)==> t/nil`

#### Description

This locks or unlocks a constraint set in the given domain. See discussion in[axlCNSIsLockedDomain](#1121134 "19").

You should usually lock or unlock the entire domain since this matches the DRC user model. We provide this interface to temporary unlock a locked cset, make changes then reapply the lock.

**Note:** Changing the lock on a cset can take a considerable amount of time since DRC needs to be updated. In the spacing domain, dynamic shapes need to be updated. If doing other changes, consider cloaking axlDBCloak the entire process. This API already uses cloaking for the individual cset.

#### Arguments

|  |
| --- | ---
| `g_domain` | domain of cset;`'physical`, `'spacing`, `'sameNet`, `'electrical`
| `t_csetName` | cset name
| `g_mode` | may either be`t` (to lock) or `nil` to unlock
#### Value Returned

Returns`t` if updated lock status, `nil` an error.

#### Examples

Lock Spacing cset DEFAULT, which has a side effect of locking spacing and same net domains

> `axlCNSCsetLock('spacing "DEFAULT" t)`

#### See Also

[axlCNSIsLockedDomain](#1121134 "19")

### axlCNSDelete

`axlCNSDelete(g_domaint_name/o_dbidEcset)==> t/nil`

#### Description

Deletes a cset and its references to any objects such as nets, net classes, etc. Locked csets must first be unlocked before you delete them. If it is a spacing or physical domain, you cannot delete the DEFAULT cset. You cannot delete electrical csets in Allegro PCB Design L.

#### Arguments

|  |
| --- | ---
| `g_domain` | Specifies the domain of cset. Valid values are:`'physical`, `'spacing`, `'sameNet`, `'electrical`
| `t_name` | Name of cset.
| `o_dbidEcset` | If an ECset, its`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Cset deleted.
| `nil` | Cset not deleted because cset does not exist or the cset is locked, or cset is`t`.
**Example**

Deletes electrical cset named UPREV\_DEFAULT.

> `axlCNSDelete('electrical "UPREV_DEFAULT")`

#### See Also

[axlCNSCreate](#1106245 "19")

### axlCnsDeleteClassClassObjects

`axlCnsDeleteClassClassObjects() => x_delCount`

#### Description

Delete all Class-Class entries.

#### Arguments

None

#### Value Returned

The count of the objects deleted.

#### See Also

[axlCnsPurgeCsets](#1096942 "19")

### axlCnsDeleteRegionClassClassObjects

`axlCnsDeleteRegionClassClassObjects() => x_delCount`

#### Description

Deletes all Region-Class-Class entries.

#### Arguments

None

#### Value Returned

The count of the objects deleted.

#### See Also

[axlCnsPurgeCsets](#1096942 "19")

### axlCnsDeleteRegionClassObjects

`axlCnsDeleteRegionClassObjects() => x_delCount`

#### Description

Delete all Region-Class entries.

#### Arguments

None

#### Value Returned

The count of the objects deleted.

#### See Also

[axlCnsPurgeCsets](#1096942 "19")

### axlCnsDeleteVia

`axlCnsDeleteVia(t_csetNamet_padstackName)=> t/nil`

#### Description

Deletes padstack from the physical via constraint list,`t_csetName`. If `t_csetName` is `nil`, delete provided padstack from all physical constraint sets.

**Notes**:

* Will return`t` if asked to delete a via that does not exist in the via list.

* Locked csets will return a`nil`.

#### Arguments

|  |
| --- | ---
| `t_csetName` | Name of physical cset or nil for all csets.
| `t_padstack` | Name of a via padstack.
#### Value Returned

|  |
| --- | ---
| `t` | If deleted.
| `nil` | Error in arguments; cset does not exist or illegal padstack name.
#### Example

Delete via to default cset

> `axlCnsDeleteVia("DEFAULT" "VIA")`

Delete via to all csets

> `axlCnsDeleteVia(nil "VIA")`

#### See Also

[axlCnsGetViaList](#1076043 "19")and[axlPurgePadstacks](06intedt.html#821249 "5")

### axlCNSDesignModeGet

`axlCNSDesignModeGet(nil)⇒ ls_constraints`

`axlCNSDesignModeGet('all)⇒ lls_constraintNModes`

`axlCNSDesignModeGet('editable)⇒ t/nil`

`axlCNSDesignModeGet(s_name/t_name)⇒ s_mode/nil`

`axlCNSDesignModeGet(s_name/t_name'print) ==> t_name/nil`

#### Description

Gets the current DRC modes for checks that fall into the set of design constraints. These constraints pertain to the entire board. To determine the design constraint checks currently supported, use the`axlCNSDesignModeGet()` command.

The`'print` mode offers the name shown in reports like show element.

This has[axlDebug](23utils.html#756141 "24") support.

**Note:** Available constraint checks may change from release to release.

#### Arguments

|  |
| --- | ---
| `nil` | Returns all checks in design type DRC.
| `'all` | Returns all checks and current mode.
| `'editable` | Returns`t` if mode can be changed, `nil` mode is not changed and when in Allegro PCB Editor studio which does not offer this option.
| `s_name` | Symbol name of check.
| `t_name` | String name of check.
| `'print` | Printable constraint name option.
#### Value Returned

|  |
| --- | ---
| `ls_names` | List of checks (`s_name` ...)
| `lls_names` | List of checks and their mode ((`s_name` `s_mode`) ...)
| `s_mode` | Mode`'on`, `'off` or `'batch`
| `t_name` | The printable constraint name
#### Example 1

`axlCNSDesignModeGet(nil)`

Gets a current list of design constraints.

#### Example 2

`axlCNSDesignModeGet('all)`

Gets a list of settings for all design constraints.

#### Example 3

`axlCNSDesignModeGet('Package_to_Package_Spacing)`

Gets current setting of package to package.

#### Example 4

`axlCNSDesignModeGet("Negative_Plane_Islands")`

Gets current setting of negative plane islands using a string.

### axlCNSDesignModeSet

`axlCNSDesignModeSet(t_name/s_namet_mode/s_mode)⇒ t/nil`

`axlCNSDesignModeSet('allt_mode/smode)⇒ t/nil`

`axlCNSDesignModeSet(l_constraintNModest_mode/smode)⇒ t/nil`

`axlCNSDesignModeSet(ll_constraintNModes)⇒ t/nil`

#### Description

Sets the current DRC modes for design constraints. The modes control the DRC for that design constraint check on the entire board.

To determine the checks that are supported, use the following command:

`axlCNSDesignModeGet()`

You can set all checks using the argument`'all`, set individual checks using `t_name`, or set a list of checks to the same mode as follows:

> `'(s_name...) t_mode/s_mode`

> `'(t_name...) t_mode/s_mode`

You can list sets of checks as follows:

> `'((s_name/t_name s_mode/t_mode)...)`

For performance reasons, changing modes or values does not invoke DRC. You must manually invoke DRC. You can mark changes in order to perform fewer DRC updates, depending on your changes (see[axlCNSMapUpdate](#1074801 "19").)

**Note:** Available constraint checks may change from release to release.

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of check.
| `t_name` | String name of check.
| `s_mode` | Mode setting may be`'on`, `'off`, or `'batch`.
| `t_mode` | String mode setting may be`"on"`, `"off"` or `"batch"`
| `'all` | Returns all checks for a given tier of Allegro PCB Editor.
#### Value Returned

|  |
| --- | ---
| `t` | Success
| `nil` | Failure.
#### Example 1

`axlCNSDesignModeSet('Package_to_Place_Keepin_Spacing 'on)`

Turns on package to package keepin check.

#### Example 2

`axlCNSDesignModeSet('all 'batch)`

Makes all design constraints batch only.

#### Example 3

`axlCNSDesignModeSet('(Negative_Plane_Islands Pad_Soldermask_Alignment)' off)`

Turns two constraints off.

#### Example 4

`axlCNSDesignModeSet('((Package_to_Place_Keepout_Spacing 'on)) )`

Sets various constraints to different modes.

For a programming example, see`cns-design.il`, which you can find in the following location:

`<cdsroot>/share/pcb/examples/skill/cmds`

### axlCNSDesignValueCheck

`axlCNSDesignValueCheck(s_name/t_nameg_value)⇒ (t_string/nil, nil/t_errorMsg)/nil`

#### Description

Checks the syntax of the given value against the allowed syntax for the given constraint. You use the function`axlCNSDesignGetValue(nil)` to get the constraint names.

**Note:** Allowed syntax may change from release to release.

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of the constraint.
| `t_name` | String name of the constraint.
| `g_value` | Value to verify
#### Value Returned

|  |
| --- | ---
| `(``t_string``/nil)` | Value correct.`t_string` shows current user unit preference. For example, if you supply "10", the return might be `"10.0 MILS"` if `MILS` is the current database unit.
| (`nil`/`t_errorMsg`) | Value incorrect.`t_errorMsg` reflects the error.
| `nil` | Arguments are incorrect.
#### Examples

`axlCNSDesignValueCheck('Negative_Plane_Islands "10 mils")`

Tests if allowed to set.

### axlCNSDesignValueGet

`axlCNSDesignValueGet(nil[g_returnNameString])⇒ ls_constraints`

`axlCNSDesignValueGet('all[g_returnString])⇒ lls_constraintNValues`

`axlCNSDesignValueGet(s_name[g_returnString])⇒ f_value/t_value/nil`

#### Description

Fetches the values from those design constraints that support values. Use`axlCNSDesignValueGet(nil)` to determine the set of these constraints.

**Note:** Constraint checks may change from release to release.

#### Arguments

|  |
| --- | ---
| `nil` | Returns all checks that support values.
| `'all` | Returns all checks with values and current value.
| `s_name` | Symbol name of value.
| `t_name` | String name of value.
| `g_returnNameString` | Returns constraint names as strings (default is symbol return.)
| `g_returnString` | By default, this returns native type in user units (a float) for all checks supported. If`t`, return is a MKS string where `nil` returns native.
#### Value Returned

|  |
| --- | ---
| `ls_names` | List of all controls that support values (symbol.)
| `lls_constraintNValues` | List of all controls with their values  `'((``s_name``f_value``/``t_value``) ...`  `f_value` = user unit value, and `t_value` = MKS string value.
#### Example 1

`axlCNSDesignValueGet(nil)`

Gets a list of design constraints that support values.

#### Example 2

`axlCNSDesignValueGet('all 't)`

Gets a list of settings for all design constraints with values returned as MKS strings.

#### Example 3

`axlCNSDesignValueGet('Negative_Plane_Islands)`

`= 10.0`

Gets the current setting of`Negative_Plane_Islands` in user units.

#### Example 4

`axlCNSDesignValueGet("Pad_Soldermask_Alignment" t)`

`= "10 mils"`

Gets the current setting of`Pad_Soldermask_Alignment` as a MKS string (this passes in inquiry as a string).

### axlCNSDesignValueSet

`axlCNSDesignValueSet(t_name/s_namef_value/t_value)⇒ t/nil`

`axlCNSDesignValueSet(ll_constraintNValues)⇒ t/nil`

#### Description

This sets the value of the design constraint.

To determine the list of supported values, use the following command:

`axlCNSDesignValueGet(nil)`

You may set single values or a list of values:

`'((s_name/t_name f_value/t_value) ...)`

For performance reasons, changing a value does not invoke DRC. You must manually invoke DRC. See[axlCNSMapUpdate](#1074801 "19") for a set of interfaces you can use to mark changes in order to perform fewer DRC updates.

**Note:** Constraint checks may change from release to release.

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of check.
| `t_name` | String name of check.
| `f_value` | Floating point value provided is assumed to be in the default user unit for the constraint. Value may be rounded.
| `t_value` | If given as a string with MKS type, the value is converted to current user units for the constraint. Rounding may result.
#### Value Returned

|  |
| --- | ---
| `t` | Design constraint value set.
| `nil` | Failed to set design constraint value.
#### Example 1

`axlCNSDesignValueSet('Negative_Plane_Islands 10.0))`

Sets a negative plan tolerance to 10 in current database units.

#### Example 2

`axlCNSDesignValueSet('Negative_Plane_Islands "10.0 mils")`

Sets a negative plan tolerance to 10 mils.

#### Example 3

```
axlCNSDesignValueSet('((Negative_Plane_Islands "20 inches")        (Pad_Soldermask_to_Pad_Soldermask_Spacing 15.9)))
```

Sets various constraints to different values.

For a programming example, see`cns-design.il` which you can find in the following location:

`<cdsroot>/share/pcb/examples/skill/cmds`

### axlCNSEcsetCreate

`axlCNSEcsetCreate(t_name[t_copyName/o_dbidCopyEcset])⇒ o_dbidEcset/nil`

#### Description

Creates a new ECset. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets. The name must be legal and less than the maximum length allowed. Function fails if the ECset already exists.

By default, the ECset is created empty. You can provide a second argument to copy the contents of another ECset into the new ECset.

#### Arguments

|  |
| --- | ---
| `t_name` | Name of new ECset (Changed to upper case)String must pass allowed character set.
| `t_copyName` | Optional name to copy from.
#### Value Returned

|  |
| --- | ---
| `o_dbidEcset` | `dbid` of the new ECset
| `nil` | Failed due to one of the following: the name is illegal, or the ECset already exists.
#### See Also

[axlCNSDesignModeSet](#1073830 "19"), [axlCNSCreate](#1106245 "19")

**Example 1**

`axlCNSEcsetCreate("MyEmptyEcset")`

Creates a new empty ECset.

**Example 2**

`p = car(axlDBGetDesign()->ecsets)`

`axlCNSEcsetCreate("MyNewEcset" p)`

Copies the contents of the first ECset in a list.

### axlCNSEcsetDelete

`axlCNSEcsetDelete(t_name/o_dbidEcset)⇒ t/nil`

#### Description

Deletes an ECset from the Allegro PCB Editor database and also deletes the`ELECTRICAL_CONSTRAINT_SET` property from any nets assigned this ECset value. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

If the ECset is locked, you must unlock it before you can delete it.

#### Arguments

|  |
| --- | ---
| `t_name` | ECset name
| `o_dbidEcset` | ECset`dbid`
#### Value Returned

|  |
| --- | ---
| `t` | ECset successfully deleted.
| `nil` | ECset is not deleted because of one of the following: the name is incorrect, or ECset is locked.
**Example 1**

`axlCNSEcsetDelete("UPREV_DEFAULT")`

Deletes an ECset by name.

**Example 2**

`p = car(axlDBGetDesign()->ecsets)`

`axlCNSEcsetDelete(p)`

Deletes the first ECset in a list of ECsets.

### axlCNSEcsetGet

`axlCNSEcsetGet(t_name)⇒ o_dbidEcset/nil`

#### Description

Returns the`dbid` of the electrical cset when you request it by the ECset name. Electrical Constraint Set (ECset) is a mechanism for grouping a set of electrical constraints and applying them to a set of nets.

#### Arguments

|  |
| --- | ---
| `t_name` | ECset name.
#### Values Returned

|  |
| --- | ---
| `o_dbidEcset` | `dbid` of the ECset requested.
| `nil` | Function failed due to an illegal name.
#### See Also

[axlCNSEcsetValueGet](#1074475 "19")and [axlCnsList](#1110584 "19")

**Example**

`axlCNSEcsetGet("foo")`

Tests for the existence of an ECset named`foo`.

### axlCNSEcsetModeGet

`axlCNSEcsetModeGet(nil)⇒ ls_constraints`

`axlCNSEcsetModeGet('all)⇒ lls_constraintNModes`

`axlCNSEcsetModeGet(s_name/t_name)⇒ s_mode/nil`

`axlCNSEcsetModeGet(s_name/t_name'print) ==> t_name/nil`

#### Description

Returns the current DRC modes for checks that are members of electrical constraints. These modes pertain to the entire board. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

The`'print` mode offers the name shown in reports, similar to the show element command.

This has[axlDebug](23utils.html#756141 "24") support.

**Note:** Not all checks are available in all levels of Allegro PCB Editor. To determine the set of checks supported, use the command:`axlCNSEcsetModeGet()`. Constraint checks may change from release to release.

#### Arguments

|  |
| --- | ---
| `nil` | Returns all checks in design type DRC.
| `'all` | Returns all checks and current mode.
| `s_name` | Symbol name of the check.
| `t_name` | String name of the check.
| `'print` | Printable constraint name option.
#### Value Returned

|  |
| --- | ---
| `ls_names` | List of checks (`s_name` ...).
| `lls_names` | List of checks and related modes ((`s_name` `s_mode`) ...)
| `s_mode` | Returns mode`'on`, `'off`, or `'batch`
| `t_name` | Printable constraint name .
#### See Also

[axlCNSEcsetModeSet](#1074474 "19"), [axlCNSEcsetValueGet](#1074475 "19")

**Example 1**

`axlCNSEcsetModeGet(nil)`

Lists currently available electrical constraints.

**Example 2**

`axlCNSEcsetModeGet('all)`

Lists settings for all electrical constraints.

**Example 3**

`axlCNSEcsetModeGet('Maximum_Stub_Length)`

Shows current setting of stub length.

**Example 4**

`axlCNSEcsetModeGet("Maximum_Via_Count")`

Shows current setting of via count.

### axlCNSEcsetModeSet

`axlCNSEcsetModeSet(t_name/s_namet_mode/s_mode)⇒ t/nil`

`` axlCNSEcsetModeSet(`allt_mode/s_mode)⇒ t/nil ``

`axlCNSEcsetModeSet(l_constraintNModest_mode/s_mode)⇒ t/nil`

`axlCNSEcsetModeSet(ll_constraintNModes)⇒ t/nil`

#### Description

Sets the DRC modes for checks that are members of the electrical constraints set. These modes control the entire board. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

**Note:** Not all checks are available in all levels of Allegro PCB Editor. To determine the set of checks supported, use the command:`axlCNSEcsetModeGet()`. Constraint checks may change from release to release.

You can set all checks using the argument`'all`, set individual checks using `t_name`, or set a list of checks with the same mode as shown:

`'(s_name ...) t_mode/s_mode`

`'(t_name ...) t_mode/s_mode`

You can list sets of checks as shown:

`'((t_name t_mode) ...)`

`'((s_name s_mode) ...)`

For performance reasons, changing modes or values does not invoke DRC. You must manually invoke DRC. See[axlCNSMapUpdate](#1074801 "19") for a set of interfaces you can use to mark changes in order to perform fewer DRC updates.

* ***Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.***

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of the check.
| `t_name` | String name of the check.
| `s_mode` | Mode setting; may be`'on`, `'off`, or `'batch`.
| `t_mode` | String mode setting; may be`"on"`, `"off"`, or `"batch"`.
| `` `all `` | Set all checks for a given tier of Allegro PCB Editor.
#### Value Returned

|  |
| --- | ---
| `t` | DRC mode set.
| `nil` | DRC mode not set.
#### Example 1

`axlCNSEcsetModeSet('Maximum_Via_Count 'off)`

Turns off max via check.

#### Example 2

`axlCNSEcsetModeSet('all 'batch)`

Makes all electrical constraints batch only.

#### Example 3

`axlCNSEcsetModeSet('(Maximum_Crosstalk Route_Delay) 'off)`

Turns two constraints off.

#### Example 4

```
axlCNSEcsetModeSet( '((Maximum_Crosstalk off)        (Propagation_Delay on) (Route_Delay 'on) (Impedance 'batch)) )
```

Sets various constraints to different modes.

### axlCNSEcsetValueCheck

`axlCNSEcsetValueCheck(s_name/t_nameg_value)⇒ (t/t_errorMsg)/nil`

#### Description

Checks the syntax of the given value against the allowed syntax for the given constraint. You use the function`axlCNSEcseValueGet (nil)` to get the constraint names. Electrical Constraint Set (ECSet) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

**Note:** Allowed syntax may change from release to release.

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of constraint.
| `t_name` | String name of constraint.
| `g_value` | Value to verify.
#### Value Returned

|  |
| --- | ---
| `t` | Syntax is correct.
| `t_errorMsg` | Syntax is incorrect. The message indicates the reason.
| `nil` | Constraint name is not supported.
#### Examples

`axlCNSEcsetValueCheck('Net_Schedule_Topology "STAR")`

Tests if allowed to set.

### axlCNSEcsetValueGet

`axlCNSEcsetValueGet(nil[g_returnNameString])⇒ ls_constraints`

`axlCNSEcsetValueGet('all[g_returnString])⇒ lls_constraintNValues`

```
axlCNSEcsetValueGet(o_ecsetDbid/t_ecsetNames_name[g_returnString])⇒ f_value/t_value/nil
```

#### Description

Fetches the constraint values for a given ECset. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

Use`axlCNSEcsetValueGet(nil)` to determine the set of allowable constraints.

Each ECset may have all or none of the allowed constraints.

You can retrieve the ECset values by the ECset name or by its`dbid`. You can get the `dbid` of an ECset by using one of the following commands:

* `axlDBGetDesign()->ecsets`

* `axlCNSEcsetCreate()`

**Note:** Constraint checks may change from release to release. Not all checks are available in all levels of Allegro PCB Editor.

#### Arguments

|  |
| --- | ---
| `o_ecsetDbid` | ECset`dbid`.
| `t_ecsetName` | ECset name.
| `nil` | Returns all checks that support values.
| `'all` | Returns all checks with values and current value.
| `s_name` | Symbol name of value.
| `t_name` | String name of value.
| `g_returnNameString` | Returns constraint names as strings (default is symbol return)
| `g_returnString` | Default is to return native type for all checks supported, this is in user units (a float). If`t`, return is an MKS string where `nil` returns native.
#### Value Returned

|  |
| --- | ---
| `ls_names` | List of all controls that support values (symbol).
| `lls_constraintNValues` | List of all controls with their values as shown:  `'((``s_name``f_value``/``t_value``) ...`  `f_value` = user unit value and `t_value` = MKS string value.
#### Example 1

`axlCNSEcsetValueGet(nil)`

Gets a current list of design constraints that support values.

#### Example 2

`ecsets = axlDBGetDesign()->ecsets`

`ecset = car(ecsets)`

`axlCNSEcsetValueGet(ecset 'all t)`

Gets a list of settings for all design constraints with values returned as MKS strings.

#### Example 3

`axlCNSEcsetValueGet("UPREVED_DEFAULT" 'Maximum_Via_Count)`

`= 10.0`

Gets the current setting of`Maximum_Via_Count` on ECset `UPREVED_DEFAULT`.

#### Example 4

`axlCNSEcsetValueGet("UPREVED_DEFAULT" "Pad_Soldermask_Alignment" t)`

`= "10 mils"`

Gets the current setting of`Pad_Soldermask_Alignment` as a MKS string (this passes in inquiry as a string).

### axlCNSGetDefaultMinLineWidth

`axlCNSGetDefaultMinLineWidth(t_sublassName)=> f_minLineWidthValue`

#### Description

Retrieves the minimum default line width value for the specific subclass.

#### Arguments

|  |
| --- | ---
| `t_subclassname` | A subclass name of the ETCH or CONDUCTOR class.
#### Value Returned

|  |
| --- | ---
| `f_minSpacingValue` | Minimum line width value (in design units) on the subclass.
#### Example

> `axlCNSGetDefaultMinLineWidth("TOP")`

> `=> 0.004`

Gets the minimum line width value for layer TOP.

### axlCNSGetPhysical

`axlCNSGetPhysical(t_csett_layers_constraint[g_string])==> g_value/nil`

`axlCNSGetPhysical(t_csett_layernil[g_string])==> ll_nameValue/nil`

`axlCNSGetPhysical(nilnilnil)==> ls_cnsTypes`

#### Description

In its first operational mode, obtains the value of a physical constraint given a cset and layer. In the second mode of operation, it obtains all physical constraint as name/value pairs for a cset on a layer. This, in turn, may be passed to`axlCNSSetPhysical`.

In the final mode, a list of all supported physical constraints may be obtained by passing three`nil`valuesto the interface:

`axlCNSGetPhysical(nil nil nil)`

#### Data types

Unless otherwise specified, constraints are in current design units.

|  |
| --- | ---
| `allow_etch` | (boolean)`t/nil`
| `allow_ts` | (symbol) NOT\_ALLOWED, ANYWHERE, PINS\_ONLY, PIN\_VIAS\_ONLY
| `allow_padconnect` | (symbol) ALL\_ALLOWED, VIAS\_PINS\_ONLY, VIAS\_VIAS\_ONLY, NOT\_ALLOWED
| `vias` | (string) colon separates the list of via names. Vias are not layer dependent, so are only returned for TOP. Order is important for etch editing working layer model. Use[axlCnsGetViaList](#1076043 "19") to get the via list as a list of strings.  When`width_max, dp_neck_gap, dp_primary_gap,`and`necklength_max` are set to 0, it indicates that this value is not used.
#### Arguments

|  |
| --- | ---
| `t_cset` | Name of a physical cset. Can use "" for "DEFAULT".
| `t_layer` | ETCH layer name (for example, "ETCH/TOP" or "TOP"). If`nil,`applies the change to all layers.
| `s_constraint` | Name of constraint. If`nil,` returns a set of symbol/value pairs of all constraints.
| `g_string` | By default, returns value in the native units of the constraint. If`g_string` is`t``,`always returns data as a string.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value of constraint in design units, except for`same_net`, which is returned as a `t/nil`.
| `ll_nameValue` | Name values of pairs of physical constraint symbol and constraint value for all physical (`s_constraint g_value`).  '((`necklength_min` 10.0) (`neckwidth_max` 5.0) ...)
|
| `ls_cnsTypes` | List of supported physical constraint names.
| `nil` | Returns`nil` on error (or `allow_etch`).
#### Example 1

> `axlCNSGetPhysical("" "TOP" 'width_min)`

Gets the minimum line width in the default cset, TOP layer.

**Example 2**

> `axlCNSGetPhysical("VOLTAGE" "BOTTOM" nil)`

Gets all physical constraints for the DEFAULT, BOTTOM layer

**Example 3**

> `axlCNSGetPhysical("" "TOP" 'vias)`

Gets the via list for default cset.

**Example 4**

> `axlCNSGetPhysical(nil nil nil)`

Gets supported physical constraint symbols.

**Example 5**

> `cset = "" ;; DEFAULT cset`

> `foreach(subclass axlSubclassRoute()`

> `layer = axlCNSGetPhysical(cset subclass nil)`

> `printf("\nLAYER=%s\n\tconstraints=%L\n" subclass, layer)`

> `)`

Fetches all layers and constraints of physical cset DEFAULT.

#### See Also

[axlCNSSetPhysical](#1084387 "19")`,`[axlCnsList](#1110584 "19")`,`[axlSubclassRoute](04parmgt.html#1119179 "3"), and [axlCnsGetViaList](#1076043 "19")

### axlCNSGetPinDelayEnabled

`axlCNSGetPinDelayEnabled() => t/nil`

#### Description

Returns if pin delay is enabled.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t:` | Pin delay is enabled.
| `nil:` | Pin delay is not enabled.
### axlCNSGetPinDelayPVF

`axlCNSGetPinDelayPVF()=> t_pinDelayPVF`

#### Description

Returns the pin delay propagation velocity factor.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t_pinDelayPVF:` | If the pin delay propagation velocity factor is defined, it is returned as a string. If not defined, a blank string is returned.
### axlCNSGetSameNet

`axlCNSGetSameNet(t_csett_layers_constraint[g_string])==> g_value/nil`

`axlCNSGetSameNet(t_csett_layernil[g_string])==> ll_nameValue/nil`

`axlCNSGetSameNet(nilnilnil)==> ls_cnsTypes`

#### Description

Documentation same as[axlCNSGetSpacing](#1093423 "19").

#### Arguments

|  |
| --- | ---
| `t_cset:` | name of a same net spacing cset. Can use "" for "DEFAULT".
| `t_layer:` | ETCH layer name ( "ETCH/TOP" or "TOP"). If`nil` apply change to all layers.
| `s_constraint:` | name of constraint. If`nil` returns a set of symbol/value pairs of all constraints.
| `g_string:` | By default returns value in the native units of the constraint. If`g_string` is`t,` it will always return data as a string.
#### Value Returned

|  |
| --- | ---
| `g_value:` | value of constraint in design units
| `l_nameValue` - | name value pairs of spacing constraint symbol and constraint value for all spacing. (`s_constraintg_value`). `'((shape_shape 10.0) (line_line 5.0) ...)`
| `ls_cnsTypes` - | list of supported same net spacing constraint names.
| `nil-` | returns nil on error (or same\_net).
#### See Also

[axlCNSSetSameNet](#1095490 "19"), [axlCnsList](#1110584 "19"), [axlCNSGetSpacing](#1093423 "19")

#### Examples

Get shape to shape same net spacing in default cset, TOP layer

> `axlCNSGetSameNet("" "TOP" 'shape_shape)`

Get all same net constraints for 25\_MIL\_SPACE, bottom layer

> `axlCNSGetSameNet("25_MIL_SPACE" "BOTTOM" nil)`

Get all same net constraints for DEFAULT, bottom layer as strings

> `axlCNSGetSameNet("" "BOTTOM" nil t)`

Get supported same net constraint symbols

> `axlCNSGetSameNet(nil nil nil)`

Fetch all layers and constraints of same net cset DEFAULT

> `cset = "" ;; DEFAULT cset`

> `foreach(subclass axlSubclassRoute()`

> `layer = axlCNSGetSameNet(cset subclass nil)`

> `printf("\nLAYER=%s\n\tconstraints=%L\n" subclass, layer)`

> `)`

### axlCNSGetSameNetXtalkEnabled

`axlCNSGetSameNetXtalkEnabled() => t/nil`

#### Description

Returns if Same Net Xtalk is enabled.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t:` | same net Xtalk is enabled.
| `nil:` | same net Xtalk is not enabled.
### axlCNSGetSpacing

`axlCNSGetSpacing(t_csett_layers_constraint[g_string])==> g_value/nil`

`axlCNSGetSpacing(t_csett_layernil[g_string])==> ll_nameValue/nil`

`axlCNSGetSpacing(nilnilnil) ==> ls_cnsTypes`

#### Description

In its first operational mode, obtains the value of a spacing constraint given a cset and layer. All values are returned in design units, except for`same_net,` which is a boolean (`t/nil`). In a second mode of operation, it obtains all spacing constraints as name/value pairs for a cset on a layer. This, in turn, may be passed to `axlCNSSetSpacing`. For the final mode, a list of supported spacing constraints may be obtained by passing three `nil` values to this interface:

`axlCNSGetSpacing(nil nil nil)`

#### Data types

* Unless otherwise specified, constraints are in current design units.

|  |
| --- | ---
| `same_net` | (boolean)`t/nil`
* bbvia\_gap is not layer dependent. You must use the TOP layer name as the`t_layer` value to get or set this value.

#### Arguments

|  |
| --- | ---
| `t_cset` | Name of a spacing cset. You can use "" for "DEFAULT".
| `t_layer` | ETCH layer name (for example, "ETCH/TOP" or "TOP"). If`nil,` applies change to all layers.
| `s_constraint` | Name of constraint. If`nil,` returns a set of symbol/value pairs of all constraints.
| `g_string` | By default, returns value in the native units of the constraint. If`g_string` is `t`, always returns data as a string.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value of constraint in design units, except for`same_net`, which is returned as `t/nil`.
| `ll_nameValue` | Name value pairs of spacing constraint symbol and constraint value for all spacing (`s_constraint g_value`).'((shape\_shape 10.0) (line\_line 5.0) ...)
| `ls_cnsTypes` | List of supported spacing constraint names.
| `nil` | Returns`nil` on error (or `same_net`).
#### Example 1

> `axlCNSGetSpacing("" "TOP" 'shape_shape)`

Gets shape to shape spacing in default cset, TOP layer.

**Example 2**

> `axlCNSGetSpacing("25_MIL_SPACE" "BOTTOM" nil)`

Gets all spacing constraints for 25\_MIL\_SPACE, bottom layer.

**Example 3**

> `axlCNSGetSpacing("" "BOTTOM" nil t)`

Gets all spacing constraints for DEFAULT, bottom layer as strings.

**Example 4**

> `axlCNSGetSpacing(nil nil nil)`

Gets supported spacing constraint symbols.

**Example 5**

> `cset = "" ;; DEFAULT cset`

> `foreach(subclass axlSubclassRoute()`

> `layer = axlCNSGetSpacing(cset subclass nil)`

> `printf("\nLAYER=%s\n\tconstraints=%L\n" subclass, layer)`

> `)`

Fetches all layers and constraints of spacing cset DEFAULT.

#### See Also

[axlCNSSetSpacing](#1111453 "19"),[axlCnsList](#1110584 "19")`,` and [axlSubclassRoute](04parmgt.html#1119179 "3")

### axlCNSGetViaZEnabled

`axlCNSGetViaZEnabled() => t/nil`

#### Description

Returns if Via Z is enabled.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t:` | via Z is enabled
| `nil:` | via Z is not enabled
### axlCNSGetViaZPVF

`axlCNSGetViaZPVF()=> t_viaZPVF`

#### Description

Returns the via Z propagation velocity factor

#### Argument

None

#### Value Returned

|  |
| --- | ---
| `t_viaZPVF:` | If the via Z propagation velocity factor is defined, it is returned as a string. If not defined, a blank string is returned.
### axlCNSPhysicalModeGet

`axlCNSPhysicalModeGet(nil) ==> ls_constraints`

`axlCNSPhysicalModeGet('all) ==> lls_constraintNModes`

`axlCNSPhysicalModeGet(s_name/t_name) ==> s_mode/nil`

`axlCNSPhysicalModeGet(s_name/t_name'print) ==> t_name/nil`

#### Description

This fetches the current physical drc mode(s). Modes determine if a particular constraint is on or off. These modes apply to the entire board. To determine the set currently supported, physical modes do a`axlCNSPhysicalModeGet`(nil). The physical mode set may be a subset of physical values since the implementation may associate certain values under a master mode. For example, via\_list is not a constraint and the diff pair mode is under the ecset domain.

**Note:** Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

|  |
| --- | ---
| `nil` | returns all modes that are in spacing domain
| `all` | returns all checks and current mode
| `s_name` | symbol name of check.
| `t_name` | string name of check
| `'print` | printable constraint name option
#### Value Returned

|  |
| --- | ---
| `ls_names` | list of checks (s\_name ...)
| `lls_names` | list of checks and their mode ((s\_name s\_mode) ...)
| `s_mode` | mode 'on, or 'off
| `t_name` | the printable constraint name
#### Examples

Get current list of physical constraints

> `axlCNSPhysicalModeGet(nil)`

Get list of settings for all physical constraints

> `axlCNSPhysicalModeGet('all)`

Get current mode of max line with

> `axlCNSPhysicalModeGet('width_max)`

Get current setting of allow Ts using a string

> `axlCNSPhysicalModeGet("allow_ts")`

#### See Also

[axlCNSPhysicalModeSet](#1094146 "19"), [axlCNSGetPhysical](#1083339 "19")

### axlCNSIsCsetLocked

`axlCNSIsCsetLocked(g_domaint_csetName)==> t/nil`

#### Description

This returns if a cset is locked. See discussion in[axlCNSIsLockedDomain](#1121134 "19").

A locked cset has the following characteristics:

* Cannot be edited

* Has the effect of locking the entire domain

#### Argument

|  |
| --- | ---
| `g_domain` | domain of cset; '`physical`, '`spacing`, '`sameNet`, '`electrical`
#### Value Returned

* `t` if cset is deleted

* `nil`, if cset is not deleted due to being locked or not a cset

#### Examples

Command to check if the cset DEFAULT is locked

`axlCNSIsCsetLocked('electrical ''DEFAULT'')`

#### See Also

[axlCNSDesignModeSet](#1073830 "19")

### axlCNSIsLockedDomain

`axlCNSIsLockedDomain(g_domain)==> t/nil`

#### Description

Used to check if the is constraint domain locked. A locked constraint domain has the following characteristics:

* csets cannot be edited, although new csets can be added

* any object (e.g. net) level property overrides are ignored

**Notes:**

* The spacing and sameNet domains are locked as a single domain.

* Locking is typically done via the techfile. In the techfile, you can lock individual csets. If one cset is locked, Allegro PCB Editor treats the entire domain as locked from the DRC perspective. When a domain is locked, any object level property constraint override is ignored.

* If a cset is locked it cannot be modified or deleted.

* Use[axlCnsList](#1110584 "19")`(nil)`to get a list all domains.

#### Arguments

|  |
| --- | ---
| `g_domain` | domain of cset;`'physical`, `'spacing`, `'sameNet`, `'electrical`
#### Value Returned

* t if a constraint domain is locked.

* nil - domain is not locked

#### Examples

* Command to check if the Electrical domain locked

> `axlCNSIsLockedDomain('electrical)`

* To find a list of locked domains

> `lockedDomains = setof( x axlCnsList(nil) axlCNSIsLockedDomain(x))`

#### See Also

[axlCNSCsetLock](#1110307 "19"), [axlCNSIsCsetLocked](#1121133 "19"), [axlCNSLockDomain](#1121115 "19"), [axlCNSDesignModeSet](#1073830 "19"), [axlCnsList](#1110584 "19")

### axlCNSLockDomain

`axlCNSLockDomain(g_domaing_mode)==> t/nil`

#### Description

This command locks or unlocks a constraint domain.

See discussion in[axlCNSIsLockedDomain](#1121134 "19").

**Note:** Changing the lock on a domain can take a considerable amount of time since DRC status for that domain needs to be updated. In the spacing domain dynamic shapes also need to be updated. If doing other changes, you should consider cloaking (axlDBCloak the entire process. This API already uses cloaking.

#### Arguments

|  |
| --- | ---
| `g_domain` | domain of cset;`'physical`, `'spacing`, `'sameNet`, `'electrical`
| `g_mode` | may either be`t` (to lock) or `nil` to unlock
#### Value Returned

Returns`t` if lock status is updated, and `nil` in case of an error.

#### Examples

Lock Spacing and Same net spacing domains

> `axlCNSLockDomain('spacing t)`

#### See Also

[axlCNSIsLockedDomain](#1121134 "19")

### axlCNSPhysicalModeSet

`axlCNSPhysicalModeSet(t_name/s_namet_mode/s_mode)==> t/nil`

`axlCNSPhysicalModeSet('allt_mode/smode)==> t/nil`

`axlCNSPhysicalModeSet(l_constraintNModest_mode/smode)==> t/nil`

`axlCNSPhysicalModeSet(ll_constraintNModes)==> t/nil`

#### Description

This sets the current drc modes (on/off) for checks in the area of physical constraints. These modes are global. To determine the constraints modes currently supported do a`axlCNSPhysicalModeGet(nil)`. We support several interfaces. All checks may be set (`'all`), individual checks, (`t_name`), list of checks with a same mode`'(s_name ...) t_mode/s_mode'(t_name ...) t_mode/s_mode` and sets of checks via a list of: `'((s_name/t_name s_mode/t_mode) ....)`

The constraints names may be be passed as a symbol or a string. For performance reasons, you should either do all your updates in a single call or wrap individual changes in the map API (see axlCNSMapUpdate).

**Note:** Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

|  |
| --- | ---
| `s_name:` | symbol name of check.
| `t_name:` | string name of check.
| `s_mode:` | mode setting; may be 'on or 'off.
| `t_mode:` | string mode setting "on or "off".
| `'all:` | set all checks for given tier of Allegro.
#### Value Returned

Returns`t` if succeeds or nil if failure.

#### See Also

[axlCNSPhysicalModeGet](#1093726 "19"), [axlCNSGetPhysical](#1083339 "19"), [axlCNSMapUpdate](#1074801 "19")

#### Examples

Turn all constraints off

> `axlCNSPhysicalModeSet('all 'off)`

Turn on line width max

> `axlCNSPhysicalModeSet('width_max 'on)`

> `Turn two constraint to on`

> `axlCNSPhysicalModeSet('(bbvia_stagger_max bbvia_stagger_min) 'on)`

Set various constraints to different modes

> `axlCNSPhysicalModeSet( '((width_max off) (allow_etch 'on)) )`

### axlCNSSameNetModeGet

`axlCNSSameNetModeGet(nil) ==> ls_constraints`

`axlCNSSameNetModeGet('all) ==> lls_constraintNModes`

`axlCNSSameNetModeGet(s_name/t_name) ==> s_mode/nil`

`axlCNSSameNetModeGet(s_name/t_name'print) ==> t_name/nil`

#### Description

Same as[axlCNSSpacingModeGet](#1096197 "19").

#### Arguments

|  |
| --- | ---
| `nil` | returns all modes that are in same net spacing domain
| `'all` | returns all checks and current mode
| `s_name` | symbol name of check.
| `t_name` | string name of check
| `'print` | printable constraint name option
#### Value Returned

|  |
| --- | ---
| `ls_names` | list of checks (`s_name ...`)
| `lls_names` | list of checks and their mode (`(s_name s_mode`) ...)
| `s_mode` | mode 'on, or 'off
| `t_name` | The printable constraint name
#### Examples

Get current list of same net spacing constraints

> `axlCNSSameNetModeGet(nil)`

Get list of settings for all same net spacing constraints

> `axlCNSSameNetModeGet('all)`

Get current setting of line to line

> `axlCNSSameNetModeGet('line_line)`

Get current setting of line to shape using a string

> `axlCNSSameNetModeGet("line_shape")`

#### See Also

[axlCNSSameNetModeSet](#1095039 "19"), [axlCNSGetSameNet](#1092689 "19"), [axlCNSSpacingModeGet](#1096197 "19")

### axlCNSSameNetModeSet

`axlCNSSameNetModeSet(t_name/s_namet_mode/s_mode)==> t/nil`

`axlCNSSameNetModeSet('allt_mode/smode)==> t/nil`

`axlCNSSameNetModeSet(l_constraintNModest_mode/smode)==> t/nil`

`axlCNSSameNetModeSet(ll_constraintNModes)==> t/nil`

#### Description

Same as axlCNSSpacingModeSet.

#### Arguments

|  |
| --- | ---
| `s_name:` | symbol name of check.
| `t_name:` | string name of check.
| `s_mode:` | mode setting; may be 'on or 'off.
| `t_mode:` | string mode setting "on or "off".
| `'all:` | set all checks for given tier of Allegro.
#### Value Returned

Returns`t` if succeeds or `nil` if failure.

#### See Also

[axlCNSSameNetModeGet](#1094771 "19"), [axlCNSGetSameNet](#1092689 "19"), [axlCNSSpacingModeSet](#1096534 "19")

#### Examples

Turn off all same net spacing constraints

> `axlCNSSameNetModeSet('all 'off)`

Turn on line to line check

> `axlCNSSameNetModeSet('line_line 'on)`

Turn two constraints to on

> `axlCNSSameNetModeSet('(line_shape thrupin_line) 'on)`

Set several constraints to different modes

> `axlCNSSameNetModeSet( '((line_line off)`

> `(thrupin_shape on)) )`

### axlCNSSetPhysical

`axlCNSSetPhysical(t_cset/nilt_layer/nils_constraintg_value)==> t/nil`

`axlCNSSetPhysical(t_cset/nilt_layer/nilll_constraintValuesnil)==> t/nil`

#### Description

Allows updating physical constraint values. By passing nil at the appropriate argument, values for all csets and all layers may be changed.

#### Data types

See`axlCNSGetPhysical` for the data type of each constraint.

Allowed Design Units:

* A number (integer or floating point) where units is current design units. Must not exceed accuracy of the design.

* Unitless string where accuracy cannot exceed database accuracy.

* String with units, data converted to current design units.

Allowed Data Values:

* Boolean: Use`t/nil` or `"true"/"false"`.

* Symbol: Use the symbol name or its string.

* For best performance, when calling multiple axlCNS interfaces to update constraint values, wrap them in the`axlCnsMap` interfaces as shown below:

`axlCNSMapClear()`

`axlCNSSetPhysical(nil nil 'width_min 5)`

`axlCNSSetPhysical("" nil 'allow_padconnect 'VIAS_PINS_ONLY)`

`...`

`axlCNSMapUpdate()`

Single change calls do not require this.

