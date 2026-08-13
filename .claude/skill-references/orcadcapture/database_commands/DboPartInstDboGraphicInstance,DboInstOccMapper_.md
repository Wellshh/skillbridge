# Class: DboPartInst(DboGraphicInstance,DboInstOccMapper):

START class DboPartInst(DboGraphicInstance,DboInstOccMapper):
GetReference(Ref) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
Ref: CString &
GetReferenceDesignator(RefDes) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
RefDes: CString &

---

GetPartValue(value) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
value: CString &
GetContents(status) : returns DboView
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetContentsViewName(name) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
GetContentsLibName(name) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
GetContentsViewType(status) : returns ViewTypeT
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetIsPrimitive(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetDefiningPart(status) : returns DboLibPart
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetIsPrimitiveProp(status) : returns PrimitiveTypeT
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &

---

IsPrimitive(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
IsPSpiceOnly(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
IsOptimizerTemplate(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetPinNumbersAreVisible(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetPinNamesAreVisible(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetPowerPinsAreVisible(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetPinNamesAreRotated(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
sGetPinCount(obj, status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetReference(obj, status) : returns CString
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPartValue(obj, status) : returns CString
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsPrimitive(obj, status) : returns PrimitiveTypeT
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsViewType(obj, status) : returns ViewTypeT
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsViewName(obj, status) : returns CString
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsLibName(obj, status) : returns CString
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPowerPinsAreVisible(obj, status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:

---

obj: DboBaseObject *
status: DboState &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetPin(nPosition, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
nPosition: int
status: DboState &
GetPinOrderedByLocation(nPosition, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
nPosition: int
status: DboState &
GetPinByHotSpot(hotSpot, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
hotSpot: CPoint
status: DboState &
GetPinByID(pPinID) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
pPinID: unsigned long
GetPinByPinNumber(PinNumber, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
PinNumber: CString &
status: DboState &
GetPinByPinName(PinName, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:

---

PinName: CString &
status: DboState &
GetPinByBasePinName(PinBaseName, nType, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
PinBaseName: CString &
nType: enum DboValue::PinTypeT
status: DboState &
FindPinByPinName(PinName, status) : returns DboPortInst
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
PinName: CString &
status: DboState &
CountPinsWithName(PinName) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
PinName: CString &
HasMultiplePinsWithName(PinName) : returns bool
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
PinName: CString &
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(occArr, pDesign, status)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &

---

GetVariantProp(strName, strVal) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
strName: CString const &
strVal: CString &
GetNextNewVariantProp(strName, strVal, bNewFound) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
strName: CString &
strVal: CString &
bNewFound: int &
IsVariantPropMapEmpty() : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
IsBoundingBoxDirty() : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
GetPinCount(status) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
HasBundleOwner(string = None) : returns bool
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
string: CString *
HasBundleOwner() : returns bool
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
GetBundleEntryPinName(entryPunName) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
entryPunName: CString &

---

IsExternalDesignPart() : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
NewPinsIter(status, mode = ALL, bReturnShared = 0) : returns DboPartInstPinsIter
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
bReturnShared: int
NewPinsIter(status, mode = ALL) : returns DboPartInstPinsIter
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPinsIter(status) : returns DboPartInstPinsIter
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
SetReference(name) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString const &
SetPartValue(name) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString const &
SetIsPrimitiveProp(prim) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
prim: enum DboValue::PrimitiveTypeT
SetContentsViewType(type, bNewVersion = 0) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):

---

Parameters:
type: enum DboValue::ViewTypeT
bNewVersion: int
SetContentsViewType(type) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
type: enum DboValue::ViewTypeT
SetContentsViewName(viewName, bNewVersion = 0) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
viewName: CString const &
bNewVersion: int
SetContentsViewName(viewName) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
viewName: CString const &
SetContentsLibName(libName, bNewVersion = 0) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
libName: CString const &
bNewVersion: int
SetContentsLibName(libName) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
libName: CString const &
SetPowerPinsAreVisible(bVal) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
bVal: int
SetId(nId, bNewVersion = 0) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
nId: unsigned long

---

bNewVersion: int
SetId(nId) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
nId: unsigned long
SetLocation(location) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
location: CPoint
Move(offset) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
offset: CPoint
SetRotation(rotation) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
rotation: enum DboValue::RotationT
SetMirror(mirror) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
mirror: int
SetCurrent(bVal)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
bVal: int
SetContentViewTypeWithoutChangingOccurrences(pType) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
pType: enum DboValue::ViewTypeT
SetContentsViewNameWithoutChangingOccurrences(newName, isForSchematicRename) : returns
DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):

---

Parameters:
newName: CString const &
isForSchematicRename: bool
SetName(newName) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
newName: CString &
Disconnect() : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
Connect() : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
SetBoundingBoxDirty(bSetting)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
bSetting: int
SetOccsModified(bVal)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
bVal: int
AddVariantProp(strName, strVal)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
strName: CString const &
strVal: CString const &
ClearVariantMap(bFlag = 1)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
bFlag: int
ClearVariantMap()
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):

---

Parameters:
PositionDisplayProp(pPage, pProp) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
pPage: DboPage *
pProp: DboDisplayProp *
ResetAllDisplayPropertiesFontToDefault()
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
PositionAllDisplayProp(pPage, pInst) : returns int
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
pPage: DboPage *
pInst: DboPartInst *
ProcessRefDesModify()
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
ProcessRefDesDelete()
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
SetOccAutoRefMode(pMode)
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
pMode: enum DboPartInst::OCC_AUTOREF_MODE
GetOccAutoRefMode() : returns OCC_AUTOREF_MODE
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
END class DboPartInst(DboGraphicInstance,DboInstOccMapper):
DboPartInst_sGetPinCount(obj, status) : returns int
Parameters:
obj: DboBaseObject *