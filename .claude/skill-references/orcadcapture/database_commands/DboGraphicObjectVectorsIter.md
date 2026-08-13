# Class: DboGraphicObjectVectorsIter

START class DboGraphicObjectVectorsIter
NextVector(status) : returns DboVector
Class : DboGraphicObjectVectorsIter
Parameters:
status: DboState &

---

END class DboGraphicObjectVectorsIter
DboLibObjectToDboView(x) : returns DboView
Parameters:
x: DboLibObject *
START class DboView(DboLibObject):
GetRefCount() : returns int
Class : DboView(DboLibObject):
Parameters:
sGetName(obj, status) : returns CString
Class : DboView(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetModifyTime(obj, status) : returns time_t
Class : DboView(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetCreateTime(obj, status) : returns time_t
Class : DboView(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
FindUnnamedNetgroupByName(name) : returns DboBaseObject
Class : DboView(DboLibObject):
Parameters:
name: CString
UpdateUnnamedNetgroupRegistry(name, pNetgrp, oldName = "")
Class : DboView(DboLibObject):
Parameters:
name: std::string
pNetgrp: DboBaseObject *