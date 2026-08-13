# Class: DboPackage(DboLibObject):

DboLibObjectToDboPackage(x) : returns DboPackage
Parameters:
x: DboLibObject *
START class DboPackage(DboLibObject):
GetObjectType() : returns ObjectTypeT
Class : DboPackage(DboLibObject):
Parameters:
GetSize(status) : returns int
Class : DboPackage(DboLibObject):
Parameters:
status: DboState &
IsHomogeneous(status) : returns int
Class : DboPackage(DboLibObject):
Parameters:
status: DboState &
IsEquivalent(pObj) : returns int
Class : DboPackage(DboLibObject):
Parameters:
pObj: DboBaseObject *
GetDesignator(designator) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
designator: CString &
GetPCBLib(lib) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
lib: CString &
GetPCBFootprint(footprint) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
footprint: CString &

---

GetDevice(position, status) : returns DboDevice
Class : DboPackage(DboLibObject):
Parameters:
position: int
status: DboState &
GetDevice(DeviceDesignator, status) : returns DboDevice
Class : DboPackage(DboLibObject):
Parameters:
DeviceDesignator: CString &
status: DboState &
sGetSize(obj, status) : returns int
Class : DboPackage(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetReferenceTemplate(obj, status) : returns CString
Class : DboPackage(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPCBLib(obj, status) : returns CString
Class : DboPackage(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPCBFootprint(obj, status) : returns CString
Class : DboPackage(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetReferenceTemplate(csRefTmpl) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:

---

csRefTmpl: CString &
GetSemanticString(str)
Class : DboPackage(DboLibObject):
Parameters:
str: CString &
GetBundleTemplateMap() : returns DboBundleTemplateMap
Class : DboPackage(DboLibObject):
Parameters:
isBundleTemplateExists() : returns bool
Class : DboPackage(DboLibObject):
Parameters:
NewDevicesIter(status) : returns DboPackageDevicesIter
Class : DboPackage(DboLibObject):
Parameters:
status: DboState &
NewPartsIter(status) : returns DboPackagePartsIter
Class : DboPackage(DboLibObject):
Parameters:
status: DboState &
NewAliasesIter(status) : returns DboPackageAliasesIter
Class : DboPackage(DboLibObject):
Parameters:
status: DboState &
AddAlias(alias) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
alias: CString &
SetName(name) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
name: CString &

---

SetDesignator(designator) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
designator: CString &
SetPCBLib(libName) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
libName: CString &
SetPCBFootprint(footprint) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
footprint: CString const &
DeleteDevice(position) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
position: int
SetReferenceTemplate(csRefTmpl) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
csRefTmpl: CString &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboPackage(DboLibObject):
Parameters:
name: CString const &
value: CString const &
Cleanup() : returns DboState
Class : DboPackage(DboLibObject):

---

Parameters:
NewDevice(designator, position, cell, status) : returns DboDevice
Class : DboPackage(DboLibObject):
Parameters:
designator: CString &
position: int
cell: DboCell *
status: DboState &
END class DboPackage(DboLibObject):
DboPackage_sGetSize(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPackage_sGetReferenceTemplate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPackage_sGetPCBLib(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPackage_sGetPCBFootprint(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
START class TBaseDboPackageDevicesIter(IterDefs):
GetType() : returns int
Class : TBaseDboPackageDevicesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPackageDevicesIter(IterDefs):