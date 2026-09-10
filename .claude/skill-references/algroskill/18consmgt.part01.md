<!--
source: algroskill/18consmgt.md
part: 1/2
estimated_tokens: 13387
-->

### axlCnsAddVia

`axlCnsAddVia( t_csetName t_padstackName ) => t/nil`

#### Description

Adds padstack to the constraint via list of a physical cset. Via is added to end of list (see axlCnsGetViaList of via ordering functionality in etch editing).

Padstack does not need to exist to be added to a constraint via list.

If `t_csetName` is `nil`, add padstack to all physical csets.

Note: If a via already exists in the via list, a `t` is returned. Locked csets return a `nil`.

#### Arguments

| Name | Description |
|---|---|
| `t_csetName` | Name of physical cset or `nil` for all csets. |
| `t_padstack` | Name of a via padstack. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | If added. |
| `nil` | Error in arguments; cset does not exist or illegal padstack name. |

#### Examples

Add ALLPAD to all csets

`axlCnsAddVia(nil "ALLPAD")`

Add ONEPAD to DEFAULT cset

`axlCnsAddVia("DEFAULT" "ONEPAD")`

### axlCnsAssignPurge

`axlCnsAssignPurge( s_tableType ) => x_delCount/ nil`

#### Description

Obsolete. Kept for backward compatibility

Purges either the physical or spacing assignment table of unused entries. Allegro PCB Editor supports two assignment tables: physical and spacing. This functionality duplicates that found in the Constraint Assignment Tables forms.

#### Arguments

| Name | Description |
|---|---|
| `s_tableType`: | Spacing or Physical. |

#### Value Returns

| Name | Description |
|---|---|
| `nil` | Error. |
| `x_delCount` | Number of entries deleted. |

#### Examples

`axlCnsAssignPurge('spacing)`

#### See Also

axlCnsList

### axlCnsClassTableChange

`axlCnsClassTableChange( o_dbidClassTable s_csetType/ll_typeAndName [t_csetName] ) => o_dbidClassTable/nil`

#### Description

This command changes the Csets associated with an existing net class table entry.

Note: See axlCnsClassTableCreate for complete family of functions.

You cannot change any table entries containing a region entry in Allegro PCB Designer or lower tiers.

#### Arguments

| Name | Description |
|---|---|
| `o_dbidClassTable` | dbid of an existing classTable entry. |
| `s_csetType` | symbol for cset type. spacing, 'physical or 'sameNet) |
| `ll_typeAndName` | lists `s_csetType` and `t_csetName` |
| `t_csetName` | cset name string |

#### Value Returns

Updated classTable dbid or nil if failure

#### Examples

Before running the sample skillcode for `axlCnsClassTableChange`, create a class table by running the example code in the axlCnsClassTableCreate command. Next, execute the following skill code and update the entry created in axlCnsClassTableCreate by adding it to the spacing.

`cset named 1, physical cset named 2 and a same net cset named 3.`

`prop = '((spacing "1") (physical "2") (sameNet "3"))`

`tbl = axlCnsClassTableChange(tbl prop)`

#### See Also

axlCnsClassTableCreate

### axlCnsClassTableCreate

`axlCnsClassTableCreate( g_class1 g_class2 g_region s_csetType/ll_typeAndName [t_csetName] ) => o_dbidClassTable/nil`

#### Description

This command creates a class table entry that consists of any of the following:

- class to class (spacing only)

- region to class (spacing, same net and physical)

- region to class to class (spacing only)

Optionally, the command also associates a spacing cset, a physical cset, and same net cset with the table entry. If a class table entry already exists, it is modified with the provided csets.

Regions are not available in Allegro PCB Designer and lower products. Command will fail if you attempt to create a region-based table entry in these products. Class tables may not be created in symbol editor.

Points to remember:

| Name | Description |
|---|---|
| 1. | The order of class1 and class2 does not matter. |

| Name | Description |
|---|---|
| 2. | If an entry already exists it will return the existing entry. |

| Name | Description |
|---|---|
| 3. | Netclasses can be classified by domain (spacing and/or physical). If a netclass is restricted to one domain, it is possible to create a netclass to any entry that crosses domains. This table entry will be ignored by DRC. For example, you have a netclass, `ANY`, in both physical and spacing domains; and another netclass `PHYS`that is restricted to the physical domain. It is possible to create a `ANY` to `PHYS` relationship which is only appropriate in the spacing domain but the `PHYS` netclass is not legal in that domain. |

Note: This condition might be tested for and rejected in future releases.

| Name | Description |
|---|---|
| 4. | DRC is set out-of-date, you must manually update the DRC. |

| Name | Description |
|---|---|
| 5. | Unlike Constraint Manager, you can add cset names that don't yet exist in the database. In these cases, we will automatically create a cset. Check via axlCnsList if your cset exists if you don't wish to create new csets. |

| Name | Description |
|---|---|
| 6. | Class table entries may also have constraint overrides attached via property overrides (`axlDBAddProp`) |

#### Arguments

| Name | Description |
|---|---|
| `g_class1` | NETCLASS dbid or name of name class |
| `g_class2` | NETCLASS dbid, name of name class or nil |
| `g_region` | REGION dbid, name of region or nil |
| `s_csetType` | symbol cset type one of 'spacing, 'physical or 'samenet |
| `t_csetName` | string cset name for given type |
| `ll_typeAndName` | option list of values where you have `((s_csetType t_csetName) (s_csetType t_csetName) ...)` |

#### Value Returns

returns `dbid` of type `classTable` for new or existing cset or nil if error

#### Examples

- Create appropriate entries in design

`region = axlRegionCreate("ANALOG")`

`ncls = axlNetClassCreate("VOLTAGE" '(spacing physical))`

| Name | Description |
|---|---|
| 1. | Add new spacing region-class table entry and give it the spacing cset "25MILS" |

`tbl = axlCnsClassTableCreate("VOLTAGE" nil "ANALOG" 'spacing "25MILS")`

| Name | Description |
|---|---|
| 2. | Alternative method plus also add a physical voltage cset. |

`props = '((spacing "25MILS") (physical "VOLTAGE"))`

`tbl = axlCnsClassTableCreate(ncls nil region props)`

#### See Also

axlCnsClassTableFind, axlCnsClassTableSeek, axlCnsClassTableChange, axlCnsClassTableDelete, axlCnsList,

Also see classTable dbid object description.

### axlCnsClassTableDelete

`axlCnsClassTableDelete( o_dbidClassTable/lo_dbidClassTable ) => t/nil`

#### Description

Deletes one or more entries in the class table.

DRC is marked out of date.

#### Arguments

| Name | Description |
|---|---|
| `o_dbidClassTable` | dbid of an existing classTable entry. |
| `lo_dbidClassTable` | deletes list of classTable entries. |

