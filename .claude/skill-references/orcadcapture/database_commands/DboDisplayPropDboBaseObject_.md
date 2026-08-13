# Class: DboDisplayProp(DboBaseObject):

Parameters:
x: DboBaseObject *
START class DboDisplayProp(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboDisplayProp(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboDisplayProp(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
name: CString &
GetValueString(strValue, pViewOccurrence = None) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
strValue: CString &
pViewOccurrence: DboInstOccurrence *
GetValueString(strValue) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
strValue: CString &
GetActualValueString(pBaseObject, value) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
pBaseObject: DboBaseObject *
value: CString &
GetId(status, bNewVersion = 0) : returns unsigned long
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
bNewVersion: int

---

GetId(status) : returns unsigned long
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
GetOwner() : returns DboBaseObject
Class : DboDisplayProp(DboBaseObject):
Parameters:
GetLocation(status) : returns CPoint
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
GetRotation(status) : returns RotationT
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
GetFont(dbFontType, logfont) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
dbFontType: int
logfont: LOGFONT &
IsFontDefault(arg0) : returns int
Class : DboDisplayProp(DboBaseObject):
Parameters:
arg2: DboState &
GetColor(status) : returns ColorT
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
GetDefaultFontType(pDboObj, status) : returns int
Class : DboDisplayProp(DboBaseObject):
Parameters:
pDboObj: DboBaseObject *

---

status: DboState &
GetDefaultFontType(status) : returns int
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
GetDisplayType(status) : returns DisplayTypeT
Class : DboDisplayProp(DboBaseObject):
Parameters:
status: DboState &
GetValueStringForOccurrence(DWID, value) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
DWID: DboDesignOccurrenceId const &
value: CString &
sGetName(obj, status) : returns CString
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetValue(obj, status) : returns CString
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationX(obj, status) : returns int
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *

---

status: DboState &
sGetRotation(obj, status) : returns RotationT
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFont(obj, status) : returns LOGFONT
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetColor(obj, status) : returns ColorT
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDisplayType(obj, status) : returns DisplayTypeT
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetBoundingBox() : returns CRect
Class : DboDisplayProp(DboBaseObject):
Parameters:
IsBoundingBoxDirty() : returns int
Class : DboDisplayProp(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboDisplayProp(DboBaseObject):
Parameters:
MarkModified() : returns DboState
Class : DboDisplayProp(DboBaseObject):

---

Parameters:
SetName(name) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
name: CString &
SetLocation(location) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
location: CPoint
SetRotation(rotation) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
rotation: enum DboValue::RotationT
SetFont(font) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
font: LOGFONT &
SetColor(color) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
color: enum DboValue::ColorT
SetDisplayType(type) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
type: enum DboValue::DisplayTypeT
SetBoundingBoxDirty(bSetting)
Class : DboDisplayProp(DboBaseObject):
Parameters:
bSetting: int
SetOwnerBoundingBoxDirty(bSetting)
Class : DboDisplayProp(DboBaseObject):
Parameters:

---

bSetting: int
SetBoundingBox(rect) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
rect: CRect
SetValueString(strValue, pViewOccurrence = None) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
strValue: CString &
pViewOccurrence: DboInstOccurrence *
SetValueString(strValue) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
strValue: CString &
sSetName(obj, name) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
name: CString &
sSetLocationX(obj, x) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
x: int
sSetLocationY(obj, y) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
y: int
sSetRotation(obj, rotation) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *

---

rotation: enum DboValue::RotationT
sSetFont(obj, font) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
font: LOGFONT &
sSetColor(obj, color) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
color: enum DboValue::ColorT
sSetDisplayType(obj, displayType) : returns DboState
Class : DboDisplayProp(DboBaseObject):
Parameters:
obj: DboBaseObject *
displayType: enum DboValue::DisplayTypeT
END class DboDisplayProp(DboBaseObject):
DboDisplayProp_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sGetValue(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *