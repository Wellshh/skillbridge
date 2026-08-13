# Class: DboPackageDevicesIter(TBaseDboPackageDevicesIter):

START class DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Next(status) : returns DboBaseObject
Class : DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Parameters:
pObject: DboDevice *&
NextDevice(status) : returns DboDevice
Class : DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Parameters:
status: DboState &
END class DboPackageDevicesIter(TBaseDboPackageDevicesIter):
START class TBaseDboPackagePartsIter(IterDefs):

---

GetType() : returns int
Class : TBaseDboPackagePartsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPackagePartsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPackagePartsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPackagePartsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPackagePartsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPackagePartsIter(IterDefs):
START class DboPackagePartsIter(TBaseDboLibPartsIter):
Next(status) : returns DboBaseObject
Class : DboPackagePartsIter(TBaseDboLibPartsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPackagePartsIter(TBaseDboLibPartsIter):
Parameters:
pObject: DboLibPart *&
NextPart(status) : returns DboLibPart

---

Class : DboPackagePartsIter(TBaseDboLibPartsIter):
Parameters:
status: DboState &
END class DboPackagePartsIter(TBaseDboLibPartsIter):
START class DboPackageAliasesIter
Next(nxt) : returns DboState
Class : DboPackageAliasesIter
Parameters:
nxt: CString &
NextAlias(nxt) : returns DboState
Class : DboPackageAliasesIter
Parameters:
nxt: CString &
END class DboPackageAliasesIter
DboBaseObjectToDboSymbolPin(x) : returns DboSymbolPin
Parameters:
x: DboBaseObject *
START class DboSymbolPin(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboSymbolPin(DboBaseObject):
Parameters:
GetOwner() : returns DboSymbol
Class : DboSymbolPin(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboSymbolPin(DboBaseObject):
Parameters:
GetPinName(name) : returns DboState
Class : DboSymbolPin(DboBaseObject):

---

Parameters:
name: CString &
GetPinType(status) : returns PinTypeT
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsLong(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsClock(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsDot(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsLeftPointing(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsRightPointing(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsNetStyle(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsNoConnect(status) : returns int
Class : DboSymbolPin(DboBaseObject):

---

Parameters:
status: DboState &
GetStartPoint(status) : returns CPoint
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetHotSpot(status) : returns CPoint
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsVisible(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsGlobal(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsNumberVisible(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetIsUserDefinedShape(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetDisplayPropsPermitted(status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
GetPinPosition(status) : returns int
Class : DboSymbolPin(DboBaseObject):

---

Parameters:
status: DboState &
GetName(name) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
name: CString &
GetDispPropArray() : returns DboPtrArray
Class : DboSymbolPin(DboBaseObject):
Parameters:
sGetPinName(obj, status) : returns CString
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinType(obj, status) : returns PinTypeT
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsLong(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsClock(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsDot(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *

---

status: DboState &
sGetIsLeftPointing(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsRightPointing(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsNetStyle(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsNoConnect(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsVisible(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsGlobal(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsNumberVisible(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):

---

Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartPointX(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartPointY(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotX(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotY(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinPosition(obj, status) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
IsEquivalent(pObj) : returns int
Class : DboSymbolPin(DboBaseObject):
Parameters:
pObj: DboBaseObject *
GetSemanticString(str)

---

Class : DboSymbolPin(DboBaseObject):
Parameters:
str: CString &
NewDisplayPropsIter(status) : returns DboDisplayPropsIter
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
SetPinName(name) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
name: CString &
SetName(name) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
name: CString &
SetPinType(type) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
type: enum DboValue::PinTypeT
SetIsLong(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetIsClock(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetIsDot(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetIsLeftPointing(bval) : returns DboState

---

Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetIsRightPointing(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetIsNetStyle(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetIsNoConnect(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
SetStartPoint(point) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
point: CPoint
SetHotSpot(point) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
point: CPoint
SetIsVisible(val) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
val: int
SetIsGlobal(val) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
val: int
SetIsNumberVisible(val) : returns DboState

---

Class : DboSymbolPin(DboBaseObject):
Parameters:
val: int
SetPinPosition(nPos) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
nPos: int
SetIsUserDefinedShape(bval) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
bval: int
InsertAtPinPosition(nPos) : returns DboState
Class : DboSymbolPin(DboBaseObject):
Parameters:
nPos: int
NewDisplayProp(status, name, location, rotation, font, color) : returns DboDisplayProp
Class : DboSymbolPin(DboBaseObject):
Parameters:
status: DboState &
name: CString &
location: CPoint
rotation: enum DboValue::RotationT
font: LOGFONT &
color: enum DboValue::ColorT
GetParentObj() : returns DboBaseObject
Class : DboSymbolPin(DboBaseObject):
Parameters:
END class DboSymbolPin(DboBaseObject):
DboSymbolPin_sGetPinName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboSymbolPin_sGetPinType(obj, status) : returns PinTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsLong(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsClock(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsDot(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsLeftPointing(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsRightPointing(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsNetStyle(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsNoConnect(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboSymbolPin_sGetIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsGlobal(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetIsNumberVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetStartPointX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetStartPointY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetHotSpotX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetHotSpotY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPin_sGetPinPosition(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &