
/*
    This demostrates use of the axlShape family of interfaces.
    All of these simple demos require shape1.brd which is located
    @ <cds_root>/share/pcb/examples/skill/brds.

    You should reopen before running one of the demo APIs.
 */

;axlShapeChangeDynamicType

pntvcc = 1000:2800	; Large VCC shape (left side)
pntgnd = 3700:2800	; Large GND shape (right side)
pntright = 4050:1300	; small dynamic with voids on right side
pntleft = 600:2200	; small static on left side of brd
pntrko = 0:1700		; route keepout on left side
pntnetch = 100:1500	; no etch dynamic side under rko

procedure( ashPickShapeAt(point)
    let((shape)
    axlSetFindFilter( ?enabled '("NOALL" "SHAPES" "BOUNDARY_SHAPES") ?onButtons "ALLTYPES")
    axlSingleSelectPoint(point)
    shape = car(axlGetSelSet())
    axlClearSelSet()
    shape
))


; shows examples of changing shapes from dynamic to static or static
;	to dynamic
;
procedure( ashShapeChangeDynamicType()
    let((shape ret fmt (msg t) (dynamic t))

    fmt = "change static to dynamic; ret=%L\n"
    shape = ashPickShapeAt(pntleft)
    ret = axlShapeChangeDynamicType(shape dynamic nil)
    printf(fmt ret)

    fmt = "change dynamic to dynamic with messages enabled; ret=%L\n"
    shape = ashPickShapeAt(pntvcc)
    ret = axlShapeChangeDynamicType(shape dynamic msg)
    printf(fmt ret)

    fmt = "change dynamic to static with messages enabled; ret=%L\n"
    shape = ashPickShapeAt(pntvcc)
    ret = axlShapeChangeDynamicType(shape nil msg)
    printf(fmt ret)

    fmt = "attempt to change a non-etch shape; ret=%L\n"
    shape = ashPickShapeAt(pntrko)
    ret = axlShapeChangeDynamicType(shape nil msg)
    printf(fmt ret)

))

; shows examples of axlShapeRaisePriority
;
procedure( ashShapeRaisePriority()
    let((shape ret)

    fmt = "raise priority of large gnd shape so it wins over small shape; ret=%L\n"
    shape = ashPickShapeAt(pntgnd)
    printf("Current priority = %d\n" shape->priority)
    ret = axlShapeRaisePriority(shape)
    printf(fmt ret)

    fmt = "\nattempt to change a non-etch shape; ret=%L\n"
    shape = ashPickShapeAt(pntrko)
    ret = axlShapeRaisePriority(shape)
    printf(fmt ret)
))


; Deleting voids
;
procedure( ashShapeDeleteVoids()
    let((shape ret)

    shape = ashPickShapeAt(pntright)

    fmt = "Delete a single user void in dynamic shape; ret=%L\n"
    ret = axlShapeDeleteVoids(car(shape->voids))
    printf(fmt ret)

    fmt = "Delete all user voids in dynamic shape except first; ret=%L\n"
    ret = axlShapeDeleteVoids(cdr(shape->voids))
    printf(fmt ret)

    fmt = "Delete all voids in static shape; ret=%L\n"
    shape = ashPickShapeAt(pntleft)
    ret = axlShapeDeleteVoids(shape)
    printf(fmt ret)

    fmt = "\nattempt to delete voids in a non-etch shape; ret=%L\n"
    shape = ashPickShapeAt(pntrko)
    ret = axlShapeDeleteVoids(shape)
    printf(fmt ret)
))

; Deleting voids
;
procedure( ashShapeAutoVoid()
    let((shape shapes ret)

    ; convert GND shape to static, delete all voids then autovoid it
    shape = ashPickShapeAt(pntgnd)
    shape = car( axlShapeChangeDynamicType(shape nil nil) )
    printf("Conversion status: %L\n" shape)
    ret = axlShapeDeleteVoids(shape)
    printf("Delete Void status: %L\n" ret)
    shapes = axlShapeAutoVoid(shape 'fragment)
    printf("Autovoid shapes: %L\n" shapes)

    fmt = "\nattempt to autovoid voids in a dynamic shape; ret=%L\n"
    shape = ashPickShapeAt(pntvcc)
    ret = axlShapeAutoVoid(shape)
    printf(fmt ret)

    fmt = "\nattempt to autovoid voids in a non-etch shape; ret=%L\n"
    shape = ashPickShapeAt(pntrko)
    ret = axlShapeAutoVoid(shape)
    printf(fmt ret)

))

