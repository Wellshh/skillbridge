# Class: DboGlobal(DboNetSymbolInstance):

START class DboGlobal(DboNetSymbolInstance):
GetPinType(status) : returns PinTypeT
Class : DboGlobal(DboNetSymbolInstance):
Parameters:
status: DboState &
GetGlobalSymbol(status) : returns DboGlobalSymbol
Class : DboGlobal(DboNetSymbolInstance):
Parameters:
status: DboState &
SetRotation(rotation) : returns DboState
Class : DboGlobal(DboNetSymbolInstance):
Parameters:
rotation: enum DboValue::RotationT
SetMirror(mirror) : returns DboState
Class : DboGlobal(DboNetSymbolInstance):
Parameters:
mirror: int
SetName(name) : returns DboState
Class : DboGlobal(DboNetSymbolInstance):
Parameters:
name: CString &
END class DboGlobal(DboNetSymbolInstance):
DboNetSymbolInstanceToDboOffPageConnector(x) : returns DboOffPageConnector
Parameters: