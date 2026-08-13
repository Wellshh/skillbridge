# Class: DboTclHelper

Parameters:
pTimeOut: unsigned long
DboPathMgr_sGetFullPath(pPath) : returns std::string
Parameters:
pPath: char const *
DboPathMgr_sIsReadOnly(pPath) : returns bool
Parameters:
pPath: char const *
sForgetReadOnlyAttribute(pPath = None)
Parameters:
pPath: char const *
DboPathMgr_sForgetReadOnlyAttribute()
sDumpToSessionLog(pPath = None)
Parameters:
pPath: char const *
DboPathMgr_sDumpToSessionLog()
DboPathMgr_sSetLegacySaveAs(bVal)
Parameters:
bVal: int
DboPathMgr_sGetLegacySaveAs() : returns int
START class DboTclHelper
sMakeStdVector() : returns std::vector<(std::string)>
Class : DboTclHelper
sGetConstCharPtrFromVector(pVector, index) : returns char
Class : DboTclHelper
Parameters:
pVector: std::vector< std::string > &
index: int

---

sGetVectorSize(pVector) : returns int
Class : DboTclHelper
Parameters:
pVector: std::vector< std::string > &
sPushBackToVector(pVector, arg1)
Class : DboTclHelper
Parameters:
pVector: std::vector< std::string > &
arg2: char const *
sRemoveFromVector(pVector, index)
Class : DboTclHelper
Parameters:
pVector: std::vector< std::string > &
index: int
sMakeStdStr(pVal) : returns std::string
Class : DboTclHelper
Parameters:
pVal: char const *
sMakeInt() : returns int
Class : DboTclHelper
sGetInt(pVal) : returns int
Class : DboTclHelper
Parameters:
pVal: int &
sMakeULong() : returns unsigned long
Class : DboTclHelper
sGetULong(pVal) : returns unsigned long
Class : DboTclHelper
Parameters:
pVal: unsigned long &
sMakeCString() : returns CString
Class : DboTclHelper

---

sMakeCString(pVal) : returns CString
Class : DboTclHelper
Parameters:
pVal: char const *
sMakeCString(pVal) : returns CString
Class : DboTclHelper
Parameters:
pVal: CString
sGetConstCharPtr(pVal) : returns char
Class : DboTclHelper
Parameters:
pVal: std::string &
sGetConstCharPtr(pVal) : returns char
Class : DboTclHelper
Parameters:
pVal: CString &
sDeleteCString(pStr)
Class : DboTclHelper
Parameters:
pStr: CString *
sMakeDboValue() : returns DboValue
Class : DboTclHelper
sMakeDboValueType() : returns ValueType
Class : DboTclHelper
sMakeCRect(x1, y1, x2, y2) : returns CRect
Class : DboTclHelper
Parameters:
x1: int
y1: int
x2: int
y2: int

---

sMakeCRect() : returns CRect
Class : DboTclHelper
sGetCRectTopLeft(arg0) : returns CPoint
Class : DboTclHelper
Parameters:
arg1: CRect &
sGetCRectBottomRight(arg0) : returns CPoint
Class : DboTclHelper
Parameters:
arg1: CRect &
sDeleteCRect(pRect)
Class : DboTclHelper
Parameters:
pRect: CRect *
sMakeCPoint(x, y) : returns CPoint
Class : DboTclHelper
Parameters:
x: int
y: int
sMakeCPoint() : returns CPoint
Class : DboTclHelper
sGetCPointX(arg0) : returns int
Class : DboTclHelper
Parameters:
arg1: CPoint &
sGetCPointY(arg0) : returns int
Class : DboTclHelper
Parameters:
arg1: CPoint &
sDeleteCPoint(pPoint)
Class : DboTclHelper
Parameters:

---

pPoint: CPoint *
sGetCSizeX(rSize) : returns int
Class : DboTclHelper
Parameters:
rSize: CSize &
sGetCSizeY(rSize) : returns int
Class : DboTclHelper
Parameters:
rSize: CSize &
sMakeLOGFONT() : returns LOGFONT
Class : DboTclHelper
sMakeLOGFONT(lfFaceName, lfHeight, lfWidth, lfEscapement, lfOrientation,
Class : DboTclHelper
lfWeight, lfItalic, lfUnderline, lfStrikeOut,
Class : DboTclHelper
lfCharSet, lfOutPrecision, lfClipPrecision,
Class : DboTclHelper
lfQuality, lfPitchAndFamily) : returns LOGFONT
Class : DboTclHelper
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
lfClipPrecision: unsigned char
lfQuality: unsigned char
lfPitchAndFamily: unsigned char
sMakeBitMapData(BoundingBox, Location, bmpFile) : returns DboBitMapData

---

Class : DboTclHelper
Parameters:
BoundingBox: CRect
Location: CPoint
bmpFile: char *
sMakeBitmap(pBitMapStruct, pGrObj, pPage, pRotation, status) : returns DboBitMap
Class : DboTclHelper
Parameters:
pBitMapStruct: DboBitMapData *
pGrObj: DboGraphicObject *
pPage: DboPage *
pRotation: enum DboValue::RotationT
status: DboState &
sGetBase64ImageData(pDboBitmap, rStatus) : returns char
Class : DboTclHelper
Parameters:
pDboBitmap: DboBitMap *
rStatus: DboState &
sCastPtr(pName, pFrom, pTo) : returns char
Class : DboTclHelper
Parameters:
pName: char const *
pFrom: char const *
pTo: char const *
sCreateSession() : returns DboSession
Class : DboTclHelper
sDeleteSession(pSession)
Class : DboTclHelper
Parameters:
pSession: DboSession *
sReleaseAllCreatedPtrs()
Class : DboTclHelper
sSetDboObjectInProcess(pObject)

---

Class : DboTclHelper
Parameters:
pObject: DboBaseObject *
sGetDboObjectInProcess() : returns DboBaseObject
Class : DboTclHelper
sEvalPage(pPage)
Class : DboTclHelper
Parameters:
pPage: DboPage *
sLockProperty(pObj, propName, lockFlag, preTrigger, postTrigger)
Class : DboTclHelper
Parameters:
pObj: DboBaseObject *
propName: CString
lockFlag: int
preTrigger: char *
postTrigger: char *
CleanOrCADRegistry(key)
Class : DboTclHelper
Parameters:
key: char *
ReRegisterOrCADPlugins()
Class : DboTclHelper
END class DboTclHelper
DboTclHelper_sMakeStdVector() : returns std::vector<(std::string)>
DboTclHelper_sGetConstCharPtrFromVector(pVector, index) : returns char
Parameters:
pVector: std::vector< std::string > &
index: int
DboTclHelper_sGetVectorSize(pVector) : returns int
Parameters: