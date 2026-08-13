# Class: NG_DCFWriter

Parameters:
propName: CString
START class NG_DCFWriter
init()
Class : NG_DCFWriter
Parameters:
end()
Class : NG_DCFWriter
Parameters:
WriteDCF()
Class : NG_DCFWriter
Parameters:
END class NG_DCFWriter
START class DBXMLWriter
CreateChild(sTag, sValue)
Class : DBXMLWriter
Parameters:
sTag: char const *
sValue: char const *
Createtag(sTag)
Class : DBXMLWriter
Parameters:
sTag: char const *
CloseLasttag()
Class : DBXMLWriter
Parameters:
CloseAlltags()
Class : DBXMLWriter
Parameters:

---

AddAtributes(sAttrName, sAttrvalue)
Class : DBXMLWriter
Parameters:
sAttrName: char const *
sAttrvalue: char const *
AddComment(sComment)
Class : DBXMLWriter
Parameters:
sComment: char const *
IsXMLWritable() : returns bool
Class : DBXMLWriter
Parameters:
DoOutput2Stream()
Class : DBXMLWriter
Parameters:
AddDesignTag(pDesignName, pName, pXsdPath)
Class : DBXMLWriter
Parameters:
pDesignName: char const *
pName: char const *
pXsdPath: char const *
AddLibraryTag(pLibName, pXsdPath)
Class : DBXMLWriter
Parameters:
pLibName: char const *
pXsdPath: char const *
AddSchematicTag(pScmName)
Class : DBXMLWriter
Parameters:
pScmName: char const *
AddPageTag(pPageName)
Class : DBXMLWriter
Parameters:

---

pPageName: char const *
AddWireTag(pName, lStart, lEnd, bIsWireScalar)
Class : DBXMLWriter
Parameters:
pName: char const *
lStart: CPoint
lEnd: CPoint
bIsWireScalar: bool
AddWireColorTag(pColor, pTagName)
Class : DBXMLWriter
Parameters:
pColor: enum DboValue::ColorT
pTagName: char const *
AddJunctionTag(pLocation)
Class : DBXMLWriter
Parameters:
pLocation: CPoint
AddAliasTag(pNxtName, pLocation, pRot, pColor)
Class : DBXMLWriter
Parameters:
pNxtName: char const *
pLocation: CPoint
pRot: enum DboValue::RotationT
pColor: enum DboValue::ColorT
AddAliasFontTag(pFont)
Class : DBXMLWriter
Parameters:
pFont: LOGFONT
AddBundlePortTag(pPortName)
Class : DBXMLWriter
Parameters:
pPortName: char const *
CreateBundleTag(BundleTemplate, bundlenames, isTop)

---

Class : DBXMLWriter
Parameters:
BundleTemplate: DboBundleTemplateMap *
bundlenames: char const *
isTop: bool
WriteBundleDefinition(BundleTemplate, lXMLWriter)
Class : DBXMLWriter
Parameters:
BundleTemplate: DboBundleTemplateMap *
lXMLWriter: DBXMLWriter &
AddDisplayPropTag(pTagName, pName, pRot, pLocation)
Class : DBXMLWriter
Parameters:
pTagName: char const *
pName: char const *
pRot: enum DboValue::RotationT
pLocation: CPoint
AddPropFontTag(pFont)
Class : DBXMLWriter
Parameters:
pFont: LOGFONT
AddPropColorTag(pColor)
Class : DBXMLWriter
Parameters:
pColor: enum DboValue::ColorT
AddPropDisplayTypeTag(pDispType)
Class : DBXMLWriter
Parameters:
pDispType: enum DboValue::DisplayTypeT
AddUserPropTag(pTagName, pName, pValue)
Class : DBXMLWriter
Parameters:
pTagName: char const *
pName: char const *

---

pValue: char const *
AddGlobalTag(pName, pLocation, pRot, pMirror, pLibName, pSymblName)
Class : DBXMLWriter
Parameters:
pName: char const *
pLocation: CPoint
pRot: enum DboValue::RotationT
pMirror: bool
pLibName: char const *
pSymblName: char const *
AddERCTag(pName, pDetail, pError, pLocationStr, pLibName, pSymblName,
Class : DBXMLWriter
pLocation, pMirror, pRot)
Class : DBXMLWriter
Parameters:
pName: char const *
pDetail: char const *
pError: char const *
pLocationStr: char const *
pLibName: char const *
pSymblName: char const *
pLocation: CPoint
pMirror: bool
pRot: enum DboValue::RotationT
AddOffPageConnector(pName, pLocation, pRot, pMirror, pLibName, pSymblName)
Class : DBXMLWriter
Parameters:
pName: char const *
pLocation: CPoint
pRot: enum DboValue::RotationT
pMirror: bool
pLibName: char const *
pSymblName: char const *
AddPortTag(pName, pLocation, pRot, pLibName, pSymblName, pMirror)
Class : DBXMLWriter
Parameters:

---

pName: char const *
pLocation: CPoint
pRot: enum DboValue::RotationT
pLibName: char const *
pSymblName: char const *
pMirror: bool
AddTitleBlockTag(pName, pLocation, pRot, pLibName, pSymblName)
Class : DBXMLWriter
Parameters:
pName: char const *
pLocation: CPoint
pRot: enum DboValue::RotationT
pLibName: char const *
pSymblName: char const *
AddTitleBlockDisplayTag(pTitleBlockDisplayed)
Class : DBXMLWriter
Parameters:
pTitleBlockDisplayed: bool
AddBorderDisplayTag(pBorderDisplayed)
Class : DBXMLWriter
Parameters:
pBorderDisplayed: bool
AddTitlePageCountTag(pCount)
Class : DBXMLWriter
Parameters:
pCount: int
AddTitlePageNumberTag(pNumber)
Class : DBXMLWriter
Parameters:
pNumber: int
AddGridRefDisplayTag(pGridRefDisplayed)
Class : DBXMLWriter
Parameters:
pGridRefDisplayed: bool

---

AddPageSizeInfoTag(pPageWidth, pPageHeight, pPinToPin, pIsMetric)
Class : DBXMLWriter
Parameters:
pPageWidth: long
pPageHeight: long
pPinToPin: long
pIsMetric: bool
AddSizeNameTag(pSize)
Class : DBXMLWriter
Parameters:
pSize: char const *
AddOuterBorderMarginTag(pOuterLocation)
Class : DBXMLWriter
Parameters:
pOuterLocation: CPoint
AddOuterBorderStyleTag(pLineStyle)
Class : DBXMLWriter
Parameters:
pLineStyle: enum DboValue::LineStyleT
AddOuterBorderWidthTag(pLinewidth)
Class : DBXMLWriter
Parameters:
pLinewidth: enum DboValue::LineWidthT
AddOuterBorderVisibleTag(pIsVisible)
Class : DBXMLWriter
Parameters:
pIsVisible: bool
AddInnerBorderMarginTag(pInnerLocation)
Class : DBXMLWriter
Parameters:
pInnerLocation: CPoint
AddInnerBorderStyleTag(pStyle)

---

Class : DBXMLWriter
Parameters:
pStyle: enum DboValue::LineStyleT
AddInnerBorderWidthTag(pwidth)
Class : DBXMLWriter
Parameters:
pwidth: enum DboValue::LineWidthT
AddInnerBorderVisibleTag(pInnerVisible)
Class : DBXMLWriter
Parameters:
pInnerVisible: bool
AddColorTag(pColor)
Class : DBXMLWriter
Parameters:
pColor: enum DboValue::ColorT
AddLabelFontTag(pFont)
Class : DBXMLWriter
Parameters:
pFont: LOGFONT
AddLabelColorTag(pLabelColor)
Class : DBXMLWriter
Parameters:
pLabelColor: enum DboValue::ColorT
AddHorizontalCountTag(pCount)
Class : DBXMLWriter
Parameters:
pCount: int
AddHorizontalWidthTag(pLabelWidth)
Class : DBXMLWriter
Parameters:
pLabelWidth: int
AddHorizontalIsCharTag(pIsChar)

---

Class : DBXMLWriter
Parameters:
pIsChar: bool
AddHorizontalVisibleTag(pLabelVisible)
Class : DBXMLWriter
Parameters:
pLabelVisible: bool
AddHorizontalAscendingTag(pIsAscending)
Class : DBXMLWriter
Parameters:
pIsAscending: bool
AddHorizontalStyleTag(pSeparatorStyle)
Class : DBXMLWriter
Parameters:
pSeparatorStyle: enum DboValue::LineStyleT
AddHorizontalSeparatorWidthTag(pSeparatorWidth)
Class : DBXMLWriter
Parameters:
pSeparatorWidth: enum DboValue::LineWidthT
AddVerticalCountTag(pVCount)
Class : DBXMLWriter
Parameters:
pVCount: int
AddVerticalWidthTag(pVWidth)
Class : DBXMLWriter
Parameters:
pVWidth: int
AddVerticalIsCharTag(pVerticalIsChar)
Class : DBXMLWriter
Parameters:
pVerticalIsChar: bool
AddVerticalVisibleTag(pVerticalIsVisible)

---

Class : DBXMLWriter
Parameters:
pVerticalIsVisible: bool
AddVerticalAscendingTag(pVerticalIsAscending)
Class : DBXMLWriter
Parameters:
pVerticalIsAscending: bool
AddVerticalStyleTag(pVerticalLineStyle)
Class : DBXMLWriter
Parameters:
pVerticalLineStyle: enum DboValue::LineStyleT
AddVerticalSeparatorWidthTag(pVerticalLineWidth)
Class : DBXMLWriter
Parameters:
pVerticalLineWidth: enum DboValue::LineWidthT
AddBusEntryTag(pBusPt, pEndPt)
Class : DBXMLWriter
Parameters:
pBusPt: CPoint
pEndPt: CPoint
AddNetTag(pName, bIsNetScalar)
Class : DBXMLWriter
Parameters:
pName: char const *
bIsNetScalar: bool
AddPartInstTag(pName, pLocation, pLibName, pPkgName, pDeviceDesignator,
Class : DBXMLWriter
pRot, pMirror, pColor)
Class : DBXMLWriter
Parameters:
pName: char const *
pLocation: CPoint
pLibName: char const *
pPkgName: char const *

---

pDeviceDesignator: char const *
pRot: enum DboValue::RotationT
pMirror: bool
pColor: enum DboValue::ColorT
AddDrawnInstTag(pName, pLocation, pLibName, pRot, pMirror, pColor,
Class : DBXMLWriter
pBBox, lDeviceDesignator)
Class : DBXMLWriter
Parameters:
pName: char const *
pLocation: CPoint
pLibName: char const *
pRot: enum DboValue::RotationT
pMirror: bool
pColor: enum DboValue::ColorT
pBBox: CRect
lDeviceDesignator: char const *
AddPCBTag(pPCBLibName)
Class : DBXMLWriter
Parameters:
pPCBLibName: char const *
AddContentsLibNameTag(pContentsLibName)
Class : DBXMLWriter
Parameters:
pContentsLibName: char const *
AddContentsViewNameTag(pContentsViewName)
Class : DBXMLWriter
Parameters:
pContentsViewName: char const *
AddContentsViewTypeTag(pType)
Class : DBXMLWriter
Parameters:
pType: enum DboValue::ViewTypeT
AddIsPrimitivePropTag(pPType)

---

Class : DBXMLWriter
Parameters:
pPType: enum DboValue::PrimitiveTypeT
AddPartValueTag(pValue)
Class : DBXMLWriter
Parameters:
pValue: char const *
AddReferenceTag(pReferenceName)
Class : DBXMLWriter
Parameters:
pReferenceName: char const *
AddPortInstTag(pName, pType, lStart, lHotPoint, lVisible, bPortInstScalar)
Class : DBXMLWriter
Parameters:
pName: char const *
pType: enum DboValue::PinTypeT
lStart: CPoint
lHotPoint: CPoint
lVisible: bool
bPortInstScalar: bool
AddIsLongTag(pLong)
Class : DBXMLWriter
Parameters:
pLong: bool
AddIsClockTag(pClock)
Class : DBXMLWriter
Parameters:
pClock: bool
AddIsDotTag(pDot)
Class : DBXMLWriter
Parameters:
pDot: bool
AddIsLeftPointingTag(pLeft)

---

Class : DBXMLWriter
Parameters:
pLeft: bool
AddIsRightPointingTag(pRight)
Class : DBXMLWriter
Parameters:
pRight: bool
AddIsNetStyleTag(pNet)
Class : DBXMLWriter
Parameters:
pNet: bool
AddIsNoConnectTag(pNoConnect)
Class : DBXMLWriter
Parameters:
pNoConnect: bool
AddIsGlobalTag(pGlobal)
Class : DBXMLWriter
Parameters:
pGlobal: bool
AddIsNumberVisibleTag(pNumVisible)
Class : DBXMLWriter
Parameters:
pNumVisible: bool
AddSymbolTag(pName, pTagName)
Class : DBXMLWriter
Parameters:
pName: char const *
pTagName: char const *
AddSymbolPinTag(pName, pStart, pHotPt, pPosition, pType, pVisible,
Class : DBXMLWriter
bIsSymbolPinScalar)
Class : DBXMLWriter
Parameters:

---

pName: char const *
pStart: CPoint
pHotPt: CPoint
pPosition: int
pType: enum DboValue::PinTypeT
pVisible: bool
bIsSymbolPinScalar: bool
AddPackageTag(pPkgName, pRefDesPrefix, pIsHomo, pAlphaNumeric)
Class : DBXMLWriter
Parameters:
pPkgName: char const *
pRefDesPrefix: char const *
pIsHomo: int
pAlphaNumeric: int
AddLibPartTag()
Class : DBXMLWriter
Parameters:
AddLibPartNormalViewTag()
Class : DBXMLWriter
Parameters:
AddLibPartConvertViewTag()
Class : DBXMLWriter
Parameters:
AddDeviceTag()
Class : DBXMLWriter
Parameters:
AddDevicePinNumberTag(pPinNumber, pPosition)
Class : DBXMLWriter
Parameters:
pPinNumber: char const *
pPosition: int
AddDevicePinSharedTag(pPosition, pIsShared)
Class : DBXMLWriter

---

Parameters:
pPosition: int
pIsShared: int
AddDevicePinSwapIdTag(pPosition, pSwapId)
Class : DBXMLWriter
Parameters:
pPosition: int
pSwapId: int
AddIsPinNumbersVisibleTag(lPinNum)
Class : DBXMLWriter
Parameters:
lPinNum: bool
AddIsPinNamesRotatedTag(lPinRot)
Class : DBXMLWriter
Parameters:
lPinRot: bool
AddIsPinNamesVisibleTag(lPinNum)
Class : DBXMLWriter
Parameters:
lPinNum: bool
AddBBoxTag(pRect, pTagName)
Class : DBXMLWriter
Parameters:
pRect: CRect
pTagName: char const *
AddEllipseTag(pRect, pStyle, pWidth, pFill, pHatch)
Class : DBXMLWriter
Parameters:
pRect: CRect
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pFill: enum DboValue::FillStyleT
pHatch: enum DboValue::HatchStyleT

---

AddBoxTag(pUpperLeft, pLowerRight, pStyle, pWidth, pFill, pHatch)
Class : DBXMLWriter
Parameters:
pUpperLeft: CPoint
pLowerRight: CPoint
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pFill: enum DboValue::FillStyleT
pHatch: enum DboValue::HatchStyleT
AddLineTag(pStart, pEnd, pStyle, pWidth)
Class : DBXMLWriter
Parameters:
pStart: CPoint
pEnd: CPoint
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
AddArcTag(pRect, pStart, pEnd, pStyle, pWidth)
Class : DBXMLWriter
Parameters:
pRect: CRect
pStart: CPoint
pEnd: CPoint
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
AddPolygonTag(pStyle, pWidth, pFill, pHatch)
Class : DBXMLWriter
Parameters:
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pFill: enum DboValue::FillStyleT
pHatch: enum DboValue::HatchStyleT
AddPolygonPointTag(pPt)
Class : DBXMLWriter
Parameters:
pPt: CPoint

---

AddPolylineTag(pStyle, pWidth)
Class : DBXMLWriter
Parameters:
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
AddPolylinePointTag(pPt)
Class : DBXMLWriter
Parameters:
pPt: CPoint
AddCommentTextTag(pText, pRect, pLoc)
Class : DBXMLWriter
Parameters:
pText: char const *
pRect: CRect
pLoc: CPoint
AddBitMapTag(pPath, pRect, pLoc)
Class : DBXMLWriter
Parameters:
pPath: char const *
pRect: CRect
pLoc: CPoint
AddFillTag(pStart, pStyle, pHatch)
Class : DBXMLWriter
Parameters:
pStart: CPoint
pStyle: enum DboValue::FillStyleT
pHatch: enum DboValue::HatchStyleT
AddBoxInstTag(pName, pLoc, pRot, pUpperLeft, pLowerRight, pStyle,
Class : DBXMLWriter
pWidth, pFill, pHatch)
Class : DBXMLWriter
Parameters:
pName: char const *
pLoc: CPoint
pRot: enum DboValue::RotationT

---

pUpperLeft: CPoint
pLowerRight: CPoint
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pFill: enum DboValue::FillStyleT
pHatch: enum DboValue::HatchStyleT
AddLineInstTag(pName, pLoc, pRot, pStart, pEnd, pStyle, pWidth)
Class : DBXMLWriter
Parameters:
pName: char const *
pLoc: CPoint
pRot: enum DboValue::RotationT
pStart: CPoint
pEnd: CPoint
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
AddArcInstTag(pName, pLoc, pRot, pRect, pStart, pEnd, pStyle, pWidth)
Class : DBXMLWriter
Parameters:
pName: char const *
pLoc: CPoint
pRot: enum DboValue::RotationT
pRect: CRect
pStart: CPoint
pEnd: CPoint
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
AddEllipseInstTag(pName, pLoc, pRot, pRect, pStyle, pWidth, pFill, lHatch)
Class : DBXMLWriter
Parameters:
pName: char const *
pLoc: CPoint
pRot: enum DboValue::RotationT
pRect: CRect
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pFill: enum DboValue::FillStyleT

---

lHatch: enum DboValue::HatchStyleT
AddPolygonInstTag(pName, pLoc, pRot, pStyle, pWidth, pFill, pHatch)
Class : DBXMLWriter
Parameters:
pName: char const *
pLoc: CPoint
pRot: enum DboValue::RotationT
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pFill: enum DboValue::FillStyleT
pHatch: enum DboValue::HatchStyleT
AddPolylineInstTag(pName, pStyle, pWidth, pLoc, pRot)
Class : DBXMLWriter
Parameters:
pName: char const *
pStyle: enum DboValue::LineStyleT
pWidth: enum DboValue::LineWidthT
pLoc: CPoint
pRot: enum DboValue::RotationT
AddCommentTextInstTag(pRect, pTxt, pLocation, pRot, pFont)
Class : DBXMLWriter
Parameters:
pRect: CRect
pTxt: char const *
pLocation: CPoint
pRot: enum DboValue::RotationT
pFont: LOGFONT
AddTextFontTag(pFont)
Class : DBXMLWriter
Parameters:
pFont: LOGFONT
AddBitMapInstTag(pRect)
Class : DBXMLWriter
Parameters:
pRect: CRect

---

AddOccurrencesTag()
Class : DBXMLWriter
Parameters:
AddInstOccTag(pPathName)
Class : DBXMLWriter
Parameters:
pPathName: char const *
AddNetOccTag(pPathName)
Class : DBXMLWriter
Parameters:
pPathName: char const *
AddPortOccTag(pPathName)
Class : DBXMLWriter
Parameters:
pPathName: char const *
AddOffPageOccTag(pPathName)
Class : DBXMLWriter
Parameters:
pPathName: char const *
AddTitleBlockOccTag(pPathName)
Class : DBXMLWriter
Parameters:
pPathName: char const *
END class DBXMLWriter
START class DboExtBlobNode
InitBlob(pBlobNode) : returns BlobNodeData_t
Class : DboExtBlobNode
Parameters:
pBlobNode: DboExtBlobNode::BlobNodeData_t *
GetType() : returns char

---

Class : DboExtBlobNode
Parameters:
SetType(pType)
Class : DboExtBlobNode
Parameters:
pType: char const *
GetVersion() : returns char
Class : DboExtBlobNode
Parameters:
SetVersion(pVersion)
Class : DboExtBlobNode
Parameters:
pVersion: char const *
GetId() : returns BlobId_t
Class : DboExtBlobNode
Parameters:
SetId(pId)
Class : DboExtBlobNode
Parameters:
pId: DboExtBlobNode::BlobId_t
GetSequence() : returns BlobSeq_t
Class : DboExtBlobNode
Parameters:
SetSequence(pSeq)
Class : DboExtBlobNode
Parameters:
pSeq: DboExtBlobNode::BlobSeq_t
GetBitmap() : returns BlobBitmap_t
Class : DboExtBlobNode
Parameters:
SetBitmap(pBitmap)

---

Class : DboExtBlobNode
Parameters:
pBitmap: DboExtBlobNode::BlobBitmap_t
GetStreamSize() : returns size_t
Class : DboExtBlobNode
Parameters:
SetStreamSize(pSize)
Class : DboExtBlobNode
Parameters:
pSize: size_t
GetNodeDataSize() : returns size_t
Class : DboExtBlobNode
Parameters:
GetStream() : returns ExtDataBytePtrT
Class : DboExtBlobNode
Parameters:
SetStream(pStream)
Class : DboExtBlobNode
Parameters:
pStream: ExtDataBytePtrT
LoadNodeData(pNodeData) : returns bool
Class : DboExtBlobNode
Parameters:
pNodeData: DboExtBlobNode::BlobNodeData_t *
StoreNodeData(pBuffer) : returns size_t
Class : DboExtBlobNode
Parameters:
pBuffer: ExtDataBytePtrT
END class DboExtBlobNode
START class DboExtCentral

---

sGetInstance() : returns DboExtCentral
Class : DboExtCentral
CopyExtensions(pSource, pDest) : returns bool
Class : DboExtCentral
Parameters:
pSource: DboBaseObject *
pDest: DboBaseObject *
CreateExtension(pObject, pType) : returns DboExtension
Class : DboExtCentral
Parameters:
pObject: DboBaseObject *
pType: enum DboExtensionTypeT
CreateBlobExtension(pObject, pType, pSubType, pVersion) : returns DboExtBlobNode
Class : DboExtCentral
Parameters:
pObject: DboBaseObject *
pType: enum DboExtensionTypeT
pSubType: char const *
pVersion: char const *
SetExtension(pObject, pExtension) : returns bool
Class : DboExtCentral
Parameters:
pObject: DboBaseObject *
pExtension: DboExtension *
GetExtension(pObject, pType) : returns DboExtension
Class : DboExtCentral
Parameters:
pObject: DboBaseObject *
pType: enum DboExtensionTypeT
GetBlobExtension(pObject, pSubType, pVersion) : returns BlobListT
Class : DboExtCentral
Parameters:
pObject: DboBaseObject *
pSubType: char const *

---

pVersion: char const *
RegisterBlobHandler(pType, pVersion, pHandler) : returns bool
Class : DboExtCentral
Parameters:
pType: char const *
pVersion: char const *
pHandler: DboExtBlobHandler *
END class DboExtCentral
DboExtCentral_sGetInstance() : returns DboExtCentral
START class Psp2CapBaseInfo
AddSub(sub)
Class : Psp2CapBaseInfo
Parameters:
sub: Psp2CapBaseInfo *
GetSub(i) : returns Psp2CapBaseInfo
Class : Psp2CapBaseInfo
Parameters:
i: int
GetNumSubs() : returns int
Class : Psp2CapBaseInfo
Parameters:
InsertProp(propname, value)
Class : Psp2CapBaseInfo
Parameters:
propname: CString
value: CString
GetName() : returns CString
Class : Psp2CapBaseInfo
Parameters:
GetType() : returns PSP2CAP_OBJ_T

---

Class : Psp2CapBaseInfo
Parameters:
GetPropValue(propName) : returns CString
Class : Psp2CapBaseInfo
Parameters:
propName: CString
IsPlaced() : returns int
Class : Psp2CapBaseInfo
Parameters:
IsPart() : returns int
Class : Psp2CapBaseInfo
Parameters:
WriteChar(buffer, index, size, ch)
Class : Psp2CapBaseInfo
Parameters:
buffer: unsigned char *
index: int &
size: int
ch: char
WriteString(buffer, index, size, str)
Class : Psp2CapBaseInfo
Parameters:
buffer: unsigned char *
index: int &
size: int
str: CString
ReadChar(buffer, index, size) : returns char
Class : Psp2CapBaseInfo
Parameters:
buffer: unsigned char *
index: int &
size: int
ReadString(buffer, index, size) : returns CString

---

Class : Psp2CapBaseInfo
Parameters:
buffer: unsigned char *
index: int &
size: int
GetStorageSize() : returns long
Class : Psp2CapBaseInfo
Parameters:
WriteToStream(buffer, index, size)
Class : Psp2CapBaseInfo
Parameters:
buffer: unsigned char *
index: int &
size: int
ReadFromStream(buffer, index, size) : returns bool
Class : Psp2CapBaseInfo
Parameters:
buffer: unsigned char *
index: int &
size: int
GetSubsIter() : returns Psp2CapBaseInfoSubsIter
Class : Psp2CapBaseInfo
Parameters:
END class Psp2CapBaseInfo
Psp2CapBaseInfo_WriteChar(buffer, index, size, ch)
Parameters:
buffer: unsigned char *
index: int &
size: int
ch: char
Psp2CapBaseInfo_WriteString(buffer, index, size, str)
Parameters:
buffer: unsigned char *