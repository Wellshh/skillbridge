# Class: CPartProp(QPropertyArray):

START class CPartProp(QPropertyArray):
Clear()
Class : CPartProp(QPropertyArray):
Parameters:
RemoveAll()
Class : CPartProp(QPropertyArray):
Parameters:
AddProp(PropName, PropValue, PropType = NO_TYPE)
Class : CPartProp(QPropertyArray):
Parameters:
PropName: CString const &
PropValue: CString const &
PropType: int
AddProp(PropName, PropValue)

---

Class : CPartProp(QPropertyArray):
Parameters:
PropName: CString const &
PropValue: CString const &
Set(DfltProps = NO_PROPS, CaseSensitive = 0)
Class : CPartProp(QPropertyArray):
Parameters:
DfltProps: enum CPartProp::PropTypeT
CaseSensitive: int
Set(DfltProps = NO_PROPS)
Class : CPartProp(QPropertyArray):
Parameters:
DfltProps: enum CPartProp::PropTypeT
Set()
Class : CPartProp(QPropertyArray):
Set(PropArray, pTypes = None)
Class : CPartProp(QPropertyArray):
Parameters:
PropArray: QPropertyArray const &
pTypes: CWordArray const *
Set(PropArray)
Class : CPartProp(QPropertyArray):
Parameters:
PropArray: QPropertyArray const &
Set(PropName, PropValue, PropType = NO_TYPE)
Class : CPartProp(QPropertyArray):
Parameters:
PropName: CString const &
PropValue: CString const &
PropType: int
Set(PropName, PropValue)
Class : CPartProp(QPropertyArray):
Parameters:

---

PropName: CString const &
PropValue: CString const &
GetPropType(Index) : returns int
Class : CPartProp(QPropertyArray):
Parameters:
Index: int
GetPropType(Name) : returns int
Class : CPartProp(QPropertyArray):
Parameters:
Name: CString const &
GetPropNames() : returns CStringArray
Class : CPartProp(QPropertyArray):
Parameters:
GetPropContents() : returns CStringArray
Class : CPartProp(QPropertyArray):
GetPropContents(PropName) : returns CString
Class : CPartProp(QPropertyArray):
Parameters:
PropName: CString const &
IsMember(pProp) : returns int
Class : CPartProp(QPropertyArray):
Parameters:
pProp: char const *
IsMember(Prop, pPropArray) : returns int
Class : CPartProp(QPropertyArray):
Parameters:
Prop: char const *
pPropArray: CStringArray const *
SetPartNumberFieldName(PartNumber)
Class : CPartProp(QPropertyArray):
Parameters:
PartNumber: CString const &

---

GetPartNumberFieldName() : returns CString
Class : CPartProp(QPropertyArray):
Parameters:
END class CPartProp(QPropertyArray):
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