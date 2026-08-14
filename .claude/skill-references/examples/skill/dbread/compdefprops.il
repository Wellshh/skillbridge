;
; This will print the comp def properties for all comp definitions of a design
;
procedure( PrintCompDefProps()
    let((comp, props)
	foreach( comp axlDBGetDesign()->compdefs
		props = axlDBGetProperties(comp)
		printf("%s compdef props %L\n" comp->deviceType props)
	)
   )
   t
)

