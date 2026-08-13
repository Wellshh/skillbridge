# Chapter 3: Learn Capture Database TCL

3.1 Database Object Model
This section presents to you a simplified version of the Capture database object hierarchy (with
corresponding Dbo* class names) that you must be aware of “at the minimum” before writing scripts for
database query/manipulation.
3.1.1 Design Database Object Model
Session DboSession
Design(s) DboDesign
Schematic(s) DboSchematic
Page(s) DboPage
Part instance(s) DboPlacedInst
Pin(s) DboPortInst (DboPortInstScalar, DboPortInstBus)
Hierarchical instance(s) DboDrawnInst
Pin(s) DboPortInst (DboPortInstScalar, DboPortInstBus)
Wire(s) DboWire (DboWireScalar, DboWireBus)
Alias(s) DboAlias
Net(s) DboNet(DboNetScalar, DboNetBus)
BusEntry(s) DboBusEntry
Global(s) DboGlobal
Port(s) DboPortInst (DboPortInstScalar, DboPortInstBus)
OffPage(s) DboOffPageConnector
TitleBlock(s) DboTitleBlock
DRC(s) DboERC
Rectangle(s) DboGraphicBoxInst
Line(s) DboGraphicLineInst
Ellipse(s) DboGraphicEllipseInst
Arc(s) DboGraphicArcInst
Polyline(s) DboGraphicPolylineInst
Polygon(s) DboGraphicPolygonInst
BitMap(s) DboGraphicBitMapInst
Text(s) DboGraphicCommentTextInst
InstanceOccurrence(Root) DboInstOccurrence
InstanceOccurrence(s) DboInstOccurrence
InstanceOccurrence(s) DboInstOccurrence
NetOccurrence(s) DboNetOccurrence
PortOccurrence(s) DboPortOccurrence
OffPageOccurrence(s) DboOffPageConnectorOccurrence
TitleBlockOccurrence(s) DboTitleBlockOccurrence
NetOccurrence(s) DboNetOccurrence
PortOccurrence(s) DboPortOccurrence
OffPageOccurrence(s) DboOffPageConnectorOccurrence
TitleBlockOccurrence(s) DboTitleBlockOccurrence
FlatNet(s) DboFlatNet

---

All these objects have their respective attributes’ Get and Set functions.
Additionally, all database objects have the following types of properties:
User property(s) DboUserProp
Display property(s) DboDisplayProp
3.1.2 Library Database Object Model
Session DboSession
Library(s) DboLib
Package(s) DboPackage
Device(s) DboDevice
Cell(s) DboCell
Part (s) DboLibPart
Pin(s) DboSymbolPin
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline
Comment text(s) DboCommentText
Bitmap(s) DboBitmap
Global symbol(s) DboSymbol
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline
Comment text(s) DboCommentText
Bitmap(s) DboBitmap
Port symbol(s) DboSymbol
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline
Comment text(s) DboCommentText
Bitmap(s) DboBitmap
Off-page connector symbol(s) DboSymbol
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline

---

Comment text(s) DboCommentText
Bitmap(s) DboBitmap
Title block symbol(s) DboSymbol
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline
Comment text(s) DboCommentText
Bitmap(s) DboBitmap
ERC symbol(s) DboSymbol
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline
Comment text(s) DboCommentText
Bitmap(s) DboBitmap
Bookmark symbol(s) DboSymbol
Rectangle(s) DboBox
Line(s) DboLine
Arc(s) DboArc
Ellipse(s) DboEllipse
Polygon(s) DboPolygon
Polyline(s) DboPolyline
Comment text(s) DboCommentText
Bitmap(s) DboBitmap
All these objects have their respective attributes’ Get and Set functions.
Additionally, all database objects have the following types of properties:
User property(s) DboUserProp
Display property(s) DboDisplayProp

---

