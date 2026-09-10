; Run a body inside an undo mark, rolling back when the body returns nil.
; axlDBTransaction* marks must not cross Allegro command boundaries (see
; verified_facts axlDBTransaction-not-active-across-commands), so the mark is
; opened and closed entirely inside this call.
procedure( withUndoMark(thunk)
    let((mark result)
        mark = axlDBTransactionStart()
        result = thunk()
        if( result
            then axlDBTransactionCommit(mark)
            else axlDBTransactionRollback(mark)
        )
        result
    )
)
