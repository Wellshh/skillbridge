# Class: DboPortInstScalar(DboPortInst):

DboPortInst_sGetPinPosition(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstToDboPortInstScalar(x) : returns DboPortInstScalar
Parameters:
x: DboPortInst *
START class DboPortInstScalar(DboPortInst):
GetObjectType() : returns ObjectTypeT
Class : DboPortInstScalar(DboPortInst):
Parameters:
END class DboPortInstScalar(DboPortInst):
DboPortInstToDboPortInstBus(x) : returns DboPortInstBus
Parameters:
x: DboPortInst *
START class DboPortInstBus(DboPortInst):
GetWidth(status) : returns int
Class : DboPortInstBus(DboPortInst):
Parameters:
status: DboState &
GetMember(nPos, status) : returns DboPortInstBusMember
Class : DboPortInstBus(DboPortInst):
Parameters:
nPos: int
status: DboState &
CopyUnnamedNegroupInfo(pObj)
Class : DboPortInstBus(DboPortInst):
Parameters:
pObj: DboBaseObject *
GetObjectType() : returns ObjectTypeT

---

Class : DboPortInstBus(DboPortInst):
Parameters:
END class DboPortInstBus(DboPortInst):
DboPortInstScalarToDboPortInstBusMember(x) : returns DboPortInstBusMember
Parameters:
x: DboPortInstScalar *
START class DboPortInstBusMember(DboPortInstScalar):
GetObjectType() : returns ObjectTypeT
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
GetContainingBus(status) : returns DboPortInstBus
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetPinName(name) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString &
GetPinNumber(number) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
number: CString &
GetNet(status) : returns DboNet
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetPinType(status) : returns PinTypeT
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &

---

GetIsLong(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsClock(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsDot(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsLeftPointing(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsRightPointing(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetStartPoint(status) : returns CPoint
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetOffsetStartPoint(status) : returns CPoint
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetHotSpot(status) : returns CPoint
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &

---

GetOffsetHotSpot(status) : returns CPoint
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsVisible(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsShared(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsGlobal(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsNetStyle(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetIsNoConnect(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetPinPosition(status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
nNameID: UINT
value: CString &

---

GetEffectivePropStringValue(name, value) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString const &
value: CString &
sGetPinName(obj, status) : returns CString
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinNumber(obj, status) : returns CString
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinType(obj, status) : returns PinTypeT
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsLong(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsClock(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsDot(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetIsLeftPointing(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsRightPointing(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsVisible(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsShared(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsGlobal(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsNetStyle(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetIsNoConnect(obj, status) : returns int

---

Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartPointX(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartPointY(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotX(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotY(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinPosition(obj, status) : returns int
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
obj: DboBaseObject *
status: DboState &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &

---

DeleteUserProp(name) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString const &
SetUserPropStringValue(name, value) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString const &
value: CString const &
DeleteUserPropValue(name) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString const &
SetPinName(arg0) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
arg2: CString &
SetPinNumber(arg0) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
arg2: CString &
SetPinType(type) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
type: enum DboValue::PinTypeT
SetIsLong(bval) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
bval: int
SetIsClock(bval) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
bval: int

---

SetIsDot(bval) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
bval: int
SetIsLeftPointing(bval) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
bval: int
SetIsRightPointing(bval) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
bval: int
SetStartPoint(point) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
point: CPoint
SetHotSpot(point) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
point: CPoint
SetIsVisible(val) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
val: int
SetIsGlobal(val) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
val: int
SetIsNetStyle(val) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
val: int

---

SetIsNoConnect(val) : returns DboState
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
val: int
NewDisplayProp(status, name, location, rotation, font, color) : returns DboDisplayProp
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
name: CString &
location: CPoint
rotation: enum DboValue::RotationT
font: LOGFONT &
color: enum DboValue::ColorT
NewDisplayProp(status, pProp, bNewVersion = 0) : returns DboDisplayProp
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
bNewVersion: int
NewDisplayProp(status, pProp) : returns DboDisplayProp
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
NewUserProp(name, status) : returns DboUserProp
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString const &
status: DboState &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboPortInstBusMember(DboPortInstScalar):
Parameters:
name: CString const &
value: CString const &

---

status: DboState &
END class DboPortInstBusMember(DboPortInstScalar):
DboPortInstBusMember_sGetPinName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetPinNumber(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetPinType(obj, status) : returns PinTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsLong(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsClock(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsDot(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsLeftPointing(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsRightPointing(obj, status) : returns int

---

Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsShared(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsGlobal(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsNetStyle(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetIsNoConnect(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetStartPointX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetStartPointY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetHotSpotX(obj, status) : returns int