3.2 Database TCL commands
3.2.1 Getting Started
3.2.1.1 An easy way to find the commands and its parameters
The best place to look for all the database commands and its parameters with types is Appendix B:
Database Commands List.
Another way to find a database TCL command is to write the following command in the Capture TCL
command window:
"info commands *<command substring>*"
e.g. info commands *_GetName* or info commands *DboPage* or info commands *DboWire* etc.
Capture> info commands *_GetName*
DboLib_GetName
DboPortOccurrence_GetName
DboAlias_GetName
DboNet_GetName
DboPage_GetName
DboLibObject_GetName
DboSchematicSymbolInst_GetName
DboGraphicInstance_GetName
DbDelProp_GetName
DboSymbolPin_GetName
DboFlatNet_GetName
DboFlatNet_GetNameStrategy
DboSchematicNet_GetName
DbBaseProp_GetName
DboBaseObject_GetName
DBProp_GetName
DBProp_GetNameID
DboUserProp_GetName
DboOffPageConnectorOccurrence_GetName
DboSymbolVector_GetName
DboDisplayProp_GetName
After doing that, the next task is to find the parameters of a particular command, e.g. “DboLib_GetName”.
For that, just write the command without any parameter in the TCL command window-
i.e. DboLib_GetName
This will print something like " Wrong number of arguments: DboLib_GetName self name argument 1".

---

Ignore the last two words, i.e. argument 1. Now we are left with DboLib_GetName self name. It means
that DboLib_GetName takes two arguments, 1) the object (self) and 2) the name in which it will return
the library name
There are two ways to call any TCL command -
a) As static functions taking the object as input –
command_with_classname $object <parameters>
e.g. DboLib_GetName $lLib $lName
b) As class object functions –
$object command_without_classname <parameters>
e.g. $lLib GetName $lName
Then, comes the type of the parameter, ie. “name” in this case. Database APIs take various types of
parameters that you can find out in the Appendix B: Database Commands List. You can also refer to the
samples in the installation hierarchy that uses the particular database command
3.2.1.2 Database class hierarchy
To know all commands available for a particular class-type, e.g. DboLib, you can give a command “info
commands DboLib_*”. This will print the commands available directly on DboLib, but not the commands
that DboLib inherits from its base class(s) in the database. For that, you must be aware of database class
hierarchy, which is as follows-
 DbBaseProp
o DboUserProp
 DboBaseObject
o DboAlias
o DboBusEntry
o DboDevice
o DboDisplayProp
o DboFlatNet
o DboGraphicInstance
 DboCustomItemInstance
 DboGraphicArcInst
 DboGraphicBezierInst
 DboGraphicBitMapInst
 DboGraphicBoxInst
 DboGraphicCommentTextInst
 DboGraphicEllipseInst

---

 DboGraphicLineInst
 DboGraphicOleEmbedInst
 DboGraphicPolygonInst
 DboGraphicPolylineInst
 DboGraphicSymbolVectorInst
 DboNetSymbolInstance
 DboBookMark
 DboERC
 DboGlobal
 DboOffPageConnector
 DboPort
 DboPartInst
 DboDrawnInst
 DboPlacedInst
 DboTitleBlock
o DboLib
 DboDesign
o DboLibObject
 DboCell
 DboGraphicObject
 DboSymbol
 DboLibPart
 DboTitleBlockSymbol
 DboPackage
 DboView
 DboSchematic
o DboNet
 DboNetBus
 DboNetScalar
o DboOccurrence
 DboInstOccurrence
 DboNetOccurrence
 DboOffPageConnectorOccurrence
 DboPortOccurrence
 DboPortBusMemberOccurrence
 DboTitleBlockOccurrence
o DboPage
o DboPortInst
 DboPortInstBus
 DboPortInstScalar
 DboPortInstBusMember
o DboSymbolPin
 DboSymbolPinBus
 DboSymbolPinScalar
o DboVector
 DboArc
 DboBezier
 DboBitMap
 DboBox
 DboCommentText
 DboEllipse
 DboFill
 DboLine
 DboOleEmbed
 DboPolygon

---

 DboPolyline
 DboSymbolVector
o DboWire
 DboWireBus
 DboWireScalar
Here, you will note that DboLib inherits from DboBaseObject, hence all the commands provided by
DboBaseObject are also available on DboLib. This means that to know all the commands available on
DboLib, you must call two commands “info commands DboLib_*” and “info commands
DboBaseObject_*”.
Similarly, for knowing all the commands from DboSchematic, you will have to call info commands for
DboSchematic, DboView, DboLibObject and DboBaseObject. This is because DboSchematic inherits from
DboView, which inherits from DboLibObject which in turn inherits from DboBaseObject.
3.2.1.3 String type conversion
As a general rule, almost all the Capture database commands take the “string” parameter as "CString".
There are helper methods available to convert a character array (TCL string) to a CString. You will have
to call DboTclHelper_sMakeCString command for this like the following-
set lName [DboTclHelper_sMakeCString]
# now suppose you have the library object as lLib, then the appropriate call would be
$lLib GetName $lName
There is another helper method DboTclHelper_sGetConstCharPtr that converts CString back to TCL string. Hence, a
subsequent command “puts *DboTclHelper_sGetConstCharPtr $lName+” will convert the library name to a TCL string
and then “puts” will print it on the command shell.
3.2.1.4 DboTclHelper* commands
As stated in the previous section, there are database helper commands available to convert the data
into the desired types, e.g. DboTclHelper_sMakeCString converts from TCL string to CString
These helper functions for data type conversion can be found by giving the commands “info commands
DboTclHelper_sMake*” and “info commands DboTclHelper_sGet*” in the TCL command window, which
will show the result like the following–
DboTclHelper_sMakeLOGFONT
DboTclHelper_sMakeBitmap
DboTclHelper_sMakeBitMapData
DboTclHelper_sMakeDboValue
DboTclHelper_sMakeStdVector

---

DboTclHelper_sMakeInt
DboTclHelper_sMakeStdStr
DboTclHelper_sMakeCPoint
DboTclHelper_sMakeCString
DboTclHelper_sMakeDboValueType
DboTclHelper_sMakeCRect
DboTclHelper_sGetCRectTopLeft
DboTclHelper_sGetCPointX
DboTclHelper_sGetCPointY
DboTclHelper_sGetVectorSize
DboTclHelper_sGetConstCharPtr
DboTclHelper_sGetCRectBottomRight
DboTclHelper_sGetConstCharPtrFromVector
You will find heavy usage of these helper commands in subsequent sections. The usage examples below will
explain the meaning of these helper commands.
3.2.1.5 Convention used in this chapter
All the database class types and database TCL commands are written as italics in subsequent sections.
3.2.2 Get the current Capture session
set lSession $::DboSession_s_pDboSession
DboSession -this $lSession
3.2.3 Create a new Capture session
set lSession [DboTclHelper_sCreateSession]
3.2.4 Open/Get a design in the Capture session
set lStatus [DboState]
# set pDesignPath d:/spb163/tools/capture/samples/fulladd.dsn  EXAMPLE
set lDesignPath [DboTclHelper_sMakeCString $pDesignPath]
set lDesign [$lSession GetDesignAndSchematics $lDesignPath $lStatus]
3.2.5 Iterate over all open designs in the session

---

set lDesignsIter [$lSession NewDesignsIter $lStatus]
#get the first design
set lDesign [$lDesignsIter NextDesign $lStatus]
set lNullObj NULL
while { $lDesign!= $lNullObj} {
#placeholder: do your processing on $lDesign
#get the next design
set lDesign [$lDesignsIter NextDesign $lStatus]
}
delete_DboSessionDesignsIter $lDesignsIter
3.2.6 Get schematic of a design
# set pSchematicName SCHEMATIC1  EXAMPLE
set lSchematicName [DboTclHelper_sMakeCString $pSchematicName]
set lSchematic [$lDesign GetSchematic $lSchematicName $lStatus]
3.2.7 Iterate over all schematics of a design
set lSchematicIter [$lDesign NewViewsIter $lStatus $::IterDefs_SCHEMATICS]
#get the first schematic view
set lView [$lSchematicIter NextView $lStatus]
set lNullObj NULL
while { $lView != $lNullObj} {
#dynamic cast from DboView to DboSchematic
set lSchematic [DboViewToDboSchematic $lView]
#placeholder: do your processing on $lSchematic
#get the next schematic view
set lView [$lSchematicIter NextView $lStatus]
}
delete_DboLibViewsIter $lSchematicIter
3.2.8 Get page of a schematic
# set pPageName PAGE1  EXAMPLE
set lPageName [DboTclHelper_sMakeCString $pPageName]
set lPage [$lSchematic GetPage $lPageName $lStatus]

