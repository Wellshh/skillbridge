# Class: DboPortInstEffectivePropsIter(DboEffectivePropsIter):

START class DboPortInstEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboPortInstEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboPortInstEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboPortInstEffectivePropsIter(DboEffectivePropsIter):
DboGraphicInstanceToDboNetSymbolInstance(x) : returns DboNetSymbolInstance
Parameters:
x: DboGraphicInstance *
START class DboNetSymbolInstance(DboGraphicInstance):
GetSymbol(status) : returns DboSymbol
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
status: DboState &
GetHotSpot(status) : returns CPoint
Class : DboNetSymbolInstance(DboGraphicInstance):

---

Parameters:
status: DboState &
GetOffsetHotSpot(status) : returns CPoint
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
status: DboState &
GetNet(status) : returns DboNet
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
status: DboState &
GetWire(status) : returns DboWire
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
status: DboState &
GetBoundingBox() : returns CRect
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
IsBus(status) : returns int
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
status: DboState &
GetSourceSymbolName(name) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
name: CString &
GetSourceLibName(name) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
name: CString &
GetOccBasedOnOccId(occId) : returns DboOccurrence
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:

---

occId: unsigned long
sGetNetName(obj, status) : returns CString
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotX(obj, status) : returns int
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHotSpotY(obj, status) : returns int
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSourceLibName(obj, status) : returns CString
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSourceSymbolName(obj, status) : returns CString
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGenerateBundleObjectName(obj) : returns CString
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
IsBoundingBoxDirty() : returns int
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:

---

SetBoundingBoxDirty(bSetting)
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
bSetting: int
SetBoundingBox(boundingBox) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
boundingBox: CRect
Move(offset) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
offset: CPoint
SetLocation(location) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
location: CPoint
SetRotation(rotation) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
rotation: enum DboValue::RotationT
SetMirror(mirror) : returns DboState
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
mirror: int
Disconnect() : returns int
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
END class DboNetSymbolInstance(DboGraphicInstance):
DboNetSymbolInstance_sGetNetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *