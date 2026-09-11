; Report the current drawing path name.
procedure( reportDrawingName()
    let((drawingName)
        drawingName = axlGetDrawingName()
        printf("drawing: %L\n" drawingName)
        drawingName
    )
)