---

3.2.9 Iterate over all pages of a schematic
set lPagesIter [$lSchematic NewPagesIter $lStatus]
#get the first page
set lPage [$lPagesIter NextPage $lStatus]
set lNullObj NULL
while {$lPage!=$lNullObj} {
#placeholder: do your processing on $lPage
#get the next page
set lPage [$lPagesIter NextPage $lStatus]
}
delete_DboSchematicPagesIter $lPagesIter
3.2.10 Iterate over all part instances of a page
set lPartInstsIter [$lPage NewPartInstsIter $lStatus]
#get the first part inst
set lInst [$lPartInstsIter NextPartInst $lStatus]
while {$lInst!=$lNullObj} {
#dynamic cast from DboPartInst to DboPlacedInst
set lPlacedInst [DboPartInstToDboPlacedInst $lInst]
if {$lPlacedInst != $lNullObj} {
#placeholder: do your processing on $lPlacedInst
}
#get the next part inst
set lInst [$lPartInstsIter NextPartInst $lStatus]
}
delete_DboPagePartInstsIter $lPartInstsIter
3.2.11 Iterate over all hierarchical instances of a page
set lPartInstsIter [$lPage NewPartInstsIter $lStatus]
#get the first part inst
set lInst [$lPartInstsIter NextPartInst $lStatus]
while {$lInst!=$lNullObj} {
#dynamic cast from DboPartInst to DboDrawnInst
set lDrawnInst [DboPartInstToDboDrawnInst $lInst]
if {$lDrawnInst != $lNullObj} {

---

#placeholder: do your processing on $lDrawnInst
}
#get the next part inst
set lInst [$lPartInstsIter NextPartInst $lStatus]
}
delete_DboPagePartInstsIter $lPartInstsIter
3.2.12 Iterate over all wires of a page
set lWiresIter [$lPage NewWiresIter $lStatus]
#get the first wire
set lWire [$lWiresIter NextWire $lStatus]
set lNullObj NULL
while {$lWire != $lNullObj} {
set lObjectType [$lWire GetObjectType]
if {$lObjectType == $::DboBaseObject_WIRE_SCALAR} {
#placeholder: do your processing on Wire scalar $lWire
} elseif {$lObjectType == $::DboBaseObject_WIRE_BUS} {
#placeholder: do your processing on Wire Bus $lWire
}
#get the next wire
set lWire [$lWiresIter NextWire $lStatus]
}
delete_DboPageWiresIter $lWiresIter
3.2.13 Iterate over all globals of a page
set lGlobalsIter [$lPage NewGlobalsIter $lStatus]
#get the first global
set lGlobal [$lGlobalsIter NextGlobal $lStatus]
while { $lGlobal!=$lNullObj } {
#placeholder: do your processing on $lGlobal
#get the next global
set lGlobal [$lGlobalsIter NextGlobal $lStatus]
}
delete_DboPageGlobalsIter $lGlobalsIter

---

