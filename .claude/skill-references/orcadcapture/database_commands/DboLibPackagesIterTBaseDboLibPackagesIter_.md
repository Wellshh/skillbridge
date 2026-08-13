# Class: DboLibPackagesIter(TBaseDboLibPackagesIter):

START class DboLibPackagesIter(TBaseDboLibPackagesIter):
NextPackage(status) : returns DboPackage
Class : DboLibPackagesIter(TBaseDboLibPackagesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibPackagesIter(TBaseDboLibPackagesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibPackagesIter(TBaseDboLibPackagesIter):
Parameters:
pObject: DboPackage *&
END class DboLibPackagesIter(TBaseDboLibPackagesIter):
START class DboPackageNamesIter
NextName(name) : returns DboState
Class : DboPackageNamesIter
Parameters:
name: CString &
END class DboPackageNamesIter
START class DboLibPackageNamesIter
NextName(name) : returns DboState
Class : DboLibPackageNamesIter
Parameters:
name: CString &
END class DboLibPackageNamesIter
START class DboLibPackageAliasesIter

---

NextAlias(name) : returns DboState
Class : DboLibPackageAliasesIter
Parameters:
name: CString &
END class DboLibPackageAliasesIter
START class TBaseDboLibSymbolsIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibSymbolsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibSymbolsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibSymbolsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibSymbolsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibSymbolsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibSymbolsIter(IterDefs):
START class DboLibSymbolsIter(TBaseDboLibSymbolsIter):
NextSymbol(status) : returns DboSymbol
Class : DboLibSymbolsIter(TBaseDboLibSymbolsIter):
Parameters:

---

status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibSymbolsIter(TBaseDboLibSymbolsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibSymbolsIter(TBaseDboLibSymbolsIter):
Parameters:
pObject: DboSymbol *&
END class DboLibSymbolsIter(TBaseDboLibSymbolsIter):
START class DboLibSymbolNamesIter
NextName(name, pType = None) : returns DboState
Class : DboLibSymbolNamesIter
Parameters:
name: CString &
pType: DboBaseObject::ObjectTypeT *
NextName(name) : returns DboState
Class : DboLibSymbolNamesIter
Parameters:
name: CString &
END class DboLibSymbolNamesIter
START class TBaseDboLibGraphicsIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibGraphicsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibGraphicsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject

---

Class : TBaseDboLibGraphicsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibGraphicsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibGraphicsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibGraphicsIter(IterDefs):
START class DboLibGraphicsIter(TBaseDboLibGraphicsIter):
NextGraphicObject(status) : returns DboGraphicObject
Class : DboLibGraphicsIter(TBaseDboLibGraphicsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibGraphicsIter(TBaseDboLibGraphicsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibGraphicsIter(TBaseDboLibGraphicsIter):
Parameters:
pObject: DboGraphicObject *&
END class DboLibGraphicsIter(TBaseDboLibGraphicsIter):
START class DboLibGraphicNamesIter
NextName(name, pType = None) : returns DboState
Class : DboLibGraphicNamesIter

---

Parameters:
name: CString &
pType: DboBaseObject::ObjectTypeT *
NextName(name) : returns DboState
Class : DboLibGraphicNamesIter
Parameters:
name: CString &
END class DboLibGraphicNamesIter
START class TBaseDboLibExportBlocksIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibExportBlocksIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibExportBlocksIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibExportBlocksIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibExportBlocksIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibExportBlocksIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibExportBlocksIter(IterDefs):
START class DboLibExportBlocksIter(TBaseDboLibExportBlocksIter):

---

NextExportBlock(status) : returns DboExportBlock
Class : DboLibExportBlocksIter(TBaseDboLibExportBlocksIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibExportBlocksIter(TBaseDboLibExportBlocksIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibExportBlocksIter(TBaseDboLibExportBlocksIter):
Parameters:
pObject: DboExportBlock *&
END class DboLibExportBlocksIter(TBaseDboLibExportBlocksIter):
START class DboLibExportBlockNamesIter
NextName(name) : returns DboState
Class : DboLibExportBlockNamesIter
Parameters:
name: CString &
END class DboLibExportBlockNamesIter
START class TBaseDboLibChangedObjectsIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibChangedObjectsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibChangedObjectsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibChangedObjectsIter(IterDefs):
Parameters:

---

status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibChangedObjectsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibChangedObjectsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibChangedObjectsIter(IterDefs):
START class DboLibChangedObjectsIter(TBaseDboLibChangedObjectsIter):
NextObject(status) : returns DboBaseObject
Class : DboLibChangedObjectsIter(TBaseDboLibChangedObjectsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibChangedObjectsIter(TBaseDboLibChangedObjectsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibChangedObjectsIter(TBaseDboLibChangedObjectsIter):
Parameters:
pObject: DboBaseObject *&
END class DboLibChangedObjectsIter(TBaseDboLibChangedObjectsIter):
START class TBaseDboLibCachesIter(IterDefs):
GetType() : returns int
Class : TBaseDboLibCachesIter(IterDefs):
Parameters:

---

GetSource() : returns DboBaseObject
Class : TBaseDboLibCachesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibCachesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibCachesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibCachesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibCachesIter(IterDefs):
START class DboLibCachesIter(TBaseDboLibChangedObjectsIter):
NextCachedObject(status) : returns DboBaseObject
Class : DboLibCachesIter(TBaseDboLibChangedObjectsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboLibCachesIter(TBaseDboLibChangedObjectsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboLibCachesIter(TBaseDboLibChangedObjectsIter):
Parameters:
pObject: DboBaseObject *&
END class DboLibCachesIter(TBaseDboLibChangedObjectsIter):