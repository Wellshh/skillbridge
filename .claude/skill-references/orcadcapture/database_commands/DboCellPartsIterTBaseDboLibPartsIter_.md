# Class: DboCellPartsIter(TBaseDboLibPartsIter):

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