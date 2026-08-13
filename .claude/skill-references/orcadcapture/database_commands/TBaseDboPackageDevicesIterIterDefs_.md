# Class: TBaseDboPackageDevicesIter(IterDefs):

START class TBaseDboPackageDevicesIter(IterDefs):
GetType() : returns int
Class : TBaseDboPackageDevicesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPackageDevicesIter(IterDefs):

---

Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPackageDevicesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPackageDevicesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPackageDevicesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPackageDevicesIter(IterDefs):
START class DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Next(status) : returns DboBaseObject
Class : DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Parameters:
pObject: DboDevice *&
NextDevice(status) : returns DboDevice
Class : DboPackageDevicesIter(TBaseDboPackageDevicesIter):
Parameters:
status: DboState &
END class DboPackageDevicesIter(TBaseDboPackageDevicesIter):
START class TBaseDboPackagePartsIter(IterDefs):