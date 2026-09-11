; Report the current design units.
procedure( reportDesignUnits()
    let((units)
        units = axlDBGetDesignUnits()
        printf("design units: %L\n" units)
        units
    )
)
