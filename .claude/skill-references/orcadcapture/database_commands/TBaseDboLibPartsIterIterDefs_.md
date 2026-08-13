# Class: TBaseDboLibPartsIter(IterDefs):

Parameters:
normalizeName: CString &
name: CString &
DboLib_sSetTimeFormat(obj, format) : returns DboState
Parameters:
obj: DboBaseObject *
format: CString &
DboLib_GetOrStorageStream(designName, storageName, arg2, arg3) : returns DboState
Parameters:
designName: char const *
storageName: char const *
arg3: std::vector< std::string > &
arg4: std::vector< std::string > &
DboLib_RemoveOrStorageStream(designName, storageName, arg2) : returns DboState
Parameters:
designName: char const *
storageName: char const *
arg3: std::vector< std::string > &
DboLib_RenameOrStorageStream(designName, storageName, streamName) : returns DboState
Parameters:
designName: char const *
storageName: char const *
streamName: std::vector< std::string > &
ReadForExistenceOfBundleMapData(pLib, pDsnStorage) : returns DboState
Parameters:
pLib: DboLib *
pDsnStorage: IStorage *
DboLib_ReadForExistenceOfBundleMapData(pDes, pDsnStorage) : returns DboState
Parameters:
pDes: DboDesign *
pDsnStorage: IStorage *
START class TBaseDboLibPartsIter(IterDefs):

---

GetType() : returns int
Class : TBaseDboLibPartsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboLibPartsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboLibPartsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboLibPartsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboLibPartsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboLibPartsIter(IterDefs):
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