# Class: DboSchematicGlobalsIter(TBaseDboSchematicGlobalsIter):

START class DboSchematicGlobalsIter(TBaseDboSchematicGlobalsIter):
NextGlobal(status) : returns DboSchematicSymbolInst
Class : DboSchematicGlobalsIter(TBaseDboSchematicGlobalsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicGlobalsIter(TBaseDboSchematicGlobalsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicGlobalsIter(TBaseDboSchematicGlobalsIter):
Parameters:
pObject: DboSchematicSymbolInst *&
END class DboSchematicGlobalsIter(TBaseDboSchematicGlobalsIter):
START class TBaseDboSchematicOffPageConnectorsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicOffPageConnectorsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicOffPageConnectorsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicOffPageConnectorsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &

---

Sort(status)
Class : TBaseDboSchematicOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicOffPageConnectorsIter(IterDefs):
START class DboSchematicOffPageConnectorsIter(TBaseDboSchematicGlobalsIter):
NextOffPageConnector(status) : returns DboSchematicSymbolInst
Class : DboSchematicOffPageConnectorsIter(TBaseDboSchematicGlobalsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicOffPageConnectorsIter(TBaseDboSchematicGlobalsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicOffPageConnectorsIter(TBaseDboSchematicGlobalsIter):
Parameters:
pObject: DboSchematicSymbolInst *&
END class DboSchematicOffPageConnectorsIter(TBaseDboSchematicGlobalsIter):
START class TBaseDboSchematicChangedPagesIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicChangedPagesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicChangedPagesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicChangedPagesIter(IterDefs):
Parameters:
status: DboState &

---

SetFlag(flag, status)
Class : TBaseDboSchematicChangedPagesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicChangedPagesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicChangedPagesIter(IterDefs):
START class DboSchematicChangedPagesIter(TBaseDboSchematicPagesIter):
NextPage(status) : returns DboPage
Class : DboSchematicChangedPagesIter(TBaseDboSchematicPagesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicChangedPagesIter(TBaseDboSchematicPagesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicChangedPagesIter(TBaseDboSchematicPagesIter):
Parameters:
pObject: DboPage *&
END class DboSchematicChangedPagesIter(TBaseDboSchematicPagesIter):
START class TBaseDboSchematicOptimizerParametersIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicOptimizerParametersIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject

---

Class : TBaseDboSchematicOptimizerParametersIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicOptimizerParametersIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicOptimizerParametersIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicOptimizerParametersIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicOptimizerParametersIter(IterDefs):
START class DboSchematicOptimizerParametersIter(TBaseDboSchematicOptimizerParametersIter):
NextOptimizerParameter(status) : returns DboOptimizerParameter
Class : DboSchematicOptimizerParametersIter(TBaseDboSchematicOptimizerParametersIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicOptimizerParametersIter(TBaseDboSchematicOptimizerParametersIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboSchematicOptimizerParametersIter(TBaseDboSchematicOptimizerParametersIter):
Parameters:
pObject: DboOptimizerParameter *&
END class DboSchematicOptimizerParametersIter(TBaseDboSchematicOptimizerParametersIter):