#### Value Returns

`t` if successful, `nil` if an error

#### Examples

Create a classTable entry by executing example code in axlCnsClassTableCreate. Delete entry just created by running the following command.

`axlCnsClassTableDelete(tbl)`

#### See Also

axlCnsClassTableCreate, axlCnsDeleteRegionClassClassObjects, axlCnsDeleteClassClassObjects

### axlCnsClassTableFind

`axlCnsClassTableFind( s_type [o_dbid] ) => lo_dbidClassTable/nil`

#### Description

This command searches the class table for class table entries matching the search criteria.

#### Arguments

| Name | Description |
|---|---|
| `s_type` | Specifies the type of search to perform. The options available are: ``netclass` - returns all class entries (all entries except for wire and component) ``classClass` - returns all class to class entries ``classRegion` - returns all class to region entries ``classClassRegion` - returns all class to class to region entries ``wireProf` - returns all wire profile entries (APD/SIP only) ``component` - returns all component entries (APD/SIP only) ``match` - returns all entries that contain provided region or class dbid (`o_dbid`) |
| `o_dbid` | only applicable for the match option will return all class table entries containing the dbid. |

#### Value Returns

List of class table dbids matching search criteria or `nil` if no match is found.

#### Examples

| Name | Description |
|---|---|
| 1. | Return all class entries that effect physical, spacing or same net DRC |

`tbl = axlCnsClassTableFind(`netclass)`

| Name | Description |
|---|---|
| 2. | Return all entries that contain Region "`ANALOG`" entry (assumes design has a region called "ANALOG") |

`region = car (axlSelectByName("REGION" "ANALOG"))`

`tbl = axlCnsClassTableFind(`match region)`

#### See Also

axlCnsClassTableCreate, axlCnsClassTableSeek, axlSelectByName

### axlCnsClassTableSeek

`axlCnsClassTableSeek( g_class1 g_class2 g_region ) => o_dbidClassTable/nil`

#### Description

This command seeks a specific class table entry matching exactly the provided `dbids`. Order of class1 and class2 does not matter since C1/C2 is the same as C2/C1 and only one entry exists in the table.

- Constraint overrides may exist on a table entry via the `prop` attribute. While fetching multiple table entries, best performance is achieved by using dbids or using axlCnsClassTableFind.

#### Arguments

| Name | Description |
|---|---|
| `g_class1` | NETCLASS dbid, name of net class or nil |
| `g_class2` | NETCLASS dbid, name of net class or nil |
| `g_region` | REGION dbid, name of region or nil |

#### Value Returns

Class table entry matching search criteria or `nil` if none found.

#### Examples

Create a classTable entry by executing example code in axlCnsClassTableCreate

| Name | Description |
|---|---|
| 1. | Return class table entry for a netclass called VOLTAGE and region called ANALOG. |

`tbl = axlCnsClassTableSeek("VOLTAGE" nil "ANALOG")`

| Name | Description |
|---|---|
| 2. | Alternative method using dbids |

`region = car( axlSelectByName("REGION" "ANALOG"))`

`netclass = car( axlSelectByName("NETCLASS" "VOLTAGE"))`

`tbl = axlCnsClassTableSeek(netclass nil region)`

#### See Also

axlCnsClassTableCreate

### axlCNSCreate

`axlCNSCreate( g_domain t_name t_copyName ) => t/nil`

#### Description

Creates a new constraint set in the specified domain. For spacing and physical csets, you must supply an existing cset as the copy cset. If the `copyName` is nil, the DEFAULT cset is used. Electrical csets (ECsets) are created empty for a nil `copyName` . By default, the ECset created is empty. If you provide a second argument, the ECset contents are copied.

To assign a cset to a logical object such as a net, bus, or a netclass, assign a PHYSICAL_CONSTRAINT_SET, SPACING_CONSTRAINT_SET, SAME_NET_SPACING_CONSTRAINT_SET or ELECTRICAL_CONSTRAINT_SET property to the logical object where the value of the property is the cset name.

Note: Electrical csets cannot be created in Allegro PCB Designer.

#### Arguments

| Name | Description |
|---|---|
| `g_domain` | Specifies the domain of the Cset. Possible values are Physical, spacing, electrical, or `sameNet. |
| `t_name` | Name of new cset. (Changed to upper case) string must pass allowed character set |
| `t_copyName` | Name of cset to use as template. If this is `nil`, spacing and physical domains use DEFAULT as the template, while in case of electrical domain, an empty ECset is created. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Cset created. |
| `nil` | Failed for the following reasons: domain name is illegal; name of cset is illegal; cset already exists; or `copyName` cset does not exist. |

#### Examples

Create a new physical cset called `foo`.

`axlCNSCreate('physical "foo" nil)`

#### See Also

axlCNSEcsetCreate , axlCNSDelete , axlCnsList, axlDBAddProp, axlNetClassCreate

### axlCNSCsetLock

`axlCNSCsetLock( g_domain t_csetName g_mode ) => t/nil`

#### Description

This locks or unlocks a constraint set in the given domain. See discussion in axlCNSIsLockedDomain.

You should usually lock or unlock the entire domain since this matches the DRC user model. We provide this interface to temporary unlock a locked cset, make changes then reapply the lock.

Note: Changing the lock on a cset can take a considerable amount of time since DRC needs to be updated. In the spacing domain, dynamic shapes need to be updated. If doing other changes, consider cloaking axlDBCloak the entire process. This API already uses cloaking for the individual cset.

#### Arguments

| Name | Description |
|---|---|
| `g_domain` | domain of cset; `'physical`, `'spacing`, `'sameNet`, `'electrical` |
| `t_csetName` | cset name |
| `g_mode` | may either be `t` (to lock) or `nil` to unlock |

#### Value Returns

Returns `t` if updated lock status, `nil` an error.

#### Examples

Lock Spacing cset DEFAULT, which has a side effect of locking spacing and same net domains

`axlCNSCsetLock('spacing "DEFAULT" t)`

#### See Also

axlCNSIsLockedDomain

### axlCNSDelete

`axlCNSDelete( g_domain t_name/o_dbidEcset ) => t/nil`

#### Description

Deletes a cset and its references to any objects such as nets, net classes, etc. Locked csets must first be unlocked before you delete them. If it is a spacing or physical domain, you cannot delete the DEFAULT cset. You cannot delete electrical csets in Allegro PCB Design L.

#### Arguments

