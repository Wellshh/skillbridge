# Appendix A: Capture Commands List

18 Appendix A: Capture Commands List
SetDesignDumpFile(pDesignName)
Parameters:
pDesignName: char const *
Paste(x, y)
Parameters:
x: double
y: double
SelectObject(x, y, boolvalue3)
Parameters:
x: double
y: double
boolvalue3: char const *
UnSelectObject(x, y)
Parameters:
x: double
y: double
UnSelectAll()
SelectBlock(x1, x2, y1, y2, boolvalue5)
Parameters:
x1: double
x2: double
y1: double
y2: double
boolvalue5: char const *
SelectAll()
FindParts(value, boolvalue2)
Parameters:
value: char const *

---

boolvalue2: char const *
FindNets(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
FindOffPageConnectors(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
FindHierarchicalPorts(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
FindBookMarks(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
FindDRCMarks(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
FindText(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
Cut()
Copy()
Delete()
Move(x, y, boolvalue3)
Parameters:

---

x: double
y: double
boolvalue3: char const *
Duplicate(x, y)
Parameters:
x: double
y: double
Drag(x, y, boolvalue3)
Parameters:
x: double
y: double
boolvalue3: char const *
Rotate()
MirrorVertical()
MirrorHorizontal()
SetColor(nColorId)
Parameters:
nColorId: int
SetLineStyle(nLineStyleId)
Parameters:
nLineStyleId: int
SetLineWidth(nLineWidthId)
Parameters:
nLineWidthId: int
SetFillStyle(nFillStyleId)
Parameters:
nFillStyleId: int
SetHatchStyle(nFillStyleId)
Parameters:
nFillStyleId: int

---

SetFont(Facename, nHeight, boolvalue3, boolvalue4)
Parameters:
Facename: char const *
nHeight: double
boolvalue3: char const *
boolvalue4: char const *
SetFontEx(Facename, nHeight, nWidth, nEscapement, nOrientation,
boolvalue6, boolvalue7, boolvalue8, boolvalue9,
nCharSet, nOutPrecision, nClipPrecision,
nQuality, nPitchAndFamily)
Parameters:
Facename: char const *
nHeight: double
nWidth: double
nEscapement: double
nOrientation: double
boolvalue6: char const *
boolvalue7: char const *
boolvalue8: char const *
boolvalue9: char const *
nCharSet: int
nOutPrecision: int
nClipPrecision: int
nQuality: int
nPitchAndFamily: int
Group()
Ungroup()
PlacePart(x, y, libName, pkgName, device, boolvalue6)
Parameters:
x: double
y: double
libName: char const *
pkgName: char const *
device: char const *
boolvalue6: char const *

---

PlacePartWithDialog(x, y)
Parameters:
x: double
y: double
ReplacePart(libName, pkgName, partName, device)
Parameters:
libName: char const *
pkgName: char const *
partName: char const *
device: char const *
PlaceWire(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceBus(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceBusEntry(x, y, boolvalue3)
Parameters:
x: double
y: double
boolvalue3: char const *
PlaceJunction(x, y)
Parameters:
x: double
y: double
PlaceNetAlias(x, y, netAlias)
Parameters:

---

x: double
y: double
netAlias: char const *
PlaceNetAliasWithDialog(x, y)
Parameters:
x: double
y: double
PlacePower(x, y, libName, symbolName, PowerName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
PowerName: char const *
PlaceNetgroupPower(x, y, libName, symbolName, OffPageName, NetgroupOwnerName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
OffPageName: char const *
NetgroupOwnerName: char const *
PlacePowerWithDialog(x, y)
Parameters:
x: double
y: double
PlaceGround(x, y, libName, symbolName, GroundName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
GroundName: char const *
PlaceNetgroupGround(x, y, libName, symbolName, OffPageName, NetgroupOwnerName)

---

Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
OffPageName: char const *
NetgroupOwnerName: char const *
PlaceGroundWithDialog(x, y)
Parameters:
x: double
y: double
PlacePort(x, y, libName, symbolName, PortName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
PortName: char const *
PlaceNetgroupPort(x, y, libName, symbolName, OffPageName, NetgroupOwnerName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
OffPageName: char const *
NetgroupOwnerName: char const *
PlacePortWithDialog(x, y)
Parameters:
x: double
y: double
PlaceOffPage(x, y, libName, symbolName, OffPageName)
Parameters:
x: double
y: double
libName: char const *

---

symbolName: char const *
OffPageName: char const *
PlaceNetgroupOffPage(x, y, libName, symbolName, OffPageName, NetgroupOwnerName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
OffPageName: char const *
NetgroupOwnerName: char const *
PlaceOffPageWithDialog(x, y)
Parameters:
x: double
y: double
PlaceBlock(x1, y1, x2, y2, libName, viewName, instName, primitiveType)
Parameters:
x1: double
y1: double
x2: double
y2: double
libName: char const *
viewName: char const *
instName: char const *
primitiveType: char const *
PlaceBlockWithDialog(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlacePin(x, y, pinName, pinType, boolvalue5)
Parameters:
x: double
y: double
pinName: char const *

---

pinType: char const *
boolvalue5: char const *
PlacePinWithDialog(x, y)
Parameters:
x: double
y: double
PlaceNoConnect(x, y)
Parameters:
x: double
y: double
PlaceTitleBlock(x, y, libName, symbolName, titleblockName)
Parameters:
x: double
y: double
libName: char const *
symbolName: char const *
titleblockName: char const *
PlaceTitleBlockWithDialog(x, y)
Parameters:
x: double
y: double
PlaceBookMark(x, y, markName)
Parameters:
x: double
y: double
markName: char const *
PlaceBookMarkWithDialog(x, y)
Parameters:
x: double
y: double
PlaceText(x1, y1, x2, y2, commentText)
Parameters:
x1: double

---

y1: double
x2: double
y2: double
commentText: char const *
PlaceTextWithDialog(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceLine(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceRectangle(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceEllipse(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceArc(x1, y1, x2, y2, x3, y3, x4, y4)
Parameters:
x1: double
y1: double
x2: double
y2: double
x3: double

---

y3: double
x4: double
y4: double
PlacePolyline(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceNextPolylinePoint(x, y)
Parameters:
x: double
y: double
PlaceBezier(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceNextBezierPoint(x, y)
Parameters:
x: double
y: double
PlacePolygon(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
PlaceNextPolygonPoint(x, y)
Parameters:
x: double
y: double

---

PlacePicture(x, y, fileName)
Parameters:
x: double
y: double
fileName: char const *
EndPlace()
ViewPalette(boolvalue1)
Parameters:
boolvalue1: char const *
ViewToolbar(boolvalue1)
Parameters:
boolvalue1: char const *
ViewStatusBar(boolvalue1)
Parameters:
boolvalue1: char const *
ViewGrid(boolvalue1)
Parameters:
boolvalue1: char const *
ViewGridReference(boolvalue1)
Parameters:
boolvalue1: char const *
GoToRelative(x, y)
Parameters:
x: double
y: double
GoToAbsolute(x, y)
Parameters:
x: double
y: double
GoToGridReference(x, y)
Parameters:

---

x: char const *
y: char const *
GoToBookMark(markName)
Parameters:
markName: char const *
ZoomIn()
ZoomOut()
ZoomArea(x1, y1, x2, y2)
Parameters:
x1: double
y1: double
x2: double
y2: double
ZoomAll()
ZoomSelection()
ZoomScale(nscale)
Parameters:
nscale: int
SetProperty(propName, propValue)
Parameters:
propName: char const *
propValue: char const *
SetOccProperty(propName, propValue)
Parameters:
propName: char const *
propValue: char const *
GetProperty(propName)
Parameters:
propName: char const *

---

GetOccProperty(propName)
Parameters:
propName: char const *
PrintGrid()
SetDisplayType(DisplayName, DisplayValue)
Parameters:
DisplayName: char const *
DisplayValue: int
DisplayProperty(propName, Facename, nHeight, boolvalue4, boolvalue5,
ncolorId, nrotation)
Parameters:
propName: char const *
Facename: char const *
nHeight: int
boolvalue4: char const *
boolvalue5: char const *
ncolorId: int
nrotation: int
DisplayPropertyEx(propName, Facename, nHeight, nWidth, nEscapement, nOrientation,
boolvalue7, boolvalue8, boolvalue9,
boolvalue10, nCharSet, nOutPrecision, nClipPrecision,
nQuality, nPitchAndFamily, ncolorId,
nrotation)
Parameters:
propName: char const *
Facename: char const *
nHeight: int
nWidth: int
nEscapement: int
nOrientation: int
boolvalue7: char const *
boolvalue8: char const *
boolvalue9: char const *
boolvalue10: char const *
nCharSet: int
nOutPrecision: int

---

nClipPrecision: int
nQuality: int
nPitchAndFamily: int
ncolorId: int
nrotation: int
RemoveProperty(propName)
Parameters:
propName: char const *
RemoveOccProperty(propName)
Parameters:
propName: char const *
RemoveDisplayProperty(propName)
Parameters:
propName: char const *
SwitchTab(tabName)
Parameters:
tabName: char const *
AddProperty(PathName, PropName, Propvalue)
Parameters:
PathName: char const *
PropName: char const *
Propvalue: char const *
DeleteProperty(PropName, PathName)
Parameters:
PropName: char const *
PathName: char const *
ModifyProperty(PathName, Property, Value, occ)
Parameters:
PathName: char const *
Property: char const *
Value: char const *
occ: int

---

ShowSpreadsheet()
FindPins(value, boolvalue2)
Parameters:
value: char const *
boolvalue2: char const *
GetSelectedObjects() : returns Tcl_Obj
PlaceNetgroup()
ViewNetgroup(NetgroupName)
Parameters:
NetgroupName: char *
AddMemberToNetgroup(NetGroupName, NetgroupMemberName, memberType)
Parameters:
NetGroupName: char const *
NetgroupMemberName: char const *
memberType: char const *
DeleteNetgroup(NetgroupName)
Parameters:
NetgroupName: char *
DeleteNetgroupMember(NetgroupName, NetgroupMemberToBeDeleted)
Parameters:
NetgroupName: char *
NetgroupMemberToBeDeleted: char *
RenameNetgroupMember(NetgroupName, NetgroupMemberToBeRenamed, NewMemberName)
Parameters:
NetgroupName: char *
NetgroupMemberToBeRenamed: char *
NewMemberName: char *
DumpStatusBar()
PlaceNetgroupBlock(x1, y1, x2, y2, sinstName, NetgroupOwner)
Parameters:

---

x1: double
y1: double
x2: double
y2: double
sinstName: char const *
NetgroupOwner: char const *
ShowAllNetgroups()
GetActiveOpjName() : returns char
GetProductVersion() : returns char
GetToolName() : returns char
GetLicenseString() : returns char
capFindActivateWindow(objType)
Parameters:
objType: enum COrFindFilterDlg::QueryModeT
capFindAddItem(objType, pBaseObj)
Parameters:
objType: enum COrFindFilterDlg::QueryModeT
pBaseObj: DboBaseObject *
capFindSetHeader(objType)
Parameters:
objType: enum COrFindFilterDlg::QueryModeT
CapFindObjects(objType, strFindWhat) : returns Tcl_Obj
Parameters:
objType: enum COrFindFilterDlg::QueryModeT
strFindWhat: CString const &
capFindGetFindOption(optionName) : returns bool
Parameters:
optionName: char const *
capFindSetFindOption(optionName, bOptionValue)

---

Parameters:
optionName: char const *
bOptionValue: bool
capFindSaveInCSV()
capMoveMouseAndClick(x, y)
Parameters:
x: double
y: double
IsDocModified() : returns int
PlacePartToolTip(value)
Parameters:
value: int
DumpSpreadsheet(fileName)
Parameters:
fileName: char const *
CloseProject()
SelectPMItem(pValue)
Parameters:
pValue: char const *
Open(pPath)
Parameters:
pPath: char const *
GetActivePM() : returns COrCapturePMDoc
GetSelectedPMItems() : returns Tcl_Obj
NDesign()
NSchematic(pSchName)
Parameters:
pSchName: char const *

---

GetPMItemName()
GetPMItemType()
CapPdfAddMarkStart(pStartPtX, pStartPtY, pEndPtX, pEndPtY, pId, pAttributeMarkType)
Parameters:
pStartPtX: int
pStartPtY: int
pEndPtX: int
pEndPtY: int
pId: CString
pAttributeMarkType: int
CapPdfAddMarkData(pName, pValue)
Parameters:
pName: char const *
pValue: char const *
CapPdfAddMarkEnd()
CapPdfPrint(lOutDir, lOutFileName)
Parameters:
lOutDir: char const *
lOutFileName: char const *
CapPdfSetOption(lOptionName, lOptionValue)
Parameters:
lOptionName: char const *
lOptionValue: char const *
CapPdfGetOption(lOptionName) : returns char
Parameters:
lOptionName: char const *
NPage(schName, pageName)
Parameters:
schName: char const *
pageName: char const *

---

DumpPage(location)
Parameters:
location: char const *
ClearTempPackage()
SetNetPropertySearch(value)
Parameters:
value: int
GetActivePMDesign() : returns DboDesign
SyncNetgroupData()
LoadNetgroupUserData(filename)
Parameters:
filename: char const *
GetInstanceOccurrence() : returns DboInstOccurrence
GetActivePage() : returns DboPage
BringToFront()
BringForward()
SendToBack()
SendBackward()
GetLastMouseClickPointOnPage() : returns char
GetActiveView() : returns CView
SetFPViewerOption(pOptionName, pOptionValue)
Parameters:
pOptionName: char const *
pOptionValue: long
GetOptionBool(szPropName) : returns bool

---

Parameters:
szPropName: char const *
GetOptionUInt(szPropName) : returns unsigned int
Parameters:
szPropName: char const *
SetOptionUInt(szPropName, dValue) : returns char
Parameters:
szPropName: char const *
dValue: double
ClearSessionLog()
DumpSessionLog(location)
Parameters:
location: char const *
Exit()
ShowDialog(value)
Parameters:
value: int
IsSchematicViewActive() : returns bool
CapCommHandleRemoteRequest(pTclObj)
Parameters:
pTclObj: Tcl_Obj *
GetDesignDumpFile() : returns char
TclScript(fileName)
Parameters:
fileName: char const *
AddMenu(pMenuStr)
Parameters:
pMenuStr: char const *

---

TclSendKeys(pMenuStr1, pMenuStr2) : returns char
Parameters:
pMenuStr1: char const *
pMenuStr2: char const *
SetAppWindowAsParent(lChildWindowHandle)
Parameters:
lChildWindowHandle: int
GetParent(lArg)
Parameters:
lArg: long
AskUserInput(pTitle, pDefVal) : returns char
Parameters:
pTitle: char const *
pDefVal: char const *
GetEnv(pEnvKey) : returns char
Parameters:
pEnvKey: char const *
SetEnv(pEnvKey, pEnvVal)
Parameters:
pEnvKey: char const *
pEnvVal: char const *
SetOptionString(pPropName, pPropValue)
Parameters:
pPropName: char const *
pPropValue: char const *
GetOptionString(pPropName) : returns char
Parameters:
pPropName: char const *
GetIniPath() : returns char
GetMACAddresses() : returns char

---

OpenURL(pUrl, pTitle) : returns bool
Parameters:
pUrl: char const *
pTitle: char const *
OpenStartPage()
RefreshStartPage()
CapCustomDRCElectricalAddItem(strDrcName, bIsExecute, strOnOKProc, vecOptionalProp) : returns
bool
Parameters:
strDrcName: char const *
bIsExecute: bool
strOnOKProc: char const *
vecOptionalProp: std::vector< std::string > &
CapCustomDRCPhysicalAddItem(strDrcName, bIsExecute, strOnOKProc, vecOptionalProp) : returns
bool
Parameters:
strDrcName: char const *
bIsExecute: bool
strOnOKProc: char const *
vecOptionalProp: std::vector< std::string > &
capOnCustomDRCElectrical() : returns Tcl_Obj
capOnCustomDRCPhysical() : returns Tcl_Obj
capGetDRCList(btype) : returns Tcl_Obj
Parameters:
btype: OrTclAdvancedDrc::Type
capGetDRCErrorSymbol() : returns DboERCSymbol
GetDRCErrorMessage(bType) : returns CString
Parameters:
bType: bool
EnableAllButCurrentWindowCloseMenu() : returns bool

---

EnableAllWindowCloseMenu() : returns bool
capGetActiveDocument() : returns CDocument
capCloseChildViewsExceptCurrent()
START class InstWithOcc
END class InstWithOcc
AddAccessoryMenu(lVendorName, lMenuName, proc, key = None) : returns bool
Parameters:
lVendorName: char const *
lMenuName: char const *
proc: char const *
key: char const *
AddAccessoryMenu(lVendorName, lMenuName, proc) : returns bool
Parameters:
lVendorName: char const *
lMenuName: char const *
proc: char const *
PlaceNew(pLibName, pName, pDeviceIndex = 0) : returns int
Parameters:
pLibName: char const *
pName: char const *
pDeviceIndex: int
PlaceNew(pLibName, pName) : returns int
Parameters:
pLibName: char const *
pName: char const *
SelectObjectById(dbid, update = None, probe = None)
Parameters:
dbid: double
update: char *
probe: char *

---

SelectObjectById(dbid, update = None)
Parameters:
dbid: double
update: char *
SelectObjectById(dbid)
Parameters:
dbid: double
capSaveCompleteProject(strDestDir, strDestProjectName = None, bLibFiles = 0,
bOutputFiles = 1, bRefProjects = 1, bIncludeTestBench = 1)
Parameters:
strDestDir: char const *
strDestProjectName: char const *
bLibFiles: int
bOutputFiles: int
bRefProjects: int
bIncludeTestBench: int
capSaveCompleteProject(strDestDir, strDestProjectName = None, bLibFiles = 0,
bOutputFiles = 1, bRefProjects = 1)
Parameters:
strDestDir: char const *
strDestProjectName: char const *
bLibFiles: int
bOutputFiles: int
bRefProjects: int
capSaveCompleteProject(strDestDir, strDestProjectName = None, bLibFiles = 0,
bOutputFiles = 1)
Parameters:
strDestDir: char const *
strDestProjectName: char const *
bLibFiles: int
bOutputFiles: int
capSaveCompleteProject(strDestDir, strDestProjectName = None, bLibFiles = 0)
Parameters:
strDestDir: char const *

---

strDestProjectName: char const *
bLibFiles: int
capSaveCompleteProject(strDestDir, strDestProjectName = None)
Parameters:
strDestDir: char const *
strDestProjectName: char const *
capSaveCompleteProject(strDestDir)
Parameters:
strDestDir: char const *
capBatchAnnotate()
capBatchAnnotate(nScope, nUpdateType, cstrCombinedProperty, additionalCombinedProperty,
bStartAtOne, bDoNotChangePageNumber,
bChangeInstances, bIncludeNonPrimitive,
bPreserveDesignator, bPreserveUserEdits,
bAnnInstExtDsgn)
Parameters:
nScope: int
nUpdateType: int
cstrCombinedProperty: char const *
additionalCombinedProperty: char const *
bStartAtOne: int
bDoNotChangePageNumber: int
bChangeInstances: int
bIncludeNonPrimitive: int
bPreserveDesignator: int
bPreserveUserEdits: int
bAnnInstExtDsgn: int
OPage(pSchName, pPageName, pOccName = "")
Parameters:
pSchName: char const *
pPageName: char const *
pOccName: char const *
OPage(pSchName, pPageName)
Parameters:

---

pSchName: char const *
pPageName: char const *
GetPageNumber(userInput = "")
Parameters:
userInput: char const *
GetPageNumber()
AddFileToOutputFolder(lFilePath, lFileType = -1)
Parameters:
lFilePath: char const *
lFileType: int
AddFileToOutputFolder(lFilePath)
Parameters:
lFilePath: char const *
CreateTestBench(testBenchName = "")
Parameters:
testBenchName: char const *
CreateTestBench()
SetUniqeNetgroupNaming(SetUniqueBundleNaming = 0)
Parameters:
SetUniqueBundleNaming: int
SetUniqeNetgroupNaming()
SetOptionBool(szPropName = "", szPropValue = "") : returns char
Parameters:
szPropName: char const *
szPropValue: char const *
SetOptionBool(szPropName = "") : returns char
Parameters:
szPropName: char const *
SetOptionBool() : returns char

---

help(lParameters = "") : returns int
Parameters:
lParameters: char const *
help() : returns int
Shell(strAppName, strArgument = "") : returns char
Parameters:
strAppName: char const *
strArgument: char const *
Shell(strAppName) : returns char
Parameters:
strAppName: char const *
svsDiffDesigns(pSrcDesign, pDstDesign, lOccMode = 0, ECO_MODE = 0)
Parameters:
pSrcDesign: char const *
pDstDesign: char const *
lOccMode: int
ECO_MODE: int
svsDiffDesigns(pSrcDesign, pDstDesign, lOccMode = 0)
Parameters:
pSrcDesign: char const *
pDstDesign: char const *
lOccMode: int
svsDiffDesigns(pSrcDesign, pDstDesign)
Parameters:
pSrcDesign: char const *
pDstDesign: char const *
capDisplayMessageBox(message, caption, type = MB_OK) : returns char
Parameters:
message: char const *
caption: char const *
type: int

---

capDisplayMessageBox(message, caption) : returns char
Parameters:
message: char const *
caption: char const *
PlacePartEx(aLibraryName, aPackageName, aDeviceDesignator, aIsConvert,
aProp = None, aValue = None)
Parameters:
aLibraryName: char const *
aPackageName: char const *
aDeviceDesignator: char const *
aIsConvert: int
aProp: Tcl_Obj *
aValue: Tcl_Obj *
PlacePartEx(aLibraryName, aPackageName, aDeviceDesignator, aIsConvert,
aProp = None)
Parameters:
aLibraryName: char const *
aPackageName: char const *
aDeviceDesignator: char const *
aIsConvert: int
aProp: Tcl_Obj *
PlacePartEx(aLibraryName, aPackageName, aDeviceDesignator, aIsConvert)
Parameters:
aLibraryName: char const *
aPackageName: char const *
aDeviceDesignator: char const *
aIsConvert: int
capCloseChildViews(pExclude = None)
Parameters:
pExclude: CDocument *
capCloseChildViews()
START class COrFindFilterDlg
END class COrFindFilterDlg

---

START class COrCapPMIter
Next() : returns DboBaseObject
Class : COrCapPMIter
Parameters:
GetCount() : returns int
Class : COrCapPMIter
Parameters:
GetDocument() : returns COrCapturePMDoc
Class : COrCapPMIter
Parameters:
END class COrCapPMIter
START class COrPMSchematicIter(COrCapPMIter):
Next() : returns DboBaseObject
Class : COrPMSchematicIter(COrCapPMIter):
Parameters:
NextSchematic(ppSchematicOcc = None) : returns DboSchematic
Class : COrPMSchematicIter(COrCapPMIter):
Parameters:
ppSchematicOcc: DboInstOccurrencePtrProxy *
NextSchematic() : returns DboSchematic
Class : COrPMSchematicIter(COrCapPMIter):
Parameters:
sNewPMSchematicIter(pDoc, stType, bTreatPhysically) : returns COrPMSchematicIter
Class : COrPMSchematicIter(COrCapPMIter):
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
bTreatPhysically: int
END class COrPMSchematicIter(COrCapPMIter):

---

COrPMSchematicIter_sNewPMSchematicIter(pDoc, stType, bTreatPhysically) : returns
COrPMSchematicIter
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
bTreatPhysically: int
START class COrPMPageIter(COrCapPMIter):
SetSort(bSort)
Class : COrPMPageIter(COrCapPMIter):
Parameters:
bSort: int
Next() : returns DboBaseObject
Class : COrPMPageIter(COrCapPMIter):
Parameters:
NextPage(ppSchematicOcc = None) : returns DboPage
Class : COrPMPageIter(COrCapPMIter):
Parameters:
ppSchematicOcc: DboInstOccurrencePtrProxy *
NextPage() : returns DboPage
Class : COrPMPageIter(COrCapPMIter):
Parameters:
sNewPMPageIter(pDoc, stType, bTreatPhysically) : returns COrPMPageIter
Class : COrPMPageIter(COrCapPMIter):
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
bTreatPhysically: int
END class COrPMPageIter(COrCapPMIter):
COrPMPageIter_sNewPMPageIter(pDoc, stType, bTreatPhysically) : returns COrPMPageIter
Parameters:
pDoc: COrCapturePMDoc *

---

stType: enum COrCapPMIter::SelectionTypeT
bTreatPhysically: int
START class COrPMInstanceIter(COrCapPMIter):
Next() : returns DboBaseObject
Class : COrPMInstanceIter(COrCapPMIter):
Parameters:
NextInstance() : returns DboPartInst
Class : COrPMInstanceIter(COrCapPMIter):
Parameters:
sNewPMInstanceIter(pDoc, stType, bTreatPhysically) : returns COrPMInstanceIter
Class : COrPMInstanceIter(COrCapPMIter):
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
bTreatPhysically: int
END class COrPMInstanceIter(COrCapPMIter):
COrPMInstanceIter_sNewPMInstanceIter(pDoc, stType, bTreatPhysically) : returns COrPMInstanceIter
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
bTreatPhysically: int
START class COrPMOccurrenceIter(COrCapPMIter):
Next() : returns DboBaseObject
Class : COrPMOccurrenceIter(COrCapPMIter):
Parameters:
NextOccurrence() : returns DboInstOccurrence
Class : COrPMOccurrenceIter(COrCapPMIter):
Parameters:
sNewPMOccurenceIter(pDoc, stType) : returns COrPMOccurrenceIter
Class : COrPMOccurrenceIter(COrCapPMIter):

---

Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
END class COrPMOccurrenceIter(COrCapPMIter):
COrPMOccurrenceIter_sNewPMOccurenceIter(pDoc, stType) : returns COrPMOccurrenceIter
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
START class COrPMLibPackageIter(COrCapPMIter):
GetCount() : returns int
Class : COrPMLibPackageIter(COrCapPMIter):
Parameters:
Next() : returns DboBaseObject
Class : COrPMLibPackageIter(COrCapPMIter):
Parameters:
NextPackage() : returns DboPackage
Class : COrPMLibPackageIter(COrCapPMIter):
Parameters:
sNewPMLibPackageIter(pDoc, stType) : returns COrPMLibPackageIter
Class : COrPMLibPackageIter(COrCapPMIter):
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
END class COrPMLibPackageIter(COrCapPMIter):
COrPMLibPackageIter_sNewPMLibPackageIter(pDoc, stType) : returns COrPMLibPackageIter
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
START class COrPMLibSymbolIter(COrCapPMIter):

---

GetCount() : returns int
Class : COrPMLibSymbolIter(COrCapPMIter):
Parameters:
Next() : returns DboBaseObject
Class : COrPMLibSymbolIter(COrCapPMIter):
Parameters:
NextSymbol() : returns DboSymbol
Class : COrPMLibSymbolIter(COrCapPMIter):
Parameters:
sNewPMLibSymbolIter(pDoc, stType) : returns COrPMLibSymbolIter
Class : COrPMLibSymbolIter(COrCapPMIter):
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT
END class COrPMLibSymbolIter(COrCapPMIter):
COrPMLibSymbolIter_sNewPMLibSymbolIter(pDoc, stType) : returns COrPMLibSymbolIter
Parameters:
pDoc: COrCapturePMDoc *
stType: enum COrCapPMIter::SelectionTypeT