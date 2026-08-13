# Class: DboInstOccurrence(DboOccurrence):

rotation: enum DboValue::RotationT
DboDisplayProp_sSetFont(obj, font) : returns DboState
Parameters:
obj: DboBaseObject *
font: LOGFONT &
DboDisplayProp_sSetColor(obj, color) : returns DboState
Parameters:
obj: DboBaseObject *
color: enum DboValue::ColorT
DboDisplayProp_sSetDisplayType(obj, displayType) : returns DboState
Parameters:
obj: DboBaseObject *
displayType: enum DboValue::DisplayTypeT
DboOccurrenceToDboInstOccurrence(x) : returns DboInstOccurrence
Parameters:
x: DboOccurrence *
START class DboInstOccurrence(DboOccurrence):
GetObjectType() : returns ObjectTypeT
Class : DboInstOccurrence(DboOccurrence):
Parameters:
GetSchematic(status) : returns DboSchematic
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathName(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):

---

Parameters:
name: CString &
GetPathNameNumber(name, chSeparator = '.') : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathNameNumber(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
GetHierPathName(name, chSeparator = '/') : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetHierPathName(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
GetImplementationName(name, chSeparator = '/') : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetImplementationName(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &

---

chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString &
GetContents(status) : returns DboView
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
IsPrimitive(status) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
IsPSpiceOnly() : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
GetInstChildrenCount(status) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
HasChildren(status) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
IsRecursive(status) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPartInst(status) : returns DboPartInst
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &

---

FindPartInst(status) : returns DboPartInst
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetReference(ref) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
ref: CString &
GetDesignator(designator) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
designator: CString &
GetReferenceDesignator(refDes) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
refDes: CString &
GetPartValue(value) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
value: CString &
GetInstOccurrenceByRef(Name, bPhysical, status) : returns DboInstOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString const &
bPhysical: int
status: DboState &
GetInstOccurrenceByHierPath(name, status) : returns DboInstOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
status: DboState &
GetInstOccurrence(nId, status) : returns DboInstOccurrence

---

Class : DboInstOccurrence(DboOccurrence):
Parameters:
nId: int
status: DboState &
GetInstOccurrence(Name, status) : returns DboInstOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString &
status: DboState &
GetInstOccurrence(pInst, status) : returns DboInstOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pInst: DboPartInst *
status: DboState &
GetTitleBlockOccurrence(nId, status) : returns DboTitleBlockOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
nId: int
status: DboState &
GetTitleBlockOccurrence(pTitleBlock, status) : returns DboTitleBlockOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pTitleBlock: DboTitleBlock *
status: DboState &
GetTitleBlockOccurrence(Name, status) : returns DboTitleBlockOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString &
status: DboState &
GetNetOccurrence(Name, status) : returns DboNetOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString &
status: DboState &

---

GetNetOccurrence(pNet, status) : returns DboNetOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pNet: DboSchematicNet *
status: DboState &
GetOffPageOccurrence(nOffPageInstanceID, status) : returns DboOffPageConnectorOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
nOffPageInstanceID: unsigned long
status: DboState &
GetOffPageOccurrence(Name, status) : returns DboOffPageConnectorOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString &
status: DboState &
CheckAndCorrectSubTreeOccurrences(pGetMapperObjects) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pGetMapperObjects: bool
GetPortOccurrence(Name, status, bBus = 0) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString const &
status: DboState &
bBus: int
GetPortOccurrence(Name, status) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString const &
status: DboState &
GetPortOccurrence(Name, Number, pDiscardedOcc, status, bBus) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:

---

Name: CString const &
Number: CString &
pDiscardedOcc: bool
status: DboState &
bBus: int
GetPortOccurrence(Name, Number, pDiscardedOcc, status, pIsBusMember,
Class : DboInstOccurrence(DboOccurrence):
bBus) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString const &
Number: CString &
pDiscardedOcc: bool
status: DboState &
pIsBusMember: bool
bBus: int
GetPortOccurrence(pPort, status) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pPort: DboSchematicPort *
status: DboState &
GetPortOccurrence(pPortInst, status) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pPortInst: DboPortInst *
status: DboState &
GetPortOccurrence(pPortInst, nPos, status) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pPortInst: DboPortInst *
nPos: int
status: DboState &
GetPortOccurrence(Name, Number, status, bBus) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:

---

Name: CString const &
Number: CString &
status: DboState &
bBus: int
GetPortOccurrence(nPinId) : returns DboPortOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
nPinId: long
GetCanonicalName(bVHDL) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int
GetCanonicalName(bVHDL, nToolID) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int
nToolID: int
GetHdlName(bVHDL) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int
GetHdlName(bVHDL, nToolID) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int
nToolID: int
GetCanonicalRefDes() : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
GetLibName(bVHDL) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int

---

GetCellName(bVHDL) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int
GetViewStr(bVHDL) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bVHDL: int
GetInstOccurrenceByName(Name, status) : returns DboInstOccurrence
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Name: CString const &
status: DboState &
sGetPathName(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetId(obj, status) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetReference(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDesignator(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetReferenceDesignator(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetName(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPartValue(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsPrimitive(obj, status) : returns PrimitiveTypeT
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsViewType(obj, status) : returns ViewTypeT
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsViewName(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsLibName(obj, status) : returns CString
Class : DboInstOccurrence(DboOccurrence):
Parameters:

---

obj: DboBaseObject *
status: DboState &
GetEffectivePropValueChoices(name, choices) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
choices: CStringList &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
HasPropertyThatExists(status) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
SetOnDiscardedPage(pOnDiscardedPage, pSchematic)
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pOnDiscardedPage: bool
pSchematic: DboSchematic *
SetOnDiscardedPage(pOnDiscardedPage)
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pOnDiscardedPage: bool
GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
bExists: int &
GetNetAndPortsValid(status) : returns int

---

Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState
GetInstance(status) : returns DboBaseObject
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
FindInstance(status) : returns DboBaseObject
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPartInstId(status) : returns unsigned long
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetVariantProp(strName, strVal) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
strName: CString const &
strVal: CString &
GetNextNewVariantProp(strName, strVal, bNewFound) : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
strName: CString &
strVal: CString &
bNewFound: int &
IsVariantPropMapEmpty() : returns int
Class : DboInstOccurrence(DboOccurrence):
Parameters:
ProcessFlatNetForPartRename()
Class : DboInstOccurrence(DboOccurrence):
Parameters:

---

IsPartInstBelongToExternalDesign() : returns bool
Class : DboInstOccurrence(DboOccurrence):
Parameters:
NewChildrenIter(status, mode = ALL) : returns DboOccurrenceChildrenIter
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewChildrenIter(status) : returns DboOccurrenceChildrenIter
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboInstOccurrence(DboOccurrence):
Parameters:
status: DboState &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
DeleteEffectiveProp(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
SetReference(reference) : returns DboState
Class : DboInstOccurrence(DboOccurrence):

---

Parameters:
reference: CString &
SetDesignator(designator) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
designator: CString &
SetPartValue(value) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
value: CString &
DeleteDBProp(name) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
name: CString const &
SetPartInstId(nPartInstId) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
nPartInstId: unsigned long
ExpandOccurrences(bMap = 0) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bMap: int
ExpandOccurrences() : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
ExpandSubTreeOccurrences() : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
Copy(pSource) : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
pSource: DboBaseObject *

---

ApplyIds() : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
AddVariantProp(strName, strVal)
Class : DboInstOccurrence(DboOccurrence):
Parameters:
strName: CString const &
strVal: CString const &
ClearVariantMap(bFlag = 1)
Class : DboInstOccurrence(DboOccurrence):
Parameters:
bFlag: int
ClearVariantMap()
Class : DboInstOccurrence(DboOccurrence):
Parameters:
UpdateNetAndPorts() : returns DboState
Class : DboInstOccurrence(DboOccurrence):
Parameters:
END class DboInstOccurrence(DboOccurrence):
DboInstOccurrence_sGetPathName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetReference(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &