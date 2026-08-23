### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

16
==

Database Group Functions
========================

Overview
--------

This chapter describes the AXL-SKILL Database Group functions.

### axlDBAddGroupObjects

`axlDBAddGroupObjects(o_grouplo_members)⇒ t/nil`

#### Description

Adds the database objects specified in the new members list to a group. All restrictions and disclaimers specified in[axlDBCreateGroup](#1076292 "16") also apply for this procedure.

#### Arguments

|  |
| --- | ---
| `o_group` | `dbid` of the group to receive new members.
| `lo_members` | List of`dbid`'s specifying the new group members. Database objects already in the group are silently ignored (giving a return value of `t`.) A single `dbid` can be substituted for a list.
#### Value Returned

|  |
| --- | ---
| `t` | Objects added to the group.
| `nil` | Objects could not be added to the group because the resulting group does not meet the restrictions specified in`axlDBCreateGroup`.
#### See Also

[axlDBCreateGroup](#1076292 "16")

### axlDBCreateGroup

`axlDBCreateGroup(t_namet_typelo_groupMembers)⇒ o_dbid/nil`

#### Description

Creates a new group database object with members specified by`lo_groupMembers`.

#### Arguments

* String providing the group name. If name is in use by an existing group, this function fails and returns`nil`.
* String defining the group type. Legal values are:

  "`generic`" - Allegro user groups

  members: anything except other non-generic group objects

  "`bus`"

  members: net and xnets

  "`net_group`"

  members: xnet, net, diffpair, bus and net\_group

  "`nets_rko`" - a net keepout group

  members: xnet, net, diffpair bus, net\_group shape and fill rects (via and route keepout)

  "`die_stack`" - SIP and APD only

  members: compinst, syminst, rectangle, shape

  "`ratbundle`"

  members: pinpair, line and figure

  "`wire_profile`" - SIP and APD only

  members: a wire (cline or wire subclass)

  "`module`" - suggest to use `axlDBCreateModuleDef`

  Accessible but not recommended.

  "`db_drill_legend`" - drill legend tables

  "`rf_nets`" - RF "super" nets
* A circular group relationship cannot be formed.
* For each group type has only certain objects that are allowed. For example generic groups only permits:
* group
* component
* symbol
* net
* path
* via
* shape
* polygon
* pin
* text

#### Value Returned

|  |
| --- | ---
| `o_dbid` | `dbid` of the newly formed group.
| `nil` | If the group could not be created.
#### See Also

[axlDBAddGroupObjects](#1065349 "16"), [axlDBDisbandGroup](#1076355 "16"), [axlDBRemoveGroupObjects](#1079477 "16")

#### Example

* Generic group

> `groupMembers = axlGetSelSet()`

> `group_dbid = axlDBCreateGroup("my_group" "generic" groupMembers)`

* Net group

> `groupMembers = axlSelectByName("NET" "NET*" t)`

> `group_dbid = axlDBCreateGroup("NG1" "net_group" groupMembers)`

**Note:** The order of the group members provided when you access the`groupMembers` property may vary from the order provided in `lo_groupMembers`.

### axlDBDisbandGroup

`axlDBDisbandGroup(o_group)⇒ t/nil`

#### Description

Disbands the database group you specify with the`o_group` argument, thereby immediately removing the group. Members of the group are not deleted.

#### Arguments

|  |
| --- | ---
| `o_group` | `dbid` of the group to be deleted.
#### Value Returned

|  |
| --- | ---
| `t` | Group disbanded.
| `nil` | Group could not be disbanded due to an invalid argument, for example, the`dbid` not being for a valid group.
#### See Also

[axlDBCreateGroup](#1076292 "16")

### axlDBGetGroupFromItem

`axlDBGetGroupFromItem(o_dbidt_groupType[g_promoteToNet]) -> lo_groupDbid/nil`

#### Description

Filter object's group membership by a group type. You can normally fetch the list of groups that an object is a member of by using the groups attribute of its dbid (etc. o\_dbid->groups). This function provides additional filtering where you can request if an belongs to a particular group type. Depending upon the group characteristics an object can either belong to single group of a type or can be a member multiple groups of a single type. For example, an object can belong to multiple generic groups can belong to only one differential pair group.

The g\_promoteToNet option for groups for which membership is limited to nets/xnets. It promotes the object provided to its owning xnet, and is targeted for use with diffpair and bus groups, where membership is limited to the net's xnet. It provides an easy way for those groups if given the dbid of a net to promote the id to its xnet.

#### Arguments

|  |
| --- | ---
| `o_dbid` | dbid to be examined
| `t_groupType` | group type name. This is the group type name NOT the name of the group. In dbid terms this is group->type.
| `g_mode` | If this value is`t`, it promotes the object to its net/xnet and performs test on that object.  If the value is set to`'all` then it traverses group hierarchy and returns both direct and indirect group membership of dbid.  For example, if net is a member of a xnet which is a member of a diffpair, and you specify group type of "DIFF\_PAIR", this returns diffpair group for object.
#### Value Returned

|  |
| --- | ---
| `lo_groupDbid` | Group dbids or nil if not a member of requested group type
***See Also***: [axlDBCreateGroup](#1076292 "16")

#### *Examples*

In both case ashOne is a shareware utility that allows user to select one object (see`<CDSROOT>``/share/pcb/examples/skill/ash-fxf/ashone.il`

* differential pair; set`g_promoteToNet` to `t` in case net is part of a xnet

`p = ashOne() ;` select a net that is a diffpair member

`l = axlDBGetGroupFromItem(p "DIFF_PAIR" t)`

* generic group

`p = ashOne() ;`create a group and select an object that is part of group

`l = axlDBGetGroupFromItem(p "GENERIC")`

### axlDBGroupRename

`axlDBGroupRename(o_groupDbidt_newName)==> t/nil`

#### Description

Renames a group. Groups supported are GENERIC, BUS, DIFF\_PAIR, NETCLASS, NET\_GROUP and MATCH\_GROUP. Do not attempt to rename group types not listed.

**Note:** All restrictions and disclaimers specified in[axlDBCreateGroup](#1076292 "16") also apply for this API.

#### Arguments

|  |
| --- | ---
| `o_groupDbid` | The dbid of the group to be renamed
| `t_newName` | New name of the group. Group name must be unique for the group type.
#### Value Returned

|  |
| --- | ---
| `t` | Successful in rename.
| `nil` | Failed in rename; dbid not a group, group can't be renamed, new name is not legal for group type or name already exists in that group type.
#### See Also

[axlDBCreateGroup](#1076292 "16")

### axlDBRemoveGroupObjects

`axlDBRemoveGroupObjects(o_grouplo_members)⇒ t/nil`

#### Description

Removes the database objects from the specified group. Group members, though removed, are not deleted.

#### Arguments

|  |
| --- | ---
| `o_group` | Group`dbid`.
| `lo_members` | List of database objects to be removed from the group. A single`dbid` can be substituted for a list.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects removed from the group.
| `nil` | `lo_members` contained no `dbids` of objects that could be removed from the group.
**Notes:**

* If a group is left with no members, the group is tagged for deletion, but is not removed immediately.

* You do not need to explicitly remove objects from a group before deleting the object with`axlDeleteObject`. Deleting an object removes it from all groups to which it belongs.

#### See Also

[axlDBCreateGroup](#1076292 "16")

### axlNetClassAdd

`axlNetClassAdd(o_netclassdbid/t_netclassNameo_dbid/lo_dbid)==> t/nil`

#### Description

Adds members to a netclass group. Eligible members are:

* nets

* xnets

* differential pairs

* busses

See netclass discussion in[axlNetClassCreate](#1077736 "16"). This will mark DRC out of date. It is up to the application to update the DRC system.

* Using dbids is faster then using names.

#### Arguments

|  |
| --- | ---
| `o_netclassdbid` | dbid of a netclass group
| `t_netclassName` | name of a netclass group
| `o_dbid` | legal database dbid to add to netclass
| `lo_dbid` | list of legal database dbids to add to netclass
#### Value Returned

|  |
| --- | ---
| `t` | added elements
| `nil` | failed one or more element adds; object might already be a member of a netclass in that domain or not legal dbid to add to a netclass
#### Examples

To netclass group created in axlNetClassCreate add two nets

> `nc = car(axlSelectByName("NETCLASS" "5_MIL"))`

> `nets = axlSelectByName("NET" '("NET8" "NET9"))`

> `axlNetClassAdd(nc nets)`

#### See Also

[axlNetClassCreate](#1077736 "16")

### axlNetClassCreate

`axlNetClassCreate(t_nameg_domain/lg_domain)==> o_dbid`

#### Description

This creates a new netclass group. If a netclass exists with this name then`nil` is returned. Net Classes need to be populated via `axlNetClassAdd`. Empty net classes may be deleted on database save. A netclass must be part of one or more domains. These domains are shown below. The Same Net Constraint domain uses the netclass spacing domain. An object (bus, diffpair, xnet or net) may be a member of single netclass in a domain. For example, if net VCC exists in the POWER netclass in the physical domain then you cannot add it to another netclass in the physical domain. You can still add this net of a netclass in the spacing or electrical domain. You can obtain the current set of netclasses in the database via: `axlDBGetDesign()->netclass`. axlNetClassGet reports if an object is a member of a netclass either directly or via the logic hierarchy.

To assign a cset to a netclass assign the PHYSICAL\_CONSTRAINT\_SET, SPACING\_CONSTRAINT\_SET, SAME\_NET\_SPACING\_CONSTRAINT\_SET or ELECTRICAL\_CONSTRAINT\_SET property to the netclass where the value of the property is the cset name.

Same Net constraints shares the same domain with the SPACING\_CONSTRAINT\_SET.

#### Arguments

|  |
| --- | ---
| `t_name` | name of netclass group (changed to upper case)
| `g_domain` | netclass domain can be 'spacing, 'physical, 'electrical or 'all
| `lg_domain` | list of netclass domains
#### Value Returns

|  |
| --- | ---
| `nil:` | error or netclass with that name exists
| `o_dbid:` | dbid of group
#### See Also

[axlNetClassDelete](#1078088 "16"), [axlNetClassAdd](#1077527 "16"), [axlNetClassRemove](#1078460 "16"), [axlNetClassGet](#1078253 "16"), [axlDBAddProp](03dbcre8.html#367701 "15"), [axlCNSCreate](18consmgt.html#1106245 "19")

#### Examples

Create a netclass in physical domain called "`5_MIL`"

> `nc = axlNetClassCreate("5_mil" 'physical)`

### axlNetClassDelete

`axlNetClassDelete(o_netclassdbid/t_netclassName/lg_netclassdbid) -> t/nil`

#### Description

This deletes a net class group. It does not delete the objects belonging to the group. It is up to the application code to update DRC.

**Note:** Using dbids is faster then using names.

#### Arguments

|  |
| --- | ---
| `o_netclassdbid:` | dbid of a net class group
| `t_netclassName:` | name of a net class group
| `lg_netclassdbid:` | list of net class groups (dbids or names)
#### Value Returned

|  |
| --- | ---
| `t:` | net class group deleted
| `nil:` | failed
#### See Also

[axlNetClassCreate](#1077736 "16")

Examples

Delete net class group created in axlNetClassCreate

> `nc = car(axlSelectByName("NETCLASS" "5_MIL"))`

> `axlNetClassDelete(nc)`

or

> `axlNetClassDelete("5_MIL")`

### axlNetClassGet

`axlNetClassGet(o_dbids_domaing_hierarchal)==> o_netclass`

#### Description

Given a dbid (net, xnet, diffpair or bus) and a domain (spacing, physical or electrical) return its netclass. If g\_hierarchical is nil, returns object's netclass if a direct member. If g\_hierarchal=t returns first netclass encountered in logical hierarchy. For example, if a net is a member of a bus and the bus is assigned to netclass, BUSCLASS, and you pass a net of the bus to this API:

> will return nil if g\_hierarchy=nil

> will return netclass dbid, BUSCLASS, if g\_hierarchy=t

#### Arguments

|  |
| --- | ---
| `o_dbid:` | dbid may be net, xnet, diffpair or bus
| `s_domain:` | netclass domain; spacing, physical or electrical
| `g_hierarchal` |
#### Value Returned

|  |
| --- | ---
| `o_netclass` | dbid of netclass
| `nil` | object not part of a netclass in the domain or an invalid object
#### See Also

[axlNetClassCreate](#1077736 "16")

#### Examples

Use example in[axlNetClassAdd](#1077527 "16")

From example in (should return netclass in both cases)

> `net = car(axlSelectByName("NET" "NET8"))`

> `axlNetClassGet(nets 'physical nil)`

> `axlNetClassGet(nets 'physical t)`

### axlNetClassRemove

`axlNetClassRemove(o_netclassdbid/t_netclassNameo_dbid/lo_dbid)==> t/nil`

#### Description

Removes elements from an existing net class group. Element must currently be a direct member of the group. This will mark DRC out of date. It is up to the application to update the DRC system.

* Using dbids is faster then using names.

#### Arguments

|  |
| --- | ---
| `o_netclassdbid:` | dbid of a netclass group
| `t_netclassName:` | name of a netclass group
| `o_dbid:` | legal database dbid to remove from group
| `lo_dbid:` | list of legal database dbids to remove from group
#### Value Returned

|  |
| --- | ---
| `t` | removed elements
| `nil` | failed to remove one or more elements. Object may not be a cset member (member must be a direct member).
#### Examples

Using the example from axlNetClassAdd remove one of the nets:

> `axlNetClassRemove(nc car(nets))`

#### See Also

[axlNetClassCreate](#1077736 "16")

### axlRegionAdd

`axlRegionAdd(o_regiondbid/t_regionNameo_dbid/lo_dbid)==> t/nil`

#### Description

Adds members to a region group. Eligible members are:

* shapes

* rectangles

Only objects on the CONS\_REGION class may be added to a region. See region discussion in axlRegionCreate. This will mark DRC out of date. It is up to the application to update the DRC system

**Note:** Using dbids is faster then using names.

#### Arguments

|  |
| --- | ---
| `o_regiondbid:` | dbid of a region group
| `t_regionName:` | name of a region group
| `o_dbid:` | legal database dbid to add to region
| `lo_dbid:` | list of legal database dbids to add to region
#### Value Returned

|  |
| --- | ---
| `t` | added elements
| `nil` | failed one or more element adds; object might already be a member of a region or not legal dbid to add to a region
#### See Also

[axlRegionAdd](#1077519 "16")

#### Examples

To region group created in axlRegionCreate add a shape

> `nc = car(axlSelectByName("REGION" "BGA"))`

> `lyr = "CONSTRAINT REGION/OUTER_LAYERS"`

> `shape = axlDBCreateRectangle( list(100:100 200:200) nil lyr)`

> `shape = car(shape)`

> `axlRegionAdd(nc shape)`

### axlRegionCreate

`axlRegionCreate(t_name)==> o_dbid`

#### Description

Creates a new region group. If a region exists with this name then`nil` is returned. Regions may contain shapes on CONS\_REGION class. Shapes are added to the region group via the [axlRegionAdd](#1077519 "16"). Empty regions may be deleted on database save. You can obtain the current set of regions in the database via: `axlDBGetDesign()->region`. None of the region APIs are enabled in the PCB L product.

**Note:** For better performance, when modifying regions you may wish to wrap all the calls with the[axlDBCloak](17dbtran.html#1065349 "18") command.

#### Arguments

|  |
| --- | ---
| `t_name` | name of region group (changed to upper case)
#### Value Returned

|  |
| --- | ---
| `nil:` | error or region with that name exists
| `o_dbid:` | dbid of group
If shapes are a member of a region then their dbid region attribute will refer to the region dbid

#### Examples

Create a region called "BGA"

> `nc = axlRegionCreate("BGA")`

#### See Also

[axlRegionDelete](#1077191 "16"), [axlRegionAdd](#1077519 "16"), [axlRegionRemove](#1077342 "16"), [axlDBCreateShape](03dbcre8.html#367593 "15"),

[axlDBCreateRectangle](03dbcre8.html#367609 "15")

### axlRegionDelete

`axlRegionDelete(o_regiondbid/t_regionName/lg_regiondbid) -> t/nil`

#### Description

This deletes a region group. It does not delete the objects belonging to the group.

**Note:** Using dbids is faster then using names.

#### Arguments

|  |
| --- | ---
| `o_regiondbid:` | dbid of a region group
| `t_regionName:` | name of a region group
| `lg_regiondbid:` | list of region groups (dbids or names)
#### Value Returned

|  |
| --- | ---
| `t:` | net class group deleted
| `nil:` | failed
#### See Also

[axlRegionCreate](#1076939 "16")

#### Examples

Delete region group created in axlRegionCreate

> `nc = car(axlSelectByName("REGION" "BGA"))`

> `axlRegionDelete(nc)`

or

> `axlRegionDelete("BGA")`

### axlRegionRemove

`axlRegionRemove(o_regiondbid/t_regionNameo_dbid/lo_dbid)==> t/nil`

#### Description

Removes shapes from an existing region group. Element must currently be a direct member of the group. This will mark DRC out of date. It is up to the application to update the DRC system.

**Note:** Using dbids is faster then using names.

#### Arguments

|  |
| --- | ---
| `o_regiondbid:` | dbid of a region group
| `t_regionName:` | name of a region group
| `o_dbid:` | legal database shapes to remove from group
| `lo_dbid:` | list of legal database shapes to remove from group
#### Value Returned

|  |
| --- | ---
| `t` | removed elements
| `nil` | failed to remove one or more elements. Object may not be a region member (member must be a direct member).
#### See Also

[axlRegionCreate](#1076939 "16")

Examples

Using the example from[axlRegionAdd](#1077519 "16") remove the shape:

> `axlRegionRemove(region shape)`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
