# Class: CorDb_Dll_Tcl

XMATIC_EDIF2CAP(pEdifPathIn, pCapPathOut, pCfgPath) : returns bool
Parameters:
pEdifPathIn: char const *
pCapPathOut: char const *
pCfgPath: char const *
START class CorDb_Dll_Tcl
InitInstance() : returns int
Class : CorDb_Dll_Tcl
Parameters:
ExitInstance() : returns int
Class : CorDb_Dll_Tcl
Parameters:
END class CorDb_Dll_Tcl
START class DboBundleType(DboLibObject):
GetName(name) : returns DboState
Class : DboBundleType(DboLibObject):
Parameters:
name: CString &
GetBundleType() : returns BundleTypeT
Class : DboBundleType(DboLibObject):
Parameters:
GetWidth() : returns int
Class : DboBundleType(DboLibObject):
Parameters:
GetParent() : returns DboBundle
Class : DboBundleType(DboLibObject):
Parameters:
GetObjectType() : returns ObjectTypeT
Class : DboBundleType(DboLibObject):
Parameters:

---

SetName(name) : returns DboState
Class : DboBundleType(DboLibObject):
Parameters:
name: CString &
AddParent(parent)
Class : DboBundleType(DboLibObject):
Parameters:
parent: DboBundle *
RemoveParent(parent)
Class : DboBundleType(DboLibObject):
Parameters:
parent: DboBundle *
SetAllParentDirty(parent)
Class : DboBundleType(DboLibObject):
Parameters:
parent: DboBundle *
END class DboBundleType(DboLibObject):
START class DboBundleScalarMember(DboBundleType):
IsBundleMember() : returns bool
Class : DboBundleScalarMember(DboBundleType):
Parameters:
END class DboBundleScalarMember(DboBundleType):
START class DboBundleBusMember(DboBundleType):
GetName(name) : returns DboState
Class : DboBundleBusMember(DboBundleType):
Parameters:
name: CString &
GetLsb() : returns int
Class : DboBundleBusMember(DboBundleType):

---

Parameters:
GetMsb() : returns int
Class : DboBundleBusMember(DboBundleType):
Parameters:
GetBaseName(name)
Class : DboBundleBusMember(DboBundleType):
Parameters:
name: CString &
GetWidth() : returns int
Class : DboBundleBusMember(DboBundleType):
Parameters:
GetDisplayName(name)
Class : DboBundleBusMember(DboBundleType):
Parameters:
name: CString &
IsBundleMember() : returns bool
Class : DboBundleBusMember(DboBundleType):
Parameters:
END class DboBundleBusMember(DboBundleType):
START class DboBundle(DboBundleBusMember):
isMemberAddable(name, type, width = 0) : returns DboState
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
type: enum DboBundleType::BundleTypeT
width: int
isMemberAddable(name, type) : returns DboState
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
type: enum DboBundleType::BundleTypeT

---

AddMember(name, type, width = 0) : returns DboState
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
type: enum DboBundleType::BundleTypeT
width: int
AddMember(name, type) : returns DboState
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
type: enum DboBundleType::BundleTypeT
GetMember(name, allBundleMember = True) : returns DboBundleType
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
allBundleMember: bool
GetMember(name) : returns DboBundleType
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
GetMemberIndex(name) : returns int
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString
GetPosition(memberName) : returns int
Class : DboBundle(DboBundleBusMember):
Parameters:
memberName: CString
StartMemberIter(pIter) : returns int
Class : DboBundle(DboBundleBusMember):
Parameters:
pIter: int &

---

GetNextMember(pIter, name, type) : returns int
Class : DboBundle(DboBundleBusMember):
Parameters:
pIter: int &
name: CString &
type: DboBundleType::BundleTypeT &
SetMsb(msb)
Class : DboBundle(DboBundleBusMember):
Parameters:
msb: int
SetBundleProperty(PropName, PropValue)
Class : DboBundle(DboBundleBusMember):
Parameters:
PropName: CString
PropValue: CString
DeleteBundleProperty(PropName)
Class : DboBundle(DboBundleBusMember):
Parameters:
PropName: CString
GetBundleProperty(PropName) : returns CString
Class : DboBundle(DboBundleBusMember):
Parameters:
PropName: CString &
GetBundlePropertyMap(PropertiesMap)
Class : DboBundle(DboBundleBusMember):
Parameters:
PropertiesMap: CMapStringToString &
GetContainingLib() : returns DboLib
Class : DboBundle(DboBundleBusMember):
Parameters:
IsBundleMember() : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:

---

CanBeMember(name, type) : returns int
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
type: enum DboBundleType::BundleTypeT
isRecursiveAdd(name) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString
GetBusOwnerName(name) : returns CString
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString
SetBundleOwnerInformation(pSourceLibName)
Class : DboBundle(DboBundleBusMember):
Parameters:
pSourceLibName: CString
GetBundleOwnerInformation(pOwnerName, pSourceLibName) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
pOwnerName: CString &
pSourceLibName: CString &
IsMemberDeleted(pMembername) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
pMembername: std::string
IsMemberRenamed(pMemberName, pNewName) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
pMemberName: std::string
pNewName: std::string &
ClearEditMaps()

---

Class : DboBundle(DboBundleBusMember):
Parameters:
ChangeMsb(width, doAdd = 1)
Class : DboBundle(DboBundleBusMember):
Parameters:
width: int
doAdd: int
ChangeMsb(width)
Class : DboBundle(DboBundleBusMember):
Parameters:
width: int
isDirty() : returns int
Class : DboBundle(DboBundleBusMember):
Parameters:
setDirty(arg0)
Class : DboBundle(DboBundleBusMember):
Parameters:
arg2: int
DeleteMember(name) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
name: CString &
RenameMember(OldName, NewName) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
OldName: CString &
NewName: CString &
MoveUpDown(index, isUp) : returns bool
Class : DboBundle(DboBundleBusMember):
Parameters:
index: int
isUp: bool

---

MergeBundlePropertyMap(PropertiesMap)
Class : DboBundle(DboBundleBusMember):
Parameters:
PropertiesMap: CMapStringToString &
END class DboBundle(DboBundleBusMember):
START class DboBundleMemberIter
Next(name, type) : returns int
Class : DboBundleMemberIter
Parameters:
name: CString &
type: DboBundleType::BundleTypeT &
END class DboBundleMemberIter
START class DboBundleNetIter
Next(name) : returns int
Class : DboBundleNetIter
Parameters:
name: CString &
END class DboBundleNetIter
START class BundleReferenceCount
GetBundleOwner() : returns CString
Class : BundleReferenceCount
Parameters:
AddReferenceCount() : returns int
Class : BundleReferenceCount
Parameters:
ReduceReferenceCount() : returns int
Class : BundleReferenceCount
Parameters:

---

END class BundleReferenceCount
START class DboBundleTemplateMap
ExportToDCF(pLib, fileName)
Class : DboBundleTemplateMap
Parameters:
pLib: DboLib *
fileName: CString
GetTempName(isTop, BundleName, bundleTempName)
Class : DboBundleTemplateMap
Parameters:
isTop: bool
BundleName: CString
bundleTempName: CString &
BundleAlreadyThere(bundleName) : returns DboState
Class : DboBundleTemplateMap
Parameters:
bundleName: CString
NewBundleMemberIter(name) : returns DboBundleMemberIter
Class : DboBundleTemplateMap
Parameters:
name: CString &
GetBundleMembers(name, bundleMemberArray) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
bundleMemberArray: CStringArray &
NewBundleNetIter(name, mode = NETSITER_UNEXPANDED) : returns DboBundleNetIter
Class : DboBundleTemplateMap
Parameters:
name: CString &
mode: enum DboBundleType::BundleNetIterMode
NewBundleNetIter(name) : returns DboBundleNetIter

---

Class : DboBundleTemplateMap
Parameters:
name: CString &
GetBundleNets(name, netArray, getExpanded = 0, getCompleteHierName = 0) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
netArray: CStringArray &
getExpanded: int
getCompleteHierName: int
GetBundleNets(name, netArray, getExpanded = 0) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
netArray: CStringArray &
getExpanded: int
GetBundleNets(name, netArray) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
netArray: CStringArray &
GetBundleNet(name, netName, index, parentName, getCompleteHierName = 0) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
netName: CString &
index: int
parentName: CString &
getCompleteHierName: int
GetBundleNet(name, netName, index, parentName) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
netName: CString &
index: int

---

parentName: CString &
GetBundleTemplates(bundleArray, isDisplay = 0)
Class : DboBundleTemplateMap
Parameters:
bundleArray: CStringArray &
isDisplay: int
GetBundleTemplates(bundleArray)
Class : DboBundleTemplateMap
Parameters:
bundleArray: CStringArray &
GetBundleTemplates(bundleArray)
Class : DboBundleTemplateMap
Parameters:
bundleArray: CPtrArray &
IsBundle(name) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
GetInternalBundleName(name)
Class : DboBundleTemplateMap
Parameters:
name: CString &
GetInternalBundleName(BundleName, InternalName)
Class : DboBundleTemplateMap
Parameters:
BundleName: CString
InternalName: CString &
GetDisplayBundleName(name, NGBaseName)
Class : DboBundleTemplateMap
Parameters:
name: CString &
NGBaseName: CString &

---