3.2.14 Iterate over all title-blocks of a page
set lTitleBlocksIter [$lPage NewTitleBlocksIter $lStatus]
#get the first title block
set lTitle [$lTitleBlocksIter NextTitleBlock $lStatus]
while {$lTitle!=$lNullObj} {
#placeholder: do your processing on $lTitle
#get the next title block
set lTitle [$lTitleBlocksIter NextTitleBlock $lStatus]
}
delete_DboPageTitleBlocksIter $lTitleBlocksIter
3.2.15 Iterate over all ports of a page
set lPortsIter [$lPage NewPortsIter $lStatus]
#get the first port of the page
set lPort [$lPortsIter NextPort $lStatus]
while {$lPort!=$lNullObj} {
#placeholder: do your processing on $lPort
#get the next port of the page
set lPort [$lPortsIter NextPort $lStatus]
}
delete_DboPagePortsIter $lPortsIter
3.2.16 Iterate over all off-pages of page
set lOffPagesIter [$lPage NewOffPageConnectorsIter $lStatus $::IterDefs_ALL]
#get the first off-page of the page
set lOffPage [$lOffPagesIter NextOffPageConnector $lStatus]
while {$lOffPage!=$lNullObj} {
#placeholder: do your processing on $lOffPage
#get the next off-page of the page
set lOffPage [$lOffPagesIter NextOffPageConnector $lStatus]
}
delete_DboPageOffPageConnectorsIter $lOffPagesIter

---

3.2.17 Iterate over all graphics of a page
set lCommentsIter [$lPage NewCommentGraphicsIter $lStatus]
#get the first graphics of the page
set lGraphic [$lCommentsIter NextCommentGraphic $lStatus]
while {$lGraphic!=$lNullObj} {
set lType [$lGraphic GetObjectType]
if {$lType == $::DboBaseObject_GRAPHIC_BOX_INST} {
set lBoxInst [DboGraphicInstanceToDboGraphicBoxInst $lGraphic]
#placeholder: do your processing on $lBoxInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_LINE_INST} {
set lLineInst [DboGraphicInstanceToDboGraphicLineInst $lGraphic]
#placeholder: do your processing on $lLineInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_ELLIPSE_INST} {
set lEllipseInst [DboGraphicInstanceToDboGraphicEllipseInst $lGraphic]
#placeholder: do your processing on $lEllipseInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_ARC_INST} {
set lArcInst [DboGraphicInstanceToDboGraphicArcInst $lGraphic]
#placeholder: do your processing on $lArcInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_POLYLINE_INST} {
set lPolylineInst [DboGraphicInstanceToDboGraphicPolylineInst $lGraphic]
#placeholder: do your processing on $lPolylineInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_POLYGON_INST} {
set $lPolygonInst [DboGraphicInstanceToDboGraphicPolygonInst $lGraphic]
#placeholder: do your processing on $lPolygonInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_BITMAP_INST} {
set lBitMapInst [DboGraphicInstanceToDboGraphicBitMapInst $lGraphic]
#placeholder: do your processing on $lBitMapInst
} elseif {$lType == $::DboBaseObject_GRAPHIC_COMMENTTEXT_INST} {
set lTextInst [DboGraphicInstanceToDboGraphicCommentTextInst $lGraphic]
#placeholder: do your processing on $lTextInst
}
#get the next graphics of the page
set lGraphic [$lCommentsIter NextCommentGraphic $lStatus]
}

---

delete_DboPageCommentGraphicsIter $lCommentsIter
3.2.18 Iterate over all pins of a part instance / drawn instance
set lIter [$lInst NewPinsIter $lStatus]
set lNullObj NULL
#get the first pin of the part
set lPin [$lIter NextPin $lStatus]
while {$lPin !=$lNullObj } {
#placeholder: do your processing on $lPin
#get the next pin of the part
set lPin [$lIter NextPin $lStatus]
}
delete_DboPartInstPinsIter $lIter
3.2.19 Iterate over all aliases of a wire
set lAliasIter [$lWire NewAliasesIter $lStatus]
#get the first alias of wire
set lAlias [$lAliasIter NextAlias $lStatus]
while { $lAlias!=$lNullObj} {
#placeholder: do your processing on $lAlias
#get the next alias of wire
set lAlias [$lAliasIter NextAlias $lStatus]
}
delete_DboWireAliasesIter $lAliasIter
3.2.20 Iterate over all flat nets of a design
set lFlatNetsIter [$pDesign NewFlatNetsIter $lStatus]
#get the first flat net of design
set lFlatNet [$lFlatNetsIter NextFlatNet $lStatus]
while {$lFlatNet!=$lNullObj} {
#placeholder: do your processing on $lFlatNet
set lNetName [DboTclHelper_sMakeCString]
$lFlatNet GetName $lNetName
#get the next flat net of design

---

set lFlatNet [$lFlatNetsIter NextFlatNet $lStatus]
}
delete_DboDesignFlatNetsIter $lFlatNetsIter
3.2.21 Iterate over all user properties of any object
set lPropsIter [$lObject NewUserPropsIter $lStatus]
set lNullObj NULL
#get the first user property on the object
set lUProp [$lPropsIter NextUserProp $lStatus]
while {$lUProp !=$lNullObj } {
#placeholder: do your processing on $lUProp
set lName [DboTclHelper_sMakeCString]
set lValue [DboTclHelper_sMakeCString]
$lUProp GetName $lName
$lUProp GetStringValue $lValue
#get the next user property on the object
set lUProp [$lPropsIter NextUserProp $lStatus]
}
delete_DboUserPropsIter $lPropsIter
3.2.22 Iterate over all display properties of any object
set lPropsIter [$lObject NewDisplayPropsIter $lStatus]
set lNullObj NULL
#get the first display property on the object
set lDProp [$lPropsIter NextProp $lStatus]
while {$lDProp !=$lNullObj } {
#placeholder: do your processing on $lDProp
#get the name
set lName [DboTclHelper_sMakeCString]
$lDProp GetName $lName
#get the location
set lLocation [$lDProp GetLocation $lStatus]
#get the rotation
set lRot [$lDProp GetRotation $lStatus]
#get the font
set lFont [DboTclHelper_sMakeLOGFONT]
set lStatus [$lDProp GetFont $::DboLib_DEFAULT_FONT_PROPERTY $lFont]

---

#get the color
set lColor [$lDProp GetColor $lStatus]
#get the next display property on the object
set lDProp [$lPropsIter NextProp $lStatus]
}
delete_DboDisplayPropsIter $lPropsIter
3.2.23 Change display property of any object
Display property can be added or its visibility type changed as shown below. It looks for display
property “ASSEMBLY”. If it is not present, then it is added at position where mouse was last
clicked. If the display property exits, its visibility type is changed to ‘Name only’.
proc ConvertUserToDoc { pPage pUser } {
set lDocDouble [expr "[$pPage GetPhysicalGranularity] * $pUser + 0.5"]
set lDoc [expr "round($lDocDouble)"]
return $lDoc
}
proc AddDisplayProperty {} {
# Get the selected objects
set lSelObjs1 [GetSelectedObjects]
set lObj1 [lindex $lSelObjs1 0]
set lPropNameCStr [DboTclHelper_sMakeCString "ASSEMBLY"]
set lPropValueCStr [DboTclHelper_sMakeCString "NC"]
set lStatus [$lObj1 SetEffectivePropStringValue $lPropNameCStr $lPropValueCStr]
set varNullObj NULL
set pDispProp [$lObj1 GetDisplayProp $lPropNameCStr $lStatus]
set lStatus [DboState]
if { $pDispProp == $varNullObj } {
set rotation 0
set logfont [DboTclHelper_sMakeLOGFONT]
set color $::DboValue_DEFAULT_OBJECT_COLOR
#set displocation [DboTclHelper_sMakeCPoint [expr $xlocation] [expr
$ylocation]]
if {[catch {set lPickPosition [GetLastMouseClickPointOnPage]} lResult] } {
set lX 0
set lY 0
set displocation [DboTclHelper_sMakeCPoint $intX $intY]
} else {
set page [$lObj1 GetOwner]
set lX [ConvertUserToDoc $page [lindex $lPickPosition 0]]
set lY [ConvertUserToDoc $page [lindex $lPickPosition 1]]
set displocation [DboTclHelper_sMakeCPoint $lX $lY]
}
set pNewDispProp [$lObj1 NewDisplayProp $lStatus $lPropNameCStr $displocation
$rotation $logfont $color]
#DO_NOT_DISPLAY = 0,
#VALUE_ONLY = 1,
#NAME_AND_VALUE = 2,
#NAME_ONLY = 3,
#BOTH_IF_VALUED = 4,
$pNewDispProp SetDisplayType $::DboValue_NAME_AND_VALUE
} else {
$pDispProp SetDisplayType $::DboValue_NAME_ONLY
}
}

