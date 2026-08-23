
; This is an example of getting the areas of all place bound shapes
; in a design using a format similar to Allegro's extracta program.
;
; To use load the skill program either via the allegro.ilinit file
; or typing: skill load "ex.il" at the Allegro command line.
;
; To generate data type the command: getareas on the Allegro command line

; register a command with allegro to perform the function
axlCmdRegister("getareas" 'ExtractPlaceBoundAreas ?cmdType "interactive")

; Main entry point to functionality
procedure( ExtractPlaceBoundAreas()
    let( (saveVis shapesTop shapesBtm fp)

    ; just make approproiate layers visible
    saveVis = axlVisibleGet()
    axlVisibleDesign(nil)

    axlVisibleLayer("PACKAGE GEOMETRY/PLACE_BOUND_TOP" t)
    shapesTop = _EXfindAllOfType("SHAPES")
    axlVisibleLayer("PACKAGE GEOMETRY/PLACE_BOUND_TOP" nil)
    axlVisibleLayer("PACKAGE GEOMETRY/PLACE_BOUND_BOTTOM" t)
    shapesBtm = _EXfindAllOfType("SHAPES")

    ; output extract like output file with shape area values
    fp = axlDMOpenFile("ALLEGRO_TEXT" "placeboundareas" "w")
    fprintf(fp "A!REFDES!CLASS|SUBCLASS!AREA!\n")
    _EXProcessShapes(fp shapesTop)
    _EXProcessShapes(fp shapesBtm)
    axlUIWPrint(nil 'info1 "Extract area file: %s" get_filename(fp))
    axlDMClose(fp)

    ; restore original visibility
    axlVisibleSet(saveVis)
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

