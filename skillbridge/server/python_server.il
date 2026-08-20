let((_filename _baseName _moduleFolder _logDirectory _executable _unbound)

    _filename = get_filename(piport)
    _filename = pcreReplace(pcreCompile("^ +| +$") _filename "" 0)
    _baseName = substring(_filename 1 strlen(_filename)-2)
    _moduleFolder = substring(_filename 1 strlen(_filename)-23)
    _executable = strcat("\"" _baseName "py\"")
    _logDirectory = getShellEnvVar("SKILLBRIDGE_LOG_DIRECTORY") || "."
    _unbound = makeTable("JustForUnbound")[""]

    ; Thin wrappers around the internal (non-redefinable) IPC built-ins so that
    ; tests can putd-mock them. User-defined, so they carry no "internal" flag.
    putd('__pyIpcBeginProcess nil)
    defun(__pyIpcBeginProcess (@rest args)
        apply('ipcBeginProcess args)
    )

    putd('__pyIpcKillProcess nil)
    defun(__pyIpcKillProcess (@rest args)
        apply('ipcKillProcess args)
    )

    putd('__pyIpcWriteProcess nil)
    defun(__pyIpcWriteProcess (@rest args)
        apply('ipcWriteProcess args)
    )

    putd('__pyWriteFrame nil)
    defun(__pyWriteFrame (id marker payload)
        __pyIpcWriteProcess(
            id
            lsprintf("%s%s%s" marker payload __pyWriteFrame.RS)
        )
    )

    ; Frame markers match protocol/response.py: STX, NAK, RST start payload; RS ends it.
    __pyWriteFrame.STX = intToChar(2)
    __pyWriteFrame.NAK = intToChar(21)
    __pyWriteFrame.RST = intToChar(18)
    __pyWriteFrame.RS = intToChar(30)

    putd('__pyIpcWait nil)
    defun(__pyIpcWait (@rest args)
        apply('ipcWait args)
    )

    putd('__pySpawnServer nil)
    defun(__pySpawnServer ()
        let((executableWithArgs process)
            pyStartServer.state = 'starting
            pyStartServer.receiveBuffer = ""

            executableWithArgs = lsprintf(
                "%s %L %s"
                pyStartServer.exe
                pyStartServer.id
                pyStartServer.logLevel
            )

            if(pyStartServer.singleMode then
                executableWithArgs = lsprintf(
                    "%s --single"
                    executableWithArgs
                )
            )

            if(pyStartServer.forceTcp then
                executableWithArgs = lsprintf(
                    "%s --force-tcp"
                    executableWithArgs
                )
            )

            if(pyStartServer.timeout then
                executableWithArgs = lsprintf(
                    "%s --timeout %L"
                    executableWithArgs
                    pyStartServer.timeout
                )
            )

            executableWithArgs = lsprintf(
                "\"%s\" %s"
                pyStartServer.python
                executableWithArgs
            )

            process = __pyIpcBeginProcess(
                executableWithArgs
                ""
                '__pyOnData
                '__pyOnError
                '__pyOnFinish
                pyStartServer.logName
            )

            if(process then
                pyStartServer.ipc = process
                pyStartServer.state = 'running
                t
            else
                pyStartServer.ipc = nil
                pyStartServer.state = 'stopped
                fprintf(stderr "failed to start server\n")
                nil
            )
        )
    )

    putd('pyKillServer nil)
    defun(pyKillServer ()
        if(!pyStartServer.ipc then
            printf("server was not running\n")
            nil
        else
            pyStartServer.restartPending = nil
            pyStartServer.state = 'stopping

            ; ipcKillProcess only requests termination. The process handle
            ; remains owned by __pyOnFinish until the matching callback arrives.
            __pyIpcKillProcess(pyStartServer.ipc)
            t
        )
    )

    putd('pyRestartServer nil)
    defun(pyRestartServer ()
        if(!pyStartServer.ipc then
            __pySpawnServer()
        else
            pyStartServer.restartPending = t
            pyStartServer.state = 'restarting

            if(pyStartServer.requestIpc == pyStartServer.ipc then
                ; This function is being evaluated for a request from the
                ; Python daemon itself. __pyOnData returns a "restart" response.
                ; The daemon acknowledges the client and then exits gracefully.
                t
            else
                ; Called directly from CIW or another SKILL entry point.
                ; There is no client response to preserve, so termination can
                ; be requested immediately.
                __pyIpcKillProcess(pyStartServer.ipc)
                t
            )
        )
    )

    putd('pyReloadScript nil)
    defun(pyReloadScript ()
        printf("killing the old server\n")
        pyKillServer()
        load(pyReloadServer.filename)
        t
    )

    pyReloadServer.filename = _filename

    putd('pyShowLog nil)
    defun(pyShowLog (@optional (length 20) "x")
        if(!fixp(length) || length <= 0 then
            fprintf(
                stderr
                "pyShowLog: length must be a positive integer\n"
            )
            nil
        else
            let((
                fin
                line
                (lines declare(lines[length]))
                (ptr 0)
                (count 0)
                (start 0)
                i
            )
                fin = infile(pyShowLog.logName)

                if(!fin then
                    fprintf(
                        stderr
                        "pyShowLog: cannot open log file %s\n"
                        pyShowLog.logName
                    )
                    nil
                else
                    unwindProtect(
                        while(gets(line fin)
                            lines[ptr] = line
                            ptr = mod(ptr + 1 length)

                            when(count < length
                                count = count + 1
                            )
                        )
                        close(fin)
                    )

                    ; Before the buffer fills, valid lines start at index 0.
                    ; After it fills, ptr points to the oldest retained line.
                    if(count < length then
                        start = 0
                    else
                        start = ptr
                    )

                    when(count > 0
                        for(i 0 count-1
                            printf(
                                "%s"
                                lines[mod(start + i length)]
                            )
                        )
                    )

                    printf("")
                    t
                )
            )
        )
    )

    pyShowLog.logName = lsprintf(
        "%s/skillbridge_skill.log"
        _logDirectory
    )

    putd('__pyCaptureWarnings nil)
    defmacro(__pyCaptureWarnings (@rest body)
        `let(((tempPort outstring()))
            unwindProtect(
                {
                    let(((woport tempPort))
                        ,@body
                        ; next two lines are to force final warning to be flushed
                        warn("")
                        getWarn()
                    )
                    getOutstring(tempPort)
                }
                close(tempPort)
            )
        )
    )

    putd('__pyOnData nil)
    defun(__pyOnData (id data)
        when(id == pyStartServer.ipc
            let((newlineTail lineLength line)
                pyStartServer.receiveBuffer = strcat(
                    pyStartServer.receiveBuffer
                    data
                )
                newlineTail = index(pyStartServer.receiveBuffer "\n")

                while(newlineTail
                    lineLength = strlen(pyStartServer.receiveBuffer) - strlen(newlineTail)
                    when(
                        lineLength > 0 &&
                        substring(pyStartServer.receiveBuffer lineLength 1) == intToChar(13)
                        lineLength = lineLength - 1
                    )
                    when(lineLength > 0
                        line = substring(
                            pyStartServer.receiveBuffer
                            1
                            lineLength
                        )
                    )
                    pyStartServer.receiveBuffer =
                        substring(newlineTail 2) || ""

                    when(lineLength > 0
                        let((result capturedWarning pythonCode responseMarker)
                            ; Remember which process is currently executing the request.
                            pyStartServer.requestIpc = id

                            capturedWarning = __pyCaptureWarnings(
                                errset(result=evalstring(line))
                            )

                            if((errset.errset) then
                                printf(
                                    "command %L resulted in error %L\n"
                                    line
                                    errset.errset
                                )
                                __pyWriteFrame(
                                    id
                                    __pyWriteFrame.NAK
                                    lsprintf("%L" errset.errset)
                                )
                            else
                                if(boundp('result) then
                                    pythonCode = __pySkillToPython(result)

                                    if(
                                        capturedWarning != "" &&
                                        capturedWarning != "*WARNING* "
                                    then
                                        pythonCode = lsprintf(
                                            "warning(%L, %s)"
                                            capturedWarning
                                            pythonCode
                                        )
                                    )

                                    if(
                                        pyStartServer.restartPending &&
                                        id == pyStartServer.ipc
                                    then
                                        responseMarker = __pyWriteFrame.RST
                                    else
                                        responseMarker = __pyWriteFrame.STX
                                    )

                                    __pyWriteFrame(
                                        id
                                        responseMarker
                                        pythonCode
                                    )
                                else
                                    __pyWriteFrame(
                                        id
                                        __pyWriteFrame.STX
                                        "error('unbound')"
                                    )
                                )
                            )

                            pyStartServer.requestIpc = nil
                        )
                    )

                    newlineTail = index(pyStartServer.receiveBuffer "\n")
                )
            )
        )
    )

    putd('__pyOnError nil)
    defun(__pyOnError (_ data)
        fprintf(stderr "PYTHON: %s\n" data)
    )

    putd('__pyOnFinish nil)
    defun(__pyOnFinish (id exitStatus)
        if(id == pyStartServer.ipc then
            let((shouldRestart)
                printf(
                    "server was stopped with code %L\n"
                    exitStatus
                )

                shouldRestart = pyStartServer.restartPending

                pyStartServer.ipc = nil
                pyStartServer.requestIpc = nil
                pyStartServer.restartPending = nil
                pyStartServer.receiveBuffer = ""
                pyStartServer.state = 'stopped

                when(shouldRestart
                    __pySpawnServer()
                )
            )
        else
            printf(
                "ignoring stale server finish callback with code %L\n"
                exitStatus
            )
        )
    )

    putd('__pyOnFinishScript nil)
    defun(__pyOnFinishScript (_ data)
        printf("script finished with code %L\n" data)
    )

    putd('__pyPropertyListToPython nil)
    defun(__pyPropertyListToPython (propList)
        ; Iterate the raw (key val key val ...) pairs in list order. propList->?
        ; returns property names in unspecified (often LIFO) order, which made the
        ; serialized dict key order nondeterministic; reading the pairs directly
        ; preserves the construction order of a literal disembodied property list.
        let((rest parts)
            rest = cdr(propList)
            while(rest
                parts = cons(
                    lsprintf("'%s':%s" car(rest) __pySkillToPython(cadr(rest)))
                    parts
                )
                rest = cddr(rest)
            )
            strcat(
                "{"
                buildString(reverse(parts) ",")
                "}"
            )
        )
    )

    putd('__pySaveToVariableAndReturn nil)
    defun(__pySaveToVariableAndReturn (thing)
        let((repr variableName split objectType address variableSymbol)
            repr = lsprintf("%L" thing)

            if(rexExecute(repr) then
                split = buildString(parseString(repr "_") "")
                split = parseString(split "@:")
                objectType = car(split)
                address = cadr(split)
                variableName = lsprintf(
                    "__py_%s_%s"
                    objectType
                    address
                )
                set(stringToSymbol(variableName) thing)
                lsprintf("Remote(%L)" variableName)
            else if(otherp(thing) then
                variableSymbol = gensym("__py_OTHER_")
                set(variableSymbol thing)
                lsprintf(
                    "Remote(%L)"
                    symbolToString(variableSymbol)
                )
            else if(portp(thing) then
                variableSymbol = gensym("__py_openfile_")
                set(variableSymbol thing)
                lsprintf(
                    "Remote(%L)"
                    symbolToString(variableSymbol)
                )
            else
                printf("I COULD NOT PARSE %L\n" repr)
                lsprintf("error(%L)" repr)
            )))
        )
    )

    putd('__pyListToPython nil)
    defun(__pyListToPython (thing)
        strcat(
            "["
            buildString(mapcar('__pySkillToPython thing) ",")
            "]"
        )
    )

    putd('__pyVectorToPython nil)
    defun(__pyVectorToPython (collection)
        let((symbol)
            symbol = gensym("__py_vector_")
            set(symbol collection)
            lsprintf(
                "Vector(%L)"
                symbolToString(symbol)
            )
        )
    )

    putd('__pyTableToPython nil)
    defun(__pyTableToPython (collection)
        let((symbol)
            symbol = gensym("__py_table_")
            set(symbol collection)
            lsprintf(
                "Table(%L)"
                symbolToString(symbol)
            )
        )
    )

    putd('__pySkillToPython nil)
    defun(__pySkillToPython (thing)
        if(thing == t then
            "True"
        else if(!thing then
            "None"
        else if(or(numberp(thing) stringp(thing)) then
            lsprintf("%L" thing)
        else if(symbolp(thing) then
            lsprintf("Symbol('%s')" thing)
        else if(listp(thing) then
            if(
                and(
                    !car(thing)
                    symbolp(cadr(thing))
                    cadr(thing) != t
                )
            then
                __pyPropertyListToPython(thing)
            else
                __pyListToPython(thing)
            )
        else if(tablep(thing) then
            __pyTableToPython(thing)
        else if(vectorp(thing) then
            __pyVectorToPython(thing)
        else
            rexCompile("^[_a-zA-Z]+[:@][x0-9a-fA-F]+$")
            __pySaveToVariableAndReturn(thing)
        )))))))
    )

    putd('pyStartServer nil)
    defun(pyStartServer (
        @key
        (id "default")
        (logLevel "INFO")
        (singleMode nil)
        (timeout nil)
        (python "python")
        (forceTcp nil)
        "ttggtg"
    )
        if(pyStartServer.ipc then
            fprintf(stderr "server is already running\n")
            nil
        else
            pyStartServer.id = id
            pyStartServer.logLevel = logLevel
            pyStartServer.singleMode = singleMode
            pyStartServer.timeout = timeout
            pyStartServer.python = python
            pyStartServer.forceTcp = forceTcp
            pyStartServer.restartPending = nil

            __pySpawnServer()
        )
    )

    pyStartServer.logName = lsprintf(
        "%s/skillbridge_skill.log"
        _logDirectory
    )

    putd('pyRunScript nil)
    defun(pyRunScript (
        script
        @key
        (python "python")
        (args nil)
        (block nil)
        "ttlg"
    )
        let((command process)
            command = lsprintf(
                "%s %s %s"
                python
                script
                buildString(args)
            )

            process = __pyIpcBeginProcess(
                command
                ""
                '__pyOnData
                '__pyOnError
                '__pyOnFinishScript
                pyRunScript.logName
            )

            if(block then
                __pyIpcWait(process)
            else
                process
            )
        )
    )

    pyRunScript.logName = lsprintf(
        "%s/skillbridge_script.log"
        _logDirectory
    )

    pyStartServer.ipc = nil
    pyStartServer.exe = _executable
    pyStartServer.id = "default"
    pyStartServer.logLevel = "INFO"
    pyStartServer.singleMode = nil
    pyStartServer.timeout = nil
    pyStartServer.python = "python"
    pyStartServer.forceTcp = nil
    pyStartServer.restartPending = nil
    pyStartServer.requestIpc = nil
    pyStartServer.receiveBuffer = ""
    pyStartServer.state = 'stopped

    printf("Available commands:\n")
    printf("\tpyStartServer ?id \"default\" ?logLevel \"WARNING\" ?singleMode nil ?timeout nil ?python \"python\" ?forceTcp nil\n")
    printf("\tpyKillServer\n")
    printf("\tpyRestartServer\n")
    printf("\tpyReloadScript\n")
    printf("\tpyShowLog [numberOfLines]\n")
    printf("\tpyRunScript path ?args list() ?python \"python\"\n")
)