---

3.2.24 Iterate over all effective properties of any object
Effective properties are the winning properties on any objects in case of any clashes, e.g. if the
same property is present on any wire as well as corresponding net, this returns the winning
property. Effective properties, by default, include all user/display properties as well.
set lPropsIter [$lObject NewEffectivePropsIter $lStatus]
set lNullObj NULL
#create the input/output parameters
set lPrpName [DboTclHelper_sMakeCString]
set lPrpValue [DboTclHelper_sMakeCString]
set lPrpType [DboTclHelper_sMakeDboValueType]
set lEditable [DboTclHelper_sMakeInt]
#get the first effective property
set lStatus [$lPropsIter NextEffectiveProp $lPrpName $lPrpValue $lPrpType $lEditable]
while {[$lStatus OK] == 1} {
#placeholder: do your processing for $lPrpName $lPrpValue $lPrpType $lEditable
#get the next effective property
set lStatus [$lPropsIter NextEffectiveProp $lPrpName $lPrpValue $lPrpType $lEditable]
}
delete_DboEffectivePropsIter $lPropsIter
3.2.25 Get part instance/drawn instance attributes
#get the name
set lName [DboTclHelper_sMakeCString]
$lInst GetName $lName
#get the location point
set lLocation [$lInst GetLocation $lStatus]
#get the location x
set lStartx [DboTclHelper_sGetCPointX $lLocation]
#get the location y
set lStarty [DboTclHelper_sGetCPointY $lLocation]
#get the source library name
set lLibName [DboTclHelper_sMakeCString]
$lInst GetSourceLibName $lLibName
#get the device designator
set lDeviceDesignator [DboTclHelper_sMakeCString]
$lInst GetReferenceDesignator $lDeviceDesignator
#get the rotation
set lRot [$lInst GetRotation $lStatus]
#get the contents lib name
set lContentsLibName [DboTclHelper_sMakeCString]

---

$lInst GetContentsLibName $lContentsLibName
#get the contents view name
set lContentsViewName [DboTclHelper_sMakeCString]
$lInst GetContentsViewName $lContentsViewName
#get the contents view type
set lType [$lInst GetContentsViewType $lStatus]
#get the primitive type
set lPrimitiveType [$lInst GetIsPrimitiveProp $lStatus]
#get the part value
set lValue [DboTclHelper_sMakeCString]
$lInst GetPartValue $lValue
#get the reference
set lReferenceName [DboTclHelper_sMakeCString]
$lInst GetReference $lReferenceName
#get the bounding box on the page
set lBBox [$lInst GetOffsetBoundingBox $lStatus]
#get the top-left of the bbox
set lTopLeft [DboTclHelper_sGetCRectTopLeft $lBBox]
#get the bottom-right of the bbox
set lBottomRight [DboTclHelper_sGetCRectBottomRight $lBBox]
#get the x1
set lStartx [DboTclHelper_sGetCPointX $lTopLeft]
#get the y1
set lStarty [DboTclHelper_sGetCPointY $lTopLeft]
#get the x2
set lEndx [DboTclHelper_sGetCPointX $lBottomRight]
#get the y2
set lEndy [DboTclHelper_sGetCPointY $lBottomRight]
3.2.26 Get wire attributes
#get the name
set lName [DboTclHelper_sMakeCString]
$lWire GetName $lName
#get the net name
set lNetName [DboTclHelper_sMakeCString]
$lWire GetNetName $lNetName
#get the start point
set lStart [$lWire GetStartPoint $lStatus]
set lStartx [DboTclHelper_sGetCPointX $lStart]
set lStarty [DboTclHelper_sGetCPointY $lStart]
#get the end point
set lEnd [$lWire GetEndPoint $lStatus]
set lEndx [DboTclHelper_sGetCPointX $lEnd]
set lEndy [DboTclHelper_sGetCPointY $lEnd]
#get the color
set lColor [$lWire GetColor $lStatus]