GetDisplayBundleName(name)
Class : DboBundleTemplateMap
Parameters:
name: CString &
IsBundleMember(BundleName, BundleMemberName, isDirect = True) : returns bool
Class : DboBundleTemplateMap
Parameters:
BundleName: CString
BundleMemberName: CString
isDirect: bool
IsBundleMember(BundleName, BundleMemberName) : returns bool
Class : DboBundleTemplateMap
Parameters:
BundleName: CString
BundleMemberName: CString
GetPortIter() : returns POSITION
Class : DboBundleTemplateMap
Parameters:
GetNextPort(nPos, Name) : returns POSITION
Class : DboBundleTemplateMap
Parameters:
nPos: POSITION &
Name: CString &
GetBundleProperty(BundleName, PropName) : returns CString
Class : DboBundleTemplateMap
Parameters:
BundleName: CString &
PropName: CString &
GetBundlePropertyMap(BundleName, PropertiesMap)
Class : DboBundleTemplateMap
Parameters:
BundleName: CString &
PropertiesMap: CMapStringToString &

---

ReadOneBundle(file, TemplateVersion)
Class : DboBundleTemplateMap
Parameters:
file: CFile &
TemplateVersion: int
SaveOneBundle(file, BundleName)
Class : DboBundleTemplateMap
Parameters:
file: CFile &
BundleName: CString
GetBundle(name, srcLibName = "") : returns DboBundle
Class : DboBundleTemplateMap
Parameters:
name: CString &
srcLibName: CString
GetBundle(name) : returns DboBundle
Class : DboBundleTemplateMap
Parameters:
name: CString &
LookUpNets(name) : returns bool
Class : DboBundleTemplateMap
Parameters:
name: CString &
sGetMemberTypeIdGivenString(memberType) : returns int
Class : DboBundleTemplateMap
Parameters:
memberType: CString
sGetMemberTypeStringGivenId(id) : returns CString
Class : DboBundleTemplateMap
Parameters:
id: int
isMemberAddable(name, memberOfName, type, width = 0) : returns DboState
Class : DboBundleTemplateMap

---

Parameters:
name: CString &
memberOfName: CString &
type: enum DboBundleType::BundleTypeT
width: int
isMemberAddable(name, memberOfName, type) : returns DboState
Class : DboBundleTemplateMap
Parameters:
name: CString &
memberOfName: CString &
type: enum DboBundleType::BundleTypeT
MarkModifiedDesign()
Class : DboBundleTemplateMap
Parameters:
GetUnnamedBundleOwnerObject(pObj, newIndex) : returns DboBaseObject
Class : DboBundleTemplateMap
Parameters:
pObj: DboBaseObject *
newIndex: int &
ClearEditMaps()
Class : DboBundleTemplateMap
Parameters:
IsInternalProperty(propName) : returns bool
Class : DboBundleTemplateMap
Parameters:
propName: CString
AddBundleTemplate(name, owner, width, isNewBundleCreated) : returns DboBundle
Class : DboBundleTemplateMap
Parameters:
name: CString &
owner: DboBaseObject *
width: int
isNewBundleCreated: bool &

---

GetMemerIndexFromUnnamedBundle(pObj, memberName) : returns int
Class : DboBundleTemplateMap
Parameters:
pObj: DboBaseObject *
memberName: CString
GetNameForUnNamedBundle(index, pObj, bundleNetName, parentName) : returns bool
Class : DboBundleTemplateMap
Parameters:
index: int
pObj: DboBaseObject *
bundleNetName: CString &
parentName: CString &
AddBundleMember(name, memberOfName, type, owner) : returns DboState
Class : DboBundleTemplateMap
Parameters:
name: CString &
memberOfName: CString &
type: enum DboBundleType::BundleTypeT
owner: DboBaseObject *
AddBundleNet(name, type, owner) : returns DboBundleType
Class : DboBundleTemplateMap
Parameters:
name: CString &
type: DboBundleType::BundleTypeT &
owner: DboLib *
DeleteBundleMember(name, memberOfName) : returns bool
Class : DboBundleTemplateMap
Parameters:
name: CString &
memberOfName: CString &
RenameBundleMember(name, OldmemberOfName, NewMemberName) : returns bool
Class : DboBundleTemplateMap
Parameters:
name: CString &
OldmemberOfName: CString &

---

NewMemberName: CString
RemoveBundleSafe(name, BundleSourceLibName) : returns int
Class : DboBundleTemplateMap
Parameters:
name: CString &
BundleSourceLibName: CString &
MoveUpDown(BundleName, index, isUp) : returns bool
Class : DboBundleTemplateMap
Parameters:
BundleName: CString
index: int
isUp: bool
END class DboBundleTemplateMap
DboBundleTemplateMap_ExportToDCF(pLib, fileName)
Parameters:
pLib: DboLib *
fileName: CString
GetDisplayBundleName(name, NGBaseName)
Parameters:
name: CString &
NGBaseName: CString &
DboBundleTemplateMap_GetDisplayBundleName(name)
Parameters:
name: CString &
DboBundleTemplateMap_sGetMemberTypeIdGivenString(memberType) : returns int
Parameters:
memberType: CString
DboBundleTemplateMap_sGetMemberTypeStringGivenId(id) : returns CString
Parameters:
id: int
DboBundleTemplateMap_IsInternalProperty(propName) : returns bool