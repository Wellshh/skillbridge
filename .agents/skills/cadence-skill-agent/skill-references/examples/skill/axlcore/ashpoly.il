
; This is an example of getting the of axlPolyOffset
;  Note use brd @ <cdsroot>/share/pcb/examples/brds/shape1.brd

; takes a shape on route keepout/all layer and duplicates it on
; offset in the y direction


; Main entry point to functionality
procedure( testPolyOffset()
    let( (saveVis shapes shape shapePoly x y height newPoly layer)

    layer = "ROUTE KEEPOUT/ALL"

    ; just make approproiate layers visible
    saveVis = axlVisibleGet()
    axlVisibleDesign(nil)
    axlVisibleLayer(layer t)

    ; get list of shapes on above layer
    shapes = _EXfindAllOfType("SHAPES")
    shape = car(shapes)

    ; restore original visibility
    axlVisibleSet(saveVis)

    ; get 1st shape found (should only be 1)
    shapePoly = car( axlPolyFromDB(shape)  )

    ; print old poly
    pprint(shapePoly->??)

    ; offset by its shape extents in the negative y direction
    x = car(car(shapePoly->bBox))
    y = cadr(car(shapePoly->bBox))
    height = cadr(cadr(shapePoly->bBox)) - y

    ; make a copy of this poly with the new offset
    ; == if third arg is nil then shapePoly is modified, t makes
    ;    a copy
    newPoly = axlPolyOffset(shapePoly 0:height t)

    ; print new poly
    pprint(newPoly->??)

    ; now make shape in db
    axlDBCreateShape(newPoly t layer)
))


; This process a list of shapes and outputs info to the extract output file
procedure( _EXProcessShapes(fp shapes)
    let( (poly refdes both)
    foreach( shape  shapes
	poly = car( axlPolyFromDB(shape) )
	refdes = shape->parent->refdes
	unless(refdes
	   refdes = "")
	both = parseString(shape->layer "/")
	fprintf(fp "S!%s!%s!%s!%f!\n" refdes car(both) cadr(both) poly->area)
    )
))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; good utilities to manage the find filter

procedure( _EXsaveFindFilter()
    let( (oldElements oldOnButtons)
    oldElements = axlGetFindFilter(nil)
    oldOnButtons =  axlGetFindFilter(t)

    list(oldElements oldOnButtons)
))


procedure( _EXrestoreFindFilter(OldFilter "l")
    let((oldElements oldOnButtons)
    (axlSetFindFilter ?enabled "NOALL" ?onButtons "NOALL")

    (when (setq oldElements (car OldFilter))
            (axlSetFindFilter ?enabled oldElements))

    (when (setq oldOnButtons (cadr OldFilter))
            (axlSetFindFilter ?onButtons oldOnButtons))
    t
))


procedure( _EXfindAllOfType(findType "t")
    let( (oldFilter newFilter onBtn selSet oldSet)
        oldSet = axlGetSelSet()
        oldFilter = _EXsaveFindFilter()
        axlClearSelSet()

        newFilter = list("NOALL" findType)
        onBtn = list(findType)
        axlSetFindFilter(?enabled newFilter ?onButtons onBtn)

        axlAddSelectAll()
        selSet = axlGetSelSet()

        ; restore old selections
        axlClearSelSet()
        when(oldSet
            axlSetFindFilter(?enabled '("NOALL" "ALLTYPES")
                              ?onButtons '("ALL"))
            axlAddSelectObject(oldSet)
	)

        _EXrestoreFindFilter(oldFilter)
        selSet
))

