# Class: DboERC(DboNetSymbolInstance):

status: DboState &
DboNetSymbolInstance_sGetHotSpotX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetSymbolInstance_sGetHotSpotY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetSymbolInstance_sGetSourceLibName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetSymbolInstance_sGetSourceSymbolName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetSymbolInstance_sGenerateBundleObjectName(obj) : returns CString
Parameters:
obj: DboBaseObject *
DboNetSymbolInstanceToDboERC(x) : returns DboERC
Parameters:
x: DboNetSymbolInstance *
START class DboERC(DboNetSymbolInstance):
GetSeverity(status) : returns ERC_Severity
Class : DboERC(DboNetSymbolInstance):
Parameters:
status: DboState &
GetError(error) : returns DboState
Class : DboERC(DboNetSymbolInstance):
Parameters:

---

error: CString &
GetDetail(detail) : returns DboState
Class : DboERC(DboNetSymbolInstance):
Parameters:
detail: CString &
GetLocationString(location) : returns DboState
Class : DboERC(DboNetSymbolInstance):
Parameters:
location: CString &
sGetError(obj, status) : returns CString
Class : DboERC(DboNetSymbolInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDetail(obj, status) : returns CString
Class : DboERC(DboNetSymbolInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSeverity(obj, status) : returns CString
Class : DboERC(DboNetSymbolInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
SetLocation(location) : returns DboState
Class : DboERC(DboNetSymbolInstance):
Parameters:
location: CPoint
SetRotation(rotation) : returns DboState
Class : DboERC(DboNetSymbolInstance):
Parameters:
rotation: enum DboValue::RotationT

---

SetMirror(mirror) : returns DboState
Class : DboERC(DboNetSymbolInstance):
Parameters:
mirror: int
END class DboERC(DboNetSymbolInstance):
DboERC_sGetError(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboERC_sGetDetail(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboERC_sGetSeverity(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetSymbolInstanceToDboBookMark(x) : returns DboBookMark
Parameters:
x: DboNetSymbolInstance *
START class DboBookMark(DboNetSymbolInstance):
SetLocation(location) : returns DboState
Class : DboBookMark(DboNetSymbolInstance):
Parameters:
location: CPoint
SetRotation(rotation) : returns DboState
Class : DboBookMark(DboNetSymbolInstance):
Parameters:
rotation: enum DboValue::RotationT
SetMirror(mirror) : returns DboState
Class : DboBookMark(DboNetSymbolInstance):