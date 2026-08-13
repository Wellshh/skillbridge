# Class: DboDrawnInst(DboPartInst):

DboPlacedInst_sGetPCBFootprint(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInstToDboDrawnInst(x) : returns DboDrawnInst
Parameters:
x: DboPartInst *
START class DboDrawnInst(DboPartInst):
GetDefiningSymbol(status) : returns DboLibPart
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboDrawnInst(DboPartInst):
Parameters:
SwapPortInstForBundle(status, newPinVec)
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
newPinVec: std::vector< std::string > &
SetBoundingBox(box) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
box: CRect
SetReference(name, bNewVersion = 0) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
name: CString const &
bNewVersion: int
SetReference(name) : returns DboState
Class : DboDrawnInst(DboPartInst):

---

Parameters:
name: CString const &
NewPortInstScalar(status, name, type, start, hotPoint, visible = 1, bundleOwner = "") : returns
DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
bundleOwner: CString
NewPortInstScalar(status, name, type, start, hotPoint, visible = 1) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
NewPortInstScalar(status, name, type, start, hotPoint) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
NewPortInstScalar(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboDrawnInst(DboPartInst):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboDrawnInst(DboPartInst):
visible = 1) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):

---

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
NewPortInstScalar(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboDrawnInst(DboPartInst):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
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
DeletePortInst(portInst, bNewVersion = 0) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
portInst: DboPortInst *
bNewVersion: int
DeletePortInst(portInst) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:

---

portInst: DboPortInst *
NewPortInstBus(status, name, type, start, hotPoint, visible = 1, bundleOwner = "") : returns
DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
bundleOwner: CString
NewPortInstBus(status, name, type, start, hotPoint, visible = 1) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
NewPortInstBus(status, name, type, start, hotPoint) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
NewPortInstBus(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboDrawnInst(DboPartInst):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle,
Class : DboDrawnInst(DboPartInst):
visible = 1) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:

---

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
NewPortInstBus(status, name, type, start, hotPoint, IsLong, IsClock,
Class : DboDrawnInst(DboPartInst):
IsDot, IsLeftPointing, IsRightPointing, IsNetStyle) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
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
NewPortInstBus(status, name, type, start, hotPoint, visible, bundleOwner,
Class : DboDrawnInst(DboPartInst):
bSourceLib) : returns DboPortInst
Class : DboDrawnInst(DboPartInst):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint

---

visible: int
bundleOwner: CString
bSourceLib: CString
GetUnnamedNetgroupPortOrder(pPortOrder) : returns int
Class : DboDrawnInst(DboPartInst):
Parameters:
pPortOrder: CString &
ChangePinNamesIfPartOfBundle(bundleName, Prefix) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
bundleName: CString
Prefix: CString
NormalizeBundleBlock() : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
NormalizeUnanamedBundleBlockIfAutoGenerated() : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
PushUserPropertiesToNets() : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
DeletePinForBundle(deletePinstList) : returns int
Class : DboDrawnInst(DboPartInst):
Parameters:
deletePinstList: std::list< UINT > &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState

---

Class : DboDrawnInst(DboPartInst):
Parameters:
name: CString const &
value: CString const &
DeleteEffectiveProp(name) : returns DboState
Class : DboDrawnInst(DboPartInst):
Parameters:
name: CString const &
END class DboDrawnInst(DboPartInst):
DboBaseObjectToDboPortInst(x) : returns DboPortInst
Parameters:
x: DboBaseObject *
DboInstOccMapperToDboPortInst(x) : returns DboPortInst
Parameters:
x: DboInstOccMapper *
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