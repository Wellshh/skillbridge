# Class: CVariant

START class CVariant
IsPartPresent(GrpName, SubGrpName, Part) : returns int
Class : CVariant
Parameters:
GrpName: CString
SubGrpName: CString
Part: UINT
GetAmbiguousPartsContainer() : returns CAmbiguousParts
Class : CVariant
Parameters:
IsGroupHasSubGroups(GroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString &
GetGroupCount() : returns int
Class : CVariant
Parameters:
GetAllGroups(arg0)
Class : CVariant
Parameters:
arg2: CStringArray &
IsGroupPressent(GroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString &
AddGroup(GroupName) : returns int

---

Class : CVariant
Parameters:
GroupName: CString &
RemoveGroup(GroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString &
ReNameGroup(OldGroupName, NewGroupName) : returns int
Class : CVariant
Parameters:
OldGroupName: CString
NewGroupName: CString
GetGroup(GroupName, arg1) : returns int
Class : CVariant
Parameters:
GroupName: CString &
arg3: CGroup *
AddSubGroup(GroupName, Array) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Array: CStringArray &
GetAllSubGroup(GroupName, OutArray) : returns int
Class : CVariant
Parameters:
GroupName: CString &
OutArray: CStringArray &
DeleteSubGroup(GroupName, delsubgrp) : returns int
Class : CVariant
Parameters:
GroupName: CString &
delsubgrp: CString
ReNameSubGroup(GroupName, OldSubGroupName, NewSubGroupName) : returns int

---

Class : CVariant
Parameters:
GroupName: CString
OldSubGroupName: CString
NewSubGroupName: CString
AddPartsToSubGroup(GroupName, SubGroupName, Parts) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
Parts: CUIntArray &
AddPartsToGroup(GroupName, arg1) : returns int
Class : CVariant
Parameters:
GroupName: CString &
arg3: CUIntArray &
GetPartsFromGroup(GroupName, mapParts)
Class : CVariant
Parameters:
GroupName: CString
mapParts: IntegerMapT &
GetPartsFromGroup(GroupName, Parts) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Parts: CUIntArray &
GetPartsFromSubGroup(GroupName, SubGroupName, mapParts)
Class : CVariant
Parameters:
GroupName: CString
SubGroupName: CString
mapParts: IntegerMapT &
GetPartsFromSubGroup(GroupName, SubGroupName, arg2) : returns int
Class : CVariant

---

Parameters:
GroupName: CString &
SubGroupName: CString &
arg4: CUIntArray &
GetGroupByIndex(Inex) : returns CString
Class : CVariant
Parameters:
Inex: int
GetSubGroupByIndex(GroupName, Index) : returns CString
Class : CVariant
Parameters:
GroupName: CString &
Index: int
GetSubGroupCount(GroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString &
GetGroupStream() : returns CString
Class : CVariant
Parameters:
GetPartStream_Group(GroupName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Data: CString &
GetPartStream_SubGroup(GroupName, SubGroupName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
Data: CString &
GetUpdatedPartsInfo_Grp(GroupName, UpdatedPatrs) : returns int
Class : CVariant

---

Parameters:
GroupName: CString &
UpdatedPatrs: CString &
GetUpdatedPartsInfo_SGrp(GroupName, SubGroupName, UpdatedPatrs) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
UpdatedPatrs: CString &
LoadUpdatedPartInfo_SubGroup(GroupName, SubGroupName, OldPartId, UpdatedPatrs) : returns
int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
OldPartId: CString &
UpdatedPatrs: CStringArray &
LoadUpdatedPartInfo_Group(GroupName, OldPartId, UpdatedPatrs) : returns int
Class : CVariant
Parameters:
GroupName: CString &
OldPartId: CString &
UpdatedPatrs: CStringArray &
GetUpdatedPartsInfo_SubGroup(GroupName, SubGroupName, OldPartId, UpdatedPatrs) : returns
int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
OldPartId: CString &
UpdatedPatrs: CStringArray &
GetUpdatedPartsInfo_Group(GroupName, OldPartId, UpdatedPatrs) : returns int
Class : CVariant
Parameters:
GroupName: CString &

---

OldPartId: CString &
UpdatedPatrs: CStringArray &
SetGroupsHeader(GroupStream) : returns int
Class : CVariant
Parameters:
GroupStream: CString &
SetGroupDataStream(GroupName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Data: CString &
SetSubGroupDataStream(GroupName, SubGroupName, GroupPartStream) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
GroupPartStream: CString &
SetUpdatedGroupData(GroupName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Data: CString &
SetUpdatedSubGpData(GroupName, SubGpName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGpName: CString &
Data: CString &
SubGroupHasUpdatedParts(GroupName, SubGroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString
SubGroupName: CString

---

GroupHasUpdatedParts(GroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString
GetUpdatedSubGpData(GroupName, SubGpName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGpName: CString &
Data: CString &
GetUpdatedGpData(GroupName, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Data: CString &
SetGroupPartsAsStuffed(GroupName, Parts, Flag) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Parts: CUIntArray &
Flag: int
SetSubGroupPartsAsStuffed(GroupName, SubGroupName, Parts, Flag) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
Parts: CUIntArray &
Flag: int
GetStuffedPartsGroup(GroupName, Parts, Stuffed) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Parts: CUIntArray &
Stuffed: int

---

GetStuffedPartsSubGroup(Groupname, SubGroupName, Parts, Stuffed) : returns int
Class : CVariant
Parameters:
Groupname: CString &
SubGroupName: CString &
Parts: CUIntArray &
Stuffed: int
Cleanup() : returns int
Class : CVariant
Parameters:
IsPartStuffedGroup(GroupName, Part) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Part: UINT &
IsPartStuffedSubGroup(GroupName, SubGroupName, Part) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
Part: UINT &
DeletePartsFromSubGroup(GroupName, SubGroupName, DelParts) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
DelParts: CUIntArray &
DeletePartsFromGroup(SubGroupName, DelParts) : returns int
Class : CVariant
Parameters:
SubGroupName: CString &
DelParts: CUIntArray &
AddUpdatedPartSubGroup(GroupName, SubGroupName, PartArray, Data, bflag = 1) : returns int
Class : CVariant

---

Parameters:
GroupName: CString &
SubGroupName: CString &
PartArray: CUIntArray &
Data: CStringArray &
bflag: int
AddUpdatedPartSubGroup(GroupName, SubGroupName, PartArray, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
PartArray: CUIntArray &
Data: CStringArray &
IsSubGroupHasUpdatedPart(GroupName, SubGroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
GetUpdatedPartSubGroup(GroupName, SubGroupName, PartArray, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
PartArray: CUIntArray &
Data: CStringArray &
GetUpdatedPartSubGroup(l_strGroupName, l_strSubGroupName, l_strData) : returns int
Class : CVariant
Parameters:
l_strGroupName: CString &
l_strSubGroupName: CString &
l_strData: CString &
AddUpdatedPartGroup(GroupName, PartArray, Data, bflag = 1) : returns int
Class : CVariant
Parameters:
GroupName: CString &

---

PartArray: CUIntArray &
Data: CStringArray &
bflag: int
AddUpdatedPartGroup(GroupName, PartArray, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
PartArray: CUIntArray &
Data: CStringArray &
IsGroupHasUpdatedPart(GroupName) : returns int
Class : CVariant
Parameters:
GroupName: CString &
GetUpdatedPartGroup(GroupName, PartArray, Data) : returns int
Class : CVariant
Parameters:
GroupName: CString &
PartArray: CUIntArray &
Data: CStringArray &
GetUpdatedPartGroup(l_strGroupName, l_strData) : returns int
Class : CVariant
Parameters:
l_strGroupName: CString &
l_strData: CString &
GetCountOfUpdatedPartsGroup(l_strGroupName) : returns int
Class : CVariant
Parameters:
l_strGroupName: CString &
GetCountOfUpdatedPartsSubGroup(l_strGroupName, l_strSubGroupName) : returns int
Class : CVariant
Parameters:
l_strGroupName: CString &
l_strSubGroupName: CString &

---

LoadUpdatedPatrsGroup(GroupName, PartStream) : returns int
Class : CVariant
Parameters:
GroupName: CString &
PartStream: CString &
LoadUpdatedPatrsSubGroup(GroupName, SubGroupName, PartStream) : returns int
Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
PartStream: CString &
HasUpdatedParts(Stream) : returns int
Class : CVariant
Parameters:
Stream: CString &
DeletePartFromAllVariants(PartId) : returns int
Class : CVariant
Parameters:
PartId: CUIntArray &
GetPartsFromAllVariants(mapParts) : returns int
Class : CVariant
Parameters:
mapParts: IntegerMapT &
GetPartsFromAllVariants(Parts) : returns int
Class : CVariant
Parameters:
Parts: QUIntArray &
DeletUpDatedPartsFromGroup(GroupName, Parts) : returns int
Class : CVariant
Parameters:
GroupName: CString &
Parts: CUIntArray &
DeletUpDatedPartsFromSubGroup(GroupName, SubGroupName, Parts) : returns int

---

Class : CVariant
Parameters:
GroupName: CString &
SubGroupName: CString &
Parts: CUIntArray &
CreateNewGroupAs(OldGrpName, NewGrpName) : returns int
Class : CVariant
Parameters:
OldGrpName: CString &
NewGrpName: CString &
CreateNewSubGroupAs(GrpName, OldSubGrpName, NewSubGrpName, ReName) : returns int
Class : CVariant
Parameters:
GrpName: CString &
OldSubGrpName: CString &
NewSubGrpName: CString &
ReName: int
IsPartPresentInGroup(GrpName, Part) : returns int
Class : CVariant
Parameters:
GrpName: CString &
Part: UINT &
IsPartPresentInSubGroup(GrpName, SubGrpName, Part) : returns int
Class : CVariant
Parameters:
GrpName: CString &
SubGrpName: CString &
Part: UINT &
sFindInUIntArray2(Array, Element) : returns int
Class : CVariant
Parameters:
Array: CUIntArray &
Element: UINT
END class CVariant