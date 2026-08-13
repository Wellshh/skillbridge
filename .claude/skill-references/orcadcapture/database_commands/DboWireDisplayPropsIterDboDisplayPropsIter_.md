# Class: DboWireDisplayPropsIter(DboDisplayPropsIter):

START class DboWireDisplayPropsIter(DboDisplayPropsIter):
Next(status) : returns DboBaseObject
Class : DboWireDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
NextProp(status) : returns DboDisplayProp
Class : DboWireDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboWireDisplayPropsIter(DboDisplayPropsIter):

---

Parameters:
pObject: DboDisplayProp *&
END class DboWireDisplayPropsIter(DboDisplayPropsIter):
START class TBaseDboWireAliasesIter(IterDefs):
GetType() : returns int
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWireAliasesIter(IterDefs):
START class DboWireAliasesIter(TBaseDboWireAliasesIter):
Next(status) : returns DboBaseObject
Class : DboWireAliasesIter(TBaseDboWireAliasesIter):
Parameters:
status: DboState &