# Class: CPMgtCfg

CISTclHelper_sGetIntFromUINTRef(p) : returns int
Parameters:
p: UINT &
CISTclHelper_sGetIntFromUINT(p) : returns int
Parameters:
p: UINT
CISTclHelper_sMakeCPartProp() : returns CPartProp
CISTclHelper_sReleaseAllCreatedPtrs()
START class CPMgtCfg
GetTotalRecords() : returns long
Class : CPMgtCfg
Parameters:
AddMultiValuedField(pFieldName)
Class : CPMgtCfg
Parameters:
pFieldName: char const *
RemoveMultiValuedField(pFieldName)
Class : CPMgtCfg
Parameters:
pFieldName: char const *
GetMultiValuedCount() : returns int
Class : CPMgtCfg
Parameters:
GetMultiValuedAtPos(index) : returns char
Class : CPMgtCfg
Parameters:
index: int
RemoveAllMultiValuedField()
Class : CPMgtCfg
Parameters:

---

IsMultiValuedField(pFieldName) : returns int
Class : CPMgtCfg
Parameters:
pFieldName: char const *
IsTableUsed(strTableName) : returns int
Class : CPMgtCfg
Parameters:
strTableName: CString
SetAutoPartTypeRefreshFlag(AutoPartTypeRefresh)
Class : CPMgtCfg
Parameters:
AutoPartTypeRefresh: int
GetAutoPartTypeRefreshFlag() : returns int
Class : CPMgtCfg
Parameters:
GetUsedTablesCount() : returns int
Class : CPMgtCfg
Parameters:
PropTypeSettingOK(PropertyType, TableName) : returns int
Class : CPMgtCfg
Parameters:
PropertyType: PropertyTypeT
TableName: CString &
GetPropertyFieldName(PropertyType, Name)
Class : CPMgtCfg
Parameters:
PropertyType: PropertyTypeT
Name: CString &
GetPropertyFieldName(PropName, Name)
Class : CPMgtCfg
Parameters:
PropName: CString const &

---

Name: CString &
GetPropertyDBFieldName(PropertyType, Name)
Class : CPMgtCfg
Parameters:
PropertyType: PropertyTypeT
Name: CString &
GetPropertyDBFieldName(PropName, Name)
Class : CPMgtCfg
Parameters:
PropName: CString const &
Name: CString &
GetPropertyDBFieldName(TableName, PropertyType, Name)
Class : CPMgtCfg
Parameters:
TableName: CString const &
PropertyType: PropertyTypeT
Name: CString &
GetPropertyValidFieldName(TableName, PropertyType, Name)
Class : CPMgtCfg
Parameters:
TableName: CString const &
PropertyType: PropertyTypeT
Name: CString &
GetDBCName() : returns CString
Class : CPMgtCfg
Parameters:
GetIniDBCName() : returns CString
Class : CPMgtCfg
Parameters:
GetNumDbs() : returns int
Class : CPMgtCfg
Parameters:

---

GetDbCfg(DbIndex) : returns CPMgtDbCfg
Class : CPMgtCfg
Parameters:
DbIndex: int
GetDbCfg(DbIndex) : returns CPMgtDbCfg
Class : CPMgtCfg
Parameters:
DbIndex: int
GetFirstTable(RefdesPrefix = "") : returns int
Class : CPMgtCfg
Parameters:
RefdesPrefix: CString
GetFirstTable() : returns int
Class : CPMgtCfg
Parameters:
GetNextTable(AfterTableIndex, RefdesPrefix = "")
Class : CPMgtCfg
Parameters:
AfterTableIndex: int &
RefdesPrefix: CString
GetNextTable(AfterTableIndex)
Class : CPMgtCfg
Parameters:
AfterTableIndex: int &
GetTableIndex(TableName, bChkUsed = 1) : returns int
Class : CPMgtCfg
Parameters:
TableName: CString const &
bChkUsed: int
GetTableIndex(TableName) : returns int
Class : CPMgtCfg
Parameters:
TableName: CString const &

---

GetLastModificationTime(T, FName = None) : returns bool
Class : CPMgtCfg
Parameters:
T: CTime &
FName: char const *
GetLastModificationTime(T) : returns bool
Class : CPMgtCfg
Parameters:
T: CTime &
GetModificationTime(time)
Class : CPMgtCfg
Parameters:
time: CTime &
GetAllowDuplicatePartNumbers() : returns int
Class : CPMgtCfg
Parameters:
GetTransferBlankProperties() : returns int
Class : CPMgtCfg
Parameters:
GetPartTypeDelimiter() : returns char
Class : CPMgtCfg
Parameters:
GetAutomaticTempPartNumber() : returns int
Class : CPMgtCfg
Parameters:
GetTempPartNumberPrefx() : returns CString
Class : CPMgtCfg
Parameters:
GetTempPartNumberTablename() : returns CString
Class : CPMgtCfg
Parameters:

---

GetDoNotStuffString() : returns CString
Class : CPMgtCfg
Parameters:
GetMultiValuesCellDelimiter() : returns CString
Class : CPMgtCfg
Parameters:
GetICAFieldList(Refresh = 1) : returns CStringArray
Class : CPMgtCfg
Parameters:
Refresh: int
GetICAFieldList() : returns CStringArray
Class : CPMgtCfg
Parameters:
GetICADefinedTables(ICATables)
Class : CPMgtCfg
Parameters:
ICATables: CStringArray &
UpdateFieldList()
Class : CPMgtCfg
Parameters:
GetCDSDistList(DistList) : returns int
Class : CPMgtCfg
Parameters:
DistList: CStringArray &
GetSelectedSupList() : returns CStringArray
Class : CPMgtCfg
Parameters:
GetTopSupNumber() : returns int
Class : CPMgtCfg
Parameters:

---

GetMechPartMappingTableName() : returns CString
Class : CPMgtCfg
Parameters:
IsKeyed() : returns int
Class : CPMgtCfg
Parameters:
IsValidFieldName(Name) : returns int
Class : CPMgtCfg
Parameters:
Name: CString const &
HasProperty(PropertyType) : returns int
Class : CPMgtCfg
Parameters:
PropertyType: PropertyTypeT
HasProperty(PropName) : returns int
Class : CPMgtCfg
Parameters:
PropName: CString const &
IsModified() : returns int
Class : CPMgtCfg
Parameters:
CheckRules() : returns int
Class : CPMgtCfg
Parameters:
IsDBCVersionCurrent(FName = None) : returns int
Class : CPMgtCfg
Parameters:
FName: char const *
IsDBCVersionCurrent() : returns int
Class : CPMgtCfg
Parameters:

---

AtLeastOneTableHasProperty(PropertyType) : returns int
Class : CPMgtCfg
Parameters:
PropertyType: PropertyTypeT
DoesTempPartNumberTableExist(TableType, pPrecision = None) : returns int
Class : CPMgtCfg
Parameters:
TableType: TableT &
pPrecision: long *
DoesTempPartNumberTableExist(TableType) : returns int
Class : CPMgtCfg
Parameters:
TableType: TableT &
DoesTempPartnumberTabeExist() : returns TableT
Class : CPMgtCfg
Parameters:
Initialize()
Class : CPMgtCfg
Parameters:
OpenPartDatabase(ReadOnly = 1) : returns int
Class : CPMgtCfg
Parameters:
ReadOnly: int
OpenPartDatabase() : returns int
Class : CPMgtCfg
Parameters:
GetOpenPartDatabase() : returns int
Class : CPMgtCfg
Parameters:
EmptyDbArray()
Class : CPMgtCfg
Parameters:

---

FindTable(TableName, TableIndex)
Class : CPMgtCfg
Parameters:
TableName: CString const &
TableIndex: int &
DelDb(Index)
Class : CPMgtCfg
Parameters:
Index: int
AddDb(pDbFileName) : returns CPMgtDbCfg
Class : CPMgtCfg
Parameters:
pDbFileName: char const *
Serialize(ar)
Class : CPMgtCfg
Parameters:
ar: CArchive &
ReadDBC(ConfigDBC = 0, FName = None, SuppressWarnings = 0) : returns int
Class : CPMgtCfg
Parameters:
ConfigDBC: int
FName: char const *
SuppressWarnings: int
ReadDBC(ConfigDBC = 0, FName = None) : returns int
Class : CPMgtCfg
Parameters:
ConfigDBC: int
FName: char const *
ReadDBC(ConfigDBC = 0) : returns int
Class : CPMgtCfg
Parameters:
ConfigDBC: int

---

ReadDBC() : returns int
Class : CPMgtCfg
Parameters:
WriteDBC(pNewDBCName = None) : returns int
Class : CPMgtCfg
Parameters:
pNewDBCName: char const *
WriteDBC() : returns int
Class : CPMgtCfg
Parameters:
FindDbFilePath(FileName) : returns CString
Class : CPMgtCfg
Parameters:
FileName: CString const &
CheckDbFmt() : returns int
Class : CPMgtCfg
Parameters:
UpdateTablesList() : returns int
Class : CPMgtCfg
Parameters:
GetFieldDetailsForTable(DbIndex) : returns int
Class : CPMgtCfg
Parameters:
DbIndex: int
GetViewTables(m_ViewTables) : returns int
Class : CPMgtCfg
Parameters:
m_ViewTables: set< string > &
GetFieldDetailsForTableForRelational(DbIndex, primaryKey) : returns bool
Class : CPMgtCfg
Parameters:
DbIndex: int

---

primaryKey: string const &
SetModified(mod)
Class : CPMgtCfg
Parameters:
mod: int
UpdateSQLStatement()
Class : CPMgtCfg
Parameters:
BuildFieldMap()
Class : CPMgtCfg
Parameters:
SetDBCOk()
Class : CPMgtCfg
Parameters:
SetLastModificationTime(time)
Class : CPMgtCfg
Parameters:
time: CTime const &
SetICAFieldList(StrField)
Class : CPMgtCfg
Parameters:
StrField: CString
SetAllowDuplicatePartNumbers(Dup)
Class : CPMgtCfg
Parameters:
Dup: int
SetTransferBlankProperties(Xfr)
Class : CPMgtCfg
Parameters:
Xfr: int
SetPartTypeDelimiter(delimiter)

---

Class : CPMgtCfg
Parameters:
delimiter: char
SetAutomaticTempPartNumber(Allow)
Class : CPMgtCfg
Parameters:
Allow: int
SetTempPartNumberPrefx(Prefix)
Class : CPMgtCfg
Parameters:
Prefix: CString const &
SetTempPartNumberTableName(TableName)
Class : CPMgtCfg
Parameters:
TableName: CString const &
SetSelectedSupList(Arr)
Class : CPMgtCfg
Parameters:
Arr: CStringArray const &
SetTopSupNumber(Top)
Class : CPMgtCfg
Parameters:
Top: int const &
SetDoNotStuffString(DoNotStuffString)
Class : CPMgtCfg
Parameters:
DoNotStuffString: CString const &
SetMultiValuesCellDelimiter(Delimiter)
Class : CPMgtCfg
Parameters:
Delimiter: CString const &
SetMechPartMappingTableName(strName)

---

Class : CPMgtCfg
Parameters:
strName: CString const &
SetOldVersion(nVal)
Class : CPMgtCfg
Parameters:
nVal: int
SetAsPartNumber(Partnum)
Class : CPMgtCfg
Parameters:
Partnum: int
SetAsPartReference(PartRef)
Class : CPMgtCfg
Parameters:
PartRef: int
GetPartNumber() : returns int
Class : CPMgtCfg
Parameters:
GetPartReference() : returns int
Class : CPMgtCfg
Parameters:
SetOccLevelLink(bVal)
Class : CPMgtCfg
Parameters:
bVal: int
GetOccLevelLink() : returns int
Class : CPMgtCfg
Parameters:
SetExtendedLinkMode(bVal)
Class : CPMgtCfg
Parameters:
bVal: int

---

GetExtendedLinkMode() : returns int
Class : CPMgtCfg
Parameters:
GetSaveQueryFile() : returns CString
Class : CPMgtCfg
Parameters:
SetSaveQueryFile(pFile)
Class : CPMgtCfg
Parameters:
pFile: char const *
CheckSectionExistDBC(pSectionName, pProfileFileName) : returns int
Class : CPMgtCfg
Parameters:
pSectionName: LPCTSTR
pProfileFileName: LPCTSTR
GetDBCFromIni(ProfileName, DBCString)
Class : CPMgtCfg
Parameters:
ProfileName: CString
DBCString: CString &
GetDemoDBCFromIni(ProfileName, DBCString)
Class : CPMgtCfg
Parameters:
ProfileName: CString
DBCString: CString &
GetLocalProfileNameDBC() : returns CString
Class : CPMgtCfg
Parameters:
GetMasterProfileNameDBC() : returns CString
Class : CPMgtCfg
Parameters:

---

CreateTempPartNumberTable() : returns int
Class : CPMgtCfg
Parameters:
IsOK() : returns int
Class : CPMgtCfg
Parameters:
IsOldVersion() : returns int
Class : CPMgtCfg
Parameters:
END class CPMgtCfg
OrCISGetDbcConfig() : returns CPMgtCfg
CISAddSearchQuery(pProperty, lCompare, lValue) : returns char
Parameters:
pProperty: char const *
lCompare: char const *
lValue: char const *
CISExecuteQuery()
CISDumpExplorerView(pFile)
Parameters:
pFile: char const *
CISExplorerSelectOption(start, end, option)
Parameters:
start: int
end: int
option: int
SetCISExplorerFont(pFontName) : returns char
Parameters:
pFontName: char const *
SetCISExplorerFontSize(size) : returns char
Parameters: