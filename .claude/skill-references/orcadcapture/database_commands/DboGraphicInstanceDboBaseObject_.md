# Class: DboGraphicInstance(DboBaseObject):

START class DboGraphicInstance(DboBaseObject):
GetGridLocation(gridValue) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
gridValue: CString &

---

GetObjectType() : returns ObjectTypeT
Class : DboGraphicInstance(DboBaseObject):
Parameters:
GetOwner() : returns DboPage
Class : DboGraphicInstance(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboGraphicInstance(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString &
GetDefiningGraphicObject(status) : returns DboGraphicObject
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetLocation(status) : returns CPoint
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetRotation(status) : returns RotationT
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetMirror(status) : returns int
Class : DboGraphicInstance(DboBaseObject):
Parameters:

---

status: DboState &
GetBoundingBox() : returns CRect
Class : DboGraphicInstance(DboBaseObject):
Parameters:
GetDisplayPropsPermitted(status) : returns int
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetSourceDefinition(status) : returns DboGraphicObject
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetSourceLibName(name) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString &
GetUserData(status) : returns void
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetId(status) : returns unsigned long
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
nNameID: UINT
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:

---

name: CString const &
value: CString &
GetEffectivePropStringValueNC(name, value) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString const &
value: CString &
GetOffsetBoundingBox(status) : returns CRect
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
sGetName(obj, status) : returns CString
Class : DboGraphicInstance(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int
Class : DboGraphicInstance(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationX(obj, status) : returns int
Class : DboGraphicInstance(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetRotation(obj, status) : returns RotationT
Class : DboGraphicInstance(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetColor(obj, status) : returns ColorT
Class : DboGraphicInstance(DboBaseObject):

---

Parameters:
obj: DboBaseObject *
status: DboState &
sGetMirror(obj, status) : returns int
Class : DboGraphicInstance(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetOffsetGraphicPoint(definingPoint) : returns CPoint
Class : DboGraphicInstance(DboBaseObject):
Parameters:
definingPoint: CPoint
GetDispPropArray() : returns DboPtrArray
Class : DboGraphicInstance(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboGraphicInstance(DboBaseObject):
Parameters:
MarkModified() : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
NewDisplayPropsIter(status) : returns DboDisplayPropsIter
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
NewUserProp(name, status) : returns DboUserProp
Class : DboGraphicInstance(DboBaseObject):
Parameters:

---

name: CString const &
status: DboState &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
status: DboState &
SetObjectType(nType) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
nType: enum DboBaseObject::ObjectTypeT
SetLocation(location) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
location: CPoint
Move(offset) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
offset: CPoint
Drag(offset) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
offset: CPoint
SetRotation(rotation) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
rotation: enum DboValue::RotationT
SetColor(color) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
color: enum DboValue::ColorT

---

SetMirror(mirror) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
mirror: int
SetName(name) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString &
SetBoundingBox(boundingBox) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
boundingBox: CRect
DeleteUserProp(name) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString const &
SetUserPropStringValue(name, value) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
DeleteUserPropValue(name) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
name: CString const &
SetUserData(pPtr) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
pPtr: void *
SetId(nId, bNewVersion = 0) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
nId: unsigned long

---

bNewVersion: int
SetId(nId) : returns DboState
Class : DboGraphicInstance(DboBaseObject):
Parameters:
nId: unsigned long
NewDisplayProp(status, name, location, rotation, font, color) : returns DboDisplayProp
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
name: CString &
location: CPoint
rotation: enum DboValue::RotationT
font: LOGFONT &
color: enum DboValue::ColorT
NewDisplayProp(status, pProp, bNewersion = 0) : returns DboDisplayProp
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
bNewersion: int
NewDisplayProp(status, pProp) : returns DboDisplayProp
Class : DboGraphicInstance(DboBaseObject):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
END class DboGraphicInstance(DboBaseObject):
DboGraphicInstance_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstance_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *