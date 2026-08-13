# Class: Psp2CapBaseInfoSubsIter

index: int &
size: int
str: CString
Psp2CapBaseInfo_ReadChar(buffer, index, size) : returns char
Parameters:
buffer: unsigned char *
index: int &
size: int
Psp2CapBaseInfo_ReadString(buffer, index, size) : returns CString
Parameters:
buffer: unsigned char *
index: int &
size: int
START class Psp2CapBaseInfoSubsIter
NextSub() : returns Psp2CapBaseInfo
Class : Psp2CapBaseInfoSubsIter
Parameters:
END class Psp2CapBaseInfoSubsIter
DboExtBlobNodeToDboExtBlobNodePsp2Cap(x) : returns DboExtBlobNodePsp2Cap
Parameters:
x: DboExtBlobNode *
START class DboExtBlobNodePsp2Cap(DboExtBlobNode):
LoadNodeData(pNodeData) : returns bool
Class : DboExtBlobNodePsp2Cap(DboExtBlobNode):
Parameters:
pNodeData: DboExtBlobNode::BlobNodeData_t *
StoreNodeData(pBuffer) : returns size_t
Class : DboExtBlobNodePsp2Cap(DboExtBlobNode):
Parameters:
pBuffer: ExtDataBytePtrT

---

SetData(pPspiceData)
Class : DboExtBlobNodePsp2Cap(DboExtBlobNode):
Parameters:
pPspiceData: Psp2CapBaseInfo *
GetData() : returns Psp2CapBaseInfo
Class : DboExtBlobNodePsp2Cap(DboExtBlobNode):
Parameters:
END class DboExtBlobNodePsp2Cap(DboExtBlobNode):
START class DboMiscFileWriter
GetOrCreateMiscStorageForWrite(pRootStorage, pSubStorage) : returns DboMiscFileWriter
Class : DboMiscFileWriter
Parameters:
pRootStorage: char *
pSubStorage: char *
GetMiscStorageForRead(pRootStorage, pSubStorage) : returns DboMiscFileWriter
Class : DboMiscFileWriter
Parameters:
pRootStorage: char *
pSubStorage: char *
AddFileStream(pStreamFileName, pDescr) : returns int
Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *
pDescr: char *
UpdateFileStream(pStreamFileName) : returns int
Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *
DeleteFileStream(pStreamFileName) : returns int
Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *

---

ReleaseStorage()
Class : DboMiscFileWriter
Parameters:
GetFileStreamData(pStreamFileName) : returns std::string
Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *
GetFileInfo(pStreamFileName, pFileInfo) : returns int
Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *
pFileInfo: std::string &
GetAllFileInfo() : returns std::string
Class : DboMiscFileWriter
Parameters:
GetFileList() : returns std::string
Class : DboMiscFileWriter
Parameters:
WasStorageOpenSuccessful() : returns int
Class : DboMiscFileWriter
Parameters:
IsThisUserStorageCreationAllowed(pStorageName) : returns int
Class : DboMiscFileWriter
Parameters:
pStorageName: char *
DumpFileAs(pStreamFileName, pFilePath)
Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *
pFilePath: char *
GetStreamInfoStringType(pStreamFileName, pAttrName) : returns std::string

---

Class : DboMiscFileWriter
Parameters:
pStreamFileName: char *
pAttrName: char *
IsOKToOverWrite(streamName, pDstFilePath, pReplace) : returns int
Class : DboMiscFileWriter
Parameters:
streamName: char *
pDstFilePath: char *
pReplace: int
IsOKToPullIn(streamName, pDstFilePath, pReplace) : returns int
Class : DboMiscFileWriter
Parameters:
streamName: char *
pDstFilePath: char *
pReplace: int
GetFileCreationTime(pFilepath) : returns std::string
Class : DboMiscFileWriter
Parameters:
pFilepath: char *
END class DboMiscFileWriter
DboMiscFileWriter_GetOrCreateMiscStorageForWrite(pRootStorage, pSubStorage) : returns
DboMiscFileWriter
Parameters:
pRootStorage: char *
pSubStorage: char *
DboMiscFileWriter_GetMiscStorageForRead(pRootStorage, pSubStorage) : returns DboMiscFileWriter
Parameters:
pRootStorage: char *
pSubStorage: char *
DboMiscFileWriter_IsThisUserStorageCreationAllowed(pStorageName) : returns int
Parameters:
pStorageName: char *