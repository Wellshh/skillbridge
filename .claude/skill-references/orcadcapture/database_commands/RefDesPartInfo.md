# Class: RefDesPartInfo

pDesNum: int
DboRefDesUtils_ResetReference(pDboBaseObj) : returns DboState
Parameters:
pDboBaseObj: DboBaseObject *
DboRefDesUtils_BuildRefNumRange(pNumRange, strRefRange, pRefPrefix) : returns bool
Parameters:
pNumRange: DboNumericRange *
strRefRange: CString
pRefPrefix: CString
START class RefDesPartInfo
END class RefDesPartInfo
START class DboRefDesMap
AddRefDesEntry(pStrRef, pStrDes, pDboBaseObj)
Class : DboRefDesMap
Parameters:
pStrRef: CString
pStrDes: CString
pDboBaseObj: DboBaseObject *
AddRefDesEntry(pDboBaseObj)
Class : DboRefDesMap
Parameters:
pDboBaseObj: DboBaseObject *
GetRefNumMap(pStrPrefix) : returns RefNumMap
Class : DboRefDesMap
Parameters:
pStrPrefix: CString
ClearMap()
Class : DboRefDesMap
Parameters:
RemoveEntry(pDboBaseObj)

---

Class : DboRefDesMap
Parameters:
pDboBaseObj: DboBaseObject *
END class DboRefDesMap
START class DboRefDesQuerySorter
END class DboRefDesQuerySorter
START class DboRefDesManager
GetInstanceRefDesMap() : returns DboRefDesMap
Class : DboRefDesManager
Parameters:
GetOccRefDesMap() : returns DboRefDesMap
Class : DboRefDesManager
Parameters:
RefreshInstanceRefDesMap()
Class : DboRefDesManager
Parameters:
RefreshOccRefDesMap(pTopOcc, bRecurseOverChildren)
Class : DboRefDesManager
Parameters:
pTopOcc: DboInstOccurrence *
bRecurseOverChildren: bool
RefreshOccRefDesMap()
Class : DboRefDesManager
Parameters:
ProcessRefDesModify(pDboBaseObj)
Class : DboRefDesManager
Parameters:
pDboBaseObj: DboBaseObject *
ProcessObjectDelete(pDboBaseObj)

---

Class : DboRefDesManager
Parameters:
pDboBaseObj: DboBaseObject *
AddInstOccToPending(pInstOcc)
Class : DboRefDesManager
Parameters:
pInstOcc: DboInstOccurrence *
AssignRefDesToPendingInstOccs()
Class : DboRefDesManager
Parameters:
ClearPendingInstOccs()
Class : DboRefDesManager
Parameters:
END class DboRefDesManager
START class DboRefDesQueryHandler
GetNextRefDes(pQueryObj) : returns bool
Class : DboRefDesQueryHandler
Parameters:
pQueryObj: RefDesQueryObject *
SetQueryOptions(pQueryOptions)
Class : DboRefDesQueryHandler
Parameters:
pQueryOptions: RefDesQueryOptions *
GetQueryOptions() : returns RefDesQueryOptions
Class : DboRefDesQueryHandler
Parameters:
SetQueryMap(pQueryMap)
Class : DboRefDesQueryHandler
Parameters:
pQueryMap: DboRefDesMap *

---

AssignRefDesToList(lQueryList)
Class : DboRefDesQueryHandler
Parameters:
lQueryList: DboBaseObjectListT *
IsRefDesValid(pDboBaseObj) : returns bool
Class : DboRefDesQueryHandler
Parameters:
pDboBaseObj: DboBaseObject *
END class DboRefDesQueryHandler
START class DboRefDesAnnotate
AnnotateIncremental()
Class : DboRefDesAnnotate
Parameters:
AnnotateUnconditional()
Class : DboRefDesAnnotate
Parameters:
END class DboRefDesAnnotate