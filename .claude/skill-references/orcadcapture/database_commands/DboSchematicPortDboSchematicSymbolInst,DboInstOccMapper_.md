# Class: DboSchematicPort(DboSchematicSymbolInst,DboInstOccMapper):

DboSchematicSymbolInst_sGetNetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSchematicSymbolInstToDboSchematicPort(x) : returns DboSchematicPort
Parameters:
x: DboSchematicSymbolInst *
DboInstOccMapperToDboSchematicPort(x) : returns DboSchematicPort
Parameters:
x: DboInstOccMapper *
START class DboSchematicPort(DboSchematicSymbolInst,DboInstOccMapper):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicPort(DboSchematicSymbolInst,DboInstOccMapper):
Parameters:
GetPinType(status) : returns PinTypeT
Class : DboSchematicPort(DboSchematicSymbolInst,DboInstOccMapper):
Parameters:
status: DboState &
END class DboSchematicPort(DboSchematicSymbolInst,DboInstOccMapper):
DboSchematicSymbolInstToDboSchematicOffPageConnector(x) : returns
DboSchematicOffPageConnector
Parameters:
x: DboSchematicSymbolInst *
START class DboSchematicOffPageConnector(DboSchematicSymbolInst):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicOffPageConnector(DboSchematicSymbolInst):
Parameters:
END class DboSchematicOffPageConnector(DboSchematicSymbolInst):