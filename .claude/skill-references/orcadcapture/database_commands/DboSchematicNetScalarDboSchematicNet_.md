# Class: DboSchematicNetScalar(DboSchematicNet):

Parameters:
obj: DboBaseObject *
status: DboState &
DboSchematicNetToDboSchematicNetScalar(x) : returns DboSchematicNetScalar
Parameters:
x: DboSchematicNet *
START class DboSchematicNetScalar(DboSchematicNet):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicNetScalar(DboSchematicNet):
Parameters:
END class DboSchematicNetScalar(DboSchematicNet):
DboSchematicNetToDboSchematicNetBus(x) : returns DboSchematicNetBus
Parameters:
x: DboSchematicNet *
START class DboSchematicNetBus(DboSchematicNet):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicNetBus(DboSchematicNet):
Parameters:
GetWidth(status) : returns int
Class : DboSchematicNetBus(DboSchematicNet):
Parameters:
status: DboState &
GetMember(nPos, status) : returns DboSchematicNet
Class : DboSchematicNetBus(DboSchematicNet):
Parameters:
nPos: int
status: DboState &
NewMembersIter(status, mode = ALL) : returns DboSchematicNetBusMembersIter
Class : DboSchematicNetBus(DboSchematicNet):
Parameters:

---

status: DboState &
mode: enum IterDefs::IterModeT
NewMembersIter(status) : returns DboSchematicNetBusMembersIter
Class : DboSchematicNetBus(DboSchematicNet):
Parameters:
status: DboState &
END class DboSchematicNetBus(DboSchematicNet):
START class TBaseDboSchematicNetWiresIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetWiresIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetWiresIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetWiresIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetWiresIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetWiresIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetWiresIter(IterDefs):
START class DboSchematicNetWiresIter(TBaseDboSchematicNetWiresIter):

---

NextWire(status) : returns DboWire
Class : DboSchematicNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboSchematicNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
pObject: DboWire *&
END class DboSchematicNetWiresIter(TBaseDboSchematicNetWiresIter):
START class TBaseDboSchematicNetPortInstsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetPortInstsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetPortInstsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetPortInstsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetPortInstsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetPortInstsIter(IterDefs):

---

Parameters:
status: DboState &
END class TBaseDboSchematicNetPortInstsIter(IterDefs):
START class DboSchematicNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
NextPortInst(status) : returns DboPortInst
Class : DboSchematicNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
pObject: DboPortInst *&
END class DboSchematicNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
START class TBaseDboSchematicNetPortsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetPortsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetPortsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetPortsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)

---

Class : TBaseDboSchematicNetPortsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetPortsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetPortsIter(IterDefs):
START class DboSchematicNetPortsIter(TBaseDboSchematicPortsIter):
NextPort(status) : returns DboSchematicPort
Class : DboSchematicNetPortsIter(TBaseDboSchematicPortsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetPortsIter(TBaseDboSchematicPortsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetPortsIter(TBaseDboSchematicPortsIter):
Parameters:
pObject: DboSchematicPort *&
END class DboSchematicNetPortsIter(TBaseDboSchematicPortsIter):
START class TBaseDboSchematicNetGlobalsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetGlobalsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetGlobalsIter(IterDefs):
Parameters:

---

Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetGlobalsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetGlobalsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetGlobalsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetGlobalsIter(IterDefs):
START class DboSchematicNetGlobalsIter(TBaseDboSchematicNetGlobalsIter):
NextGlobal(status) : returns DboSchematicGlobal
Class : DboSchematicNetGlobalsIter(TBaseDboSchematicNetGlobalsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetGlobalsIter(TBaseDboSchematicNetGlobalsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetGlobalsIter(TBaseDboSchematicNetGlobalsIter):
Parameters:
pObject: DboSchematicGlobal *&
END class DboSchematicNetGlobalsIter(TBaseDboSchematicNetGlobalsIter):
START class TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):

---

GetType() : returns int
Class : TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetOffPageConnectorsIter(IterDefs):
START class DboSchematicNetOffPageConnectorsIter(TBaseDboSchematicNetOffPageConnectorsIter):
NextOffPageConnector(status) : returns DboSchematicOffPageConnector
Class : DboSchematicNetOffPageConnectorsIter(TBaseDboSchematicNetOffPageConnectorsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetOffPageConnectorsIter(TBaseDboSchematicNetOffPageConnectorsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetOffPageConnectorsIter(TBaseDboSchematicNetOffPageConnectorsIter):

---

Parameters:
pObject: DboSchematicOffPageConnector *&
END class DboSchematicNetOffPageConnectorsIter(TBaseDboSchematicNetOffPageConnectorsIter):
START class TBaseDboSchematicNetNetsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetNetsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetNetsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetNetsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetNetsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetNetsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetNetsIter(IterDefs):
START class DboSchematicNetNetsIter(TBaseDboSchematicNetNetsIter):
NextNet(status) : returns DboNet
Class : DboSchematicNetNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &

---

Next(status) : returns DboBaseObject
Class : DboSchematicNetNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
pObject: DboNet *&
END class DboSchematicNetNetsIter(TBaseDboSchematicNetNetsIter):
START class TBaseDboSchematicNetBusMembersIter(IterDefs):
GetType() : returns int
Class : TBaseDboSchematicNetBusMembersIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSchematicNetBusMembersIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSchematicNetBusMembersIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSchematicNetBusMembersIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSchematicNetBusMembersIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSchematicNetBusMembersIter(IterDefs):