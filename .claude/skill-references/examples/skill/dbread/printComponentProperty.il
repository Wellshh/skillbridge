
; This example shows printing 2 properties on a component. By
; changing one line you can print the property on a symbol.
; If property doesn't exist on component a 'nil' is printed as the
; value. You can filter this out by adding a a test.

procedure( PrintCompProp()
let( (s syms value myprop)
    syms = axlDBGetDesign()->components

    ; If you want the properties on symbols instead of components
    ; use the following
    ;syms = axlDBGetDesign()->symbols

    myprop = "COMP_PART_NUMBER"
    
    foreach( s syms
	value = get(s->prop myprop)
	printf("name= %s,\t %s = %L\n", s->name, myprop, value)
    )
    t
))

