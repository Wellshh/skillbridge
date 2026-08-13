# Class: DboPortInst(DboBaseObject,DboInstOccMapper):

START class DboPortInst(DboBaseObject,DboInstOccMapper):
GetObjectType() : returns ObjectTypeT
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
GetOwner() : returns DboPartInst
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
GetContainingLib() : returns DboLib
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
GetDefiningPin(status) : returns DboSymbolPin
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetWire(status) : returns DboWire

---

Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetNet(status) : returns DboNet
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetDisplayPropsPermitted(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetId(status) : returns unsigned long
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetId(status, bNewVersion) : returns unsigned long
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
bNewVersion: int
GetPinName(name) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString &
GetPinNumber(number) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
number: CString &
GetPinSwapId(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &

---

GetPinType(status) : returns PinTypeT
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsLong(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsClock(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsDot(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsLeftPointing(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsRightPointing(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetStartPoint(status) : returns CPoint
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetOffsetStartPoint(status) : returns CPoint
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &

---

GetHotSpot(status) : returns CPoint
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetOffsetHotSpot(status) : returns CPoint
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsVisible(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsShared(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsNumberVisible(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsGlobal(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsNetStyle(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetIsNoConnect(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &

---

IsBundlePin(bGenerateNet = 1) : returns bool
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
bGenerateNet: int
IsBundlePin() : returns bool
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
IsBundleObject() : returns bool
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
nNameID: UINT
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
value: CString &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
GetPinPosition(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetDispPropArray() : returns DboPtrArray
Class : DboPortInst(DboBaseObject,DboInstOccMapper):

---

Parameters:
GetIsUserDefinedShape(status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetCachedPinShapePtr() : returns DboPinShapeSymbol
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
sGetPinName(obj, status) : returns CString
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinNumber(obj, status) : returns CString
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinSwapId(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinType(obj, status) : returns PinTypeT
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsLong(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetIsClock(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsDot(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsLeftPointing(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsRightPointing(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsVisible(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsShared(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsGlobal(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetIsNetStyle(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsNoConnect(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartPointX(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartPointY(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotX(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotY(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetNetName(obj, status) : returns CString

---

Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(occArr, pDesign, status)
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
sGetPinPosition(obj, status) : returns int
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
GetParentObj() : returns DboBaseObject
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
NewDisplayPropsIter(status) : returns DboDisplayPropsIter
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &

---

NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
SetPinName(name) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString &
SetPinNumber(name) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString &
DeleteUserProp(name) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
SetUserPropStringValue(name, value) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
value: CString const &
DeleteUserPropValue(name) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
SetPinType(type) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
type: enum DboValue::PinTypeT
SetIsLong(bval) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
bval: int

---

SetIsClock(bval) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
bval: int
SetIsDot(bval) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
bval: int
SetIsLeftPointing(bval) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
bval: int
SetIsRightPointing(bval) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
bval: int
SetStartPoint(point) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
point: CPoint
SetHotSpot(point) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
point: CPoint
SetIsVisible(val) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
val: int
SetIsGlobal(val) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
val: int

---

SetIsNetStyle(val) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
val: int
SetIsNoConnect(val) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
val: int
SetId(nId, bNewVersion = 0) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
nId: unsigned long
bNewVersion: int
SetId(nId) : returns DboState
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
nId: unsigned long
SetCachedPinShapePtr(pPinShape)
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
pPinShape: DboPinShapeSymbol *
NewDisplayProp(status, name, location, rotation, font, color) : returns DboDisplayProp
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
name: CString &
location: CPoint
rotation: enum DboValue::RotationT
font: LOGFONT &
color: enum DboValue::ColorT
NewDisplayProp(status, pProp, bNewVersion = 0) : returns DboDisplayProp
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:

---

status: DboState &
pProp: DboDisplayProp const *
bNewVersion: int
NewDisplayProp(status, pProp) : returns DboDisplayProp
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
NewUserProp(name, status) : returns DboUserProp
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
status: DboState &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboPortInst(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
value: CString const &
status: DboState &
END class DboPortInst(DboBaseObject,DboInstOccMapper):
DboPortInst_sGetPinName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetPinNumber(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetPinSwapId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &