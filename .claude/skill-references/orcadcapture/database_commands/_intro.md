# Appendix B: Database Commands List

DboLib_sGetDefaultPinNameFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPinNumberFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPartReferenceFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultNoConnectFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultERCFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultBookMarkFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPowerFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultOffPageConnectorFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboLib_sGetDefaultPortFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPartValueFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPropertyFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultDrawnInstNameFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultAliasFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultCommentFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultTitleBlockFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultBorderFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboLib_sGetDefaultNetNameFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultStimulusSymbolFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPSpiceSourceSymbolFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPSpiceSimulationDirectiveSymbolFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPSpiceABMSymbolFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultParameterFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultOptimizerFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultGraphicObjectFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetTempName(pszName, pDir) : returns CString
Parameters:
pszName: char const *
pDir: DboDirectory *
DboLib_sGetTempName(pszName, pDir, nLength) : returns CString
Parameters:
pszName: char const *
pDir: DboDirectory *
nLength: int
DboLib_SizeOfLibTitle() : returns int
DboLib_LibTitle() : returns char
DboLib_sGetTimeFormat(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sSplitName(pszName, BaseName, Uniquifier, Extension)
Parameters:
pszName: char const *
BaseName: CString &
Uniquifier: CString &
Extension: CString &
DboLib_sEquivalentNames(name1, name2, status) : returns int
Parameters:
name1: CString &
name2: CString &
status: DboState &
DboLib_sGetNormalizedObjectName(name, NormalizedName) : returns DboState
Parameters:
name: CString &
NormalizedName: CString &
DboLib_sGetUnNormalizedObjectName(normalizeName, name) : returns DboState

---

DboGraphicBoxInst_sGetLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBoxInst_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *
status: DboState &

---

obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicEllipseInst_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicPolygonInst(x) : returns DboGraphicPolygonInst
Parameters:

---

status: DboState &
DboPartInst_sGetReference(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_sGetPartValue(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_sGetIsPrimitive(obj, status) : returns PrimitiveTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_sGetContentsViewType(obj, status) : returns ViewTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_sGetContentsViewName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_sGetContentsLibName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_sGetPowerPinsAreVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPartInst_PositionDisplayProp(pPage, pProp) : returns int
Parameters:
pPage: DboPage *

---

DboPortInst_sGetPinType(obj, status) : returns PinTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsLong(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsClock(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsDot(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsLeftPointing(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsRightPointing(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsShared(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboPortInst_sGetIsGlobal(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsNetStyle(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetIsNoConnect(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetStartPointX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetStartPointY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetHotSpotX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetHotSpotY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInst_sGetNetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &

---

status: DboState &
DboDisplayProp_sGetRotation(obj, status) : returns RotationT
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sGetFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sGetDisplayType(obj, status) : returns DisplayTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayProp_sSetName(obj, name) : returns DboState
Parameters:
obj: DboBaseObject *
name: CString &
DboDisplayProp_sSetLocationX(obj, x) : returns DboState
Parameters:
obj: DboBaseObject *
x: int
DboDisplayProp_sSetLocationY(obj, y) : returns DboState
Parameters:
obj: DboBaseObject *
y: int
DboDisplayProp_sSetRotation(obj, rotation) : returns DboState
Parameters:
obj: DboBaseObject *

---

DboInstOccurrence_sGetDesignator(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetReferenceDesignator(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetPartValue(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetIsPrimitive(obj, status) : returns PrimitiveTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetContentsViewType(obj, status) : returns ViewTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetContentsViewName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboInstOccurrence_sGetContentsLibName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &

---

status: DboState &
DboTitleBlock_sGetDesignCreateDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetDesignModifyDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetSchematicCreateDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetSchematicModifyDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetPageCreateDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetPageModifyDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetDesignCreateTime(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetDesignModifyTime(obj, status) : returns CString
Parameters:
obj: DboBaseObject *

---

status: DboState &
DboTitleBlock_sGetPageCreateTime(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetPageModifyTime(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetSchematicCreateTime(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetSchematicModifyTime(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetPageCount(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetPageSize(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetSchematicName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetPageNumber(obj, status) : returns int
Parameters:
obj: DboBaseObject *

---

DboBox_sGetLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboBox_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *
status: DboState &

---

pVector: std::vector< std::string > &
DboTclHelper_sPushBackToVector(pVector, arg1)
Parameters:
pVector: std::vector< std::string > &
arg2: char const *
DboTclHelper_sRemoveFromVector(pVector, index)
Parameters:
pVector: std::vector< std::string > &
index: int
DboTclHelper_sMakeStdStr(pVal) : returns std::string
Parameters:
pVal: char const *
DboTclHelper_sMakeInt() : returns int
DboTclHelper_sGetInt(pVal) : returns int
Parameters:
pVal: int &
DboTclHelper_sMakeULong() : returns unsigned long
DboTclHelper_sGetULong(pVal) : returns unsigned long
Parameters:
pVal: unsigned long &
sMakeCString() : returns CString
sMakeCString(pVal) : returns CString
Parameters:
pVal: char const *
DboTclHelper_sMakeCString(pVal) : returns CString
Parameters:
pVal: CString
sGetConstCharPtr(pVal) : returns char
Parameters:

---

pVal: std::string &
DboTclHelper_sGetConstCharPtr(pVal) : returns char
Parameters:
pVal: CString &
DboTclHelper_sDeleteCString(pStr)
Parameters:
pStr: CString *
DboTclHelper_sMakeDboValue() : returns DboValue
DboTclHelper_sMakeDboValueType() : returns ValueType
sMakeCRect(x1, y1, x2, y2) : returns CRect
Parameters:
x1: int
y1: int
x2: int
y2: int
DboTclHelper_sMakeCRect() : returns CRect
DboTclHelper_sGetCRectTopLeft(arg0) : returns CPoint
Parameters:
arg1: CRect &
DboTclHelper_sGetCRectBottomRight(arg0) : returns CPoint
Parameters:
arg1: CRect &
DboTclHelper_sDeleteCRect(pRect)
Parameters:
pRect: CRect *
sMakeCPoint(x, y) : returns CPoint
Parameters:
x: int
y: int

---

DboTclHelper_sMakeCPoint() : returns CPoint
DboTclHelper_sGetCPointX(arg0) : returns int
Parameters:
arg1: CPoint &
DboTclHelper_sGetCPointY(arg0) : returns int
Parameters:
arg1: CPoint &
DboTclHelper_sDeleteCPoint(pPoint)
Parameters:
pPoint: CPoint *
DboTclHelper_sGetCSizeX(rSize) : returns int
Parameters:
rSize: CSize &
DboTclHelper_sGetCSizeY(rSize) : returns int
Parameters:
rSize: CSize &
sMakeLOGFONT() : returns LOGFONT
DboTclHelper_sMakeLOGFONT(lfFaceName, lfHeight, lfWidth, lfEscapement, lfOrientation,
lfWeight, lfItalic, lfUnderline, lfStrikeOut,
lfCharSet, lfOutPrecision, lfClipPrecision,
lfQuality, lfPitchAndFamily) : returns LOGFONT
Parameters:
lfFaceName: char *
lfHeight: long
lfWidth: long
lfEscapement: long
lfOrientation: long
lfWeight: long
lfItalic: unsigned char
lfUnderline: unsigned char
lfStrikeOut: unsigned char
lfCharSet: unsigned char
lfOutPrecision: unsigned char

---

lfClipPrecision: unsigned char
lfQuality: unsigned char
lfPitchAndFamily: unsigned char
DboTclHelper_sMakeBitMapData(BoundingBox, Location, bmpFile) : returns DboBitMapData
Parameters:
BoundingBox: CRect
Location: CPoint
bmpFile: char *
DboTclHelper_sMakeBitmap(pBitMapStruct, pGrObj, pPage, pRotation, status) : returns DboBitMap
Parameters:
pBitMapStruct: DboBitMapData *
pGrObj: DboGraphicObject *
pPage: DboPage *
pRotation: enum DboValue::RotationT
status: DboState &
DboTclHelper_sGetBase64ImageData(pDboBitmap, rStatus) : returns char
Parameters:
pDboBitmap: DboBitMap *
rStatus: DboState &
DboTclHelper_sCastPtr(pName, pFrom, pTo) : returns char
Parameters:
pName: char const *
pFrom: char const *
pTo: char const *
DboTclHelper_sCreateSession() : returns DboSession
DboTclHelper_sDeleteSession(pSession)
Parameters:
pSession: DboSession *
DboTclHelper_sReleaseAllCreatedPtrs()
DboTclHelper_sSetDboObjectInProcess(pObject)
Parameters:
pObject: DboBaseObject *

---

Parameters:
pXmlPathIn: char const *
pOlbPathOut: char const *
XMATIC_XML2OLB(pXmlPathIn) : returns DboState
Parameters:
pXmlPathIn: char const *
XML2DSN(pXmlPathIn, pDsnPathOut = None, pAppendMode = False,
pLogFilePath = None) : returns DboState
Parameters:
pXmlPathIn: char const *
pDsnPathOut: char const *
pAppendMode: bool
pLogFilePath: char const *
XML2DSN(pXmlPathIn, pDsnPathOut = None, pAppendMode = False) : returns DboState
Parameters:
pXmlPathIn: char const *
pDsnPathOut: char const *
pAppendMode: bool
XML2DSN(pXmlPathIn, pDsnPathOut = None) : returns DboState
Parameters:
pXmlPathIn: char const *
pDsnPathOut: char const *
XMATIC_XML2DSN(pXmlPathIn) : returns DboState
Parameters:
pXmlPathIn: char const *
OLB2XML(pOlbPathIn, pXmlPathOut, pXsdPath = None, pLogFilePath = None) : returns DboState
Parameters:
pOlbPathIn: char const *
pXmlPathOut: char const *
pXsdPath: char const *
pLogFilePath: char const *
OLB2XML(pOlbPathIn, pXmlPathOut, pXsdPath = None) : returns DboState
Parameters:

---

pOlbPathIn: char const *
pXmlPathOut: char const *
pXsdPath: char const *
XMATIC_OLB2XML(pOlbPathIn, pXmlPathOut) : returns DboState
Parameters:
pOlbPathIn: char const *
pXmlPathOut: char const *
DSN2XML(pDsnPathIn, pXmlPathOut, pXsdPath = None, pLogFilePath = None) : returns DboState
Parameters:
pDsnPathIn: char const *
pXmlPathOut: char const *
pXsdPath: char const *
pLogFilePath: char const *
DSN2XML(pDsnPathIn, pXmlPathOut, pXsdPath = None) : returns DboState
Parameters:
pDsnPathIn: char const *
pXmlPathOut: char const *
pXsdPath: char const *
XMATIC_DSN2XML(pDsnPathIn, pXmlPathOut) : returns DboState
Parameters:
pDsnPathIn: char const *
pXmlPathOut: char const *
XMATIC_ExportNetGroupXML(pDsnPathIn, pXmlPathOut, pXsdPath, pLogFilePath) : returns DboState
Parameters:
pDsnPathIn: char const *
pXmlPathOut: char const *
pXsdPath: char const *
pLogFilePath: char const *
XMATIC_CAP2EDIF(pCapPathIn, pEdifPathOut, pCfgPath) : returns bool
Parameters:
pCapPathIn: char const *
pEdifPathOut: char const *
pCfgPath: char const *