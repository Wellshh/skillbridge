# Class: DboDesign(DboLib):

DboLibToDboDesign(x) : returns DboDesign
Parameters:
x: DboLib *
START class DboDesign(DboLib):
IsRootOccurrenceExisting() : returns bool
Class : DboDesign(DboLib):
Parameters:
GetObjectType() : returns ObjectTypeT
Class : DboDesign(DboLib):
Parameters:
IsModified(status) : returns int
Class : DboDesign(DboLib):
Parameters:
status: DboState &
GetRoot(status) : returns DboView
Class : DboDesign(DboLib):
Parameters:
status: DboState &
GetRootName(rootName) : returns DboState
Class : DboDesign(DboLib):
Parameters:
rootName: CString &
HasRootOccurrence() : returns bool
Class : DboDesign(DboLib):
Parameters:
GetRootOccurrence(status) : returns DboInstOccurrence
Class : DboDesign(DboLib):
Parameters:
status: DboState &
GetInstOccurrenceByName(pathname, chSeparator, status) : returns DboInstOccurrence

---

Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
status: DboState &
GetInstOccurrenceByRef(pathname, chSeparator, bPhysical, status) : returns DboInstOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
bPhysical: int
status: DboState &
GetOffPageOccurrence(id, status) : returns DboOffPageConnectorOccurrence
Class : DboDesign(DboLib):
Parameters:
id: unsigned long
status: DboState &
GetPortOccurrenceByRef(pathname, chSeparator, bPhysical, status) : returns DboPortOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
bPhysical: int
status: DboState &
GetNetOccurrenceByRef(pathname, chSeparator, bPhysical, status) : returns DboNetOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
bPhysical: int
status: DboState &
GetOffPageOccurrenceByRef(pathname, chSeparator, bPhysical, status) : returns
DboOffPageConnectorOccurrence
Class : DboDesign(DboLib):
Parameters:

---

pathname: CString const &
chSeparator: char
bPhysical: int
status: DboState &
GetTitleBlockOccurrenceByRef(pathname, chSeparator, bPhysical, status) : returns
DboTitleBlockOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
bPhysical: int
status: DboState &
GetOccurrence(id, status) : returns DboOccurrence
Class : DboDesign(DboLib):
Parameters:
id: unsigned long
status: DboState &
GetInstOccurrence(pathname, chSeparator, status) : returns DboInstOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString
chSeparator: char
status: DboState &
GetInstOccurrence(id, status) : returns DboInstOccurrence
Class : DboDesign(DboLib):
Parameters:
id: unsigned long
status: DboState &
GetPortOccurrence(pathname, chSeparator, status) : returns DboPortOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
status: DboState &

---

GetPortOccurrence(id, status) : returns DboPortOccurrence
Class : DboDesign(DboLib):
Parameters:
id: unsigned long
status: DboState &
GetNetOccurrence(pathname, chSeparator, status) : returns DboNetOccurrence
Class : DboDesign(DboLib):
Parameters:
pathname: CString const &
chSeparator: char
status: DboState &
GetNetOccurrence(id, status) : returns DboNetOccurrence
Class : DboDesign(DboLib):
Parameters:
id: unsigned long
status: DboState &
GetTitleBlockOccurrence(id, status) : returns DboTitleBlockOccurrence
Class : DboDesign(DboLib):
Parameters:
id: unsigned long
status: DboState &
GetContainingLib() : returns DboLib
Class : DboDesign(DboLib):
Parameters:
GetPowerPinsVisible(arg0) : returns int
Class : DboDesign(DboLib):
Parameters:
arg2: DboState &
GetPageFromID(nPageID) : returns DboPage
Class : DboDesign(DboLib):
Parameters:
nPageID: UINT
OccurrencesExist(pObj, status) : returns int

---

Class : DboDesign(DboLib):
Parameters:
pObj: DboBaseObject *
status: DboState &
GetRootSchematic(status) : returns DboSchematic
Class : DboDesign(DboLib):
Parameters:
status: DboState &
GetCISNotStuffedString() : returns CString
Class : DboDesign(DboLib):
Parameters:
isHSObjectsExist() : returns int
Class : DboDesign(DboLib):
Parameters:
AnnotateControlExists() : returns int
Class : DboDesign(DboLib):
Parameters:
isFlatNetsPresent() : returns bool
Class : DboDesign(DboLib):
Parameters:
DesignHasReusedSchematics() : returns int
Class : DboDesign(DboLib):
Parameters:
GetDesignId(bCreate = True) : returns int
Class : DboDesign(DboLib):
Parameters:
bCreate: bool
GetDesignId() : returns int
Class : DboDesign(DboLib):
Parameters:
HasBoardNetlistGenerated() : returns int

---

Class : DboDesign(DboLib):
Parameters:
IsRemovePNNMSelected() : returns int
Class : DboDesign(DboLib):
Parameters:
IsPNNMActive() : returns int
Class : DboDesign(DboLib):
Parameters:
GetFlatNetNamefrmId(arg0) : returns CString
Class : DboDesign(DboLib):
Parameters:
arg2: int
GetFlatNetfrmId(arg0) : returns DboFlatNet
Class : DboDesign(DboLib):
Parameters:
arg2: int
DesignHasOccurrenceProperties(status) : returns int
Class : DboDesign(DboLib):
Parameters:
status: DboState &
IsDesignInOccurrenceMode(status) : returns int
Class : DboDesign(DboLib):
Parameters:
status: DboState
GetParentObj() : returns DboBaseObject
Class : DboDesign(DboLib):
Parameters:
GetModifiedFlatNets() : returns std::map<(unsigned long,int)>
Class : DboDesign(DboLib):
Parameters:
MarkModified(pOccurrence)

---

Class : DboDesign(DboLib):
Parameters:
pOccurrence: DboOccurrence *
NewCachesIter(status, mode = ALL) : returns DboDesignCachesIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewCachesIter(status) : returns DboDesignCachesIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
NewFlatNetsIter(status, mode = SCALARS) : returns DboDesignFlatNetsIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewFlatNetsIter(status) : returns DboDesignFlatNetsIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
NewGlobalsIter(status, mode = SCALARS) : returns DboDesignGlobalsIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewGlobalsIter(status) : returns DboDesignGlobalsIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
NewSchematicOccurrencesIter(status, pSchematic = None) : returns
DboDesignSchematicOccurrencesIter
Class : DboDesign(DboLib):

---

Parameters:
status: DboState &
pSchematic: DboSchematic *
NewSchematicOccurrencesIter(status) : returns DboDesignSchematicOccurrencesIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
NewOccurrencesIter(status) : returns DboDesignOccurrencesIter
Class : DboDesign(DboLib):
Parameters:
status: DboState &
SetBoardNetListGenerated(flag)
Class : DboDesign(DboLib):
Parameters:
flag: short
SetPowerPinsVisible(bPowerPinsVisible) : returns DboState
Class : DboDesign(DboLib):
Parameters:
bPowerPinsVisible: int
SetRemovePNNMSelected(pm_RemovePNNM)
Class : DboDesign(DboLib):
Parameters:
pm_RemovePNNM: int
SetIsPNNMActive(pm_PNNMActive)
Class : DboDesign(DboLib):
Parameters:
pm_PNNMActive: int
SetCISNotStuffedString(strNotStuff)
Class : DboDesign(DboLib):
Parameters:
strNotStuff: CString &
SetRoot(view) : returns DboState

---

Class : DboDesign(DboLib):
Parameters:
view: DboView *
GetRefDesMgr() : returns DboRefDesManager
Class : DboDesign(DboLib):
Parameters:
END class DboDesign(DboLib):
START class DboDesignUpdateOccurrenceBlockerManager
Release(bDoMarkModified = False)
Class : DboDesignUpdateOccurrenceBlockerManager
Parameters:
bDoMarkModified: bool
Release()
Class : DboDesignUpdateOccurrenceBlockerManager
Parameters:
END class DboDesignUpdateOccurrenceBlockerManager
START class TBaseDboDesignOccurrencesIter(IterDefs):
GetType() : returns int
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboDesignOccurrencesIter(IterDefs):