# Class: DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):

x: DboNetSymbolInstance *
DboInstOccMapperToDboOffPageConnector(x) : returns DboOffPageConnector
Parameters:
x: DboInstOccMapper *
START class DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
GetObjectOccurrence(pParentSchematicOcc) : returns DboOffPageConnectorOccurrence
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(occArr, pDesign, status)
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
GetOccBasedOnOccId(occId) : returns DboOccurrence
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
Parameters:
occId: unsigned long
SetRotation(rotation) : returns DboState
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
Parameters:
rotation: enum DboValue::RotationT
SetMirror(mirror) : returns DboState
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):

---

Parameters:
mirror: int
SetName(name) : returns DboState
Class : DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
Parameters:
name: CString &
END class DboOffPageConnector(DboNetSymbolInstance,DboInstOccMapper):
DboNetSymbolInstanceToDboPort(x) : returns DboPort
Parameters:
x: DboNetSymbolInstance *
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