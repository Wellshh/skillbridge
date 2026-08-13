### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

Contents
========

[Alphabetical List of Functions](algroskillAPL.md "Alphabetical List of Functions")
-----------------------------------------------------------------------------------

[Before You Start](preface.md "Before You Start")
-------------------------------------------------

[About This Manual](preface.html#1032531 "Before You Start")

[Prerequisites](preface.html#1033838 "Before You Start")

[Command Syntax Conventions](preface.html#1033870 "Before You Start")

[Referencing Objects by Name](preface.html#1033888 "Before You Start")

[Finding Information in This Manual](preface.html#1033866 "Before You Start")

[Other Sources of Information](preface.html#1032810 "Before You Start")

[1](01ovrvew.md "1")
--------------------

[Introduction to Allegro PCB Editor SKILL Functions](01ovrvew.html#103136 "1")
------------------------------------------------------------------------------

[Overview](01ovrvew.html#69599 "1")

[AXL-SKILL in Allegro PCB Editor](01ovrvew.html#67472 "1")

[AXL-SKILL Database](01ovrvew.html#105377 "1")

[2](02dbdesc.md "2")
--------------------

[The Allegro PCB Editor Database User Model](02dbdesc.html#462876 "2")
----------------------------------------------------------------------

[Overview](02dbdesc.html#597403 "2")

[Description of Database Objects](02dbdesc.html#452619 "2")

[Figure Database Types](02dbdesc.html#452639 "2")

[Logical Database Types](02dbdesc.html#459373 "2")

[Property Dictionary Database Types](02dbdesc.html#609757 "2")

[Parameter Database Types](02dbdesc.html#459399 "2")

[3](04parmgt.md "3")
--------------------

[Parameter Management Functions](04parmgt.html#1069532 "3")
-----------------------------------------------------------

[Overview](04parmgt.html#1065276 "3")

:   [axlcreate](04parmgt.html#1173701 "3")
:   [axlDBGetTextBlockCount](04parmgt.html#1148233 "3")
:   [axlDBGridGet](04parmgt.html#1120502 "3")
:   [axlDBGridSet](04parmgt.html#1120503 "3")
:   [axlDBTextBlockCreate](04parmgt.html#1120504 "3")
:   [axlDBTextBlockFindName](04parmgt.html#1148303 "3")
:   [axlDBTextBlockGetName](04parmgt.html#1148390 "3")
:   [axlDBTextBlockSetName](04parmgt.html#1148454 "3")
:   [axlExportXmlDBRecords](04parmgt.html#1120505 "3")
:   [axlFilmCreate](04parmgt.html#1148038 "3")
:   [axlImportXmlDBRecords](04parmgt.html#1120492 "3")
:   [axlMiniStatusReset](04parmgt.html#1167427 "3")
:   [axlPadSuppressGet](04parmgt.html#1167420 "3")
:   [axlPadSuppressOkLayer](04parmgt.html#1126057 "3")
:   [axlPadSuppressSet](04parmgt.html#1126058 "3")
:   [axlParamFilletDoc](04parmgt.html#1148650 "3")
:   [axlGetParam](04parmgt.html#1126060 "3")
:   [axlSetParam](04parmgt.html#1109729 "3")

[Color Access](04parmgt.html#1099823 "3")

:   [axlColorDoc](04parmgt.html#1109167 "3")
:   [axlColorGet](04parmgt.html#1093245 "3")
:   [axlColorShadowGet](04parmgt.html#1096002 "3")
:   [axlColorShadowSet](04parmgt.html#1096006 "3")
:   [axlColorLoad](04parmgt.html#1093428 "3")
:   [axlColorOnGet - Obsolete Command](04parmgt.html#1093862 "3")
:   [axlColorOnSet - Obsolete Command](04parmgt.html#1094229 "3")
:   [axlColorPriorityGet - Obsolete Command](04parmgt.html#1094443 "3")
:   [axlColorPrioritySet - Obsolete Command](04parmgt.html#1094694 "3")
:   [axlColorSave](04parmgt.html#1135484 "3")
:   [axlColorSet](04parmgt.html#1095354 "3")
:   [axlCVFColorChooserDlg](04parmgt.html#1109859 "3")
:   [axlClearObjectCustomColor](04parmgt.html#1110182 "3")
:   [axlCustomColorObject](04parmgt.html#1110302 "3")
:   [axlLayerPriorityClearAll](04parmgt.html#1110678 "3")
:   [axlLayerPriorityGet](04parmgt.html#1120655 "3")
:   [axlLayerPriorityRestoreAll](04parmgt.html#1110767 "3")
:   [axlLayerPrioritySaveAll](04parmgt.html#1110848 "3")
:   [axlLayerPrioritySet](04parmgt.html#1110972 "3")
:   [axlIsCustomColored](04parmgt.html#1110545 "3")

[Database Layer Management](04parmgt.html#1066386 "3")

:   [axlClasses](04parmgt.html#1140503 "3")
:   [axlDBGetLayerType](04parmgt.html#1066845 "3")
:   [axlGetXSection](04parmgt.html#1151911 "3")
:   [axlIsEtchLayer](04parmgt.html#1150414 "3")
:   [axlIsLayer](04parmgt.html#1067159 "3")
:   [axlIsVisibleLayer](04parmgt.html#1067336 "3")
:   [axlLayerCreateCrossSection](04parmgt.html#1085461 "3")
:   [axlLayerCreateNonConductor](04parmgt.html#1173941 "3")
:   [axlLayerDelete](04parmgt.html#1150567 "3")
:   [axlLayerGet](04parmgt.html#1173865 "3")
:   [axlLayerViaLabel](04parmgt.html#1150817 "3")
:   [axlMaterialGet](04parmgt.html#1167495 "3")
:   [axlVisibleDesign](04parmgt.html#1068075 "3")
:   [axlVisibleGet](04parmgt.html#1068227 "3")
:   [axlVisibleLayer](04parmgt.html#1068430 "3")
:   [axlVisibleSet](04parmgt.html#1068662 "3")
:   [axlConductorBottomLayer](04parmgt.html#1092676 "3")
:   [axlConductorTopLayer](04parmgt.html#1092735 "3")
:   [axlDBCreateFilmRec](04parmgt.html#1092717 "3")
:   [axlSetPlaneType](04parmgt.html#1148171 "3")
:   [axlSubclasses](04parmgt.html#1107319 "3")
:   [axlSubclassRoute](04parmgt.html#1119179 "3")
:   [axlXSectionCopy](04parmgt.html#1168597 "3")
:   [axlXSectionCreate](04parmgt.html#1168694 "3")
:   [axlXSectionDelete](04parmgt.html#1169205 "3")
:   [axlXSectionGet](04parmgt.html#1169585 "3")
:   [axlXSectionLayerFunctions](04parmgt.html#1172264 "3")
:   [axlXSectionLayerTypes](04parmgt.html#1172321 "3")
:   [axlXSectionModify](04parmgt.html#1172362 "3")
:   [axlXSectionSet](04parmgt.html#1172523 "3")

[4](05selfnd.md "4")
--------------------

[Selection and Find Functions](05selfnd.html#580309 "4")
--------------------------------------------------------

[Overview](05selfnd.html#606474 "4")

[Select Set Highlighting](05selfnd.html#581578 "4")

[Select Modes](05selfnd.html#581591 "4")

[Finding Objects by Name](05selfnd.html#581608 "4")

[Point Selection](05selfnd.html#581631 "4")

[Area Selection](05selfnd.html#581652 "4")

[Miscellaneous Select Functions](05selfnd.html#581669 "4")

[axlSelect-The General Select Function](05selfnd.html#581690 "4")

[Select Set Management](05selfnd.html#581715 "4")

[Find Filter Control](05selfnd.html#581736 "4")

[Selection and Find Functions](05selfnd.html#580411 "4")

:   [axlSingleSelectPoint](05selfnd.html#580413 "4")
:   [axlAddSelectPoint](05selfnd.html#609263 "4")
:   [axlSubSelectPoint](05selfnd.html#580437 "4")
:   [axlSingleSelectBox](05selfnd.html#580450 "4")
:   [axlAddSelectBox](05selfnd.html#580462 "4")
:   [axlSubSelectBox](05selfnd.html#580472 "4")
:   [axlAddSelectAll](05selfnd.html#582878 "4")
:   [axlSubSelectAll](05selfnd.html#580493 "4")
:   [axlSingleSelectName](05selfnd.html#580506 "4")
:   [axlAddSelectName](05selfnd.html#580526 "4")
:   [axlSubSelectName](05selfnd.html#580542 "4")
:   [axlSingleSelectObject](05selfnd.html#584203 "4")
:   [axlAddSelectObject](05selfnd.html#580568 "4")
:   [axlSubSelectObject](05selfnd.html#580579 "4")
:   [axlSelect](05selfnd.html#584508 "4")
:   [axlGetSelSet](05selfnd.html#580611 "4")
:   [axlGetSelSetCount](05selfnd.html#580623 "4")
:   [axlClearSelSet](05selfnd.html#580634 "4")
:   [axlGetFindFilter](05selfnd.html#580646 "4")
:   [axlSetFindFilter](05selfnd.html#580660 "4")
:   [axlAutoOpenFindFilter](05selfnd.html#580692 "4")
:   [axlOpenFindFilter](05selfnd.html#580703 "4")
:   [axlCloseFindFilter](05selfnd.html#580712 "4")
:   [axlDBFindByName](05selfnd.html#667882 "4")
:   [axlFindFilterIsOpen](05selfnd.html#580721 "4")
:   [axlSelectByName](05selfnd.html#665244 "4")
:   [axlSelectByProperty](05selfnd.html#669477 "4")
:   [axlSnapToObject](05selfnd.html#668490 "4")
:   [axlLastPickIsSnapped](05selfnd.html#668494 "4")

[5](06intedt.md "5")
--------------------

[Interactive Edit Functions](06intedt.html#822268 "5")
------------------------------------------------------

[Overview](06intedt.html#822269 "5")

[AXL/SKILL Interactive Edit Functions](06intedt.html#808725 "5")

:   [axlBondFingerDelete](06intedt.html#831995 "5")
:   [axlDeleteBondWire](06intedt.html#832534 "5")
:   [axlChangeLine2Cline](06intedt.html#853831 "5")
:   [axlChangeLineFont](06intedt.html#860226 "5")
:   [axlChangeWidth](06intedt.html#823183 "5")
:   [axlCopyProperties](06intedt.html#860810 "5")
:   [axlCopyObject](06intedt.html#832061 "5")
:   [axlDBAltOrigin](06intedt.html#825701 "5")
:   [axlDBChangeText](06intedt.html#832157 "5")
:   [axlDeleteObject](06intedt.html#832160 "5")
:   [axlDeleteTaper](06intedt.html#847309 "5")
:   [axlDBDeleteProp](06intedt.html#808739 "5")
:   [axlDBDeletePropAll](06intedt.html#827023 "5")
:   [axlDBDeletePropDictEntry](06intedt.html#827658 "5")
:   [axlDBOpenShape](06intedt.html#832168 "5")
:   [axlDeleteFillet](06intedt.html#861756 "5")
:   [axlFillet](06intedt.html#861831 "5")
:   [axlFilletConvert](06intedt.html#861370 "5")
:   [axlGetLastEnterPoint](06intedt.html#861744 "5")
:   [axlLastPick](06intedt.html#826372 "5")
:   [axlWindowBoxGet](06intedt.html#810387 "5")
:   [axlWindowBoxSet](06intedt.html#810566 "5")
:   [axlReplacePadstack](06intedt.html#31833 "5")
:   [axlPurgePadstacks](06intedt.html#821249 "5")
:   [axlShapeAutoVoid](06intedt.html#851093 "5")
:   [axlShapeChangeDynamicType](06intedt.html#823379 "5")
:   [axlShapeDeleteVoids](06intedt.html#823700 "5")
:   [axlShapeDynamicUpdate](06intedt.html#823966 "5")
:   [axlShapeRaisePriority](06intedt.html#824257 "5")
:   [axlShapeMerge](06intedt.html#832204 "5")
:   [axlShoveItems](06intedt.html#821320 "5")
:   [axlShoveSetParams](06intedt.html#821365 "5")
:   [axlSmoothDesign](06intedt.html#832245 "5")
:   [axlSmoothItems](06intedt.html#832246 "5")
:   [axlSmoothSetParams](06intedt.html#832247 "5")
:   [axlSymbolAttach](06intedt.html#853770 "5")
:   [axlSymbolDetach](06intedt.html#853787 "5")
:   [axlAddTaper](06intedt.html#847291 "5")
:   [axlTextOrientationCopy](06intedt.html#847294 "5")
:   [axlTransformObject](06intedt.html#821370 "5")

[Padstack Access Functions](06intedt.html#876690 "5")

:   [axlDBCreatePadStack](06intedt.html#876722 "5")
:   [axlPadFigureTypes](06intedt.html#877610 "5")
:   [axlPadstackEdit](06intedt.html#877090 "5")
:   [axlPadstackSetType](06intedt.html#877417 "5")
:   [axlPadstackUsageTypes](06intedt.html#877499 "5")
:   [axlPadUserMaskLayers](06intedt.html#877553 "5")

[6](07dbaccs.md "6")
--------------------

[Database Read Functions](07dbaccs.html#718825 "6")
---------------------------------------------------

[AXL-SKILL Database Read Functions](07dbaccs.html#718849 "6")

:   [axlAltSymbolList](07dbaccs.html#739212 "6")
:   [axlAltSymbolOK](07dbaccs.html#739294 "6")
:   [axlAltSymbolReplace](07dbaccs.html#739374 "6")
:   [axlBackdrillGet](07dbaccs.html#739500 "6")
:   [axlDBGetDesign](07dbaccs.html#700317 "6")
:   [axlDBGetDrillPlating](07dbaccs.html#705379 "6")
:   [axlIsDBIDType](07dbaccs.html#705289 "6")
:   [axlDBGetAttachedText](07dbaccs.html#700342 "6")
:   [axlDBGetPad](07dbaccs.html#700355 "6")
:   [axlDBGetPropDict](07dbaccs.html#735276 "6")
:   [axlDBGetPropDictEntry](07dbaccs.html#735236 "6")
:   [axlDBGetProperties](07dbaccs.html#700383 "6")
:   [axlDBGetDesignUnits](07dbaccs.html#700396 "6")
:   [axlDBRefreshId](07dbaccs.html#700407 "6")
:   [axlDBGetLonelyBranches](07dbaccs.html#700419 "6")
:   [axlDBGetConnect](07dbaccs.html#719173 "6")
:   [axlDBIsFixed](07dbaccs.html#719327 "6")
:   [axlDBIsPackagePin](07dbaccs.html#719354 "6")
:   [axlGetModuleInstanceDefinition](07dbaccs.html#719416 "6")
:   [axlGetModuleInstanceLocation](07dbaccs.html#719439 "6")
:   [axlGetModuleInstanceLogicMethod](07dbaccs.html#719496 "6")
:   [axlGetModuleInstanceNetExceptions](07dbaccs.html#719960 "6")
:   [axlIsDummyNet](07dbaccs.html#719568 "6")
:   [axlIsLayerNegative](07dbaccs.html#719601 "6")
:   [axlIsPinUnused](07dbaccs.html#719636 "6")
:   [axlIsitFill](07dbaccs.html#719658 "6")
:   [axlOK2Void](07dbaccs.html#719680 "6")
:   [axlDBDynamicShapes](07dbaccs.html#720167 "6")
:   [axlDBGetShapes](07dbaccs.html#720190 "6")
:   [axlDBTextBlockCompact](07dbaccs.html#720279 "6")

[7](08intprm.md "7")
--------------------

[Allegro PCB Editor Interface Functions](08intprm.html#571929 "7")
------------------------------------------------------------------

[Overview](08intprm.html#592635 "7")

[AXL-SKILL Interface Function Examples](08intprm.html#571950 "7")

[Allegro PCB Editor Interface Functions](08intprm.html#571974 "7")

:   [axlClearDynamics](08intprm.html#627949 "7")
:   [axlAddSimpleRbandDynamics](08intprm.html#600852 "7")
:   [axlAddSimpleMoveDynamics](08intprm.html#572000 "7")
:   [axlDesignFlip](08intprm.html#624549 "7")
:   [axlEnterPoint](08intprm.html#572013 "7")
:   [axlEnterString](08intprm.html#572025 "7")
:   [axlEnterAngle](08intprm.html#572040 "7")
:   [axlCancelEnterFun](08intprm.html#572054 "7")
:   [axlFinishEnterFun](08intprm.html#572064 "7")
:   [axlGetDynamicsSegs](08intprm.html#619261 "7")
:   [axlGetLineLock](08intprm.html#624571 "7")
:   [axlEnterBox](08intprm.html#572074 "7")
:   [axlEnterPath](08intprm.html#572086 "7")
:   [axlHighlightObject](08intprm.html#572099 "7")
:   [axlDehighlightObject](08intprm.html#572109 "7")
:   [axlMiniStatusLoad](08intprm.html#582611 "7")
:   [axlDrawObject](08intprm.html#588891 "7")
:   [axlDynamicsObject](08intprm.html#588912 "7")
:   [axlEraseObject](08intprm.html#195442 "7")
:   [axlControlRaise](08intprm.html#616422 "7")
:   [axlEnterEvent](08intprm.html#616446 "7")
:   [axlEventSetStartPopup](08intprm.html#616811 "7")
:   [axlGetTrapBox](08intprm.html#616877 "7")
:   [axlRatsnestBlank](08intprm.html#616882 "7")
:   [axlRatsnestDisplay](08intprm.html#616906 "7")
:   [axlSetDynamicsMirror](08intprm.html#624608 "7")
:   [axlSetDynamicsRotation](08intprm.html#624600 "7")
:   [axlShowObjectToFile](08intprm.html#616937 "7")
:   [axlUICmdPopupSet](08intprm.html#616987 "7")
:   [axlWindowFit](08intprm.html#643396 "7")
:   [axlZoomBbox](08intprm.html#642159 "7")
:   [axlZoomCenter](08intprm.html#642227 "7")
:   [axlZoomControl](08intprm.html#642299 "7")
:   [axlZoomFit](08intprm.html#642682 "7")
:   [axlZoomInOut](08intprm.html#642784 "7")
:   [axlZoomPoints](08intprm.html#642855 "7")
:   [axlZoomToDbid](08intprm.html#642151 "7")
:   [axlZoomWorld](08intprm.html#642917 "7")
:   [axlMakeDynamicsPath](08intprm.html#617484 "7")

[8](09cmdshl.md "8")
--------------------

[Allegro PCB Editor Command Shell Functions](09cmdshl.html#883012 "8")
----------------------------------------------------------------------

[Command Shell Functions](09cmdshl.html#883021 "8")

:   [axlGetAlias](09cmdshl.html#894702 "8")
:   [axlGetFuncKey](09cmdshl.html#894759 "8")
:   [axlGetVariable](09cmdshl.html#883023 "8")
:   [axlGetVariableList](09cmdshl.html#893710 "8")
:   [axlJournal](09cmdshl.html#897865 "8")
:   [axlProtectAlias](09cmdshl.html#895146 "8")
:   [axlIsProtectAlias](09cmdshl.html#895182 "8")
:   [axlReadOnlyVariable](09cmdshl.html#895229 "8")
:   [axlSetAlias](09cmdshl.html#895302 "8")
:   [axlSetAlias](09cmdshl.html#895485 "8")
:   [axlSetFunckey](09cmdshl.html#895632 "8")
:   [axlSetVariable](09cmdshl.html#883036 "8")
:   [axlSetVariableFile](09cmdshl.html#903021 "8")
:   [axlShell](09cmdshl.html#903025 "8")
:   [axlShellPost](09cmdshl.html#896845 "8")
:   [axlUnsetVariable](09cmdshl.html#896847 "8")
:   [axlUnsetVariableFile](09cmdshl.html#903107 "8")

[9](sipapd.md "9")
------------------

[SiP/APD Commands](sipapd.html#1037521 "9")
-------------------------------------------

:   [axlChangeLayer](sipapd.html#1086782 "9")
:   [axlCNSAssemblyModeGet](sipapd.html#1105112 "9")
:   [axlCNSAssemblyModeSet](sipapd.html#1105318 "9")
:   [axlCNSGetAssembly](sipapd.html#1105625 "9")
:   [axlCNSSetAssembly](sipapd.html#1106263 "9")
:   [axlCreateDeviceFileTemplate](sipapd.html#1105916 "9")
:   [axlCompAddPin](sipapd.html#1091129 "9")
:   [axlCompDeletePin](sipapd.html#1085880 "9")
:   [axlCompMovePin](sipapd.html#1085881 "9")
:   [axlComponentChangeClass](sipapd.html#1099342 "9")
:   [axlCompSetPinAttributes](sipapd.html#1099808 "9")
:   [axlDBIsBondingWireLayer](sipapd.html#1092666 "9")
:   [axlDBIsBondpad](sipapd.html#1092522 "9")
:   [axlDBIsBondwire](sipapd.html#1092539 "9")
:   [axlDBIsDiePad](sipapd.html#1092555 "9")
:   [axlDBIsPlatingbarPin](sipapd.html#1092742 "9")
:   [axlGetDieType](sipapd.html#1092794 "9")
:   [axlGetMetalUsageForLayer](sipapd.html#1077587 "9")
:   [axlGetWireProfileDefinition](sipapd.html#1078975 "9")
:   [axlAddAutoAssignNetAlgorithm](sipapd.html#1077588 "9")
:   [axlGetWireProfileDirection](sipapd.html#1078568 "9")
:   [axlGetAllVisibleProfiles](sipapd.html#1077590 "9")
:   [axlSetAllProfilesVisible](sipapd.html#1077591 "9")
:   [axlSetBondWireProfile](sipapd.html#1099257 "9")
:   [axlImportWireProfileDefinitions](sipapd.html#1077592 "9")
:   [axlSetBondWireProfile](sipapd.html#1099231 "9")
:   [axlSetDieStackData](sipapd.html#1076715 "9")
:   [axlDBIsDieStackLayer](sipapd.html#1077713 "9")
:   [axlGetDieData](sipapd.html#1077759 "9")
:   [axlGetDieStackData](sipapd.html#1077801 "9")
:   [axlGetDieStackMemberSet](sipapd.html#1077828 "9")
:   [axlGetDieStackNames](sipapd.html#1077859 "9")
:   [axlGetIposerData](sipapd.html#1077868 "9")
:   [axlGetSpacerData](sipapd.html#1077904 "9")
:   [axlGetWireProfileColor](sipapd.html#1077938 "9")
:   [axlGetWireProfileVisible](sipapd.html#1077948 "9")
:   [axlPackageDesignCheckAddCategory](sipapd.html#1085975 "9")
:   [axlPackageDesignCheckAddCheck](sipapd.html#1085976 "9")
:   [axlPackageDesignCheckDrcError](sipapd.html#1085977 "9")
:   [axlPackageDesignCheckLogError](sipapd.html#1077751 "9")
:   [axlSetDieData](sipapd.html#1078060 "9")
:   [axlSetDieType](sipapd.html#1086008 "9")
:   [axlSetIposerData](sipapd.html#1078087 "9")
:   [axlSetSpacerData](sipapd.html#1078110 "9")
:   [axlSetWireProfileColor](sipapd.html#1078131 "9")
:   [axlSetWireProfileVisible](sipapd.html#1078144 "9")

[10](10usrint.md "10")
----------------------

[User Interface Functions](10usrint.html#101740 "10")
-----------------------------------------------------

[Window Placement](10usrint.html#101699 "10")

[Using Menu Files](10usrint.html#109910 "10")

[Dynamically Loading Menus](10usrint.html#380398 "10")

[Understanding the Menu File Format](10usrint.html#380542 "10")

[AXL-SKILL User Interface Functions](10usrint.html#380538 "10")

:   [axlCancelOff](10usrint.html#381670 "10")
:   [axlCancelOn](10usrint.html#381672 "10")
:   [axlCancelTest](10usrint.html#381710 "10")
:   [axlClipboardGetText](10usrint.html#417343 "10")
:   [axlClipboardSetText](10usrint.html#417404 "10")
:   [axlCursorGet](10usrint.html#405060 "10")
:   [axlCursorWarp](10usrint.html#405062 "10")
:   [axlMeterCreate](10usrint.html#381730 "10")
:   [axlMeterDestroy](10usrint.html#382496 "10")
:   [axlMeterIsCancelled](10usrint.html#382852 "10")
:   [axlMeterUpdate](10usrint.html#404809 "10")
:   [axlUIMenuLoad](10usrint.html#379533 "10")
:   [axlUIMenuDump](10usrint.html#379567 "10")
:   [axlUIColorDialog](10usrint.html#425029 "10")
:   [axlUIConfirm](10usrint.html#101764 "10")
:   [axlUIConfirmEx](10usrint.html#383585 "10")
:   [axlUIControl](10usrint.html#410372 "10")
:   [axlUIMenuChange](10usrint.html#390726 "10")
:   [axlUIMenuDebug](10usrint.html#390812 "10")
:   [axlUIMenuDelete](10usrint.html#390814 "10")
:   [axlUIMenuFind](10usrint.html#390729 "10")
:   [axlUIMenuInsert](10usrint.html#392601 "10")
:   [axlUIMenuRegister](10usrint.html#383589 "10")
:   [axlUIPrompt](10usrint.html#386611 "10")
:   [axlUIWCloseAll](10usrint.html#386859 "10")
:   [axlUIWIconify](10usrint.html#417517 "10")
:   [axlUIWIsIconic](10usrint.html#417702 "10")
:   [axlUIWIsWindow](10usrint.html#417824 "10")
:   [axlUIWMove](10usrint.html#386643 "10")
:   [axlUIWRedraw](10usrint.html#417924 "10")
:   [axlUIWSize](10usrint.html#413785 "10")
:   [axlIsViewFileType](10usrint.html#101794 "10")
:   [axlUIViewFileCreate](10usrint.html#101806 "10")
:   [axlUIViewFileReuse](10usrint.html#101823 "10")
:   [axlUIYesNo](10usrint.html#101837 "10")
:   [axlUIWExpose](10usrint.html#101852 "10")
:   [axlUIWClose](10usrint.html#101864 "10")
:   [axlUIWHelpRegister](10usrint.html#404919 "10")
:   [axlUIWPrint](10usrint.html#101875 "10")
:   [axlUIWRedraw](10usrint.html#373816 "10")
:   [axlUIWBlock](10usrint.html#373849 "10")
:   [axlUIEditFile](10usrint.html#379766 "10")
:   [axlUIMultipleChoice](10usrint.html#379767 "10")
:   [axlUIViewFileScrollTo](10usrint.html#379862 "10")
:   [axlUIWBeep](10usrint.html#379913 "10")
:   [axlUIWDisableQuit](10usrint.html#379963 "10")
:   [axlUIWExposeByName](10usrint.html#380008 "10")
:   [axlUIWPerm](10usrint.html#380009 "10")
:   [axlUIWSetHelpTag](10usrint.html#380100 "10")
:   [axlUIWSetParent](10usrint.html#380155 "10")
:   [axlUIWShow](10usrint.html#380205 "10")
:   [axlUIWTimerAdd](10usrint.html#380243 "10")
:   [axlUIWTimerRemove](10usrint.html#380248 "10")
:   [axlUIWUpdate](10usrint.html#380206 "10")
:   [axlUIYesNoCancel](10usrint.html#380347 "10")
:   [axlUIDataBrowse](10usrint.html#381369 "10")

[11](11frmint.md "11")
----------------------

[Form Interface Functions](11frmint.html#414284 "11")
-----------------------------------------------------

[Overview](11frmint.html#431514 "11")

:   [Programming](11frmint.html#465719 "11")
:   [Field / Control](11frmint.html#465745 "11")

[Using Forms Specification Language](11frmint.html#480398 "11")

[Moving and Sizing Form Controls During Form Resizing](11frmint.html#461205 "11")

[Using Grids](11frmint.html#461722 "11")

[AXL-SKILL Form Interface Functions](11frmint.html#433187 "11")

:   [axlFormBNFDoc](11frmint.html#472343 "11")
:   [axlFormCallback](11frmint.html#469106 "11")
:   [axlFormCreate](11frmint.html#414342 "11")
:   [axlFormClearMouseActive](11frmint.html#507209 "11")
:   [axlFormClose](11frmint.html#435469 "11")
:   [axlFormDisplay](11frmint.html#414374 "11")
:   [axlFormBuildPopup](11frmint.html#424697 "11")
:   [axlFormGetField](11frmint.html#414403 "11")
:   [axlFormGridSelected](11frmint.html#495999 "11")
:   [axlFormGridSelectedCnt](11frmint.html#495786 "11")
:   [axlFormGridSetSelectRows](11frmint.html#495777 "11")
:   [axlFormListDeleteAll](11frmint.html#414416 "11")
:   [axlFormListSelect](11frmint.html#425524 "11")
:   [axlFormSetEventAction](11frmint.html#479215 "11")
:   [axlFormSetField](11frmint.html#425442 "11")
:   [axlFormSetInfo](11frmint.html#414446 "11")
:   [axlFormSetMouseActive](11frmint.html#507238 "11")
:   [axlFormTest](11frmint.html#477426 "11")
:   [axlFormRestoreField](11frmint.html#414460 "11")
:   [axlFormTitle](11frmint.html#414473 "11")
:   [axlIsFormType](11frmint.html#414485 "11")
:   [axlFormSetFieldVisible](11frmint.html#458395 "11")
:   [axlFormIsFieldVisible](11frmint.html#428685 "11")
:   [Callback Procedure: formCallback](11frmint.html#428663 "11")
:   [axlFormAutoResize](11frmint.html#461096 "11")
:   [axlFormColorize](11frmint.html#463432 "11")
:   [axlFormGetActiveField](11frmint.html#458881 "11")
:   [axlFormGridBatch](11frmint.html#458963 "11")
:   [axlFormGridCancelPopup](11frmint.html#458986 "11")
:   [axlFormGridDeleteRows](11frmint.html#459010 "11")
:   [axlFormGridEvents](11frmint.html#459032 "11")
:   [axlFormGridGetCell](11frmint.html#459256 "11")
:   [axlFormGridInsertCol](11frmint.html#459328 "11")
:   [axlIsGridCellType](11frmint.html#467799 "11")
:   [axlFormGridInsertRows](11frmint.html#459407 "11")
:   [axlFormGridNewCell](11frmint.html#459451 "11")
:   [axlFormGridReset](11frmint.html#459504 "11")
:   [axlFormGridSetBatch](11frmint.html#459633 "11")
:   [axlFormGridUpdate](11frmint.html#468154 "11")
:   [axlFormInvalidateField](11frmint.html#459614 "11")
:   [axlFormIsFieldEditable](11frmint.html#468149 "11")
:   [axlFormListAddItem](11frmint.html#459736 "11")
:   [axlFormListDeleteItem](11frmint.html#459840 "11")
:   [axlFormListGetItem](11frmint.html#459821 "11")
:   [axlFormListGetSelCount](11frmint.html#468183 "11")
:   [axlFormListGetSelItems](11frmint.html#468467 "11")
:   [axlFormListOptions](11frmint.html#468753 "11")
:   [axlFormListSelAll](11frmint.html#468774 "11")
:   [axlFormMsg](11frmint.html#459971 "11")
:   [axlFormGetFieldType](11frmint.html#459906 "11")
:   [axlFormDefaultButton](11frmint.html#460129 "11")
:   [axlFormGridOptions](11frmint.html#460054 "11")
:   [axlFormSetActiveField](11frmint.html#461027 "11")
:   [axlFormSetDecimal](11frmint.html#460185 "11")
:   [axlFormSetFieldEditable](11frmint.html#460233 "11")
:   [axlFormSetFieldLimits](11frmint.html#460274 "11")
:   [axlFormTreeViewAddItem](11frmint.html#460322 "11")
:   [axlFormTreeViewChangeImages](11frmint.html#460588 "11")
:   [axlFormTreeViewChangeLabel](11frmint.html#460624 "11")
:   [axlFormTreeViewGetImages](11frmint.html#460366 "11")
:   [axlFormTreeViewGetLabel](11frmint.html#460667 "11")
:   [axlFormTreeViewGetParents](11frmint.html#460702 "11")
:   [axlFormTreeViewGetSelectState](11frmint.html#460739 "11")
:   [axlFormTreeViewLoadBitmaps](11frmint.html#460771 "11")
:   [axlFormTreeViewSet](11frmint.html#520741 "11")
:   [axlFormTreeViewSetSelectState](11frmint.html#460971 "11")

[12](12draw.md "12")
--------------------

[Simple Graphics Drawing Functions](12draw.html#1037521 "12")
-------------------------------------------------------------

[Functions](12draw.html#1065349 "12")

:   [axlGRPDrwBitmap](12draw.html#1075417 "12")
:   [axlGRPDrwCircle](12draw.html#1074897 "12")
:   [axlGRPDrwInit](12draw.html#1074902 "12")
:   [axlGRPDrwLine](12draw.html#1074929 "12")
:   [axlGRPDrwMapWindow](12draw.html#1074977 "12")
:   [axlGRPDrwPoly](12draw.html#1074983 "12")
:   [axlGRPDrwRectangle](12draw.html#1075013 "12")
:   [axlGRPDrwText](12draw.html#1075039 "12")
:   [axlGRPDrwUpdate](12draw.html#1075068 "12")

[13](13msghnd.md "13")
----------------------

[Message Handler Functions](13msghnd.html#673512 "13")
------------------------------------------------------

[Overview](13msghnd.html#673530 "13")

[Message Handler Functions](13msghnd.html#687747 "13")

:   [axlMsgPut](13msghnd.html#673546 "13")
:   [axlMsgContextPrint](13msghnd.html#673559 "13")
:   [axlMsgContextGetString](13msghnd.html#673573 "13")
:   [axlMsgContextGet](13msghnd.html#673584 "13")
:   [axlMsgContextTest](13msghnd.html#673595 "13")
:   [axlMsgContextInBuf](13msghnd.html#673606 "13")
:   [axlMsgContextRemove](13msghnd.html#673618 "13")
:   [axlMsgContextStart](13msghnd.html#673630 "13")
:   [axlMsgContextFinish](13msghnd.html#673642 "13")
:   [axlMsgContextClear](13msghnd.html#673653 "13")
:   [axlMsgCancelPrint](13msghnd.html#673664 "13")
:   [axlMsgCancelSeen](13msghnd.html#673676 "13")
:   [axlMsgClear](13msghnd.html#677014 "13")
:   [axlMsgSet](13msghnd.html#676586 "13")
:   [axlMsgTest](13msghnd.html#673712 "13")

[14](14dsnctl.md "14")
----------------------

[Design Control Functions](14dsnctl.html#688730 "14")
-----------------------------------------------------

[AXL-SKILL Design Control Functions](14dsnctl.html#693693 "14")

:   [axlCurrentDesign](14dsnctl.html#688736 "14")
:   [axlDesignType](14dsnctl.html#688746 "14")
:   [axlCompileSymbol](14dsnctl.html#705886 "14")
:   [axlSetSymbolType](14dsnctl.html#690003 "14")
:   [axlDBControl](14dsnctl.html#690074 "14")
:   [axlDBGetExtents](14dsnctl.html#730938 "14")
:   [axlDBIgnoreFixed](14dsnctl.html#715890 "14")
:   [axlDBIsReadOnly](14dsnctl.html#721395 "14")
:   [axlDBSectorSize - Obsolete](14dsnctl.html#717203 "14")
:   [axlGetDrawingName](14dsnctl.html#717176 "14")
:   [axlIgnoreFixed](14dsnctl.html#729461 "14")
:   [axlInTrigger](14dsnctl.html#721368 "14")
:   [axlInTriggerFunc](14dsnctl.html#735150 "14")
:   [axlIsSymbolEditor](14dsnctl.html#721385 "14")
:   [axlKillDesign](14dsnctl.html#711442 "14")
:   [axlOpenDesign](14dsnctl.html#690418 "14")
:   [axlOpenDesignForBatch](14dsnctl.html#710593 "14")
:   [axlRenameDesign](14dsnctl.html#690475 "14")
:   [axlSaveDesign](14dsnctl.html#690505 "14")
:   [axlSaveEnable](14dsnctl.html#711074 "14")
:   [axlDBChangeDesignExtents](14dsnctl.html#706236 "14")
:   [axlDBChangeDesignOrigin](14dsnctl.html#706271 "14")
:   [axlDBChangeDesignUnits](14dsnctl.html#706311 "14")
:   [axlDBCheck](14dsnctl.html#706276 "14")
:   [axlDBCopyPadstack](14dsnctl.html#706488 "14")
:   [axlDBDelLock](14dsnctl.html#708657 "14")
:   [axlDBGetLock](14dsnctl.html#706694 "14")
:   [axlDBMemoryReclaim](14dsnctl.html#728362 "14")
:   [axlDBSetLock](14dsnctl.html#706672 "14")
:   [axlDBTuneSectorSize](14dsnctl.html#716035 "14")
:   [axlTechnologyType](14dsnctl.html#706825 "14")
:   [axlTriggerClear](14dsnctl.html#706815 "14")
:   [axlTriggerPrint](14dsnctl.html#706903 "14")
:   [axlTriggerSet](14dsnctl.html#706908 "14")
:   [axlGetActiveLayer](14dsnctl.html#707686 "14")
:   [axlGetActiveTextBlock](14dsnctl.html#707713 "14")
:   [axlSetActiveLayer](14dsnctl.html#707735 "14")
:   [axlWFMAnyExported](14dsnctl.html#715943 "14")
:   [axlDBDisplayControl](14dsnctl.html#721955 "14")

[15](03dbcre8.md "15")
----------------------

[Database Create Functions](03dbcre8.html#854400 "15")
------------------------------------------------------

[Overview](03dbcre8.html#424859 "15")

[Path Functions](03dbcre8.html#367312 "15")

:   [axlPathStart](03dbcre8.html#435992 "15")
:   [axlPathArcRadius](03dbcre8.html#436067 "15")
:   [axlPathArcAngle](03dbcre8.html#882648 "15")
:   [axlPathArcCenter](03dbcre8.html#882649 "15")
:   [axlPathLine](03dbcre8.html#367364 "15")
:   [axlPathGetWidth](03dbcre8.html#367376 "15")
:   [axlPathSegGetWidth](03dbcre8.html#881988 "15")
:   [axlPathGetPathSegs](03dbcre8.html#367401 "15")
:   [axlPathGetLastPathSeg](03dbcre8.html#367414 "15")
:   [axlPathSegGetEndPoint](03dbcre8.html#367427 "15")
:   [axlPathSegGetArcCenter](03dbcre8.html#367440 "15")
:   [axlPathSegGetArcClockwise](03dbcre8.html#367453 "15")
:   [axlPathStartCircle](03dbcre8.html#423106 "15")
:   [axlPathOffset](03dbcre8.html#895775 "15")
:   [axlDB2Path](03dbcre8.html#895808 "15")
:   [axlDBCreatePath](03dbcre8.html#895769 "15")
:   [axlDBCreateLine](03dbcre8.html#367481 "15")
:   [axlDBCreateCircle](03dbcre8.html#367498 "15")

[Create Shape Interface](03dbcre8.html#367513 "15")

:   [axlDBCreateOpenShape](03dbcre8.html#438449 "15")
:   [axlDBCreateCloseShape](03dbcre8.html#367549 "15")
:   [axlDBActiveShape](03dbcre8.html#367559 "15")
:   [axlDBCreateVoidCircle](03dbcre8.html#367569 "15")
:   [axlDBCreateVoid](03dbcre8.html#367581 "15")
:   [axlDBCreateShape](03dbcre8.html#367593 "15")
:   [axlDBCreateRectangle](03dbcre8.html#367609 "15")

[Nonpath DBCreate Functions](03dbcre8.html#881387 "15")

:   [axlCreateBondFinger](03dbcre8.html#895658 "15")
:   [axlCreateBondWire](03dbcre8.html#895650 "15")
:   [axlDBCreateExternalDRC](03dbcre8.html#367631 "15")
:   [axlDBCreatePin](03dbcre8.html#890656 "15")
:   [axlDBCreateSymbol](03dbcre8.html#439738 "15")
:   [axlDBCreateSymbolSkeleton](03dbcre8.html#439990 "15")
:   [axlDBCreateText](03dbcre8.html#367746 "15")
:   [axlDBCreateVia](03dbcre8.html#897737 "15")
:   [axlDBCreateSymbolAutosilk](03dbcre8.html#881713 "15")
:   [axlCreateWirebondGuide](03dbcre8.html#895686 "15")

[Property Functions](03dbcre8.html#435890 "15")

:   [axlDBCreatePropDictEntry](03dbcre8.html#367783 "15")
:   [axlDBAddProp](03dbcre8.html#367701 "15")

[Load and Save Functions](03dbcre8.html#836346 "15")

:   [axlLoadPadstack](03dbcre8.html#836368 "15")
:   [axlLoadSymbol](03dbcre8.html#882503 "15")
:   [axlPadstackToDisk](03dbcre8.html#900567 "15")
:   [axlRefreshSymbol](03dbcre8.html#900626 "15")

[16](15dbgrp.md "16")
---------------------

[Database Group Functions](15dbgrp.html#1037521 "16")
-----------------------------------------------------

[Overview](15dbgrp.html#1065213 "16")

:   [axlDBAddGroupObjects](15dbgrp.html#1065349 "16")
:   [axlDBCreateGroup](15dbgrp.html#1076292 "16")
:   [axlDBDisbandGroup](15dbgrp.html#1076355 "16")
:   [axlDBGetGroupFromItem](15dbgrp.html#1079476 "16")
:   [axlDBGroupRename](15dbgrp.html#1079482 "16")
:   [axlDBRemoveGroupObjects](15dbgrp.html#1079477 "16")
:   [axlNetClassAdd](15dbgrp.html#1077527 "16")
:   [axlNetClassCreate](15dbgrp.html#1077736 "16")
:   [axlNetClassDelete](15dbgrp.html#1078088 "16")
:   [axlNetClassGet](15dbgrp.html#1078253 "16")
:   [axlNetClassRemove](15dbgrp.html#1078460 "16")
:   [axlRegionAdd](15dbgrp.html#1077519 "16")
:   [axlRegionCreate](15dbgrp.html#1076939 "16")
:   [axlRegionDelete](15dbgrp.html#1077191 "16")
:   [axlRegionRemove](15dbgrp.html#1077342 "16")

[17](16dbatt.md "17")
---------------------

[Database Attachment Functions](16dbatt.html#1037521 "17")
----------------------------------------------------------

[Overview](16dbatt.html#1065213 "17")

:   [axlCreateAttachment](16dbatt.html#1065349 "17")
:   [axlDeleteAttachment](16dbatt.html#1075932 "17")
:   [axlGetAllAttachmentNames](16dbatt.html#1075968 "17")
:   [axlGetAttachment](16dbatt.html#1076005 "17")
:   [axlIsAttachment](16dbatt.html#1076213 "17")
:   [axlSetAttachment](16dbatt.html#1076214 "17")

[18](17dbtran.md "18")
----------------------

[Database Transaction Functions](17dbtran.html#1037521 "18")
------------------------------------------------------------

:   [axlDBCloak](17dbtran.html#1065349 "18")
:   [axlDBTransactionCommit](17dbtran.html#1076340 "18")
:   [axlDBTransactionMark](17dbtran.html#1076368 "18")
:   [axlDBTransactionOops](17dbtran.html#1076373 "18")
:   [axlDBTransactionRollback](17dbtran.html#1076401 "18")
:   [axlDBTransactionStart](17dbtran.html#1076430 "18")

[19](18consmgt.md "19")
-----------------------

[Constraint Management Functions](18consmgt.html#1037521 "19")
--------------------------------------------------------------

[Overview](18consmgt.html#1065213 "19")

:   [axlCnsAddVia](18consmgt.html#1104370 "19")
:   [axlCnsAssignPurge](18consmgt.html#1076224 "19")
:   [axlCnsClassTableChange](18consmgt.html#1102955 "19")
:   [axlCnsClassTableCreate](18consmgt.html#1102983 "19")
:   [axlCnsClassTableDelete](18consmgt.html#1103600 "19")
:   [axlCnsClassTableFind](18consmgt.html#1102985 "19")
:   [axlCnsClassTableSeek](18consmgt.html#1104268 "19")
:   [axlCNSCreate](18consmgt.html#1106245 "19")
:   [axlCNSCsetLock](18consmgt.html#1110307 "19")
:   [axlCNSDelete](18consmgt.html#1110310 "19")
:   [axlCnsDeleteClassClassObjects](18consmgt.html#1092356 "19")
:   [axlCnsDeleteRegionClassClassObjects](18consmgt.html#1092421 "19")
:   [axlCnsDeleteRegionClassObjects](18consmgt.html#1092487 "19")
:   [axlCnsDeleteVia](18consmgt.html#1092387 "19")
:   [axlCNSDesignModeGet](18consmgt.html#1065349 "19")
:   [axlCNSDesignModeSet](18consmgt.html#1073830 "19")
:   [axlCNSDesignValueCheck](18consmgt.html#1065432 "19")
:   [axlCNSDesignValueGet](18consmgt.html#1073947 "19")
:   [axlCNSDesignValueSet](18consmgt.html#1074088 "19")
:   [axlCNSEcsetCreate](18consmgt.html#1074235 "19")
:   [axlCNSEcsetDelete](18consmgt.html#1074323 "19")
:   [axlCNSEcsetGet](18consmgt.html#1074324 "19")
:   [axlCNSEcsetModeGet](18consmgt.html#1074359 "19")
:   [axlCNSEcsetModeSet](18consmgt.html#1074474 "19")
:   [axlCNSEcsetValueCheck](18consmgt.html#1074568 "19")
:   [axlCNSEcsetValueGet](18consmgt.html#1074475 "19")
:   [axlCNSGetDefaultMinLineWidth](18consmgt.html#1083185 "19")
:   [axlCNSGetPhysical](18consmgt.html#1083339 "19")
:   [axlCNSGetPinDelayEnabled](18consmgt.html#1092650 "19")
:   [axlCNSGetPinDelayPVF](18consmgt.html#1092648 "19")
:   [axlCNSGetSameNet](18consmgt.html#1092689 "19")
:   [axlCNSGetSameNetXtalkEnabled](18consmgt.html#1093427 "19")
:   [axlCNSGetSpacing](18consmgt.html#1093423 "19")
:   [axlCNSGetViaZEnabled](18consmgt.html#1093527 "19")
:   [axlCNSGetViaZPVF](18consmgt.html#1093618 "19")
:   [axlCNSPhysicalModeGet](18consmgt.html#1093726 "19")
:   [axlCNSIsCsetLocked](18consmgt.html#1121133 "19")
:   [axlCNSIsLockedDomain](18consmgt.html#1121134 "19")
:   [axlCNSLockDomain](18consmgt.html#1121115 "19")
:   [axlCNSPhysicalModeSet](18consmgt.html#1094146 "19")
:   [axlCNSSameNetModeGet](18consmgt.html#1094771 "19")
:   [axlCNSSameNetModeSet](18consmgt.html#1095039 "19")
:   [axlCNSSetPhysical](18consmgt.html#1084387 "19")
:   [axlCNSSetSpacing](18consmgt.html#1111453 "19")
:   [axlCNSSetPinDelayEnabled](18consmgt.html#1095308 "19")
:   [axlCNSSetPinDelayPVF](18consmgt.html#1095398 "19")
:   [axlCNSSetSameNet](18consmgt.html#1095490 "19")
:   [axlCNSSetSameNetXtalkEnabled](18consmgt.html#1095920 "19")
:   [axlCNSSetViaZEnabled](18consmgt.html#1096005 "19")
:   [axlCNSSetViaZPVF](18consmgt.html#1096078 "19")
:   [axlCNSSpacingMax](18consmgt.html#1131567 "19")
:   [axlCNSSpacingMin](18consmgt.html#1131466 "19")
:   [axlCNSSpacingModeGet](18consmgt.html#1096197 "19")
:   [axlCNSSpacingModeSet](18consmgt.html#1096534 "19")
:   [axlCnsPurgeAll()](18consmgt.html#1096928 "19")
:   [axlCnsPurgeCsets](18consmgt.html#1096942 "19")
:   [axlCnsPurgeObjects](18consmgt.html#1097092 "19")
:   [axlViaZLength](18consmgt.html#1097191 "19")
:   [axlNetEcsetValueGet](18consmgt.html#1087126 "19")
:   [axlCNSEcsetValueSet](18consmgt.html#1074630 "19")
:   [axlCnsGetViaList](18consmgt.html#1076043 "19")
:   [axlGetAllViaList](18consmgt.html#1077466 "19")
:   [axlDRCUpdate](18consmgt.html#1081297 "19")
:   [axlDRCWaive](18consmgt.html#1079924 "19")
:   [axlDRCGetCount](18consmgt.html#1079214 "19")
:   [axlDRCItem](18consmgt.html#1079243 "19")
:   [axlDRCWaiveGetCount](18consmgt.html#1079288 "19")
:   [axlLayerSet](18consmgt.html#1077641 "19")
:   [axlCnsList](18consmgt.html#1110584 "19")
:   [axlCNSMapClear](18consmgt.html#1076663 "19")
:   [axlCNSMapUpdate](18consmgt.html#1074801 "19")
:   [axlCnsNetFlattened](18consmgt.html#1133015 "19")

[20](19cmdctl.md "20")
----------------------

[Command Control Functions](19cmdctl.html#978462 "20")
------------------------------------------------------

[AXL-SKILL Command Control Functions](19cmdctl.html#954294 "20")

:   [axlCmdRegister](19cmdctl.html#954297 "20")
:   [axlCmdUnregister](19cmdctl.html#954317 "20")
:   [axlEndSkillMode](19cmdctl.html#954328 "20")
:   [axlFlushDisplay](19cmdctl.html#954339 "20")
:   [axlOKToProceed](19cmdctl.html#963366 "20")
:   [axlSetLineLock](19cmdctl.html#954384 "20")
:   [axlSetRotateIncrement](19cmdctl.html#954402 "20")
:   [axlUIGetUserData](19cmdctl.html#954414 "20")
:   [axlUIPopupDefine](19cmdctl.html#954427 "20")
:   [axlUIPopupSet](19cmdctl.html#954439 "20")
:   [axlBuildClassPopup](19cmdctl.html#984532 "20")
:   [axlBuildSubclassPopup](19cmdctl.html#984545 "20")
:   [axlSubclassFormPopup](19cmdctl.html#984569 "20")
:   [axlVisibleUpdate](19cmdctl.html#984586 "20")

[21](20plyopr.md "21")
----------------------

[Polygon Operation Functions](20plyopr.html#1037521 "21")
---------------------------------------------------------

[About Polygon Operations](20plyopr.html#1075910 "21")

[AXL-SKILL Polygon Operation Attributes](20plyopr.html#1076003 "21")

[AXL-SKILL Polygon Operation Functions](20plyopr.html#1085420 "21")

:   [axlPolyFromDB](20plyopr.html#1076123 "21")
:   [axlPolyMemUse](20plyopr.html#1077325 "21")
:   [axlPolyOffset](20plyopr.html#1077718 "21")
:   [axlPolyOperation](20plyopr.html#1077319 "21")
:   [axlPolyExpand](20plyopr.html#1076223 "21")
:   [axlIsPolyType](20plyopr.html#1076291 "21")
:   [axlPolyFromHole](20plyopr.html#1076322 "21")
:   [axlPolyErrorGet](20plyopr.html#1076347 "21")

[Use Models](20plyopr.html#1076438 "21")

[22](21filacc.md "22")
----------------------

[Allegro PCB Editor File Access Functions](21filacc.html#38804 "22")
--------------------------------------------------------------------

[AXL-SKILL File Access Functions](21filacc.html#38810 "22")

:   [axlDMFileError](21filacc.html#652319 "22")
:   [axlDMFindFile](21filacc.html#652311 "22")
:   [axlDMGetFile](21filacc.html#40703 "22")
:   [axlDMOpenFile](21filacc.html#38826 "22")
:   [axlDMOpenLog](21filacc.html#652179 "22")
:   [axlDMClose](21filacc.html#652248 "22")
:   [axlDMBrowsePath](21filacc.html#650409 "22")
:   [axlDMDirectoryBrowse](21filacc.html#650452 "22")
:   [axlDMFileBrowse](21filacc.html#650496 "22")
:   [axlDMFileParts](21filacc.html#655376 "22")
:   [axlOSFileCopy](21filacc.html#650586 "22")
:   [axlOSFileMove](21filacc.html#650636 "22")
:   [axlOSSlash](21filacc.html#650668 "22")
:   [axlRecursiveDelete](21filacc.html#650739 "22")
:   [axlTempDirectory](21filacc.html#650778 "22")
:   [axlTempFile](21filacc.html#650783 "22")
:   [axlTempFileRemove](21filacc.html#650811 "22")

[23](22extrct.md "23")
----------------------

[Reports and Extract Functions](22extrct.html#665470 "23")
----------------------------------------------------------

[AXL-SKILL Data Extract Functions](22extrct.html#665474 "23")

:   [axlExtractToFile](22extrct.html#665476 "23")
:   [axlExtractMap](22extrct.html#665495 "23")
:   [axlReportList](22extrct.html#672158 "23")
:   [axlReportRegister](22extrct.html#675451 "23")

[24](23utils.md "24")
---------------------

[Utility Functions](23utils.html#756635 "24")
---------------------------------------------

:   [axlCheckString](23utils.html#929851 "24")
:   [axlCmdList](23utils.html#913642 "24")
:   [axlDebug](23utils.html#756141 "24")
:   [axlDetailLoad](23utils.html#917788 "24")
:   [axlDetailSave](23utils.html#925640 "24")
:   [axlEmail](23utils.html#914698 "24")
:   [axlHistory](23utils.html#929803 "24")
:   [axlHttp](23utils.html#911428 "24")
:   [axlIsDebug](23utils.html#913830 "24")
:   [axlIsProductLineActive](23utils.html#920201 "24")
:   [axlISProductStarted](23utils.html#941335 "24")
:   [axlLicDefaultVersion](23utils.html#945078 "24")
:   [axlLicFeatureExists](23utils.html#922655 "24")
:   [axlLicIsProductEnabled](23utils.html#922656 "24")
:   [axlLogHeader](23utils.html#911489 "24")
:   [axlMKS2UU](23utils.html#913774 "24")
:   [axlMKSAlias](23utils.html#911586 "24")
:   [axlMKSConvert](23utils.html#913784 "24")
:   [axlMKSStr2UU](23utils.html#911603 "24")
:   [axlMapClassName](23utils.html#911688 "24")
:   [axlMemSize](23utils.html#911693 "24")
:   [axlOSBackSlash](23utils.html#929945 "24")
:   [axlOSControl](23utils.html#929974 "24")
:   [axlOSNtp](23utils.html#941516 "24")
:   [axlPPrint](23utils.html#911727 "24")
:   [axlPdfView](23utils.html#911798 "24")
:   [axlPrintDbid](23utils.html#932613 "24")
:   [axlRegexpIs](23utils.html#911833 "24")
:   [axlRunBatchDBProgram](23utils.html#911838 "24")
:   [axlShowObject](23utils.html#927096 "24")
:   [axlSleep](23utils.html#914328 "24")
:   [axlSort](23utils.html#914325 "24")
:   [axlStrcmpAlpNum](23utils.html#912258 "24")
:   [axlStringCSVParse](23utils.html#929886 "24")
:   [axlStringRemoveSpaces](23utils.html#929915 "24")
:   [axlVersion](23utils.html#913164 "24")
:   [axlVersionIdGet](23utils.html#912587 "24")
:   [axlVersionIdPrint](23utils.html#912635 "24")

[25](24mthutl.md "25")
----------------------

[Math Utility Functions](24mthutl.html#1037521 "25")
----------------------------------------------------

[Overview](24mthutl.html#1065213 "25")

:   [axlDegToRad](24mthutl.html#1083945 "25")
:   [axlDistance](24mthutl.html#1085632 "25")
:   [axlGeo2Str](24mthutl.html#1077434 "25")
:   [axlGeoArcCenterAngle](24mthutl.html#1078190 "25")
:   [axlGeoArcCenterRadius](24mthutl.html#1078318 "25")
:   [axlGeoEqual](24mthutl.html#1080527 "25")
:   [axlGeoRotatePt](24mthutl.html#1082761 "25")
:   [axlGeoPointsEqual](24mthutl.html#1076790 "25")
:   [axlIsBetween](24mthutl.html#1084159 "25")
:   [axlIsPointInsideBox](24mthutl.html#1075662 "25")
:   [axlIsPointOnLine](24mthutl.html#1075689 "25")
:   [axlLineSlope](24mthutl.html#1075704 "25")
:   [axlLineXLine](24mthutl.html#1075765 "25")
:   [axlMathConstants](24mthutl.html#1088431 "25")
:   [axlMathDotProduct](24mthutl.html#1090832 "25")
:   [axlMidPointArc](24mthutl.html#1088434 "25")
:   [axlMidPointLine](24mthutl.html#1084008 "25")
:   [axlMPythag](24mthutl.html#1076082 "25")
:   [axlMUniVector](24mthutl.html#1077779 "25")
:   [axlMXYAdd](24mthutl.html#1076329 "25")
:   [axlMXYMult](24mthutl.html#1078010 "25")
:   [axlMXYSub](24mthutl.html#1076545 "25")
:   [axlRadToDeg](24mthutl.html#1083972 "25")
:   [axl\_ol\_ol2](24mthutl.html#1076324 "25")
:   [bBoxAdd](24mthutl.html#1079864 "25")

[26](25dbmisc.md "26")
----------------------

[Database Miscellaneous Functions](25dbmisc.html#1037521 "26")
--------------------------------------------------------------

[Overview](25dbmisc.html#1065213 "26")

:   [axlAirGap](25dbmisc.html#1073939 "26")
:   [axlBackDrill](25dbmisc.html#1080061 "26")
:   [axlDBGetLength](25dbmisc.html#1081218 "26")
:   [axlDBGetManhattan](25dbmisc.html#1077976 "26")
:   [axlDBGetSymbolBodyExtent](25dbmisc.html#1095181 "26")
:   [axlDBPinPairLength](25dbmisc.html#1095182 "26")
:   [axlDeleteByLayer](25dbmisc.html#1095212 "26")
:   [axlExtentDB](25dbmisc.html#1095185 "26")
:   [axlExtentLayout](25dbmisc.html#1065432 "26")
:   [axlExtentSymbol](25dbmisc.html#1065544 "26")
:   [axlFindPath](25dbmisc.html#1095243 "26")
:   [axlGeoPointInShape](25dbmisc.html#1066799 "26")
:   [axlGeoPointShapeInfo](25dbmisc.html#1080089 "26")
:   [axlGetImpedance](25dbmisc.html#1089568 "26")
:   [axlImpdedanceGetLayerBroadsideDPImp](25dbmisc.html#1076247 "26")
:   [axlImpdedanceGetLayerBroadsideDPWidth](25dbmisc.html#1076248 "26")
:   [axlImpdedanceGetLayerEdgeDPImp](25dbmisc.html#1076505 "26")
:   [axlImpdedanceGetLayerEdgeDPSpacing](25dbmisc.html#1076777 "26")
:   [axlImpdedanceGetLayerEdgeDPWidth](25dbmisc.html#1076996 "26")
:   [axlImpedance2Width](25dbmisc.html#1077241 "26")
:   [axlPadOnLayer](25dbmisc.html#1095281 "26")
:   [axlPinExport](25dbmisc.html#1078217 "26")
:   [axlPinImport](25dbmisc.html#1095314 "26")
:   [axlReratNet](25dbmisc.html#1095344 "26")
:   [axlText2Lines](25dbmisc.html#1097245 "26")
:   [axlUnfixAll](25dbmisc.html#1095392 "26")
:   [axlWidth2Impedance](25dbmisc.html#1077749 "26")
:   [axlIsHighlighted](25dbmisc.html#1077752 "26")
:   [axlTestPoint](25dbmisc.html#1073615 "26")
:   [axlChangeNet](25dbmisc.html#1073658 "26")
:   [axlSegDelayAndZ0](25dbmisc.html#1073778 "26")
:   [axlSetDefaultDieInformation](25dbmisc.html#1080128 "26")

[27](msexl.md "27")
-------------------

[Microsoft Excel Integration Functions](msexl.html#1065083 "27")
----------------------------------------------------------------

:   [axlSpreadsheetClose](msexl.html#1065095 "27")
:   [axlSpreadsheetDefineCell](msexl.html#1065096 "27")
:   [axlSpreadsheetDoc](msexl.html#1065097 "27")
:   [axlSpreadsheetGetCell](msexl.html#1067927 "27")
:   [axlSpreadsheetGetRGBColorString](msexl.html#1067947 "27")
:   [axlSpreadsheetGetRGBForNamedColor](msexl.html#1067966 "27")
:   [axlSpreadsheetGetStyles](msexl.html#1067985 "27")
:   [axlSpreadsheetGetWorksheets](msexl.html#1068002 "27")
:   [axlSpreadsheetGetWorksheetSize](msexl.html#1068019 "27")
:   [axlSpreadsheetInit](msexl.html#1068036 "27")
:   [axlSpreadsheetRead](msexl.html#1069134 "27")
:   [axlSpreadsheetReadDelimited](msexl.html#1068081 "27")
:   [axlSpreadsheetSetCell](msexl.html#1068101 "27")
:   [axlSpreadsheetSetCellProp](msexl.html#1075986 "27")
:   [axlSpreadsheetSetColumnProp](msexl.html#1068141 "27")
:   [axlSpreadsheetSetDocProp](msexl.html#1068160 "27")
:   [axlSpreadsheetSetRowProp](msexl.html#1068177 "27")
:   [axlSpreadsheetSetStyle](msexl.html#1068196 "27")
:   [axlSpreadsheetSetStyleBorder](msexl.html#1070205 "27")
:   [axlSpreadsheetSetStyleParent](msexl.html#1070391 "27")
:   [axlSpreadsheetSetStyleProp](msexl.html#1068263 "27")
:   [axlSpreadsheetSetWorksheet](msexl.html#1068285 "27")
:   [axlSpreadsheetWrite](msexl.html#1068304 "27")

[28](27plugin.md "28")
----------------------

[Plugin Functions](27plugin.html#1037521 "28")
----------------------------------------------

[Overview](27plugin.html#1065213 "28")

:   [SKILL Programming](27plugin.html#1084153 "28")
:   [DLL Programming](27plugin.html#1084169 "28")
:   [Input/Output Data Primitives](27plugin.html#1084243 "28")
:   [Programming Restrictions, Cautions and Hints](27plugin.html#1084287 "28")
:   [Performance Considerations](27plugin.html#1084328 "28")
:   [Cadence Customer Support](27plugin.html#1084341 "28")
:   [Examples](27plugin.html#1084348 "28")
:   [axlDllCall](27plugin.html#1082969 "28")
:   [axlDllCallList](27plugin.html#1091355 "28")
:   [axlDllClose](27plugin.html#1083879 "28")
:   [axlDllDump](27plugin.html#1083931 "28")
:   [axlDllOpen](27plugin.html#1087703 "28")
:   [axlDllSym](27plugin.html#1088093 "28")

[29](27langexten.md "29")
-------------------------

[Skill Language Extensions](27langexten.html#1064814 "29")
----------------------------------------------------------

:   [axldo](27langexten.html#1066448 "29")
:   [copyDeep](27langexten.html#1065090 "29")
:   [isBoxp](27langexten.html#1065091 "29")
:   [lastelem](27langexten.html#1067560 "29")
:   [letStar](27langexten.html#1067563 "29")
:   [listnindex](27langexten.html#1065094 "29")
:   [movedown](27langexten.html#1065095 "29")
:   [moveup](27langexten.html#1065096 "29")
:   [parseFile](27langexten.html#1066150 "29")
:   [parseQuotedString](27langexten.html#1066152 "29")
:   [pprintln](27langexten.html#1065539 "29")
:   [propNames](27langexten.html#1065541 "29")

[30](26logacc.md "30")
----------------------

[Logic Access Functions](26logacc.html#1037521 "30")
----------------------------------------------------

[Overview](26logacc.html#1065213 "30")

:   [axlDBAssignNet](26logacc.html#1092015 "30")
:   [axlDBCreateConceptComponent](26logacc.html#1065349 "30")
:   [axlDBCreateComponent](26logacc.html#1076090 "30")
:   [axlDBCreateManyModuleInstances](26logacc.html#1076329 "30")
:   [axlDBCreateModuleDef](26logacc.html#1075174 "30")
:   [axlDBCreateModuleInstance](26logacc.html#1075221 "30")
:   [axlDBCreateNet](26logacc.html#1092110 "30")
:   [axlDBCreateSymDefSkeleton](26logacc.html#1076599 "30")
:   [axlDBDummyNet](26logacc.html#1087265 "30")
:   [axlDbidName](26logacc.html#1076610 "30")
:   [axlDiffPair](26logacc.html#1075197 "30")
:   [axlDiffPairAuto](26logacc.html#1075277 "30")
:   [axlDiffPairDBID](26logacc.html#1075366 "30")
:   [axlMatchGroupAdd](26logacc.html#1076859 "30")
:   [axlMatchGroupCreate](26logacc.html#1077223 "30")
:   [axlMatchGroupDelete](26logacc.html#1077449 "30")
:   [axlMatchGroupProp](26logacc.html#1078079 "30")
:   [axlMatchGroupRemove](26logacc.html#1080542 "30")
:   [axlNetSched](26logacc.html#1081079 "30")
:   [axlPinPair](26logacc.html#1078535 "30")
:   [axlPinPairSeek](26logacc.html#1078813 "30")
:   [axlPinsOfNet](26logacc.html#1078733 "30")
:   [axlRemoveNet](26logacc.html#1075367 "30")
:   [axlRenameNet](26logacc.html#1091800 "30")
:   [axlRenameRefdes](26logacc.html#1075491 "30")
:   [axlSchedule](26logacc.html#1083124 "30")
:   [axlScheduleNet](26logacc.html#1081172 "30")
:   [axlWriteDeviceFile](26logacc.html#1075859 "30")
:   [axlWritePackageFile](26logacc.html#1075894 "30")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
