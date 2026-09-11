; Report the current selection count without changing selection state.
procedure( reportSelectionCount()
    let((count)
        count = axlGetSelSetCount()
        printf("selection count: %L\n" count)
        count
    )
)