---

#get the net
set lNet [$lWire GetNet $lStatus]
3.2.27 Get other objects attributes
After analyzing the examples of querying the attributes for placed instance and wires, you must have got
the basic idea of how you can query design objects, their properties and their attributes.
Similar attributes “Get” functions and objects iteration/get functions are available for all other types of
objects also. There is various TCL script samples set present in the installation hierarchy that you can
refer to get the exact details.
3.2.28 Hierarchy traversal
3.2.28.1 Get root instance occurrence of a design
set lRootOcc [$lDesign GetRootOccurrence $lStatus]
3.2.28.2 Iterate over instance occurrence hierarchy
proc traverse_hierarchy { lInstOcc } {
set lStatus [DboState]
set lNullObj NULL
set lInstOccIter [$lInstOcc NewChildrenIter $lStatus $::IterDefs_INSTS]
#get the first child occurrence
set lChildOcc [$lInstOccIter NextOccurrence $lStatus]
while { $lChildOcc!= $lNullObj} {
#get the DboInstOccurrence pointer from DboOccurrence pointer
set lChildInstOcc [DboOccurrenceToDboInstOccurrence $lChildOcc]
# placeholder: do your processing on $lChildInstOcc
# do a recursion of the procedure call for $lChildInstOcc
traverse_hierarchy $lChildInstOcc
#get the next child occurrence
set lChildOcc [$lInstOccIter NextOccurrence $lStatus]
}
delete_DboOccurrenceChildrenIter $lInstOccIter
}

---

3.2.28.3 Iterating port occurrence within an instance occurrence
set lPortOccIter [$pInstOcc NewChildrenIter $lStatus $::IterDefs_PORTS]
#get the first child port occurrence
set lPortOcc [$lPortOccIter NextOccurrence $lStatus]
while { $lPortOcc!= $lNullObj} {
# placeholder: do your processing on $lPortOcc
#get the next child port occurrence
set lPortOcc [$lPortOccIter NextOccurrence $lStatus]
}
delete_DboOccurrenceChildrenIter $lPortOccIter
3.2.28.4 Iterating off-page occurrence within an instance occurrence
set lOffpageOccIter [$pInstOcc NewChildrenIter $lStatus $::IterDefs_OFFPAGES]
#get the first child offpage occurrence
set lOffpageOcc [$lOffpageOccIter NextOccurrence $lStatus]
while { $lOffpageOcc!= $lNullObj} {
# placeholder: do your processing on $lOffpageOcc
#get the next child offpage occurrence
set lOffpageOcc [$lOffpageOccIter NextOccurrence $lStatus]
}
delete_DboOccurrenceChildrenIter $lOffpageOccIter
3.2.28.5 Iterating net occurrence within an instance occurrence
set lNetOccIter [$pInstOcc NewChildrenIter $lStatus $::IterDefs_NETS]
#get the first child Net occurrence
set lNetOcc [$lNetOccIter NextOccurrence $lStatus]
while { $lNetOcc!= $lNullObj} {
# placeholder: do your processing on $lNetOcc
#get the next child Net occurrence
set lNetOcc [$lNetOccIter NextOccurrence $lStatus]
}
delete_DboOccurrenceChildrenIter $lNetOccIter

---

3.2.28.6 Iterating title-block occurrence within an instance occurrence
set lTitleBlockOccIter [$pInstOcc NewChildrenIter $lStatus $::IterDefs_TITLEBLOCKS]
#get the first child TitleBlock occurrence
set lTitleBlockOcc [$lTitleBlockOccIter NextOccurrence $lStatus]
while { $lTitleBlockOcc!= $lNullObj} {
# placeholder: do your processing on $lTitleBlockOcc
#get the next child TitleBlock occurrence
set lTitleBlockOcc [$lTitleBlockOccIter NextOccurrence $lStatus]
}
delete_DboOccurrenceChildrenIter $lTitleBlockOccIter