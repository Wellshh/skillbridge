# Class: DboLibObject(DboBaseObject):

DboBaseObjectToDboLibObject(x) : returns DboLibObject
Parameters:
x: DboBaseObject *
START class DboLibObject(DboBaseObject):
GetName(name) : returns DboState
Class : DboLibObject(DboBaseObject):
Parameters:
name: CString &
GetOwner() : returns DboLib
Class : DboLibObject(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboLibObject(DboBaseObject):
Parameters:
IsModified(status) : returns int
Class : DboLibObject(DboBaseObject):
Parameters:
status: DboState &
IsPersistent(status) : returns int
Class : DboLibObject(DboBaseObject):
Parameters:
status: DboState &
IsEquivalent(pObj) : returns int
Class : DboLibObject(DboBaseObject):
Parameters:
pObj: DboBaseObject *
GetModifyTime(status) : returns time_t
Class : DboLibObject(DboBaseObject):
Parameters:
status: DboState &
GetCreateTime(status) : returns time_t

---

Class : DboLibObject(DboBaseObject):
Parameters:
status: DboState &
GetSourceLibName(name) : returns DboState
Class : DboLibObject(DboBaseObject):
Parameters:
name: CString &
IsCachedCopy() : returns int
Class : DboLibObject(DboBaseObject):
Parameters:
IsOutOfDate(status) : returns int
Class : DboLibObject(DboBaseObject):
Parameters:
status: DboState &
GetObjectType() : returns ObjectTypeT
Class : DboLibObject(DboBaseObject):
Parameters:
sGetName(obj, status) : returns CString
Class : DboLibObject(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetSemanticString(str)
Class : DboLibObject(DboBaseObject):
Parameters:
str: CString &
GetParentObj() : returns DboBaseObject
Class : DboLibObject(DboBaseObject):
Parameters:
MarkModified() : returns DboState
Class : DboLibObject(DboBaseObject):
Parameters:

---

SetName(name) : returns DboState
Class : DboLibObject(DboBaseObject):
Parameters:
name: CString &
SetObjectType(nType) : returns DboState
Class : DboLibObject(DboBaseObject):
Parameters:
nType: enum DboBaseObject::ObjectTypeT
SetSourceLibName(name) : returns DboState
Class : DboLibObject(DboBaseObject):
Parameters:
name: CString &
END class DboLibObject(DboBaseObject):
DboLibObject_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibObjectToDboGraphicObject(x) : returns DboGraphicObject
Parameters:
x: DboLibObject *
START class DboGraphicObject(DboLibObject):
GetBoundingBox() : returns CRect
Class : DboGraphicObject(DboLibObject):
Parameters:
PinsAllowed(status) : returns int
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboGraphicObject(DboLibObject):