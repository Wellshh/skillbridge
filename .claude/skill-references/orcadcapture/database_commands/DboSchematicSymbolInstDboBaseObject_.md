# Class: DboSchematicSymbolInst(DboBaseObject):

DboBaseObjectToDboSchematicSymbolInst(x) : returns DboSchematicSymbolInst
Parameters:
x: DboBaseObject *
START class DboSchematicSymbolInst(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
name: CString &
GetOwner() : returns DboSchematic
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
GetNet(status) : returns DboSchematicNet
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
status: DboState &
GetNetId(status) : returns unsigned long
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
status: DboState &
GetIsBus(status) : returns int
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
status: DboState &
IsBundleObject() : returns bool
Class : DboSchematicSymbolInst(DboBaseObject):

---

Parameters:
GetEntry(pos, status) : returns DboBaseObject
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
pos: int
status: DboState &
GetSize(status) : returns int
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
status: DboState &
sGetName(obj, status) : returns CString
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetNetId(obj, status) : returns int
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetParentObj() : returns DboBaseObject
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
SetIsBus(bVal) : returns DboState
Class : DboSchematicSymbolInst(DboBaseObject):
Parameters:
bVal: int
END class DboSchematicSymbolInst(DboBaseObject):
DboSchematicSymbolInst_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &