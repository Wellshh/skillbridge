# Class: DboLibPartsIter(TBaseDboLibPartsIter):

START class DboLibPartsIter(TBaseDboLibPartsIter):
NextPart(status) : returns DboLibPart
Class : DboLibPartsIter(TBaseDboLibPartsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibPartsIter(TBaseDboLibPartsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibPartsIter(TBaseDboLibPartsIter):

---

Parameters:
pObject: DboLibPart *&
END class DboLibPartsIter(TBaseDboLibPartsIter):
START class TBaseDboLibUnusedCacheEntriesIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibUnusedCacheEntriesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibUnusedCacheEntriesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibUnusedCacheEntriesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibUnusedCacheEntriesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibUnusedCacheEntriesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibUnusedCacheEntriesIter(IterDefs):
START class DboLibUnusedCacheEntriesIter(TBaseDboLibUnusedCacheEntriesIter):
NextUnusedEntry(status) : returns DboLibObject
Class : DboLibUnusedCacheEntriesIter(TBaseDboLibUnusedCacheEntriesIter):
Parameters:
status: DboState &