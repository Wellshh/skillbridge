# Class: DboGraphicSymbolVectorInst(DboGraphicInstance):

Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicOleEmbedInst_sGetRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicOleEmbedInst_sGetBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicSymbolVectorInst(x) : returns DboGraphicSymbolVectorInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicSymbolVectorInst(DboGraphicInstance):
GetDboSymbolVector() : returns DboSymbolVector
Class : DboGraphicSymbolVectorInst(DboGraphicInstance):
Parameters:
END class DboGraphicSymbolVectorInst(DboGraphicInstance):
DboEffectivePropsIterToDboGraphicInstEffectivePropsIter(x) : returns
DboGraphicInstEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboGraphicInstEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboGraphicInstEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &

---

NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboGraphicInstEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboGraphicInstEffectivePropsIter(DboEffectivePropsIter):
DboDisplayPropsIterToDboInstanceDisplayPropsIter(x) : returns DboInstanceDisplayPropsIter
Parameters:
x: DboDisplayPropsIter *
START class DboInstanceDisplayPropsIter(DboDisplayPropsIter):
Next(status) : returns DboBaseObject
Class : DboInstanceDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
NextProp(status) : returns DboDisplayProp
Class : DboInstanceDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboInstanceDisplayPropsIter(DboDisplayPropsIter):
Parameters:
pObject: DboDisplayProp *&
END class DboInstanceDisplayPropsIter(DboDisplayPropsIter):
DboGraphicObjectToDboSymbol(x) : returns DboSymbol
Parameters:
x: DboGraphicObject *
START class DboSymbol(DboGraphicObject):

---

PinsAllowed(status) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
GetPinCount(status, mode = TOP) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
GetPinCount(status) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
GetSymbolPin(name, status) : returns DboSymbolPin
Class : DboSymbol(DboGraphicObject):
Parameters:
name: CString &
status: DboState &
GetSymbolPin(position, status) : returns DboSymbolPin
Class : DboSymbol(DboGraphicObject):
Parameters:
position: unsigned int
status: DboState &
GetSymbolPin(location, status) : returns DboSymbolPin
Class : DboSymbol(DboGraphicObject):
Parameters:
location: CPoint
status: DboState &
GetDisplayPropsPermitted(status) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &

---

GetSize(status) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
GetPinPosition(pPin, status) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
pPin: DboSymbolPin *
status: DboState &
IsEquivalent(pObj) : returns int
Class : DboSymbol(DboGraphicObject):
Parameters:
pObj: DboBaseObject *
GetSemanticString(str)
Class : DboSymbol(DboGraphicObject):
Parameters:
str: CString &
GetDispPropArray() : returns DboPtrArray
Class : DboSymbol(DboGraphicObject):
Parameters:
MarkModified() : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
NewPinsIter(status, mode = ALL) : returns DboSymbolPinsIter
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPinsIter(status) : returns DboSymbolPinsIter
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &

---

NewDisplayPropsIter(status) : returns DboDisplayPropsIter
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
Clear() : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
DeleteSymbolPin(nPos) : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
nPos: int
DeleteSymbolPinAtPosition(nPos) : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
nPos: int
RemoveSymbolPinFromPosition(nPos) : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
nPos: int
RemoveSymbolPins() : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
NewSymbolPinScalar(status, name, type, start, hotPoint, visible = 1, position = -1) : returns
DboSymbolPinScalar
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
position: int

---

NewSymbolPinScalar(status, name, type, start, hotPoint, visible = 1) : returns DboSymbolPinScalar
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
NewSymbolPinScalar(status, name, type, start, hotPoint) : returns DboSymbolPinScalar
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
NewSymbolPinScalar(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboSymbol(DboGraphicObject):
visible = 1, position = -1) : returns DboSymbolPinScalar
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
visible: int
position: int

---

NewSymbolPinScalar(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboSymbol(DboGraphicObject):
visible = 1) : returns DboSymbolPinScalar
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
visible: int
NewSymbolPinScalar(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle) : returns DboSymbolPinScalar
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
NewDisplayProp(status, name, location, rotation, font, color) : returns DboDisplayProp
Class : DboSymbol(DboGraphicObject):
Parameters:

---

status: DboState &
name: CString &
location: CPoint
rotation: enum DboValue::RotationT
font: LOGFONT &
color: enum DboValue::ColorT
NewDisplayProp(status, pProp) : returns DboDisplayProp
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
NewSymbolPinBus(status, name, type, start, hotPoint, visible = 1, position = -1,
Class : DboSymbol(DboGraphicObject):
strBOwner = "") : returns DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
position: int
strBOwner: CString
NewSymbolPinBus(status, name, type, start, hotPoint, visible = 1, position = -1) : returns
DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
position: int
NewSymbolPinBus(status, name, type, start, hotPoint, visible = 1) : returns DboSymbolPinBus

---

Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
NewSymbolPinBus(status, name, type, start, hotPoint) : returns DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
NewSymbolPinBus(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboSymbol(DboGraphicObject):
visible = 1, position = -1, strBOwner = "") : returns DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
visible: int
position: int
strBOwner: CString

---

NewSymbolPinBus(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboSymbol(DboGraphicObject):
visible = 1, position = -1) : returns DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
visible: int
position: int
NewSymbolPinBus(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboSymbol(DboGraphicObject):
visible = 1) : returns DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
visible: int

---

NewSymbolPinBus(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboSymbol(DboGraphicObject):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle) : returns DboSymbolPinBus
Class : DboSymbol(DboGraphicObject):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
IsLong: int
IsClock: int
IsDot: int
IsLeftPointing: int
IsRightPointing: int
IsNetStyle: int
DeleteDisplayProp(pProp) : returns DboState
Class : DboSymbol(DboGraphicObject):
Parameters:
pProp: DboDisplayProp *
END class DboSymbol(DboGraphicObject):
START class TBaseDboSymbolPinsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSymbolPinsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSymbolPinsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSymbolPinsIter(IterDefs):
Parameters:
status: DboState &

---

SetFlag(flag, status)
Class : TBaseDboSymbolPinsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSymbolPinsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSymbolPinsIter(IterDefs):
START class DboSymbolPinsIter(TBaseDboSymbolPinsIter):
Next(status) : returns DboBaseObject
Class : DboSymbolPinsIter(TBaseDboSymbolPinsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSymbolPinsIter(TBaseDboSymbolPinsIter):
Parameters:
pObject: DboSymbolPin *&
NextPin(status) : returns DboSymbolPin
Class : DboSymbolPinsIter(TBaseDboSymbolPinsIter):
Parameters:
status: DboState &
END class DboSymbolPinsIter(TBaseDboSymbolPinsIter):
DboDisplayPropsIterToDboSymbolDisplayPropsIter(x) : returns DboSymbolDisplayPropsIter
Parameters:
x: DboDisplayPropsIter *
START class DboSymbolDisplayPropsIter(DboDisplayPropsIter):
Next(status) : returns DboBaseObject
Class : DboSymbolDisplayPropsIter(DboDisplayPropsIter):

---

Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboSymbolDisplayPropsIter(DboDisplayPropsIter):
Parameters:
pObject: DboDisplayProp *&
NextProp(status) : returns DboDisplayProp
Class : DboSymbolDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
END class DboSymbolDisplayPropsIter(DboDisplayPropsIter):
DboViewToDboSchematic(x) : returns DboSchematic
Parameters:
x: DboView *
DboInstOccMapperToDboSchematic(x) : returns DboSchematic
Parameters:
x: DboInstOccMapper *
START class DboSchematic(DboView,DboInstOccMapper):
GetObjectType() : returns ObjectTypeT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
GetOptimizerTemplate() : returns DboPlacedInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
IsOptimizerUseCurrentValue() : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
GetOpStartWithCurrenV(status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:

---

status: DboState &
IsOptimizerTemplateExist() : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
GetOptFileName() : returns CString
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
ReadAllPages() : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
IsModified(status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
IsOccsModified() : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
GetNextReference(partName, sourcePkgName, strReferencePrefix, suffixStr,
Class : DboSchematic(DboView,DboInstOccMapper):
wPart, bIncrementNext = 1) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
partName: CString
sourcePkgName: CString
strReferencePrefix: CString &
suffixStr: CString &
wPart: int
bIncrementNext: int
GetNextReference(partName, sourcePkgName, strReferencePrefix, suffixStr,
Class : DboSchematic(DboView,DboInstOccMapper):
wPart) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:

---

partName: CString
sourcePkgName: CString
strReferencePrefix: CString &
suffixStr: CString &
wPart: int
GetNextReference(strReferencePrefix, bIncrementNext = 1) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
strReferencePrefix: CString &
bIncrementNext: int
GetNextReference(strReferencePrefix) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
strReferencePrefix: CString &
GetNextReferenceEx(partName, sourcePkgName, strReferencePrefix, suffixStr,
Class : DboSchematic(DboView,DboInstOccMapper):
wPart, bIncrementNext = 1) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
partName: CString
sourcePkgName: CString
strReferencePrefix: CString &
suffixStr: CString &
wPart: int
bIncrementNext: int
GetNextReferenceEx(partName, sourcePkgName, strReferencePrefix, suffixStr,
Class : DboSchematic(DboView,DboInstOccMapper):
wPart) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
partName: CString
sourcePkgName: CString
strReferencePrefix: CString &
suffixStr: CString &
wPart: int

---

GetNextReferenceEx(strReferencePrefix, bIncrementNext = 1) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
strReferencePrefix: CString &
bIncrementNext: int
GetNextReferenceEx(strReferencePrefix) : returns UINT
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
strReferencePrefix: CString &
CanAssignRefDes(pPartInst, pRef, pDes) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPartInst: DboPartInst *
pRef: CString
pDes: CString
GetPage(name, status) : returns DboPage
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetPage(position, status) : returns DboPage
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
position: int
status: DboState &
GetPageFromID(nPageID, status) : returns DboPage
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nPageID: UINT
status: DboState &
GetPageCount(status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &

---

GetPageNumber(name, status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
PageExists(name, status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
IsPageInMemory(name, status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
IsPagePersistent(pPage, status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
status: DboState &
IsPagePersistent(name, status) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetNet(name, status) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetNet(pWire, status) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:

---

pWire: DboWire *
status: DboState &
GetNet(pNet, status) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pNet: DboNet *
status: DboState &
GetNet(pPortInst, status) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPortInst: DboPortInst *
status: DboState &
GetNet(nId, status) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nId: unsigned long
status: DboState &
GetDeletedNet(nId, status) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nId: unsigned long
status: DboState &
GetTitleBlock(nId, status) : returns DboTitleBlock
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nId: unsigned long
status: DboState &
GetPortIgnoreWidth(Name, status) : returns DboSchematicPort
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
Name: CString &
status: DboState &
GetPort(name, status) : returns DboSchematicPort

---

Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetGlobal(name, status) : returns DboSchematicSymbolInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetOffPageConnector(name, status) : returns DboSchematicSymbolInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetOffPageConnectorForOcc(nID) : returns DboOffPageConnector
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nID: unsigned long
GetDefaultPageName() : returns CString
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
IsPageModified(pPage) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
GetOccUndoStack(pDesign, pDboPage, occId, bAutoCreate = 1) : returns DboOccurrenceUndoStack
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pDesign: DboDesign *
pDboPage: DboPage *
occId: unsigned long
bAutoCreate: int
GetOccUndoStack(pDesign, pDboPage, occId) : returns DboOccurrenceUndoStack

---

Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pDesign: DboDesign *
pDboPage: DboPage *
occId: unsigned long
GetOptimizerParameter(name, st) : returns DboOptimizerParameter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
st: DboState &
GetUserStorage(name, status) : returns IStorage
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
status: DboState &
GetOpenReferringDesigns(designs, status)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
designs: DboDesignList &
status: DboState &
GetRegisteredObject(nID) : returns DboBaseObject
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nID: unsigned long
GetUnnamedNetGroupOwnerObject(pUnnamedBundleOwner) : returns DboDrawnInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pUnnamedBundleOwner: CString
IsExpanded() : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
GetId() : returns unsigned long
Class : DboSchematic(DboView,DboInstOccMapper):

---

Parameters:
GetPartInst(nId, status) : returns DboPartInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nId: unsigned long
status: DboState &
GetPartInst(id) : returns DboPartInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
id: unsigned long
GetSchematicID() : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
GetSchematicAtID(nSchematicID) : returns DboSchematic
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
nSchematicID: int
sGetName(obj, status) : returns CString
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
GetNextDeviceAndPartToBePlaced(aPackage, aPartValue, aPackageRef, aDeviceDesignator,
Class : DboSchematic(DboView,DboInstOccMapper):
aIsNormal, aDevice, aLibPart) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
aPackage: DboPackage *
aPartValue: CString const &
aPackageRef: CString const &
aDeviceDesignator: CString const
aIsNormal: int
aDevice: DboDevice *&
aLibPart: DboLibPart *&

---

GetUnNamedBundleList(UnNamedBundleList) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
UnNamedBundleList: CStringList &
UpdateUnnamedNetSymbols(bOwnerName, bEntryPinName, newBOwner, pInitatingPage)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
bOwnerName: CString
bEntryPinName: CString
newBOwner: CString
pInitatingPage: DboPage *
MarkModified() : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
MarkModified(pPage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
ClearModified(pPage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
NewPagesIter(status) : returns DboSchematicPagesIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
NewPageNamesIter(status) : returns DboSchematicPageNamesIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
NewInstsIter(status) : returns DboSchematicInstsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:

---

status: DboState &
NewNetsIter(status, mode = SCALARS) : returns DboSchematicNetsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewNetsIter(status) : returns DboSchematicNetsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
NewPortsIter(status, mode = TOP) : returns DboSchematicPortsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPortsIter(status) : returns DboSchematicPortsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
NewGlobalsIter(status) : returns DboSchematicGlobalsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
NewOffPageConnectorsIter(status, mode = TOP) : returns DboSchematicOffPageConnectorsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewOffPageConnectorsIter(status) : returns DboSchematicOffPageConnectorsIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &

---

NewChangedPagesIter(status) : returns DboSchematicChangedPagesIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
NewOccUndoStackEntryIter(pDesign, pDboPage, occId, mode = DboOccurrenceUndoStack::ALL) :
returns DboOccUndoStackEntryIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pDesign: DboDesign *
pDboPage: DboPage *
occId: unsigned long
mode: DboOccurrenceUndoStack::StackEntryType
NewOccUndoStackEntryIter(pDesign, pDboPage, occId) : returns DboOccUndoStackEntryIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pDesign: DboDesign *
pDboPage: DboPage *
occId: unsigned long
NewOptimizerParametersIter(st) : returns DboSchematicOptimizerParametersIter
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
st: DboState &
BuildIDMap() : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
SetOpStartWithCurrenV(bVal) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
bVal: int
DeleteAllOptimizerParameter()
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
RestoreOptimizerParameter()

---

Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
SetOccsModified(isModified = 1)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
isModified: int
SetOccsModified()
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
SetNextReference(strReferencePrefix, nNextReference)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
strReferencePrefix: CString &
nNextReference: UINT
ClearNextReferences()
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
UpdateNextReference(strReference)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
strReference: CString &
DeleteOptimizerParameter(name) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
RemoveOptimizerParameter(name) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
name: CString &
Expand() : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:

---

FilterSchematicNetsForPage(pPage, pReferredSchNetsMap, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pDboNetScalars = None, pDboNetBuses = None)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pProcessEditMapOnly: bool
pDboNetScalars: DboPtrArray *
pDboNetBuses: DboPtrArray *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
FilterSchematicNetsForPage(pPage, pReferredSchNetsMap, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pDboNetScalars = None)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pProcessEditMapOnly: bool
pDboNetScalars: DboPtrArray *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
FilterSchematicNetsForPage(pPage, pReferredSchNetsMap, pProcessEditMapOnly = 0)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pProcessEditMapOnly: bool
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
FilterSchematicNetsForPage(pPage, pReferredSchNetsMap)
Class : DboSchematic(DboView,DboInstOccMapper):

---

Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pDeletedSourcesMap = None, pNewScalarSourcesMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewBusSourcesMap = None, pAvailableOccurrencesMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pDeletedOccurrencesMap = None) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool
pNewDboNetsMap: DboMapPtrToPtr *
pDeletedSourcesMap: DboMapPtrToPtr *
pNewScalarSourcesMap: DboMapPtrToPtr *
pNewBusSourcesMap: DboMapPtrToPtr *
pAvailableOccurrencesMap: objectMap *
pDeletedOccurrencesMap: objectMap *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pDeletedSourcesMap = None, pNewScalarSourcesMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewBusSourcesMap = None, pAvailableOccurrencesMap = None) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):

---

Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool
pNewDboNetsMap: DboMapPtrToPtr *
pDeletedSourcesMap: DboMapPtrToPtr *
pNewScalarSourcesMap: DboMapPtrToPtr *
pNewBusSourcesMap: DboMapPtrToPtr *
pAvailableOccurrencesMap: objectMap *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pDeletedSourcesMap = None, pNewScalarSourcesMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewBusSourcesMap = None) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool
pNewDboNetsMap: DboMapPtrToPtr *
pDeletedSourcesMap: DboMapPtrToPtr *
pNewScalarSourcesMap: DboMapPtrToPtr *
pNewBusSourcesMap: DboMapPtrToPtr *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pDeletedSourcesMap = None, pNewScalarSourcesMap = None) : returns DboState

---

Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool
pNewDboNetsMap: DboMapPtrToPtr *
pDeletedSourcesMap: DboMapPtrToPtr *
pNewScalarSourcesMap: DboMapPtrToPtr *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap = None,
Class : DboSchematic(DboView,DboInstOccMapper):
pDeletedSourcesMap = None) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool
pNewDboNetsMap: DboMapPtrToPtr *
pDeletedSourcesMap: DboMapPtrToPtr *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0,
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap = None) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool

---

pNewDboNetsMap: DboMapPtrToPtr *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True, pProcessEditMapOnly = 0) :
returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pProcessEditMapOnly: bool
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap, pRecreatePage = True) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pRecreatePage: bool
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
ExpandMinimal(pPage, pReferredSchNetsMap) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
DoActualSchematicExpansion(pPage, pReferredSchNetsMap, pNewDboNetsMap,
pDeletedSourcesMap,
Class : DboSchematic(DboView,DboInstOccMapper):
pAvailableSourcesMap, pAvailableOccurrencesMap,
Class : DboSchematic(DboView,DboInstOccMapper):

---

pDeletedOccurrencesMap, pRecreatePage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pNewDboNetsMap: DboMapPtrToPtr *
pDeletedSourcesMap: DboMapPtrToPtr *
pAvailableSourcesMap: DboMapPtrToPtr *
pAvailableOccurrencesMap: objectMap *
pDeletedOccurrencesMap: objectMap *
pRecreatePage: bool
pReferredSchNetsMap: CMap< CString,LPCSTR,unsigned long,unsigned long > & value
Class : DboSchematic(DboView,DboInstOccMapper):
GetLowestPageNumberFromDboNets(pSchNet) : returns int
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pSchNet: DboSchematicNet *
ResolveBaseNameConflict(pSchNet1, pSchNet2) : returns DboSchematicNet
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pSchNet1: DboSchematicNet *
pSchNet2: DboSchematicNet *
MarkSchematicNetForDeletion(pSchematicNet)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pSchematicNet: DboSchematicNet *
CreateSchNetAndContainerMapping(pObject, pSchNetMapping, pSymInst = None, pOldName =
None)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pObject: DboBaseObject *
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pSymInst: DboSchematicSymbolInst *

---

pOldName: LPCSTR
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
CreateSchNetAndContainerMapping(pObject, pSchNetMapping, pSymInst = None)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pObject: DboBaseObject *
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pSymInst: DboSchematicSymbolInst *
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
CreateSchNetAndContainerMapping(pObject, pSchNetMapping)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pObject: DboBaseObject *
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
CreateSchNetAndContainerMapping(pBusSource, pMemberName, pSchNetMapping)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pBusSource: DboBaseObject *
pMemberName: CString
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):
pSchNetMapping: CMap< DboSchematicNet *,DboSchematicNet *,containerMap *,containerMap
* > & value
Class : DboSchematic(DboView,DboInstOccMapper):

---

CheckSchematicSymbolInstContainersAndUpdateConnectivity(pPage, pNewDboNetsMap,
pDeletedSourcesMap, pAvailableSourcesMap)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pNewDboNetsMap: DboMapPtrToPtr *&
pDeletedSourcesMap: DboMapPtrToPtr *
pAvailableSourcesMap: DboMapPtrToPtr *
RemoveSchematicNetAndRebuildFromPageNets(lSchNet, pNewDboNetsMap)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
lSchNet: DboSchematicNet *
pNewDboNetsMap: DboMapPtrToPtr *
GetObjectContainer(pObject) : returns DboSchematicSymbolInst
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pObject: DboBaseObject *
Rename(pObj, newName) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pObj: DboPage *
newName: CString &
NewPage(status, name, pageNumber = -1) : returns DboPage
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
name: CString &
pageNumber: int
NewPage(status, name) : returns DboPage
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
status: DboState &
name: CString &
SavePage(pPage, bVal = 0) : returns DboState

---

Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
bVal: int
SavePage(pPage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
DeletePage(pPage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
sDeleteTempShadowPage(pPage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboShadowPage *
UpdateFlatNetsOfAllInstantiatingDesigns()
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
RemovePage(pPage) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
ReleaseCollectedPageIDs(pPageIDList)
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPageIDList: std::vector< unsigned long > &
SetPageNumber(pPage, pageNumber) : returns DboState
Class : DboSchematic(DboView,DboInstOccMapper):
Parameters:
pPage: DboPage *
pageNumber: int

---

END class DboSchematic(DboView,DboInstOccMapper):
DboSchematic_GetSchematicAtID(nSchematicID) : returns DboSchematic
Parameters:
nSchematicID: int
DboSchematic_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboSchematic_sDeleteTempShadowPage(pPage) : returns DboState
Parameters:
pPage: DboShadowPage *
START class TBaseDboSchematicPagesIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicPagesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicPagesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicPagesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicPagesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicPagesIter(IterDefs):
Parameters:
status: DboState &

---

END class TBaseDboSchematicPagesIter(IterDefs):
START class DboSchematicPagesIter(TBaseDboSchematicPagesIter):
NextPage(status) : returns DboPage
Class : DboSchematicPagesIter(TBaseDboSchematicPagesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicPagesIter(TBaseDboSchematicPagesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicPagesIter(TBaseDboSchematicPagesIter):
Parameters:
pObject: DboPage *&
END class DboSchematicPagesIter(TBaseDboSchematicPagesIter):
START class DboSchematicPageNamesIter
NextName(status) : returns char
Class : DboSchematicPageNamesIter
Parameters:
status: DboState &
END class DboSchematicPageNamesIter
START class TBaseDboSchematicNetsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetsIter(IterDefs):
Parameters:

---

Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetsIter(IterDefs):
START class DboSchematicNetsIter(TBaseDboSchematicNetsIter):
NextNet(status) : returns DboSchematicNet
Class : DboSchematicNetsIter(TBaseDboSchematicNetsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetsIter(TBaseDboSchematicNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetsIter(TBaseDboSchematicNetsIter):
Parameters:
pObject: DboSchematicNet *&
END class DboSchematicNetsIter(TBaseDboSchematicNetsIter):
START class TBaseDboSchematicInstsIter(IterDefs):

---

GetType() : returns int
Class : TBaseDboSchematicInstsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicInstsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicInstsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicInstsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicInstsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicInstsIter(IterDefs):
START class DboSchematicInstsIter(TBaseDboSchematicInstsIter):
NextInst(status) : returns DboPartInst
Class : DboSchematicInstsIter(TBaseDboSchematicInstsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicInstsIter(TBaseDboSchematicInstsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicInstsIter(TBaseDboSchematicInstsIter):

---

Parameters:
pObject: DboPartInst *&
END class DboSchematicInstsIter(TBaseDboSchematicInstsIter):
START class TBaseDboSchematicPortsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicPortsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicPortsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicPortsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicPortsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicPortsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicPortsIter(IterDefs):
START class DboSchematicPortsIter(TBaseDboSchematicPortsIter):
NextPort(status) : returns DboSchematicPort
Class : DboSchematicPortsIter(TBaseDboSchematicPortsIter):
Parameters:
status: DboState &

---

Next(status) : returns DboBaseObject
Class : DboSchematicPortsIter(TBaseDboSchematicPortsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicPortsIter(TBaseDboSchematicPortsIter):
Parameters:
pObject: DboSchematicPort *&
END class DboSchematicPortsIter(TBaseDboSchematicPortsIter):
START class TBaseDboSchematicGlobalsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicGlobalsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicGlobalsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicGlobalsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicGlobalsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicGlobalsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicGlobalsIter(IterDefs):