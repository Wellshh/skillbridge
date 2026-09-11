; Report the top and bottom conductor layer names.
procedure( reportConductorLayers()
    let((topLayer bottomLayer)
        topLayer = axlConductorTopLayer()
        bottomLayer = axlConductorBottomLayer()
        printf("conductors: %L / %L\n" topLayer bottomLayer)
        list(topLayer bottomLayer)
    )
)
