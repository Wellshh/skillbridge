# Class: CNewBOm

CVariant_sFindInUIntArray2(Array, Element) : returns int
Parameters:
Array: CUIntArray &
Element: UINT
START class CNewBOm
DeleteGroup(BomGroupName) : returns int
Class : CNewBOm
Parameters:
BomGroupName: CString &
RenameGroup(OldBomGroupName, NewBomGroupName) : returns int
Class : CNewBOm
Parameters:
OldBomGroupName: CString &
NewBomGroupName: CString &
AddGroup(BomGroupName) : returns int
Class : CNewBOm
Parameters:
BomGroupName: CString &
GetBomVariants(OutGroupName) : returns int
Class : CNewBOm
Parameters:
OutGroupName: CSStringArray &
GetBomGroups(BomName, OutSubGroupName) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
OutSubGroupName: CStringArray &
AddGroupToBomVariant(VariantName, GroupName) : returns int
Class : CNewBOm
Parameters:
VariantName: CString &
GroupName: CString &

---

IsGroupInBom(GroupName) : returns int
Class : CNewBOm
Parameters:
GroupName: CString &
RenameInBom(Current, Parent, NewGroupName) : returns int
Class : CNewBOm
Parameters:
Current: CString &
Parent: CString &
NewGroupName: CString &
DeleteInBom(Current, Parent) : returns int
Class : CNewBOm
Parameters:
Current: CString &
Parent: CString &
Close()
Class : CNewBOm
Parameters:
DeleteGroupInBom(BomName, GroupName) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
GroupName: CString &
GetAvailBomVariantForGroup(GroupName, BomVariants) : returns int
Class : CNewBOm
Parameters:
GroupName: CString &
BomVariants: CStringArray &
AddPartsToBom(BomName, PartArray) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
PartArray: CUIntArray &

---

GetPartsFromBom(BomName, PartArray) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
PartArray: CUIntArray &
GetAllParts(Array) : returns int
Class : CNewBOm
Parameters:
Array: QUIntArray &
DeleteParts(Array) : returns int
Class : CNewBOm
Parameters:
Array: QUIntArray &
GetBomHeaderInfo(HeaderInfo) : returns int
Class : CNewBOm
Parameters:
HeaderInfo: CString &
GetBomCount() : returns int
Class : CNewBOm
Parameters:
GetBomData(index, BomName, BomData) : returns int
Class : CNewBOm
Parameters:
index: int
BomName: CString &
BomData: CString &
GetBomPartData(Data) : returns int
Class : CNewBOm
Parameters:
Data: CString &
SetBomHeaderInfo(HeaderInfo) : returns int
Class : CNewBOm

---

Parameters:
HeaderInfo: CString &
SetBomData(Data) : returns int
Class : CNewBOm
Parameters:
Data: CString &
SetBomPartData(Data) : returns int
Class : CNewBOm
Parameters:
Data: CString &
CloneBomVariant(BomName, NewName) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
NewName: CString
GetBomName(index, GroupName) : returns int
Class : CNewBOm
Parameters:
index: int
GroupName: CString &
GetBomName(GroupName, BomNames) : returns int
Class : CNewBOm
Parameters:
GroupName: CString
BomNames: CStringArray &
SetArray(PartArray) : returns int
Class : CNewBOm
Parameters:
PartArray: CUIntArray &
GetArray(PartArray) : returns int
Class : CNewBOm
Parameters:
PartArray: CUIntArray &

---

AddPtrForBom(BomName, Array) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
Array: CSStringArray &
GetPtrFromBom(BomName, Array) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
Array: CSStringArray &
CleanBomPtr() : returns int
Class : CNewBOm
Parameters:
AddPtrForBom1(BomName, Array) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
Array: CPtrArray &
GetPtrFromBom1(BomName, Array) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
Array: CPtrArray &
CleanBomPtr1() : returns int
Class : CNewBOm
Parameters:
SetPartAmbig(BomName, GroupName, PartArray, Ambig)
Class : CNewBOm
Parameters:
BomName: CString &
GroupName: CString &
PartArray: CUIntArray &
Ambig: int

---

ClearAmbig(BomName)
Class : CNewBOm
Parameters:
BomName: CString &
IsPartAmbig(BomName, GroupName, id) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
GroupName: CString &
id: int
IsAmbigResolved(BomName) : returns int
Class : CNewBOm
Parameters:
BomName: CString &
SetAmbigResolved(BomName, flag = 1)
Class : CNewBOm
Parameters:
BomName: CString &
flag: int
SetAmbigResolved(BomName)
Class : CNewBOm
Parameters:
BomName: CString &
END class CNewBOm
START class CISBase
Delete()
Class : CISBase
Parameters:
UnDelete()
Class : CISBase
Parameters: