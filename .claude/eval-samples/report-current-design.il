; Report the current Allegro design handle.
procedure( reportCurrentDesign()
    let((design)
        design = axlCurrentDesign()
        printf("current design: %L\n" design)
        design
    )
)
