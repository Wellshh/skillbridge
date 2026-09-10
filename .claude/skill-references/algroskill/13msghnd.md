### axlMsgPut

`axlMsgPut( g_message_format [g_arg1 ...] ) => t`

#### Description

Puts a message in the journal file. Use this function to "print" messages. It buffers any errors or warnings, but processes other message classes immediately.

#### Arguments

| Name | Description |
|---|---|
| `g_message_format` | Context message (`printf` like) format string. See "Overview" for a description of messages and valid arguments. |
| `g_arg1` ... | Values for substitution arguments for the format string. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`axlMsgPut(list("Cannot find via %s" 3) "VIA10")``⇒ t`

### axlMsgContextPrint

`axlMsgContextPrint( r_context ) => t`

#### Description

Prints the buffered messages and removes them from the message buffer.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. Prints messages only for this context (or any children). An argument of `nil` causes `axlMsgContextPrint` to look through all contexts. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example" in the beginning of this chapter.

`axlMsgContextPrint(context)``⇒ t`

Prints the buffered messages in that context to SKILL command line:

`W- My warning`

`E- My error`

`F- My fatal error BAD ERROR`

### axlMsgContextGetString

`axlMsgContextGetString( r_context ) => lt_messages/nil`

#### Description

Gets the messages in the message buffer and removes them from the buffer. Call `axlMsgContextGetString` subsequently to communicate those messages to the user (for example, in a log file).

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. Gets messages only for this context (or any children). An argument of `nil` causes `axlMsgContextGetString` to look through all contexts. |

#### Value Returns

| Name | Description |
|---|---|
| `lt_messages` | List of the text strings of the buffered messages. |
| `nil` | No buffered messages found. |

#### Examples

See the "Message Handler Example".

`axlMsgContextGetString(context)``⇒ ("My warning" "My error" "My fatal error BAD ERROR")`

### axlMsgContextGet

`axlMsgContextGet( r_context ) => lt_format_strings/nil`

#### Description

Gets the format strings of the buffered messages. (Not the messages themselves. Compare the example here and the one shown for `axlMsgContextGetString`.) Does not remove the messages from the message buffer, rather it simply provides the caller an alternative to making a number of `axlMsgContextInBuf` calls.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. Gets messages only for this context (or any children). An argument of `nil` causes `axlMsgContextGet` to look through all contexts. |

#### Value Returns

| Name | Description |
|---|---|
| `lt_format_strings` | List of format strings of the buffered messages. |
| `nil` | No buffered messages found. |

#### Examples

See the "Message Handler Example".

`mylist = axlMsgContextGet(context)``⇒ ("My warning" "My error" "My fatal error %s")`

### axlMsgContextTest

`axlMsgContextTest( r_context ) => x_class`

#### Description

Returns the most severe message class of the messages in the context message buffer. See axlMsgContextInBuf to check for a particular message class.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. Looks only for messages for this context. If `r_context` is `nil`, `axlMsgContextTest` looks through all contexts. |

#### Value Returns

| Name | Description |
|---|---|
| `x_class` | The most severe message class of the messages in the message buffer of the given context. |

#### Examples

See the Message Handler Example.

`printf("Message severity %d\n" axlMsgContextTest(context))``⇒ Message severity 4`

### axlMsgContextInBuf

`axlMsgContextInBuf( r_context t_format_string ) => t`

#### Description

Checks whether message `t_format_string` is in the message buffer of context `r_context`. Gives the application the ability to control code flow based on a particular message reported by a called function. The check is based on the original format string, not the fully substituted message.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. Looks only for messages in this context (or any children). If `r_context` is `nil`, `axlMsgContextInBuf` looks through all contexts. |
| `t_format_string` | Format string of the message. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Specified message is in the buffer. |
| `nil` | Specified message is not in the buffer. |

#### Examples

See the "Message Handler Example".

`if( axlMsgContextInBuf(context "My error")``printf(%s\n" "My error is there"))`

### axlMsgContextRemove

`axlMsgContextRemove( r_context t_format_string ) => t`

#### Description

Removes a message (or messages) from the buffered messages. Lets you remove messages (usually warnings) from the buffer that you decide, later in a procedure, that you do not want the user to see.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. Removes messages for only this context (or any children). If `r_context` is `nil`, `axlMsgContextRemove` looks through all contexts. |
| `t_format_string` | Format string of the message. The match for the message in the buffer ignores the substitution parameters used to generate the full text of the message. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`axlMsgContextRemove(context, "My fatal error %s")``⇒ t`

### axlMsgContextStart

`axlMsgContextStart( g_format_string [g_arg1 ...] ) => r_context`

#### Description

Indicates the start of a message context. Prints any buffered messages for the context.

#### Arguments

| Name | Description |
|---|---|
| `g_format_string` | Context message (`printf` like) message format string. |
| `g_arg1` ... | Values for the substitution arguments for the format string. Use `axlMsgClear` (and `Test`/`Set`) functions to control code flow if the function returns insufficient values. |

#### Value Returns

| Name | Description |
|---|---|
| `r_context` | Context handle to use in subsequent `axlMsgContext` calls. |

#### Examples

See the "Message Handler Example".

`context = axlMsgContextStart("Messages for %s" "add line")``Messages for add line``5`

### axlMsgContextFinish

`axlMsgContextFinish( r_context ) => t`

#### Description

Indicates the finish of a message context. Prints any buffered messages in the context and clears the context buffer.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`context = axlMsgContextStart()``... do some things ...``axlMsgContextFinish(context)`

### axlMsgContextClear

`axlMsgContextClear( r_context ) => t`

#### Description

Clears the buffered messages for a context.

Note: You should not normally use this function. Use functions that print (`axlMsgContextPrint`) or retrieve (`axlMsgContextGetString`) messages and then clear them, or use a context finish (`axlMsgContextFinish`) that forces the messages to be printed.

#### Arguments

| Name | Description |
|---|---|
| `r_context` | Context handle from `axlMsgContextStart`. If `r_context` is `nil`, clears all messages in all contexts. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`context = axlMsgContextStart()``... do some things ...``axlMsgContextClear(context)`

### axlMsgCancelPrint

`axlMsgCancelPrint() => t`

#### Description

Prints a message informing the user that he requested cancel. Since the severity of this message is Error (3), AXL writes it to the context buffer as it does other warning, error, and fatal messages. Call this function only from a routine that requests user input.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`axlMsgCancelPrint()`

Sets severity level to 2 (warning) and puts the following into the message buffer (if `axlMsgSys` messages are in English):

`User CANCEL received`

### axlMsgCancelSeen

`axlMsgCancelSeen() => t/nil`

#### Description

Checks to see if the `axlMsgCancelPrint` message was printed. Does not poll the input stream for a CANCEL key. Checks the buffer of current messages for the occurrence of the `axlSsgSys.cancelRequest` message.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t` | Requested cancel has been seen. |
| `nil` | No requested cancel has been seen. |

#### Examples

See the "Message Handler Example".

`if( axlMsgCancelSeen()``; clear input and return``...`

### axlMsgClear

`axlMsgClear() => t`

#### Description

Clears the current error severity level. You can reset the severity by first saving it using `axlMsgTest`, then setting it using `axlMsgSet`.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`axlMsgClear()`

### axlMsgSet

`axlMsgSet( x_class ) => t`

#### Description

Sets the current error severity level. Use only to reset the severity cleared using `axlMsgClear`.

#### Arguments

| Name | Description |
|---|---|
| `x_class` | Severity level. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See the "Message Handler Example".

`level = axlMsgTest()``; Do something``...``axlMsgSet(level)`

### axlMsgTest

`axlMsgTest() => x_class`

#### Description

Determines the current error severity level. Returns a single number giving the severity level of the most severe message that has been printed since the last `axlMsgClear` or `axlMsgContextClear`/`Print`/`GetMsg` call.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `x_class` | Highest severity level of all the messages currently in the message buffer. |

#### Examples

See the "Message Handler Example".

`level = axlMsgTest()``⇒ 4`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

