# Class: StatusInfo

START class StatusInfo
END class StatusInfo
START class CAmbiguousParts
DeleteAmbiguousMapForBOM(BOMName) : returns int
Class : CAmbiguousParts
Parameters:

---

BOMName: CString
DeletePartFromGrpSGrp(BOMName, GrpSGrpName, Id, RevertOthers = 0) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
GrpSGrpName: CString
Id: UINT
RevertOthers: int
DeletePartFromGrpSGrp(BOMName, GrpSGrpName, Id) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
GrpSGrpName: CString
Id: UINT
DelteGrpSGrpFromAllBOM(GroupSGrpName, Flg = 0) : returns int
Class : CAmbiguousParts
Parameters:
GroupSGrpName: CString
Flg: int
DelteGrpSGrpFromAllBOM(GroupSGrpName) : returns int
Class : CAmbiguousParts
Parameters:
GroupSGrpName: CString
DeleteAllPartsFromGrpSGrp(BOMName, GrpSGrpName, Flg = 0) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
GrpSGrpName: CString
Flg: int
DeleteAllPartsFromGrpSGrp(BOMName, GrpSGrpName) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
GrpSGrpName: CString

---

DeletePartsFromBOM(BOMName, Id) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
Id: UINT
RevertToAmbiguous(BOMName, IdArray) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
IdArray: CUIntArray &
RevertToAmbiguous(BOMName, GrpSGrpName) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
GrpSGrpName: CString
GetStatus(BOMName, Id, GrpSGrpName) : returns CString
Class : CAmbiguousParts
Parameters:
BOMName: CString
Id: UINT
GrpSGrpName: CString
AddPartToMap(BOMName, Id, PartStatus, GrpSGrpName) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
Id: UINT
PartStatus: CString
GrpSGrpName: CString
GetPartsCount(BOMName, Id) : returns int
Class : CAmbiguousParts
Parameters:
BOMName: CString
Id: UINT

---

RevertToAmbiguousInAllBOM(GrpSGrpName, Id) : returns int
Class : CAmbiguousParts
Parameters:
GrpSGrpName: CString
Id: UINT
DeletePartFromAllBOM(GrpSGrpName, Id) : returns int
Class : CAmbiguousParts
Parameters:
GrpSGrpName: CString
Id: UINT
DeletePartFromAllBOM(Id) : returns int
Class : CAmbiguousParts
Parameters:
Id: UINT
GetAmbugityStoreforBOM(l_strBOMVar, l_strBOMambData)
Class : CAmbiguousParts
Parameters:
l_strBOMVar: CString &
l_strBOMambData: CString &
SetAmbiguousDataForBOM(l_strBOMName, l_strbomPartAmbData)
Class : CAmbiguousParts
Parameters:
l_strBOMName: CString &
l_strbomPartAmbData: CString &
END class CAmbiguousParts
START class CPartMgmt
GetCisDesign(pDesign) : returns CISDesign
Class : CPartMgmt
Parameters:
pDesign: DboDesign *
UpdateAllPartStatus() : returns int
Class : CPartMgmt

---

SetCisAutomation(value) : returns int
Class : CPartMgmt
Parameters:
value: int
END class CPartMgmt
CPartMgmt_GetCisDesign(pDesign) : returns CISDesign
Parameters:
pDesign: DboDesign *
CPartMgmt_UpdateAllPartStatus() : returns int
CPartMgmt_SetCisAutomation(value) : returns int
Parameters:
value: int
START class CISTclHelper
sMakeCSStringArray() : returns CSStringArray
Class : CISTclHelper
sMakeQUIntArray() : returns QUIntArray
Class : CISTclHelper
sMakeCStringArray() : returns CStringArray
Class : CISTclHelper
sAddToCStringArray(pArray, str)
Class : CISTclHelper
Parameters:
pArray: CStringArray &
str: CString &
sRemoveFromCStringArray(pArray, pIndex)
Class : CISTclHelper
Parameters:
pArray: CStringArray &
pIndex: int

---

sGetCStringArraySize(pArray) : returns int
Class : CISTclHelper
Parameters:
pArray: CStringArray &
sGetCString(pArray, pIndex) : returns CString
Class : CISTclHelper
Parameters:
pArray: CStringArray &
pIndex: int
sMakeCUIntArray() : returns CUIntArray
Class : CISTclHelper
sAddToCUIntArray(pArray, num)
Class : CISTclHelper
Parameters:
pArray: CUIntArray &
num: int
sRemoveFromCUIntArray(pArray, pIndex)
Class : CISTclHelper
Parameters:
pArray: CUIntArray &
pIndex: int
sGetCUIntArraySize(pArray) : returns int
Class : CISTclHelper
Parameters:
pArray: CUIntArray &
sGetUInt(pArray, pIndex) : returns int
Class : CISTclHelper
Parameters:
pArray: CUIntArray &
pIndex: int
sGetUINTFromIntRef(p) : returns UINT
Class : CISTclHelper

---

Parameters:
p: int &
sGetUINTFromInt(p) : returns UINT
Class : CISTclHelper
Parameters:
p: int
sGetIntFromUINTRef(p) : returns int
Class : CISTclHelper
Parameters:
p: UINT &
sGetIntFromUINT(p) : returns int
Class : CISTclHelper
Parameters:
p: UINT
sMakeCPartProp() : returns CPartProp
Class : CISTclHelper
sReleaseAllCreatedPtrs()
Class : CISTclHelper
END class CISTclHelper
CISTclHelper_sMakeCSStringArray() : returns CSStringArray
CISTclHelper_sMakeQUIntArray() : returns QUIntArray
CISTclHelper_sMakeCStringArray() : returns CStringArray
CISTclHelper_sAddToCStringArray(pArray, str)
Parameters:
pArray: CStringArray &
str: CString &
CISTclHelper_sRemoveFromCStringArray(pArray, pIndex)
Parameters:
pArray: CStringArray &

---

pIndex: int
CISTclHelper_sGetCStringArraySize(pArray) : returns int
Parameters:
pArray: CStringArray &
CISTclHelper_sGetCString(pArray, pIndex) : returns CString
Parameters:
pArray: CStringArray &
pIndex: int
CISTclHelper_sMakeCUIntArray() : returns CUIntArray
CISTclHelper_sAddToCUIntArray(pArray, num)
Parameters:
pArray: CUIntArray &
num: int
CISTclHelper_sRemoveFromCUIntArray(pArray, pIndex)
Parameters:
pArray: CUIntArray &
pIndex: int
CISTclHelper_sGetCUIntArraySize(pArray) : returns int
Parameters:
pArray: CUIntArray &
CISTclHelper_sGetUInt(pArray, pIndex) : returns int
Parameters:
pArray: CUIntArray &
pIndex: int
CISTclHelper_sGetUINTFromIntRef(p) : returns UINT
Parameters:
p: int &
CISTclHelper_sGetUINTFromInt(p) : returns UINT
Parameters:
p: int