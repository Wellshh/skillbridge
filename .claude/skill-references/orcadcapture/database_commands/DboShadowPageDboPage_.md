# Class: DboShadowPage(DboPage):

DboPage_sGetVerticalLabelIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetVerticalLabelIsAscending(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetVerticalSeparatorLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetVerticalSeparatorLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_IsValidNetName(csNetName) : returns int
Parameters:
csNetName: CString &
DboPage_PartAlreadyExistsWithName(UniqueNm) : returns int
Parameters:
UniqueNm: CString
DboPageToDboShadowPage(x) : returns DboShadowPage
Parameters:
x: DboPage *
START class DboShadowPage(DboPage):
GetObjectType() : returns ObjectTypeT
Class : DboShadowPage(DboPage):
Parameters:
END class DboShadowPage(DboPage):