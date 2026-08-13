# Class: TBaseDboLibUnusedCacheEntriesIter(IterDefs):

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

---

Next(status) : returns DboBaseObject
Class : DboLibUnusedCacheEntriesIter(TBaseDboLibUnusedCacheEntriesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibUnusedCacheEntriesIter(TBaseDboLibUnusedCacheEntriesIter):
Parameters:
pObject: DboLibObject *&
END class DboLibUnusedCacheEntriesIter(TBaseDboLibUnusedCacheEntriesIter):
START class DboLibPartNamesIter
NextName(name) : returns DboState
Class : DboLibPartNamesIter
Parameters:
name: CString &
END class DboLibPartNamesIter
START class TBaseDboLibCellsIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibCellsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibCellsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibCellsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibCellsIter(IterDefs):
Parameters:
flag: UINT

---

status: DboState &
Sort(status)
Class : TBaseDboLibCellsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibCellsIter(IterDefs):
START class DboLibCellsIter(TBaseDboLibCellsIter):
NextCell(status) : returns DboCell
Class : DboLibCellsIter(TBaseDboLibCellsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibCellsIter(TBaseDboLibCellsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibCellsIter(TBaseDboLibCellsIter):
Parameters:
pObject: DboCell *&
END class DboLibCellsIter(TBaseDboLibCellsIter):
START class DboLibCellNamesIter
NextName(name) : returns DboState
Class : DboLibCellNamesIter
Parameters:
name: CString &
END class DboLibCellNamesIter
START class TBaseDboLibViewsIter(IterDefs):
GetType() : returns int

---

Class : TBaseDboLibViewsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibViewsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibViewsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibViewsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibViewsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibViewsIter(IterDefs):
START class DboLibViewsIter(TBaseDboLibViewsIter):
NextView(status) : returns DboView
Class : DboLibViewsIter(TBaseDboLibViewsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibViewsIter(TBaseDboLibViewsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibViewsIter(TBaseDboLibViewsIter):
Parameters:

---

pObject: DboView *&
END class DboLibViewsIter(TBaseDboLibViewsIter):
START class DboLibViewNamesIter
NextName(name) : returns DboState
Class : DboLibViewNamesIter
Parameters:
name: CString &
END class DboLibViewNamesIter
START class TBaseDboLibPackagesIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibPackagesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibPackagesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibPackagesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibPackagesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibPackagesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibPackagesIter(IterDefs):