| Name | Description |
|---|---|
| `g_domain` | Specifies the domain of cset. Valid values are: `'physical`, `'spacing`, `'sameNet`, `'electrical` |
| `t_name` | Name of cset. |
| `o_dbidEcset` | If an ECset, its `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Cset deleted. |
| `nil` | Cset not deleted because cset does not exist or the cset is locked, or cset is `t`. |

#### Examples

Deletes electrical cset named UPREV_DEFAULT.

`axlCNSDelete('electrical "UPREV_DEFAULT")`

#### See Also

axlCNSCreate

### axlCnsDeleteClassClassObjects

`axlCnsDeleteClassClassObjects( ) => x_delCount`

#### Description

Delete all Class-Class entries.

#### Arguments

None

#### Value Returns

The count of the objects deleted.

#### See Also

axlCnsPurgeCsets

### axlCnsDeleteRegionClassClassObjects

`axlCnsDeleteRegionClassClassObjects( ) => x_delCount`

#### Description

Deletes all Region-Class-Class entries.

#### Arguments

None

#### Value Returns

The count of the objects deleted.

#### See Also

axlCnsPurgeCsets

### axlCnsDeleteRegionClassObjects

`axlCnsDeleteRegionClassObjects( ) => x_delCount`

#### Description

Delete all Region-Class entries.

#### Arguments

None

#### Value Returns

The count of the objects deleted.

#### See Also

axlCnsPurgeCsets

### axlCnsDeleteVia

`axlCnsDeleteVia( t_csetName t_padstackName ) => t/nil`

#### Description

Deletes padstack from the physical via constraint list, `t_csetName`. If `t_csetName` is `nil`, delete provided padstack from all physical constraint sets.

Notes:

- Will return `t` if asked to delete a via that does not exist in the via list.

- Locked csets will return a `nil`.

#### Arguments

| Name | Description |
|---|---|
| `t_csetName` | Name of physical cset or nil for all csets. |
| `t_padstack` | Name of a via padstack. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | If deleted. |
| `nil` | Error in arguments; cset does not exist or illegal padstack name. |

#### Examples

Delete via to default cset

`axlCnsDeleteVia("DEFAULT" "VIA")`

Delete via to all csets

`axlCnsDeleteVia(nil "VIA")`

#### See Also

axlCnsGetViaListandaxlPurgePadstacks

### axlCNSDesignModeGet

`axlCNSDesignModeGet( nil ) => ls_constraints`

or

`axlCNSDesignModeGet( 'all ) => lls_constraintNModes`

or

`axlCNSDesignModeGet( 'editable ) => t/nil`

or

`axlCNSDesignModeGet( s_name/t_name ) => s_mode/nil`

or

`axlCNSDesignModeGet( s_name/t_name 'print ) => t_name/nil`

#### Description

Gets the current DRC modes for checks that fall into the set of design constraints. These constraints pertain to the entire board. To determine the design constraint checks currently supported, use the `axlCNSDesignModeGet()` command.

The `'print` mode offers the name shown in reports like show element.

This has axlDebug support.

Note: Available constraint checks may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `nil` | Returns all checks in design type DRC. |
| `'all` | Returns all checks and current mode. |
| `'editable` | Returns `t` if mode can be changed, `nil` mode is not changed and when in Allegro PCB Editor studio which does not offer this option. |
| `s_name` | Symbol name of check. |
| `t_name` | String name of check. |
| `'print` | Printable constraint name option. |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | List of checks (`s_name` ...) |
| `lls_names` | List of checks and their mode ((`s_name s_mode`) ...) |
| `s_mode` | Mode `'on`, `'off` or `'batch` |
| `t_name` | The printable constraint name |

### axlCNSDesignModeSet

`axlCNSDesignModeSet( t_name/s_name t_mode/s_mode ) => t/nil`

or

`axlCNSDesignModeSet( 'all t_mode/smode ) => t/nil`

or

`axlCNSDesignModeSet( l_constraintNModes t_mode/smode ) => t/nil`

or

`axlCNSDesignModeSet( ll_constraintNModes ) => t/nil`

#### Description

Sets the current DRC modes for design constraints. The modes control the DRC for that design constraint check on the entire board.

To determine the checks that are supported, use the following command:

axlCNSDesignModeGet()

You can set all checks using the argument `'all`, set individual checks using `t_name`, or set a list of checks to the same mode as follows:

`'(``s_name``...)``t_mode``/``s_mode`

`'(``t_name``...)``t_mode``/``s_mode`

You can list sets of checks as follows:

`'((``s_name``/``t_name``s_mode``/``t_mode``)...)`

For performance reasons, changing modes or values does not invoke DRC. You must manually invoke DRC. You can mark changes in order to perform fewer DRC updates, depending on your changes (see axlCNSMapUpdate.)

Note: Available constraint checks may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of check. |
| `t_name` | String name of check. |
| `s_mode` | Mode setting may be `'on`, `'off`, or `'batch`. |
| `t_mode` | String mode setting may be `"on"`, `"off"` or `"batch"` |
| `'all` | Returns all checks for a given tier of Allegro PCB Editor. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Success |
| `nil` | Failure. |

### axlCNSDesignValueCheck

`axlCNSDesignValueCheck( s_name/t_name g_value ) => (t_string/nil, nil/t_errorMsg)/nil`

#### Description

Checks the syntax of the given value against the allowed syntax for the given constraint. You use the function `axlCNSDesignGetValue(nil)` to get the constraint names.

Note: Allowed syntax may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of the constraint. |
| `t_name` | String name of the constraint. |
| `g_value` | Value to verify |

#### Value Returns

| Name | Description |
|---|---|
| `(``t_string``/nil)` | Value correct. `t_string` shows current user unit preference. For example, if you supply "10", the return might be `"10.0 MILS"` if `MILS` is the current database unit. |
| (`nil`/`t_errorMsg`) | Value incorrect. `t_errorMsg` reflects the error. |
| `nil` | Arguments are incorrect. |

#### Examples

`axlCNSDesignValueCheck('Negative_Plane_Islands "10 mils")`

Tests if allowed to set.

### axlCNSDesignValueGet

`axlCNSDesignValueGet( nil [g_returnNameString] ) => ls_constraints`

or

`axlCNSDesignValueGet( 'all [g_returnString] ) => lls_constraintNValues`

or

`axlCNSDesignValueGet( s_name [g_returnString] ) => f_value/t_value/nil`

#### Description

Fetches the values from those design constraints that support values. Use `axlCNSDesignValueGet(nil)` to determine the set of these constraints.

Note: Constraint checks may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `nil` | Returns all checks that support values. |
| `'all` | Returns all checks with values and current value. |
| `s_name` | Symbol name of value. |
| `t_name` | String name of value. |
| `g_returnNameString` | Returns constraint names as strings (default is symbol return.) |
| `g_returnString` | By default, this returns native type in user units (a float) for all checks supported. If `t`, return is a MKS string where `nil` returns native. |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | List of all controls that support values (symbol.) |
| `lls_constraintNValues` | List of all controls with their values `'((``s_name``f_value``/``t_value``) ... f_value` = user unit value, and `t_value` = MKS string value. |

### axlCNSDesignValueSet

`axlCNSDesignValueSet( t_name/s_name f_value/t_value ) => t/nil`

or

`axlCNSDesignValueSet( ll_constraintNValues ) => t/nil`

#### Description

This sets the value of the design constraint.

To determine the list of supported values, use the following command:

`axlCNSDesignValueGet(nil)`

You may set single values or a list of values:

`'((``s_name``/``t_name``f_value``/``t_value``) ...)`

For performance reasons, changing a value does not invoke DRC. You must manually invoke DRC. See axlCNSMapUpdate for a set of interfaces you can use to mark changes in order to perform fewer DRC updates.

Note: Constraint checks may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of check. |
| `t_name` | String name of check. |
| `f_value` | Floating point value provided is assumed to be in the default user unit for the constraint. Value may be rounded. |
| `t_value` | If given as a string with MKS type, the value is converted to current user units for the constraint. Rounding may result. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Design constraint value set. |
| `nil` | Failed to set design constraint value. |

### axlCNSEcsetCreate

`axlCNSEcsetCreate( t_name [t_copyName/o_dbidCopyEcset] ) => o_dbidEcset/nil`

#### Description

Creates a new ECset. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets. The name must be legal and less than the maximum length allowed. Function fails if the ECset already exists.

By default, the ECset is created empty. You can provide a second argument to copy the contents of another ECset into the new ECset.

#### Arguments

| Name | Description |
|---|---|
| `t_name` | Name of new ECset (Changed to upper case)String must pass allowed character set. |
| `t_copyName` | Optional name to copy from. |

#### Value Returns

| Name | Description |
|---|---|
| `o_dbidEcset` | `dbid` of the new ECset |
| `nil` | Failed due to one of the following: the name is illegal, or the ECset already exists. |

#### See Also

axlCNSDesignModeSet, axlCNSCreate

Example 1

`axlCNSEcsetCreate("MyEmptyEcset")`

Creates a new empty ECset.

Example 2

`p = car(axlDBGetDesign()->ecsets)`

`axlCNSEcsetCreate("MyNewEcset" p)`

Copies the contents of the first ECset in a list.

### axlCNSEcsetDelete

`axlCNSEcsetDelete( t_name/o_dbidEcset ) => t/nil`

#### Description

Deletes an ECset from the Allegro PCB Editor database and also deletes the `ELECTRICAL_CONSTRAINT_SET` property from any nets assigned this ECset value. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

If the ECset is locked, you must unlock it before you can delete it.

#### Arguments

| Name | Description |
|---|---|
| `t_name` | ECset name |
| `o_dbidEcset` | ECset `dbid` |

#### Value Returns

| Name | Description |
|---|---|
| `t` | ECset successfully deleted. |
| `nil` | ECset is not deleted because of one of the following: the name is incorrect, or ECset is locked. |

Example 1

`axlCNSEcsetDelete("UPREV_DEFAULT")`

Deletes an ECset by name.

Example 2

`p = car(axlDBGetDesign()->ecsets)`

`axlCNSEcsetDelete(p)`

Deletes the first ECset in a list of ECsets.

### axlCNSEcsetGet

`axlCNSEcsetGet( t_name ) => o_dbidEcset/nil`

#### Description

Returns the `dbid` of the electrical cset when you request it by the ECset name. Electrical Constraint Set (ECset) is a mechanism for grouping a set of electrical constraints and applying them to a set of nets.

#### Arguments

| Name | Description |
|---|---|
| `t_name` | ECset name. |

#### Examples

`axlCNSEcsetGet("foo")`

Tests for the existence of an ECset named `foo`.

#### See Also

axlCNSEcsetValueGetand axlCnsList

### axlCNSEcsetModeGet

`axlCNSEcsetModeGet( nil ) => ls_constraints`

or

`axlCNSEcsetModeGet( 'all ) => lls_constraintNModes`

or

`axlCNSEcsetModeGet( s_name/t_name ) => s_mode/nil`

or

`axlCNSEcsetModeGet( s_name/t_name 'print ) => t_name/nil`

#### Description

Returns the current DRC modes for checks that are members of electrical constraints. These modes pertain to the entire board. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

The `'print` mode offers the name shown in reports, similar to the show element command.

This has axlDebug support.

Note: Not all checks are available in all levels of Allegro PCB Editor. To determine the set of checks supported, use the command: `axlCNSEcsetModeGet()`. Constraint checks may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `nil` | Returns all checks in design type DRC. |
| `'all` | Returns all checks and current mode. |
| `s_name` | Symbol name of the check. |
| `t_name` | String name of the check. |
| `'print` | Printable constraint name option. |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | List of checks (`s_name` ...). |
| `lls_names` | List of checks and related modes ((`s_name s_mode`) ...) |
| `s_mode` | Returns mode `'on`, `'off`, or `'batch` |
| `t_name` | Printable constraint name . |

#### See Also

axlCNSEcsetModeSet, axlCNSEcsetValueGet

Example 1

`axlCNSEcsetModeGet(nil)`

Lists currently available electrical constraints.

Example 2

`axlCNSEcsetModeGet('all)`

Lists settings for all electrical constraints.

Example 3

`axlCNSEcsetModeGet('Maximum_Stub_Length)`

Shows current setting of stub length.

Example 4

`axlCNSEcsetModeGet("Maximum_Via_Count")`

Shows current setting of via count.

### axlCNSEcsetModeSet

`axlCNSEcsetModeSet( t_name/s_name t_mode/s_mode ) => t/nil`

or

`axlCNSEcsetModeSet( all t_mode/s_mode ) => t/nil`

or

`axlCNSEcsetModeSet( l_constraintNModes t_mode/s_mode ) => t/nil`

or

`axlCNSEcsetModeSet( ll_constraintNModes ) => t/nil`

#### Description

Sets the DRC modes for checks that are members of the electrical constraints set. These modes control the entire board. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

Note: Not all checks are available in all levels of Allegro PCB Editor. To determine the set of checks supported, use the command: `axlCNSEcsetModeGet()`. Constraint checks may change from release to release.

You can set all checks using the argument `'all`, set individual checks using `t_name`, or set a list of checks with the same mode as shown:

`'(``s_name``...)``t_mode``/``s_mode`

`'(``t_name``...)``t_mode``/``s_mode`

You can list sets of checks as shown:

`'((``t_name``t_mode``) ...)`

`'((``s_name``s_mode``) ...)`

For performance reasons, changing modes or values does not invoke DRC. You must manually invoke DRC. See axlCNSMapUpdate for a set of interfaces you can use to mark changes in order to perform fewer DRC updates.

- Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of the check. |
| `t_name` | String name of the check. |
| `s_mode` | Mode setting; may be `'on`, `'off`, or `'batch`. |
| `t_mode` | String mode setting; may be `"on"`, `"off"`, or `"batch"`. |
| ``all` | Set all checks for a given tier of Allegro PCB Editor. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | DRC mode set. |
| `nil` | DRC mode not set. |

### axlCNSEcsetValueCheck

`axlCNSEcsetValueCheck( s_name/t_name g_value ) => (t/t_errorMsg)/nil`

#### Description

Checks the syntax of the given value against the allowed syntax for the given constraint. You use the function `axlCNSEcseValueGet (nil)` to get the constraint names. Electrical Constraint Set (ECSet) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

Note: Allowed syntax may change from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of constraint. |
| `t_name` | String name of constraint. |
| `g_value` | Value to verify. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Syntax is correct. |
| `t_errorMsg` | Syntax is incorrect. The message indicates the reason. |
| `nil` | Constraint name is not supported. |

#### Examples

`axlCNSEcsetValueCheck('Net_Schedule_Topology "STAR")`

Tests if allowed to set.

### axlCNSEcsetValueGet

`axlCNSEcsetValueGet( nil [g_returnNameString] ) => ls_constraints`

or

`axlCNSEcsetValueGet( 'all [g_returnString] ) => lls_constraintNValues`

or

`axlCNSEcsetValueGet( o_ecsetDbid/t_ecsetName s_name [g_returnString] ) => f_value/t_value/nil`

#### Description

Fetches the constraint values for a given ECset. Electrical Constraint Set (ECset) is a mechanism for packaging up a set of electrical constraints into a group and applying them to a set of nets.

Use `axlCNSEcsetValueGet(nil)` to determine the set of allowable constraints.

Each ECset may have all or none of the allowed constraints.

You can retrieve the ECset values by the ECset name or by its `dbid`. You can get the `dbid` of an ECset by using one of the following commands:

- `axlDBGetDesign()->ecsets`

- `axlCNSEcsetCreate()`

Note: Constraint checks may change from release to release. Not all checks are available in all levels of Allegro PCB Editor.

#### Arguments

| Name | Description |
|---|---|
| `o_ecsetDbid` | ECset `dbid`. |
| `t_ecsetName` | ECset name. |
| `nil` | Returns all checks that support values. |
| `'all` | Returns all checks with values and current value. |
| `s_name` | Symbol name of value. |
| `t_name` | String name of value. |
| `g_returnNameString` | Returns constraint names as strings (default is symbol return) |
| `g_returnString` | Default is to return native type for all checks supported, this is in user units (a float). If `t`, return is an MKS string where `nil` returns native. |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | List of all controls that support values (symbol). |
| `lls_constraintNValues` | List of all controls with their values as shown: `'((``s_name``f_value``/``t_value``) ... f_value` = user unit value and `t_value` = MKS string value. |

### axlCNSGetDefaultMinLineWidth

`axlCNSGetDefaultMinLineWidth( t_sublassName ) => f_minLineWidthValue`

#### Description

Retrieves the minimum default line width value for the specific subclass.

#### Arguments

| Name | Description |
|---|---|
| `t_subclassname` | A subclass name of the ETCH or CONDUCTOR class. |

#### Value Returns

| Name | Description |
|---|---|
| `f_minSpacingValue` | Minimum line width value (in design units) on the subclass. |

#### Examples

`axlCNSGetDefaultMinLineWidth("TOP")`

`=> 0.004`

Gets the minimum line width value for layer TOP.

### axlCNSGetPhysical

`axlCNSGetPhysical( t_cset t_layer s_constraint [g_string] ) => g_value/nil`

or

`axlCNSGetPhysical( t_cset t_layer nil [g_string] ) => ll_nameValue/nil`

or

`axlCNSGetPhysical( nil nil nil ) => ls_cnsTypes`

#### Description

In its first operational mode, obtains the value of a physical constraint given a cset and layer. In the second mode of operation, it obtains all physical constraint as name/value pairs for a cset on a layer. This, in turn, may be passed to `axlCNSSetPhysical`.

In the final mode, a list of all supported physical constraints may be obtained by passing three `nil`valuesto the interface:

`axlCNSGetPhysical(nil nil nil)`

#### Arguments

| Name | Description |
|---|---|
| `t_cset` | Name of a physical cset. Can use "" for "DEFAULT". |
| `t_layer` | ETCH layer name (for example, "ETCH/TOP" or "TOP"). If `nil,`applies the change to all layers. |
| `s_constraint` | Name of constraint. If `nil,` returns a set of symbol/value pairs of all constraints. |
| `g_string` | By default, returns value in the native units of the constraint. If `g_string` is`t``,`always returns data as a string. |

#### Value Returns

| Name | Description |
|---|---|
| `g_value` | Value of constraint in design units, except for `same_net`, which is returned as a `t/nil`. |
| `ll_nameValue` | Name values of pairs of physical constraint symbol and constraint value for all physical (`s_constraint g_value`).
 '((`necklength_min` 10.0) (`neckwidth_max` 5.0) ...) |
| `ls_cnsTypes` | List of supported physical constraint names. |
| `nil` | Returns `nil` on error (or `allow_etch`). |

#### See Also

axlCNSSetPhysical`,`axlCnsList`,`axlSubclassRoute, and axlCnsGetViaList

### axlCNSGetPinDelayEnabled

`axlCNSGetPinDelayEnabled() => t/nil`

#### Description

Returns if pin delay is enabled.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t:` | Pin delay is enabled. |
| `nil:` | Pin delay is not enabled. |

### axlCNSGetPinDelayPVF

`axlCNSGetPinDelayPVF() => t_pinDelayPVF`

#### Description

Returns the pin delay propagation velocity factor.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t_pinDelayPVF:` | If the pin delay propagation velocity factor is defined, it is returned as a string. If not defined, a blank string is returned. |

### axlCNSGetSameNet

`axlCNSGetSameNet( t_cset t_layer s_constraint [g_string] ) => g_value/nil`

or

`axlCNSGetSameNet( t_cset t_layer nil [g_string] ) => ll_nameValue/nil`

or

`axlCNSGetSameNet( nil nil nil ) => ls_cnsTypes`

#### Description

Documentation same as axlCNSGetSpacing.

#### Arguments

| Name | Description |
|---|---|
| `t_cset:` | name of a same net spacing cset. Can use "" for "DEFAULT". |
| `t_layer:` | ETCH layer name ( "ETCH/TOP" or "TOP"). If `nil` apply change to all layers. |
| `s_constraint:` | name of constraint. If `nil` returns a set of symbol/value pairs of all constraints. |
| `g_string:` | By default returns value in the native units of the constraint. If `g_string` is`t,` it will always return data as a string. |

#### Value Returns

| Name | Description |
|---|---|
| `g_value:` | value of constraint in design units |
| `l_nameValue` - | name value pairs of spacing constraint symbol and constraint value for all spacing. (`s_constraintg_value`). `'((shape_shape 10.0) (line_line 5.0) ...)` |
| `ls_cnsTypes` - | list of supported same net spacing constraint names. |
| `nil-` | returns nil on error (or same_net). |

#### Examples

Get shape to shape same net spacing in default cset, TOP layer

`axlCNSGetSameNet("" "TOP" 'shape_shape)`

Get all same net constraints for 25_MIL_SPACE, bottom layer

`axlCNSGetSameNet("25_MIL_SPACE" "BOTTOM" nil)`

Get all same net constraints for DEFAULT, bottom layer as strings

`axlCNSGetSameNet("" "BOTTOM" nil t)`

Get supported same net constraint symbols

`axlCNSGetSameNet(nil nil nil)`

Fetch all layers and constraints of same net cset DEFAULT

`cset = "" ;; DEFAULT cset`

`foreach(subclass axlSubclassRoute()`

`layer = axlCNSGetSameNet(cset subclass nil)`

`printf("\nLAYER=%s\n\tconstraints=%L\n" subclass, layer)`

`)`

#### See Also

axlCNSSetSameNet, axlCnsList, axlCNSGetSpacing

### axlCNSGetSameNetXtalkEnabled

`axlCNSGetSameNetXtalkEnabled() => t/nil`

#### Description

Returns if Same Net Xtalk is enabled.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t:` | same net Xtalk is enabled. |
| `nil:` | same net Xtalk is not enabled. |

### axlCNSGetSpacing

`axlCNSGetSpacing( t_cset t_layer s_constraint [g_string] ) => g_value/nil`

or

`axlCNSGetSpacing( t_cset t_layer nil [g_string] ) => ll_nameValue/nil`

or

`axlCNSGetSpacing( nil nil nil ) => ls_cnsTypes`

#### Description

In its first operational mode, obtains the value of a spacing constraint given a cset and layer. All values are returned in design units, except for `same_net,` which is a boolean (`t/nil`). In a second mode of operation, it obtains all spacing constraints as name/value pairs for a cset on a layer. This, in turn, may be passed to `axlCNSSetSpacing`. For the final mode, a list of supported spacing constraints may be obtained by passing three `nil` values to this interface:

`axlCNSGetSpacing(nil nil nil)`

#### Arguments

| Name | Description |
|---|---|
| `t_cset` | Name of a spacing cset. You can use "" for "DEFAULT". |
| `t_layer` | ETCH layer name (for example, "ETCH/TOP" or "TOP"). If `nil,` applies change to all layers. |
| `s_constraint` | Name of constraint. If `nil,` returns a set of symbol/value pairs of all constraints. |
| `g_string` | By default, returns value in the native units of the constraint. If `g_string` is `t`, always returns data as a string. |

#### Value Returns

| Name | Description |
|---|---|
| `g_value` | Value of constraint in design units, except for `same_net`, which is returned as `t/nil`. |
| `ll_nameValue` | Name value pairs of spacing constraint symbol and constraint value for all spacing (`s_constraint g_value`).'((shape_shape 10.0) (line_line 5.0) ...) |
| `ls_cnsTypes` | List of supported spacing constraint names. |
| `nil` | Returns `nil` on error (or `same_net`). |

#### See Also

axlCNSSetSpacing,axlCnsList`,` and axlSubclassRoute

### axlCNSGetViaZEnabled

`axlCNSGetViaZEnabled() => t/nil`

#### Description

Returns if Via Z is enabled.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t:` | via Z is enabled |
| `nil:` | via Z is not enabled |

### axlCNSGetViaZPVF

`axlCNSGetViaZPVF() => t_viaZPVF`

#### Description

Returns the via Z propagation velocity factor

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t_viaZPVF:` | If the via Z propagation velocity factor is defined, it is returned as a string. If not defined, a blank string is returned. |

### axlCNSPhysicalModeGet

`axlCNSPhysicalModeGet( nil ) => ls_constraints`

or

`axlCNSPhysicalModeGet( 'all ) => lls_constraintNModes`

or

`axlCNSPhysicalModeGet( s_name/t_name ) => s_mode/nil`

or

`axlCNSPhysicalModeGet( s_name/t_name 'print ) => t_name/nil`

#### Description

This fetches the current physical drc mode(s). Modes determine if a particular constraint is on or off. These modes apply to the entire board. To determine the set currently supported, physical modes do a `axlCNSPhysicalModeGet`(nil). The physical mode set may be a subset of physical values since the implementation may associate certain values under a master mode. For example, via_list is not a constraint and the diff pair mode is under the ecset domain.

Note: Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

| Name | Description |
|---|---|
| `nil` | returns all modes that are in spacing domain |
| `all` | returns all checks and current mode |
| `s_name` | symbol name of check. |
| `t_name` | string name of check |
| `'print` | printable constraint name option |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | list of checks (s_name ...) |
| `lls_names` | list of checks and their mode ((s_name s_mode) ...) |
| `s_mode` | mode 'on, or 'off |
| `t_name` | the printable constraint name |

#### Examples

Get current list of physical constraints

`axlCNSPhysicalModeGet(nil)`

Get list of settings for all physical constraints

`axlCNSPhysicalModeGet('all)`

Get current mode of max line with

`axlCNSPhysicalModeGet('width_max)`

Get current setting of allow Ts using a string

`axlCNSPhysicalModeGet("allow_ts")`

#### See Also

axlCNSPhysicalModeSet, axlCNSGetPhysical

### axlCNSIsCsetLocked

`axlCNSIsCsetLocked( g_domain t_csetName ) => t/nil`

#### Description

This returns if a cset is locked. See discussion in axlCNSIsLockedDomain.

A locked cset has the following characteristics:

- Cannot be edited

- Has the effect of locking the entire domain

#### Arguments

| Name | Description |
|---|---|
| `g_domain` | domain of cset; '`physical`, '`spacing`, '`sameNet`, '`electrical` |

#### Value Returns

- `t` if cset is deleted

- `nil`, if cset is not deleted due to being locked or not a cset

#### Examples

Command to check if the cset DEFAULT is locked

#### See Also

`axlCNSIsCsetLocked('electrical``''``DEFAULT``'')` axlCNSDesignModeSet

### axlCNSIsLockedDomain

`axlCNSIsLockedDomain( g_domain ) => t/nil`

#### Description

Used to check if the is constraint domain locked. A locked constraint domain has the following characteristics:

- csets cannot be edited, although new csets can be added

- any object (e.g. net) level property overrides are ignored

Notes:

- The spacing and sameNet domains are locked as a single domain.

- Locking is typically done via the techfile. In the techfile, you can lock individual csets. If one cset is locked, Allegro PCB Editor treats the entire domain as locked from the DRC perspective. When a domain is locked, any object level property constraint override is ignored.

- If a cset is locked it cannot be modified or deleted.

- Use axlCnsList`(nil)`to get a list all domains.

#### Arguments

| Name | Description |
|---|---|
| `g_domain` | domain of cset; `'physical`, `'spacing`, `'sameNet`, `'electrical` |

#### Value Returns

- t if a constraint domain is locked.

- nil - domain is not locked

#### Examples

- Command to check if the Electrical domain locked

`axlCNSIsLockedDomain('electrical)`

- To find a list of locked domains

`lockedDomains = setof( x axlCnsList(nil) axlCNSIsLockedDomain(x))`

#### See Also

axlCNSCsetLock, axlCNSIsCsetLocked, axlCNSLockDomain, axlCNSDesignModeSet, axlCnsList

### axlCNSLockDomain

`axlCNSLockDomain( g_domain g_mode ) => t/nil`

#### Description

This command locks or unlocks a constraint domain.

See discussion in axlCNSIsLockedDomain.

Note: Changing the lock on a domain can take a considerable amount of time since DRC status for that domain needs to be updated. In the spacing domain dynamic shapes also need to be updated. If doing other changes, you should consider cloaking (axlDBCloak the entire process. This API already uses cloaking.

#### Arguments

| Name | Description |
|---|---|
| `g_domain` | domain of cset; `'physical`, `'spacing`, `'sameNet`, `'electrical` |
| `g_mode` | may either be `t` (to lock) or `nil` to unlock |

#### Value Returns

Returns `t` if lock status is updated, and `nil` in case of an error.

#### Examples

Lock Spacing and Same net spacing domains

`axlCNSLockDomain('spacing t)`

#### See Also

axlCNSIsLockedDomain

### axlCNSPhysicalModeSet

`axlCNSPhysicalModeSet( t_name/s_name t_mode/s_mode ) => t/nil`

or

`axlCNSPhysicalModeSet( 'all t_mode/smode ) => t/nil`

or

`axlCNSPhysicalModeSet( l_constraintNModes t_mode/smode ) => t/nil`

or

`axlCNSPhysicalModeSet( ll_constraintNModes ) => t/nil`

#### Description

This sets the current drc modes (on/off) for checks in the area of physical constraints. These modes are global. To determine the constraints modes currently supported do a `axlCNSPhysicalModeGet(nil)`. We support several interfaces. All checks may be set (`'all`), individual checks, (`t_name`), list of checks with a same mode`'(s_name ...) t_mode/s_mode'(t_name ...) t_mode/s_mode` and sets of checks via a list of: `'((s_name/t_name s_mode/t_mode) ....)`

The constraints names may be be passed as a symbol or a string. For performance reasons, you should either do all your updates in a single call or wrap individual changes in the map API (see axlCNSMapUpdate).

Note: Future releases may add or subtract constraint checks. The axl interface does guarantee the checks returned by this interface will remain constant from release to release.

#### Arguments

| Name | Description |
|---|---|
| `s_name:` | symbol name of check. |
| `t_name:` | string name of check. |
| `s_mode:` | mode setting; may be 'on or 'off. |
| `t_mode:` | string mode setting "on or "off". |
| `'all:` | set all checks for given tier of Allegro. |

#### Value Returns

Returns `t` if succeeds or nil if failure.

#### Examples

Turn all constraints off

`axlCNSPhysicalModeSet('all 'off)`

Turn on line width max

`axlCNSPhysicalModeSet('width_max 'on)`

`Turn two constraint to on`

`axlCNSPhysicalModeSet('(bbvia_stagger_max bbvia_stagger_min) 'on)`

Set various constraints to different modes

`axlCNSPhysicalModeSet( '((width_max off) (allow_etch 'on)) )`

#### See Also

axlCNSPhysicalModeGet, axlCNSGetPhysical, axlCNSMapUpdate

### axlCNSSameNetModeGet

`axlCNSSameNetModeGet( nil ) => ls_constraints`

or

`axlCNSSameNetModeGet( 'all ) => lls_constraintNModes`

or

`axlCNSSameNetModeGet( s_name/t_name ) => s_mode/nil`

or

`axlCNSSameNetModeGet( s_name/t_name 'print ) => t_name/nil`

#### Description

Same as axlCNSSpacingModeGet.

#### Arguments

| Name | Description |
|---|---|
| `nil` | returns all modes that are in same net spacing domain |
| `'all` | returns all checks and current mode |
| `s_name` | symbol name of check. |
| `t_name` | string name of check |
| `'print` | printable constraint name option |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | list of checks (`s_name ...`) |
| `lls_names` | list of checks and their mode (`(s_name s_mode`) ...) |
| `s_mode` | mode 'on, or 'off |
| `t_name` | The printable constraint name |

#### Examples

Get current list of same net spacing constraints

`axlCNSSameNetModeGet(nil)`

Get list of settings for all same net spacing constraints

`axlCNSSameNetModeGet('all)`

Get current setting of line to line

`axlCNSSameNetModeGet('line_line)`

Get current setting of line to shape using a string

`axlCNSSameNetModeGet("line_shape")`

#### See Also

axlCNSSameNetModeSet, axlCNSGetSameNet, axlCNSSpacingModeGet

### axlCNSSameNetModeSet

`axlCNSSameNetModeSet( t_name/s_name t_mode/s_mode ) => t/nil`

or

`axlCNSSameNetModeSet( 'all t_mode/smode ) => t/nil`

or

`axlCNSSameNetModeSet( l_constraintNModes t_mode/smode ) => t/nil`

or

`axlCNSSameNetModeSet( ll_constraintNModes ) => t/nil`

#### Description

Same as axlCNSSpacingModeSet.

#### Arguments

| Name | Description |
|---|---|
| `s_name:` | symbol name of check. |
| `t_name:` | string name of check. |
| `s_mode:` | mode setting; may be 'on or 'off. |
| `t_mode:` | string mode setting "on or "off". |
| `'all:` | set all checks for given tier of Allegro. |

#### Value Returns

Returns `t` if succeeds or `nil` if failure.

#### Examples

Turn off all same net spacing constraints

`axlCNSSameNetModeSet('all 'off)`

Turn on line to line check

`axlCNSSameNetModeSet('line_line 'on)`

Turn two constraints to on

`axlCNSSameNetModeSet('(line_shape thrupin_line) 'on)`

Set several constraints to different modes

`axlCNSSameNetModeSet( '((line_line off)`

`(thrupin_shape on)) )`

#### See Also

axlCNSSameNetModeGet, axlCNSGetSameNet, axlCNSSpacingModeSet

### axlCNSSetPhysical

`axlCNSSetPhysical( t_cset/nil t_layer/nil s_constraint g_value ) => t/nil`

or

`axlCNSSetPhysical( t_cset/nil t_layer/nil ll_constraintValues nil ) => t/nil`

#### Description

Allows updating physical constraint values. By passing nil at the appropriate argument, values for all csets and all layers may be changed.

#### Arguments

| Name | Description |
|---|---|
| `t_cset` | Cset name. You can use "" for the DEFAULT cset. Use `nil` to apply changes to all csets. |
| `t_layer` | ETCH layer name (for example, "ETCH/TOP" or "TOP"). If nil, applies changes to all layers. |
| `s_constraint` | Constraint symbol to change. Use `axlCNSGetPhysical(nil nil nil)` for list of permissible values. |
| `g_value` | Value to update. For data types, see Data Types above. |
| `ll_constraintValues` | Multiple values may be updated by passing a list of lists for the third argument.
 '((s_constraint g_value) ... ) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Success. |
| `nil` | An error occurs when the ECset name does not exist; the layer does not exist; the constraint does not exist; the value for the constraint is illegal; or the cset is locked. |

#### See Also

axlCNSGetPhysical`,`axlCNSMapClear`,`axlCNSMapUpdateaxlCnsAddVia`,` and axlCnsDeleteVia

### axlCNSSetSpacing

`axlCNSSetSpacing( t_cset/nil t_layer/nil s_constraint g_value ) => t/nil`

or

`axlCNSSetSpacing( t_cset/nil t_layer/nil ll_constraintValues nil ) => t/nil`

#### Description

Allows updating spacing constraint values. By passing `nil`at the appropriate argument, values for all csets and all layers may be changed.

#### Arguments

| Name | Description |
|---|---|
| `t_cset` | The cset name. You can use "" for DEFAULT cset. Use`nil`to apply the changes to all csets. |
| `t_layer` | The ETCH layer name (e.g "ETCH/TOP" or "TOP"). If `nil,` applies the changes to all layers. |
| `s_constraint` | Constraint symbol to change. Use `axlCNSGetPhysical(nil nil nil)` for a list of permissible values. |
| `g_value` | Value to update. For data types, see Data types above. |
| `ll_constraintValues` | Multiple values may be updated by passing a list of lists for the third argument.
 '((s_constraint g_value) ... ) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Success. |
| `nil` | Indicates an error. An error occurs when the ECset name does not exist; the layer does not exist; the constraint does not exist; the value for the constraint is illegal; or the cset is locked. |

#### Examples

- Set line to shape spacing in all csets, all layers

`axlCNSSetSpacing(nil nil 'line_shape 5)`

- Set line to line spacing to 5 on DEFAULT cset, all layers

`axlCNSSetSpacing("" nil 'line_line 5)`

- Value of DEFAULT cset

`axlCNSSetSpacing("25_MIL_SPACE" "top" 'line_line 5)`

- Set a single spacing for all ids for all layers

`cnsIds = axlCNSGetSpacing(nil nil nil)`

`values = nil`

`defaultSpace = 10.0`

`foreach( id cnsIds`

`values = cons(list(id defaultSpace) values)`

`)`

`axlCNSSetSpacing("10_MIL_SPACE" nil values)`

#### See Also

axlCNSGetSpacing`,`axlCNSMapClear`,`and axlCNSMapUpdate

### axlCNSSetPinDelayEnabled

`axlCNSSetPinDelayEnabled(g_value) => t`

#### Description

Enables or disables Pin Delay.

#### Arguments

| Name | Description |
|---|---|
| `g_value:` | `t` or `nil` to indicate if Pin Delay is turned on or off. |

#### Value Returns

`t`

### axlCNSSetPinDelayPVF

`axlCNSSetPinDelayPVF(g_value) => t/nil`

#### Description

Sets a value for pin delay propagation velocity.

#### Arguments

| Name | Description |
|---|---|
| `g_value:` | a string to define the new pin delay propagation velocity factor. A `nil` value indicates that the value is to be deleted. |

#### Value Returns

| Name | Description |
|---|---|
| `t:` | no errors |
| `nil:` | error detected |

### axlCNSSetSameNet

`axlCNSSetSameNet( t_cset/nil t_layer/nil s_constraint g_value ) => t/nil`

or

`axlCNSSetSameNet( t_cset/nil t_layer/nil ll_constraintValues nil ) => t/nil`

#### Description

Documentation same as axlCNSSetSpacing.

#### Arguments

| Name | Description |
|---|---|
| `t_cset:` | cset name, can use "" for DEFAULT cset. Use `nil` to apply change to all cset. |
| `t_layer:` | ETCH layer name ( "ETCH/TOP" or "TOP"). If `nil` apply change to all layers. |
| `s_contraint:` | Constraint symbol to change. Use `axlCNSGetSameNet`(`nil nil nil`) for list of permissible values. |
| `g_value:` | Value to update. For data type, see above for "DATA TYPES". |
| `ll_constraintValues:` | Multiple values may be updated by passing a list of lists for the third argument. '((s_contraint g_value) ... ) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if succeeds |
| `nil` | an error
 - ecset name does not exit
 - layer does not exist
 - contraint does not exist
 - illegal value for constraint
 - cset is locked |

#### Examples

Set line to same net spacing in all csets, all layers

`axlCNSSetSameNet(nil nil 'line_shape 5)`

Set line to line same net to 5 on DEFAULT cset, all layers

`axlCNSSetSameNet("" nil 'line_line 5)`

Value of DEFAULT cset

`axlCNSSetSameNet("25_MIL_SPACE" "top" 'line_line 5)`

#### See Also

axlCNSGetSameNet, axlCNSSetSpacing

### axlCNSSetSameNetXtalkEnabled

`axlCNSSetSameNetXtalkEnabled(g_value) => t`

#### Description

Enables or disables Same Net Xtalk.

#### Arguments

| Name | Description |
|---|---|
| `g_value:` | `t` or `nil` to indicate if same net Xnet is turned on or off. |

#### Value Returns

`t`

### axlCNSSetViaZEnabled

`axlCNSSetViaZEnabled( g_value ) => t`

#### Description

Enables or disables Via Z.

#### Arguments

| Name | Description |
|---|---|
| `g_value:` | `t` or `nil` to indicate if Via Z is turned on or off. |

#### Value Returns

`t`

### axlCNSSetViaZPVF

`axlCNSSetViaZPVF(g_value) => t/nil`

#### Description

Sets a value for Via Z propagation velocity factor.

#### Arguments

| Name | Description |
|---|---|
| `g_value:` | a string to define the new via Z propagation velocity factor. A `nil` value indicates that the value is to be deleted. |

#### Value Returns

| Name | Description |
|---|---|
| `t:` | no errors |
| `nil:` | error detected |

