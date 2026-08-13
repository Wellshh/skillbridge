# Class: TBaseDboCellPartsIter(IterDefs):

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

---

SetFlag(flag, status)
Class : TBaseDboCellPartsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboCellPartsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboCellPartsIter(IterDefs):
START class DboCellPartsIter(TBaseDboLibPartsIter):
NextPart(status) : returns DboLibPart
Class : DboCellPartsIter(TBaseDboLibPartsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboCellPartsIter(TBaseDboLibPartsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboCellPartsIter(TBaseDboLibPartsIter):
Parameters:
pObject: DboLibPart *&
END class DboCellPartsIter(TBaseDboLibPartsIter):
START class DboCellPartNamesIter
NextName(NxtName) : returns DboState
Class : DboCellPartNamesIter
Parameters:
NxtName: CString &
END class DboCellPartNamesIter