# Class: DboCell(DboLibObject):

DboBusEntry_sGetEndPointY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBusEntry_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibObjectToDboCell(x) : returns DboCell
Parameters:
x: DboLibObject *
START class DboCell(DboLibObject):
GetPart(name, status) : returns DboLibPart
Class : DboCell(DboLibObject):
Parameters:
name: CString &
status: DboState &
FindPart(index, status) : returns DboLibPart
Class : DboCell(DboLibObject):
Parameters:
index: int
status: DboState &
GetSize(status) : returns int
Class : DboCell(DboLibObject):
Parameters:
status: DboState &
GetObjectType() : returns ObjectTypeT
Class : DboCell(DboLibObject):
Parameters:
IsEquivalent(pObj) : returns int
Class : DboCell(DboLibObject):

---

Parameters:
pObj: DboBaseObject *
GetSemanticString(str)
Class : DboCell(DboLibObject):
Parameters:
str: CString &
NewPartsIter(status) : returns DboCellPartsIter
Class : DboCell(DboLibObject):
Parameters:
status: DboState &
NewPartNamesIter(status) : returns DboCellPartNamesIter
Class : DboCell(DboLibObject):
Parameters:
status: DboState &
AddPart(part) : returns DboState
Class : DboCell(DboLibObject):
Parameters:
part: DboLibPart *
END class DboCell(DboLibObject):
START class TBaseDboCellPartsIter(IterDefs):
GetType() : returns int
Class : TBaseDboCellPartsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboCellPartsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboCellPartsIter(IterDefs):
Parameters:
status: DboState &