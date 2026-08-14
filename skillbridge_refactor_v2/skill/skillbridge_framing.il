; Explicit response framing for the Python SkillBridge daemon.
;
; Python sends one command terminated by LF.  SKILL returns exactly one frame:
;
;   success: STX (0x02) + payload + RS (0x1E)
;   failure: NAK (0x15) + payload + RS (0x1E)
;
; The payload may contain newlines.  Do not place ASCII RS (0x1E) inside a
; payload; normal %L-formatted SKILL values do not contain it.

SB_STX = intToChar(2)
SB_NAK = intToChar(21)
SB_RS  = intToChar(30)

procedure(SBWriteFrame(ipcId marker payload)
    ipcWriteProcess(
        ipcId
        sprintf(nil "%s%s%s" marker payload SB_RS)
    )
)

procedure(SBWriteSuccess(ipcId value)
    SBWriteFrame(ipcId SB_STX sprintf(nil "%L" value))
)

procedure(SBWriteFailure(ipcId value)
    SBWriteFrame(ipcId SB_NAK sprintf(nil "%L" value))
)

; Example callback.  Merge the SBWriteSuccess/SBWriteFailure calls into the
; data handler that your existing ipcBeginProcess registration already uses.
;
; Wrapping in progn allows multiple forms in one request and returns the last
; form.  Remove the progn wrapper if your existing command grammar differs.
procedure(SBExampleDataHandler(ipcId data)
    let((result)
        if(errset(result = evalstring(strcat("(progn " data ")"))) then
            SBWriteSuccess(ipcId result)
        else
            SBWriteFailure(ipcId errset.errset)
        )
    )
)
