; Report whether the Allegro find filter is open.
procedure( reportFindFilterState()
    let((isOpen)
        isOpen = axlFindFilterIsOpen()
        printf("find filter open: %L\n" isOpen)
        isOpen
    )
)
