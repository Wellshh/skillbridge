# Class: DboBusEntry(DboBaseObject):

START class DboBusEntry(DboBaseObject):
IsBundle(status) : returns int
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
GetObjectType() : returns ObjectTypeT
Class : DboBusEntry(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboBusEntry(DboBaseObject):
Parameters:
GetOwner() : returns DboPage
Class : DboBusEntry(DboBaseObject):
Parameters:
GetEntryPoint(status) : returns CPoint
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &

---

GetEndPoint(status) : returns CPoint
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
GetEntryWire(status) : returns DboWire
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
GetEndWire(status) : returns DboWire
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
IsBus(status) : returns int
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
GetUserData(status) : returns void
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
GetId(status) : returns unsigned long
Class : DboBusEntry(DboBaseObject):
Parameters:
status: DboState &
sGetEntryPointX(obj, status) : returns int
Class : DboBusEntry(DboBaseObject):
Parameters:
obj: DboBaseObject *

---

status: DboState &
sGetEntryPointY(obj, status) : returns int
Class : DboBusEntry(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndPointX(obj, status) : returns int
Class : DboBusEntry(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndPointY(obj, status) : returns int
Class : DboBusEntry(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetColor(obj, status) : returns ColorT
Class : DboBusEntry(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
MarkModified() : returns DboState
Class : DboBusEntry(DboBaseObject):
Parameters:
SetId(nId) : returns DboState
Class : DboBusEntry(DboBaseObject):
Parameters:
nId: unsigned long
SetEntryPoint(location) : returns DboState
Class : DboBusEntry(DboBaseObject):
Parameters:
location: CPoint

---

SetEndPoint(location) : returns DboState
Class : DboBusEntry(DboBaseObject):
Parameters:
location: CPoint
SetColor(color) : returns DboState
Class : DboBusEntry(DboBaseObject):
Parameters:
color: enum DboValue::ColorT
SetUserData(pPtr) : returns DboState
Class : DboBusEntry(DboBaseObject):
Parameters:
pPtr: void *
SetBoundingBox(rect)
Class : DboBusEntry(DboBaseObject):
Parameters:
rect: CRect
GetBoundingBox() : returns CRect
Class : DboBusEntry(DboBaseObject):
Parameters:
END class DboBusEntry(DboBaseObject):
DboBusEntry_sGetEntryPointX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBusEntry_sGetEntryPointY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBusEntry_sGetEndPointX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &