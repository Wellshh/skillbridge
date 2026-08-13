# Class: DboPort(DboNetSymbolInstance):

START class DboPort(DboNetSymbolInstance):
GetObjectOccurrence(pParentSchematicOcc) : returns DboPortOccurrence
Class : DboPort(DboNetSymbolInstance):
Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetObjectOccurrences(portName, occArr, pDesign, status, bOnlyCurrent = False)
Class : DboPort(DboNetSymbolInstance):
Parameters:
portName: CString const &
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(portName, occArr, pDesign, status)
Class : DboPort(DboNetSymbolInstance):
Parameters:
portName: CString const &
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
GetPinType(status) : returns PinTypeT
Class : DboPort(DboNetSymbolInstance):

---

Parameters:
status: DboState &
GetPortSymbol(status) : returns DboPortSymbol
Class : DboPort(DboNetSymbolInstance):
Parameters:
status: DboState &
sGetPinType(obj, status) : returns PinTypeT
Class : DboPort(DboNetSymbolInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
IsBundleObject() : returns bool
Class : DboPort(DboNetSymbolInstance):
Parameters:
SetRotation(rotation) : returns DboState
Class : DboPort(DboNetSymbolInstance):
Parameters:
rotation: enum DboValue::RotationT
SetMirror(mirror) : returns DboState
Class : DboPort(DboNetSymbolInstance):
Parameters:
mirror: int
SetName(name) : returns DboState
Class : DboPort(DboNetSymbolInstance):
Parameters:
name: CString &
SetPinType(pinType) : returns DboState
Class : DboPort(DboNetSymbolInstance):
Parameters:
pinType: enum DboValue::PinTypeT
END class DboPort(DboNetSymbolInstance):