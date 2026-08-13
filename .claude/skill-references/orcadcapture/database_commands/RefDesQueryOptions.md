# Class: RefDesQueryOptions

DboMiscFileWriter_GetFileCreationTime(pFilepath) : returns std::string
Parameters:
pFilepath: char *
START class RefDesQueryOptions
END class RefDesQueryOptions
START class RefDesQueryObject
AssignProposedRefDes()
Class : RefDesQueryObject
Parameters:
BuildRefNumRange(pInstOcc)
Class : RefDesQueryObject
Parameters:
pInstOcc: DboInstOccurrence *
END class RefDesQueryObject
START class DboRefDesUtils
SplitPartReference(pRef, pRefPrefix, pRefNum)
Class : DboRefDesUtils
Parameters:
pRef: CString
pRefPrefix: CString &
pRefNum: int &
GetDesignatorNumber(pDesStr) : returns int
Class : DboRefDesUtils
Parameters:
pDesStr: CString const &
GetReference(pStrPrefix, pNum) : returns CString
Class : DboRefDesUtils
Parameters:
pStrPrefix: CString

---

pNum: int
GetDesignatorString(pDboBaseObj, pDesNum) : returns CString
Class : DboRefDesUtils
Parameters:
pDboBaseObj: DboBaseObject *
pDesNum: int
ResetReference(pDboBaseObj) : returns DboState
Class : DboRefDesUtils
Parameters:
pDboBaseObj: DboBaseObject *
BuildRefNumRange(pNumRange, strRefRange, pRefPrefix) : returns bool
Class : DboRefDesUtils
Parameters:
pNumRange: DboNumericRange *
strRefRange: CString
pRefPrefix: CString
END class DboRefDesUtils
DboRefDesUtils_SplitPartReference(pRef, pRefPrefix, pRefNum)
Parameters:
pRef: CString
pRefPrefix: CString &
pRefNum: int &
DboRefDesUtils_GetDesignatorNumber(pDesStr) : returns int
Parameters:
pDesStr: CString const &
DboRefDesUtils_GetReference(pStrPrefix, pNum) : returns CString
Parameters:
pStrPrefix: CString
pNum: int
DboRefDesUtils_GetDesignatorString(pDboBaseObj, pDesNum) : returns CString
Parameters:
pDboBaseObj: DboBaseObject *