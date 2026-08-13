### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

17
==

Database Attachment Functions
=============================

Overview
--------

This chapter describes the AXL-SKILL Database Attachment functions.

### axlCreateAttachment

```
axlCreateAttachment(t_attachmentIdt_passwdx_revisions_dataFormatt_data)⇒ o_attachment/nil
```

#### Description

Creates a new Allegro PCB Editor database attachment with the given attachment id. The attachment may optionally be given a password and a revision number. The attachment data may be specified as a string or as a file name.

`axlDBControl('maxAttachmentSize)` returns the maximum size of data that can attach to the database.

* ***Do NOT create or replace attachments you do not own. This includes any predefined Allegro attachments like DFA or quickviews.***

#### Arguments

|  |
| --- | ---
| `t_attachmentId` | Id or name of the attachment to retrieve. Can be up to 31 characters in length.
| `t_passwd` | Password for this attachment. Can be up to 31 characters in length. If no password is desired this may be`nil`.
| `x_revision` | Revision number of the attachment. If`nil`, the revision number is set to zero.
| `s_dataFormat` | Indicates the format of the`t_data` argument.  Permitted values:  'string -- the value of the t\_data argument is used for the attachment data.  'file -- t\_data references an ASCII file that is read into the database attachment.
|
|
|
| `t_data` | 'binary -- t\_data references a binary file that is read into the database attachment. Use this option with zip or compressed files.
#### Value Returned

|  |
| --- | ---
| `o_attachment` | AXL id for the new attachment, which can then be queried using the right arrow (->) operator.
| `nil` | Failed to create an attachment due to incorrect arguments.
**Note:** Once an attachment is password protected it needs to be deleted, then re-added to remove or change the password protection.

#### See Also

