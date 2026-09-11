; Report the current Allegro design database object.
procedure( reportDesign()
    let((design)
        design = axlDBGetDesign()
        when( design printf("design: %L\n" design) )
        design
    )
)
