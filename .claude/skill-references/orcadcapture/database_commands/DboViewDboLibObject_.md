# Class: DboView(DboLibObject):

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

---

oldName: std::string
UpdateUnnamedNetgroupRegistry(name, pNetgrp)
Class : DboView(DboLibObject):
Parameters:
name: std::string
pNetgrp: DboBaseObject *
CanThisPinBeAddedToUnnamedNetgroup(pinName) : returns int
Class : DboView(DboLibObject):
Parameters:
pinName: CString
IncRefCount()
Class : DboView(DboLibObject):
Parameters:
DecrefCount()
Class : DboView(DboLibObject):
Parameters:
END class DboView(DboLibObject):
DboView_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboView_sGetModifyTime(obj, status) : returns time_t
Parameters:
obj: DboBaseObject *
status: DboState &
DboView_sGetCreateTime(obj, status) : returns time_t
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboColorRotMirror