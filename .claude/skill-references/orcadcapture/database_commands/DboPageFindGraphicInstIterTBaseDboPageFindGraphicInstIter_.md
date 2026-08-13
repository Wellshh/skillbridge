# Class: DboPageFindGraphicInstIter(TBaseDboPageFindGraphicInstIter):

START class DboPageFindGraphicInstIter(TBaseDboPageFindGraphicInstIter):
NextGraphicInstance(status) : returns DboGraphicInstance
Class : DboPageFindGraphicInstIter(TBaseDboPageFindGraphicInstIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageFindGraphicInstIter(TBaseDboPageFindGraphicInstIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageFindGraphicInstIter(TBaseDboPageFindGraphicInstIter):
Parameters:
pObject: DboGraphicInstance *&
END class DboPageFindGraphicInstIter(TBaseDboPageFindGraphicInstIter):
START class TBaseDboPageBusEntriesIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageBusEntriesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageBusEntriesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageBusEntriesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageBusEntriesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &

---

Sort(status)
Class : TBaseDboPageBusEntriesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageBusEntriesIter(IterDefs):
START class DboPageBusEntriesIter(TBaseDboPageBusEntriesIter):
NextBusEntry(status) : returns DboBusEntry
Class : DboPageBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
pObject: DboBusEntry *&
END class DboPageBusEntriesIter(TBaseDboPageBusEntriesIter):
START class TBaseDboPageCommentGraphicsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageCommentGraphicsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageCommentGraphicsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageCommentGraphicsIter(IterDefs):
Parameters:

---

status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageCommentGraphicsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageCommentGraphicsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageCommentGraphicsIter(IterDefs):
START class DboPageCommentGraphicsIter(TBaseDboPageFindGraphicInstIter):
NextCommentGraphic(status) : returns DboGraphicInstance
Class : DboPageCommentGraphicsIter(TBaseDboPageFindGraphicInstIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageCommentGraphicsIter(TBaseDboPageFindGraphicInstIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageCommentGraphicsIter(TBaseDboPageFindGraphicInstIter):
Parameters:
pObject: DboGraphicInstance *&
END class DboPageCommentGraphicsIter(TBaseDboPageFindGraphicInstIter):
START class DboWiresInAreaIter
NextWire(status) : returns DboWire
Class : DboWiresInAreaIter
Parameters:
status: DboState &

---

END class DboWiresInAreaIter
START class DboWiresAtPointIter
NextWire(status) : returns DboWire
Class : DboWiresAtPointIter
Parameters:
status: DboState &
END class DboWiresAtPointIter
START class DboPageTransaction
InitiateInternalTransaction()
Class : DboPageTransaction
Parameters:
RegisterSchDocCommand()
Class : DboPageTransaction
Parameters:
ClearTransactionHistory()
Class : DboPageTransaction
Parameters:
InitAutoTransactions()
Class : DboPageTransaction
Parameters:
DumpTransactionVector()
Class : DboPageTransaction
Parameters:
TerminatePage()
Class : DboPageTransaction
Parameters:
PlaceUndoMarker(pCheckForDuplicate)
Class : DboPageTransaction

---

Parameters:
pCheckForDuplicate: bool
END class DboPageTransaction
DboBaseObjectToDboWire(x) : returns DboWire
Parameters:
x: DboBaseObject *
START class DboWire(DboBaseObject):
GetOwner() : returns DboPage
Class : DboWire(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboWire(DboBaseObject):
Parameters:
GetId(status) : returns unsigned long
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetPoint(position, status) : returns CPoint
Class : DboWire(DboBaseObject):
Parameters:
position: int
status: DboState &
GetPointPosition(point, status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
point: CPoint
status: DboState &
GetStartPoint(status) : returns CPoint
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &

---

GetEndPoint(status) : returns CPoint
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetPointCount(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetLineStyle(status) : returns LineStyleT
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetNetName(name) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
name: CString &
GetDisplayPropsPermitted(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
PointIsJunction(point, status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
point: CPoint

---

status: DboState &
RemoveExtraJunctions() : returns bool
Class : DboWire(DboBaseObject):
Parameters:
GetNet(status) : returns DboNet
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
IsGlobal(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetUserData(status) : returns void
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
JunctionOnWire(point) : returns int
Class : DboWire(DboBaseObject):
Parameters:
point: CPoint
IsHorizontal(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
IsVertical(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
IsNonOrthogonal(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &

---

IsZeroLen(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
AreConnectionsAbuttingAtPoint(pLocation, rStatus) : returns bool
Class : DboWire(DboBaseObject):
Parameters:
pLocation: CPoint
rStatus: DboState &
GetDispPropArray() : returns DboPtrArray
Class : DboWire(DboBaseObject):
Parameters:
GetNetAliasArray() : returns DboPtrArray
Class : DboWire(DboBaseObject):
Parameters:
sGetColor(obj, status) : returns ColorT
Class : DboWire(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetNetName(obj, status) : returns CString
Class : DboWire(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboWire(DboBaseObject):
Parameters:
pParentSchematicOcc: DboInstOccurrence *
PointOnLine(point, LineStart, LineEnd) : returns int
Class : DboWire(DboBaseObject):
Parameters:

---

point: CPoint
LineStart: CPoint
LineEnd: CPoint
LinesIntersect(Start1, End1, Start2, End2) : returns int
Class : DboWire(DboBaseObject):
Parameters:
Start1: CPoint
End1: CPoint
Start2: CPoint
End2: CPoint
GetLinesIntersect(Start1, End1, Start2, End2, Intersection) : returns int
Class : DboWire(DboBaseObject):
Parameters:
Start1: CPoint
End1: CPoint
Start2: CPoint
End2: CPoint
Intersection: CPoint &
LineIntersectsRect(rect, LineStart, LineEnd) : returns int
Class : DboWire(DboBaseObject):
Parameters:
rect: CRect
LineStart: CPoint
LineEnd: CPoint
PointOnWire(point) : returns int
Class : DboWire(DboBaseObject):
Parameters:
point: CPoint
GetStart(status) : returns DboConnection
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetEnd(status) : returns DboConnection
Class : DboWire(DboBaseObject):

---

Parameters:
status: DboState &
GetConnection(nPosition, status) : returns DboConnection
Class : DboWire(DboBaseObject):
Parameters:
nPosition: int
status: DboState &
GetCreatedByDB(status) : returns int
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
IsBoundingBoxDirty() : returns int
Class : DboWire(DboBaseObject):
Parameters:
GetBoundingBox(status) : returns CRect
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
GetBoundingBox() : returns CRect
Class : DboWire(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboWire(DboBaseObject):
Parameters:
IsBundleObject() : returns bool
Class : DboWire(DboBaseObject):
Parameters:
NewAliasesIter(status) : returns DboWireAliasesIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &

---

NewDisplayPropsIter(status) : returns DboDisplayPropsIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
NewJunctionsIter(status) : returns DboWireJunctionsIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
NewConnectedWiresIter(status) : returns DboWireConnectedWiresIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
NewPortInstsIter(status, mode) : returns DboWirePortInstsIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewBusEntriesIter(status) : returns DboWireBusEntriesIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
NewPortsIter(status, mode) : returns DboWirePortsIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewGlobalsIter(status) : returns DboWireGlobalsIter
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
NewOffPageConnectorsIter(status) : returns DboWireOffPageConnectorsIter
Class : DboWire(DboBaseObject):
Parameters:

---

status: DboState &
NewPoint(location, position = -1) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
location: CPoint
position: int
NewPoint(location) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
location: CPoint
SetPoint(position, location) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
position: int
location: CPoint
MovePoint(position, offset) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
position: int
offset: CPoint
SetColor(color) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
color: enum DboValue::ColorT
SetLineStyle(linestyle) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
linestyle: enum DboValue::LineStyleT
SetLineWidth(linewidth) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
linewidth: enum DboValue::LineWidthT

---

NewJunction(location) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
location: CPoint
DeleteJunction(location) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
location: CPoint
NewName(name, location, font, rotation, color) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
name: CString &
location: CPoint
font: LOGFONT &
rotation: enum DboValue::RotationT
color: enum DboValue::ColorT
DeleteUserProp(name) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
name: CString const &
SetUserPropStringValue(name, value) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
DeleteUserPropValue(name) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
name: CString const &
SetUserData(pPtr) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
pPtr: void *

---

NewConnection(location) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
location: CPoint
NewConnection(location, position) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
location: CPoint
position: int
DeletePoints() : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
SetId(newId) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
newId: unsigned long
SetDuplicateId(newId) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
newId: unsigned long
ClearCreatedByDB() : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
SetBoundingBoxDirty(bSetting)
Class : DboWire(DboBaseObject):
Parameters:
bSetting: int
SetBoundingBox(rect)
Class : DboWire(DboBaseObject):
Parameters:
rect: CRect
NewDisplayProp(status, name, location, rotation, font, color) : returns DboDisplayProp

---

Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
name: CString &
location: CPoint
rotation: enum DboValue::RotationT
font: LOGFONT &
color: enum DboValue::ColorT
NewDisplayProp(status, pProp, bNewVersion = 0) : returns DboDisplayProp
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
bNewVersion: int
NewDisplayProp(status, pProp) : returns DboDisplayProp
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
pProp: DboDisplayProp const *
NewUserProp(name, status) : returns DboUserProp
Class : DboWire(DboBaseObject):
Parameters:
name: CString const &
status: DboState &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboWire(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
status: DboState &
NewAlias(status, alias, location, font, rotation, color, ID = 0) : returns DboAlias
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
alias: CString &

---

location: CPoint
font: LOGFONT &
rotation: enum DboValue::RotationT
color: enum DboValue::ColorT
ID: unsigned long
NewAlias(status, alias, location, font, rotation, color) : returns DboAlias
Class : DboWire(DboBaseObject):
Parameters:
status: DboState &
alias: CString &
location: CPoint
font: LOGFONT &
rotation: enum DboValue::RotationT
color: enum DboValue::ColorT
SyncNetGroupAliases()
Class : DboWire(DboBaseObject):
Parameters:
DeleteAlias(pAlias) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
pAlias: DboAlias *
CleanupQuad()
Class : DboWire(DboBaseObject):
Parameters:
ConnectInitialization(StartPoint, EndPoint) : returns DboState
Class : DboWire(DboBaseObject):
Parameters:
StartPoint: CPoint const &
EndPoint: CPoint const &
END class DboWire(DboBaseObject):
DboWire_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *