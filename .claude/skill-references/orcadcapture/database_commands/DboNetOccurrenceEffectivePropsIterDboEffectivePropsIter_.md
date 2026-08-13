# Class: DboNetOccurrenceEffectivePropsIter(DboEffectivePropsIter):

obj: DboBaseObject *
status: DboState &
DboEffectivePropsIterToDboNetOccurrenceEffectivePropsIter(x) : returns
DboNetOccurrenceEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboNetOccurrenceEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboNetOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboNetOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboNetOccurrenceEffectivePropsIter(DboEffectivePropsIter):
DboOccurrenceToDboTitleBlockOccurrence(x) : returns DboTitleBlockOccurrence
Parameters:
x: DboOccurrence *
START class DboTitleBlockOccurrence(DboOccurrence):
GetObjectType() : returns ObjectTypeT
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
GetSchematic(status) : returns DboSchematic

---

Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathName(name) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString &
GetSchematicPath(name) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString &
SetTitleBlock(pTitleBlock) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
pTitleBlock: DboTitleBlock *
GetTitleBlock(status) : returns DboTitleBlock
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
status: DboState &

---

SetTitleBlockId(nTitleBlockId) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
nTitleBlockId: unsigned long
GetTitleBlockId(status) : returns unsigned long
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
status: DboState &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
DeleteEffectiveProp(name) : returns DboState
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
name: CString const &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
status: DboState &
AddVariantProp(strName, strVal)
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
strName: CString const &
strVal: CString const &

---

ClearVariantMap(bFlag = 1)
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
bFlag: int
ClearVariantMap()
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
GetVariantProp(strName, strVal) : returns int
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
strName: CString const &
strVal: CString &
GetNextNewVariantProp(strName, strVal, bNewFound) : returns int
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
strName: CString &
strVal: CString &
bNewFound: int &
IsVariantPropMapEmpty() : returns int
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
sGetPathName(obj, status) : returns CString
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSchematicPath(obj, status) : returns CString
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetId(obj, status) : returns int
Class : DboTitleBlockOccurrence(DboOccurrence):

---

Parameters:
obj: DboBaseObject *
status: DboState &
GetInstance(status) : returns DboBaseObject
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
status: DboState &
FindInstance(status) : returns DboBaseObject
Class : DboTitleBlockOccurrence(DboOccurrence):
Parameters:
status: DboState &
END class DboTitleBlockOccurrence(DboOccurrence):
DboTitleBlockOccurrence_sGetPathName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlockOccurrence_sGetSchematicPath(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlockOccurrence_sGetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboEffectivePropsIterToDboTitleBlockOccurrenceEffectivePropsIter(x) : returns
DboTitleBlockOccurrenceEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboTitleBlockOccurrenceEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboTitleBlockOccurrenceEffectivePropsIter(DboEffectivePropsIter):

---

Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboTitleBlockOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboTitleBlockOccurrenceEffectivePropsIter(DboEffectivePropsIter):
DboBaseObjectToDboFlatNet(x) : returns DboFlatNet
Parameters:
x: DboBaseObject *
START class DboFlatNet(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboFlatNet(DboBaseObject):
Parameters:
GetId(status) : returns unsigned long
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
GetOwner() : returns DboDesign
Class : DboFlatNet(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboFlatNet(DboBaseObject):
Parameters:

---

GetTopNet(status) : returns DboNetOccurrence
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
GetName(Name) : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
Name: CString &
ComputeName(pSchNetName = "") : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
pSchNetName: CString
ComputeName() : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
GetIsGlobal(status) : returns int
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
nNameID: UINT
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
name: CString const &
value: CString &
sGetName(obj, status) : returns CString
Class : DboFlatNet(DboBaseObject):
Parameters:
obj: DboBaseObject *

---

status: DboState &
sGetId(obj, status) : returns int
Class : DboFlatNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsGlobal(obj, status) : returns int
Class : DboFlatNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboFlatNet(DboBaseObject):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(occArr, pDesign, status)
Class : DboFlatNet(DboBaseObject):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
sGetColor(obj, status) : returns ColorT
Class : DboFlatNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboFlatNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetLineStyle(obj, status) : returns LineStyleT
Class : DboFlatNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetColor(status) : returns ColorT
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
GetLineStyle(status) : returns LineStyleT
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
GetNameStrategy() : returns FlatNetNamingStrategyT
Class : DboFlatNet(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboFlatNet(DboBaseObject):
Parameters:
NewNetsIter(status, mode = TOP) : returns DboFlatNetNetsIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewNetsIter(status) : returns DboFlatNetNetsIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &

---

NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
NewWiresIter(status, mode = TOP) : returns DboFlatNetWiresIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewWiresIter(status) : returns DboFlatNetWiresIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
NewNetOccurrencesIter() : returns DboFlatNetNetOccurrencesIter
Class : DboFlatNet(DboBaseObject):
Parameters:
NewPortOccurrencesIter(status, mode = ALL) : returns DboFlatNetPortOccurrencesIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPortOccurrencesIter(status) : returns DboFlatNetPortOccurrencesIter
Class : DboFlatNet(DboBaseObject):
Parameters:
status: DboState &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState

---

Class : DboFlatNet(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
GetAttributeLockingInfo(propName, lLock, preTrigger, postTrigger) : returns bool
Class : DboFlatNet(DboBaseObject):
Parameters:
propName: CString
lLock: MaskT &
preTrigger: CString &
postTrigger: CString &
DeleteEffectiveProp(name) : returns DboState
Class : DboFlatNet(DboBaseObject):
Parameters:
name: CString const &
END class DboFlatNet(DboBaseObject):
DboFlatNet_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboFlatNet_sGetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboFlatNet_sGetIsGlobal(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboFlatNet_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &