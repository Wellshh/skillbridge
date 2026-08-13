# Class: DboCustomItemInstance(DboGraphicInstance):

DboPort_sGetPinType(obj, status) : returns PinTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboCustomItemInstance(x) : returns DboCustomItemInstance
Parameters:
x: DboGraphicInstance *
START class DboCustomItemInstance(DboGraphicInstance):
GetCookie() : returns int
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
GetInterfaceID() : returns IID
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
GetPluginName() : returns CString
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
GetType() : returns int
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
GetOwningOccurrence() : returns DboInstOccurrence
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
SetCookie(nCookie)
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
nCookie: int
SetInterfaceID(idInterfaceID)
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
idInterfaceID: IID

---

SetPluginName(strPluginName)
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
strPluginName: CString &
SetType(nType)
Class : DboCustomItemInstance(DboGraphicInstance):
Parameters:
nType: int
END class DboCustomItemInstance(DboGraphicInstance):
DboBaseObjectToDboBusEntry(x) : returns DboBusEntry
Parameters:
x: DboBaseObject *
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