[axlGetAttachment](#1076005 "17")

#### EXAMPLE

This uses an attachment to store in the database a list of variables. For example, you design a form where the user enters in their preferences and you manage them in Skill via a disembodied property list. You would like to store the user's preferences with the design.

Create an attachment name, DO NOT USE "fxf". I would suggest using an underscore, company name and application to make it unique. For example,`_acme_bom_rpt`, would be a good attachment name.

`attachName = "fxf"`

; A typical disembodied property list

`mylist = ncons(nil)`

`mylist->ccw = t`

`mylist->middle = nil`

`mylist->cx = 0.12`

`mylist->cy = 10.192`

`mylist->layer = "TOP"`

**Note:** Do NOT store dbid's in the disembodied list or make sure to remove them before storing as an attachment.

Store list in current design (assuming user saves design)

`dataString = sprintf(nil " '%L" mylist)`

`axlCreateAttachment(attachName nil 0 'string dataString)`

Next time user runs the Skill code, here is how to init the list:

`attach = axlGetAttachment(attachName 'string)`

> `if( attach) then`

> > `mylist = car(errsetstring(attach->data))`

> `else ; no list stored in design so init to default settings`

> > `mylist = ncons(nil)`

> > `mylist->ccw = t`

> `)`

### axlDeleteAttachment

`axlDeleteAttachment(t_attachmentId[t_passwd])⇒ t/nil`

#### Description

Deletes the given attachment. If the attachment is password protected, the correct password must be given.

* ***Do NOT delete attachments you do not own. This includes any predefined Allegro attachments like DFA or quickviews.***

#### Arguments

|  |
| --- | ---
| `t_attachmentId` | Id or name of the attachment to delete.
| `t_passwd` | Password for this attachment.
#### Value Returned

|  |
| --- | ---
| `t` | Attachment successfully deleted.
| `nil` | Attachment not deleted.
#### See Also

[axlGetAttachment](#1076005 "17")

### axlGetAllAttachmentNames

`axlGetAllAttachmentNames()⇒ l_attachment/nil`

#### Description

Returns a list of the ids for all database attachments in the current Allegro PCB Editor database. If no attachments are present, then`nil` is returned. The attachments can retrieved using the [axlGetAttachment](#1076005 "17")`()` function.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `l_attachment` | List of attachment ids.
| `nil` | No attachments exist in the database.
### axlGetAttachment

`axlGetAttachment(t_attachmentId[s_dataFormat])⇒ o_attachment/nil`

#### Description

Returns the database attachment with the given id. If the attachment exists, an*attachment record* is returned containing information about the attachment. The data is in the format specified by the `s_dataFormat` argument. If `'file` format, then the `data` attribute contains a temporary file name to which the data was written. If `'string`, then the `data` attribute contains the attachment data itself. If the `s_dataFormat` argument is omitted or is `nil`, then the `data` attribute is `nil`.

The attachment record has the following attributes:

|  |  |  |
| --- | --- | --- | ---
| ****Name**** | **Type** | **Set?** | **Description**
| `objType` | string | NO | Is always "`attachment"`.
| `id` | string | NO | Id (name) of the attachment.
| `password` | boolean | NO | `t`/`nil` - Indicates if the attachment is password protected.
| `timeStamp` | integer | NO | Indicates the time last modified in seconds.
| `revision` | integer | YES | User defined revision number for the attachment data.
| `dataFormat` | symbol | YES | Indicates the format of the data stored in the "data" attribute and is one of`'file`, `'string`, or `nil` (in which case the data is not displayed.)  'file is displayed if you 'binary option to create the attachment.
| `data` | string | YES | Attachment data. May be a file name, the data itself, or`nil` depending on the value of the `dataFormat` attribute.
| timeStamp | integer | NO | Indicates the size of the attachment.
* ***Access to attachments in the private database is allowed. Do not create, change, or delete these attachments. The rule for attachments access is:
  If your application did NOT create the attachment do NOT change it.***

#### Arguments

* Id or name of the attachment to retrieve. Can be up to 31 characters in length.
* `nil:`use the method destribe in the attachmennt dataFormat attribute.
* `'string:`return data as a string.
* `'file:`return data stored in a tmp file. You should use this option if you used 'binary method to create the attachment.

#### Value Returned

|  |
| --- | ---
| `o_attachment` | AXL id for the attachment structure which can be queried using the right arrow (->) operator.
| `nil` | Attachment does not exist.
#### Example

`attachment = axlGetAttachment("attachmentOne" 'file)`

`⇒ attachment:attachmentOne`

#### See Also

[axlIsAttachment](#1076213 "17"), [axlGetAllAttachmentNames](#1075968 "17"), [axlCreateAttachment](#1065349 "17"), [axlSetAttachment](#1076214 "17"), [axlDeleteAttachment](#1075932 "17")

### axlIsAttachment

`axlIsAttachment(o_attachment)⇒ t/nil`

#### Description

Determines if the given object is an AXL attachment.

#### Arguments

|  |
| --- | ---
| `o_attachment` | Object to check.
#### Value Returned

|  |
| --- | ---
| `t` | Object is an attachment.
| `nil` | Object is not an attachment.
#### See Also

[axlGetAttachment](#1076005 "17")

### axlSetAttachment

`axlSetAttachment(o_attachment[t_password])⇒ o_attachment/nil`

#### Description

Modifies an existing Allegro PCB Editor database attachment with the data contained in the given AXL attachment id. Original attachment object must be obtained from the`axlCreateAttachment`, `axlGetAttachment`, or `axlGetAllAttachments` function. The attachment revision number and the attachment data may both be modified.

Format of the data is determined by the`dataFormat` attribute structure, which may be set by the user. If `"``dataFormat``"` is `'string`, then the value of the `data` attribute is used for the new attachment data. If "`dataFormat`" is `'file`, then the value of the `data` attribute is a file name from which the attachment data is read.

If the existing attachment is password protected, you must provide the correct password or the function fails.

#### Arguments

|  |
| --- | ---
| `o_attachment` | AXL id of the existing attachment to be modified. The`revision`, `dataFormat`, and `data` attributes may all be set to new values by the user.
| `t_password` | Password for the given existing attachment. If this does not match the password of the existing attribute, the attachment update fails. If the existing attachment is not password protected, you may omit this.
#### Value Returned

|  |
| --- | ---
| `o_attachment` | AXL id of the modified attachment.
| `nil` | Failed to modify the attachment.
**Note:** Once an attachment is password protected, to remove or change the password protection you must delete and then re-add the attachment.

#### See Also

[axlGetAttachment](#1076005 "17")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
