# Class: DboPageEditsIter

START class DboPageEditsIter
NextEdit(pChangedObjectPtr, pUserDataPtr) : returns DboState
Class : DboPageEditsIter
Parameters:
pChangedObjectPtr: DboBaseObject *&
pUserDataPtr: void *&
END class DboPageEditsIter
START class DboPageObjectsAtPointIter(TBaseDboLibChangedObjectsIter):
NextObject(status) : returns DboBaseObject
Class : DboPageObjectsAtPointIter(TBaseDboLibChangedObjectsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageObjectsAtPointIter(TBaseDboLibChangedObjectsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageObjectsAtPointIter(TBaseDboLibChangedObjectsIter):
Parameters:
pObject: DboBaseObject *&
END class DboPageObjectsAtPointIter(TBaseDboLibChangedObjectsIter):
START class TBaseDboPagePartInstsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPagePartInstsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPagePartInstsIter(IterDefs):
Parameters:

---

Next(status) : returns DboBaseObject
Class : TBaseDboPagePartInstsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPagePartInstsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPagePartInstsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPagePartInstsIter(IterDefs):
START class DboPagePartInstsIter(TBaseDboPagePartInstsIter):
NextPartInst(status) : returns DboPartInst
Class : DboPagePartInstsIter(TBaseDboPagePartInstsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPagePartInstsIter(TBaseDboPagePartInstsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPagePartInstsIter(TBaseDboPagePartInstsIter):
Parameters:
pObject: DboPartInst *&
END class DboPagePartInstsIter(TBaseDboPagePartInstsIter):
START class TBaseDboPageWiresIter(IterDefs):
GetType() : returns int

---

Class : TBaseDboPageWiresIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageWiresIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageWiresIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageWiresIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageWiresIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageWiresIter(IterDefs):
START class DboPageWiresIter(TBaseDboSchematicNetWiresIter):
NextWire(status) : returns DboWire
Class : DboPageWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:

---

pObject: DboWire *&
END class DboPageWiresIter(TBaseDboSchematicNetWiresIter):
START class TBaseDboPageNetsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageNetsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageNetsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageNetsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageNetsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageNetsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageNetsIter(IterDefs):
START class DboPageNetsIter(TBaseDboSchematicNetNetsIter):
NextNet(status) : returns DboNet
Class : DboPageNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject

---

Class : DboPageNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboPageNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
pObject: DboNet *&
END class DboPageNetsIter(TBaseDboSchematicNetNetsIter):
START class TBaseDboPagePortsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPagePortsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPagePortsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPagePortsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPagePortsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPagePortsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPagePortsIter(IterDefs):
START class DboPagePortsIter(TBaseDboPagePortsIter):

---

NextPort(status) : returns DboPort
Class : DboPagePortsIter(TBaseDboPagePortsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPagePortsIter(TBaseDboPagePortsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboPagePortsIter(TBaseDboPagePortsIter):
Parameters:
pObject: DboPort *&
END class DboPagePortsIter(TBaseDboPagePortsIter):
START class TBaseDboPageERCsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageERCsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageERCsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageERCsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageERCsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)

---

Class : TBaseDboPageERCsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageERCsIter(IterDefs):
START class DboPageERCsIter(TBaseDboPageERCsIter):
NextERC(status) : returns DboERC
Class : DboPageERCsIter(TBaseDboPageERCsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageERCsIter(TBaseDboPageERCsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageERCsIter(TBaseDboPageERCsIter):
Parameters:
pObject: DboERC *&
END class DboPageERCsIter(TBaseDboPageERCsIter):
START class TBaseDboPageBookMarksIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageBookMarksIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageBookMarksIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageBookMarksIter(IterDefs):
Parameters:
status: DboState &

---

SetFlag(flag, status)
Class : TBaseDboPageBookMarksIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageBookMarksIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageBookMarksIter(IterDefs):
START class DboPageBookMarksIter(TBaseDboPageBookMarksIter):
NextBookMark(status) : returns DboBookMark
Class : DboPageBookMarksIter(TBaseDboPageBookMarksIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageBookMarksIter(TBaseDboPageBookMarksIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageBookMarksIter(TBaseDboPageBookMarksIter):
Parameters:
pObject: DboBookMark *&
END class DboPageBookMarksIter(TBaseDboPageBookMarksIter):
START class TBaseDboPageGlobalsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageGlobalsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageGlobalsIter(IterDefs):

---

Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageGlobalsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageGlobalsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageGlobalsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageGlobalsIter(IterDefs):
START class DboPageGlobalsIter(TBaseDboPageGlobalsIter):
NextGlobal(status) : returns DboGlobal
Class : DboPageGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboPageGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
pObject: DboGlobal *&
END class DboPageGlobalsIter(TBaseDboPageGlobalsIter):
START class TBaseDboPageOffPageConnectorsIter(IterDefs):

---

GetType() : returns int
Class : TBaseDboPageOffPageConnectorsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageOffPageConnectorsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageOffPageConnectorsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageOffPageConnectorsIter(IterDefs):
START class DboPageOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
NextOffPageConnector(status) : returns DboOffPageConnector
Class : DboPageOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboPageOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string

---

Class : DboPageOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
pObject: DboOffPageConnector *&
END class DboPageOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
START class TBaseDboPageTitleBlocksIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageTitleBlocksIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageTitleBlocksIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageTitleBlocksIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageTitleBlocksIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageTitleBlocksIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageTitleBlocksIter(IterDefs):
START class DboPageTitleBlocksIter(TBaseDboPageTitleBlocksIter):
NextTitleBlock(status) : returns DboTitleBlock
Class : DboPageTitleBlocksIter(TBaseDboPageTitleBlocksIter):
Parameters:
status: DboState &

---

Next(status) : returns DboBaseObject
Class : DboPageTitleBlocksIter(TBaseDboPageTitleBlocksIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPageTitleBlocksIter(TBaseDboPageTitleBlocksIter):
Parameters:
pObject: DboTitleBlock *&
END class DboPageTitleBlocksIter(TBaseDboPageTitleBlocksIter):
START class TBaseDboPageFindGraphicInstIter(IterDefs):
GetType() : returns int
Class : TBaseDboPageFindGraphicInstIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPageFindGraphicInstIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPageFindGraphicInstIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPageFindGraphicInstIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPageFindGraphicInstIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPageFindGraphicInstIter(IterDefs):