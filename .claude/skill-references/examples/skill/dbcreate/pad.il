;;; Examples of creating padstacks in Allegro 
;;;     File is: <cdsroot>/share/pcb/examples/skill/dbcreate/pad.il

; axlPadstackToDisk(t_padstack_name)
alias apd axlPadstackToDisk

; create a simple SMD pad
procedure( CreateSMD()
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP", ?type 'REGULAR,
				?figure 'RECTANGLE, ?figureSize 25:60) nil)
    ps_id = axlDBCreatePadStack("smt_pad", nil, pad_list t)
)


; thru pad with flash and a pad as shape
procedure( CreateThru()
       (let (name)
       name = "thru"

       drill_data = make_axlPadStackDrill(
		 ?holeType  'CIRCLE_DRILL
		 ?drillDiameter 42
		 ?plating 'PLATED
                 ?figure 'SQUARE
		 ?figureSize 60:60
		 ?drillChar "abc"
		 )

	pad_list = nil
        pad = make_axlPadStackPad(?layer "TOP",
                        ?type 'REGULAR, ?figure 'CIRCLE,
                        ?figureSize 80:80)
        pad_list = cons(pad pad_list)

	; alternative way of creating a pad
	pad = copy_axlPadStackPad(pad)
	pad->type = 'ANTIPAD
	pad->figure = 'SQUARE
        pad_list = cons(pad pad_list)

	pad = copy_axlPadStackPad(pad)
	pad->type = 'THERMAL
	pad->figure = 'SQUARE
	pad->figureSize = 100:100
        pad_list = cons(pad pad_list)

	pad = copy_axlPadStackPad(pad)
	pad->type = 'KEEPOUT
	pad->figure = 'RECTANGLE
	pad->figureSize = 100:50
        pad_list = cons(pad pad_list)

        pad_list = cons(make_axlPadStackPad(
                        ?layer "DEFAULT_INTERNAL", ?type 'REGULAR,
                        ?figure 'CIRCLE, ?figureSize 75:75) pad_list)

	pad = copy_axlPadStackPad(pad)
	pad->type = 'REGULAR
	pad->layer = "BOTTOM"
	pad->figure = 'SQUARE
	pad->figureSize = 70:70
        pad_list = cons(pad pad_list)

        ps_id = axlDBCreatePadStack(name, drill_data, pad_list t)


        ; To use a shape symbol; "myshape" do
        pad_list = cons( make_axlPadStackPad(?layer "TOP",
                                ?type 'REGULAR, ?figure "myshape"
                                ?figureSize 80:80) pad_list)

        ; To use a flash symbol; "myflash" do
        pad_list = cons( make_axlPadStackPad(?layer "TOP",
                                ?type 'THERMAL,
                                ?figure 'FLASH ?flash "myflash"
                                ?figureSize 80:80) pad_list)
	ps_id
))

; thru bbvia Padstack. Assumes brd has a LAYER_1
; also shows
;	drillToolSize

procedure( CreateBBvia()
       (let (name)
       name = "bbvia"

       drill_data = make_axlPadStackDrill(
		 ?usage "bbvia"
		 ?drillDiameter 38
		 ?plating 'PLATED
		 ?drillToolSize "Keith"
		 ?spanLockCount t
		 ?holeTolerance 1:2
		 ?drillNonStandard 'LASER_DRILL
		 )

	pad_list = nil
        pad_list = cons(make_axlPadStackPad(?layer "TOP",
                        ?type 'REGULAR, ?figure 'CIRCLE,
                        ?figureSize 80:80) pad_list)
        pad_list = cons(make_axlPadStackPad(
                        ?layer "DEFAULT INTERNAL", ?type 'REGULAR,
                        ?figure 'CIRCLE, ?figureSize 75:75) pad_list)
        pad_list = cons(make_axlPadStackPad(
                        ?layer "LAYER_1", ?type 'REGULAR,
                        ?figure 'SQUARE, ?figureSize 80:80) pad_list)

        ps_id = axlDBCreatePadStack(name, drill_data, pad_list t)
))

;-----------------------------------------------------------------------------------
; create a simple SMD with SOLDERMASK
procedure( CreateMask()
    (let (name)

    name = "solder"
    pad_list = nil
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP", ?type 'REGULAR,
				?figure 'RECTANGLE, ?figureSize 25:60) pad_list)
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "SOLDERMASK_TOP", ?type 'REGULAR,
				?figure 'RECTANGLE, ?figureSize 35:70) pad_list)
    ps_id = axlDBCreatePadStack(name, nil, pad_list t)
))

; create a simple SMD with New COVERLAY masks
procedure( CreateCoverlayMask()
    (let (name)

    name = "coverlay"
    pad_list = nil
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP", ?type 'REGULAR,
				?figure 'RECTANGLE, ?figureSize 25:60) pad_list)
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "COVERLAY_TOP", ?type 'REGULAR,
				?figure 'RECTANGLE, ?figureSize 35:70) pad_list)
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "COVERLAY_BOTTOM", ?type 'REGULAR,
				?figure 'SQUARE, ?figureSize 50:50) pad_list)
    ps_id = axlDBCreatePadStack(name, nil, pad_list t)
))

; create a simple SMD with user mask layer
procedure( CreateUserMask()
    (let (name usermask)

    name = "usermask"
    usermask = "MY_TOP"

    ; insure that the user mask is created in the design.
    ; this is not required if you know the design has the mask layer already defined
    axlPadUserMaskLayers('create usermask)

    pad_list = nil
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP", ?type 'REGULAR,
				?figure 'RECTANGLE, ?figureSize 25:60) pad_list)
    pad_list = cons(make_axlPadStackPad(
	                        ?layer usermask, ?type 'REGULAR,
				?figure 'SQUARE, ?figureSize 70:70) pad_list)
    ps_id = axlDBCreatePadStack(name, nil, pad_list t)
))

;-----------------------------------------------------------------------------------
procedure( Create2PadExamples()
       (let (pad ipad pad_list ps_id drill_data)

        ;The following example adds a surface mount padstack having a
        ;25 by 60 rectangular pad on the top layer.

        pad_list = cons(make_axlPadStackPad(
                ?layer "TOP", ?type 'REGULAR,
                ?figure 'RECTANGLE, ?figureSize 25:60) nil)
        ps_id = axlDBCreatePadStack("smt_pad", nil, pad_list t)

        ;The following example adds a padstack with an 80 diameter circle
        pad on the top layer, 75 diameter circle pad on internal layers,
        ;a 62 plated thru hole. The drill symbol will be a 60 square.
	; (uncomment) BOTTOM layer

        drill_data = make_axlPadStackDrill(?drillDiameter 42
                ?figure 'SQUARE, ?figureSize 60:60, ?plating 'PLATED)
        pad_list = cons(make_axlPadStackPad(?layer "TOP",
                        ?type 'REGULAR, ?figure 'CIRCLE,
                        ?figureSize 80:80) pad_list)
        ipad = make_axlPadStackPad(
                        ?layer "DEFAULT INTERNAL", ?type 'REGULAR, 
                        ?figure 'CIRCLE, ?figureSize 75:75)
	pad_list = cons(ipad, pad_list)

	; faster way of changing just a single item in a pad def
	ipad->layer = "SIG2"
	pad_list = cons(ipad, pad_list)

        pad = make_axlPadStackPad( 
                        ?layer "BOTTOM", ?type 'REGULAR,
                        ?figure 'SQUARE, ?figureSize 80:80)
	; commented out to permit a bbvia so can enable uvia option (below)
	pad_list = cons(pad pad_list)

	; alt way of setting defstruct types
	drill_data->drillNonStandard = "LASER_DRILL";

        ps_id = axlDBCreatePadStack("my_pad", drill_data, pad_list t)
))



;-----------------------------------------------------------------------------------
; create a donut pad
procedure( CreateDonut()
    (let (name insideDia)
    name = "donut-1"
    insideDia = 20.1
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure 'DONUT
				?figureSize 60:60
				?inside insideDia 
			) nil)
    ps_id = axlDBCreatePadStack(name nil pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))

; Create a chamfer pad
procedure( CreateCamfer()
    (let (type name radius corners)

    type = 'ROUNDED_RECTANGLE
    type = 'CHAMFERED_RECTANGLE
    name = "chamfer-1"

    radius = 20
    corners = "UL-LR"
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure type
				?figureSize 60:120
				?corners corners
				?radius radius 
			) nil)
    ps_id = axlDBCreatePadStack(name nil pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))

; create a n-sided polygon with 12 sides
procedure( CreateNPoly()
    (let (name sides)
    name = "npoly"
    sides = 12
    pad_list = cons(make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure 'N_SIDED_POLY
				?figureSize 60:60
				?sides sides 
			) nil)
    ps_id = axlDBCreatePadStack(name nil pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))

;-----------------------------------------------------------------------------------
; create keepout on TOP layer and adjecent layer
procedure( CreateKO()
    (let (name )
    name = "ko"
    ; regular
    pad_list = cons( make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure 'CIRCLE
				?figureSize 60:60)
			nil)

    ; ko same layer
    pad_list = cons( make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'KEEPOUT
				?figure 'CIRCLE
				?figureSize 80:80)
			pad_list)
    ; ko adjacent layer
    pad_list = cons( make_axlPadStackPad(
	                        ?layer 'adjacent
				?type 'KEEPOUT
				?figure 'SQUARE
				?figureSize 70:70)
			pad_list)

    ps_id = axlDBCreatePadStack(name nil pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))


;-----------------------------------------------------------------------------------
; create a slot 
procedure( CreateSlot()
    (let (name )
    name = "slot-1"
    ; regular
    pad_list = nil
    pad_list = cons( make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure 'RECTANGLE
				?figureSize 160:40)
			pad_list)
    pad_list = cons( make_axlPadStackPad(
	                        ?layer "BOTTOM" 
				?type 'REGULAR
				?figure 'RECTANGLE
				?figureSize 160:40)
			pad_list)

    ; create the global padstack data
    base = make_axlPadStackDrill(
	                        ?usage "SLOT"
				?holeType 'RECTANGLE_SLOT
				?slotSize 100:200
				?holeTolerance 1:2
				?holeToleranceY 3:4
				?plating 'NON_PLATED
				)

    ps_id = axlDBCreatePadStack(name base pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))

;-----------------------------------------------------------------------------------
; create a counter bore or sink
procedure( CreateCounter()
    (let (name  counter)
    name = "counter-1"

    counter = "bore"
    counter = "sink"

    ; regular
    pad_list = nil
    pad = make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure 'CIRCLE
				?figureSize 160:160)
    pad_list = cons(pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->layer = "DEFAULT INTERNAL"
    pad_list = cons( pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->layer = "BOTTOM"
    pad_list = cons( pad pad_list)

    ; create the global padstack data
    base = make_axlPadStackDrill(
	                        ?usage "Tooling_hole"
				?holeType 'CIRCLE_DRILL
				?drillDiameter 80
				?plating 'NON_PLATED
				?holeCounterType counter
				?holeCounterAngle 45
				?holeCounterDiameter 120
				?holeCounterDepth 0.1234
				?holeCounterTolerance 1:2
				)

    ps_id = axlDBCreatePadStack(name base pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))

;-----------------------------------------------------------------------------------
; Create a padstack with backdrill info

procedure( CreateBackdrill()
    (let (name  counter)
    name = "backdrill"

    ; regular
    pad_list = nil
    pad = make_axlPadStackPad(
	                        ?layer "TOP" 
				?type 'REGULAR
				?figure 'CIRCLE
				?figureSize 160:160)
    pad_list = cons(pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->layer = "DEFAULT INTERNAL"
    pad_list = cons( pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->layer = "BOTTOM"
    pad_list = cons( pad pad_list)

    ;; in real designs you may not need to create all of these backdrill pad types
    ; create backdrill pad info
    pad = copy_axlPadStackPad(pad)
    pad->figureSize = '170:170
    pad->layer = 'backdrillStart
    pad->type = 'REGULAR
    pad_list = cons( pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->figureSize = '180:180
    pad->layer = 'backdrillStart
    pad->type = 'ANTIPAD
    pad_list = cons( pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->figureSize = '190:190
    pad->layer = 'backdrillClearance
    pad->type = 'ANTIPAD
    pad_list = cons( pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->figureSize = '200:200
    pad->layer = 'backdrillClearance
    pad->type = 'KEEPOUT
    pad_list = cons( pad pad_list)

    pad = copy_axlPadStackPad(pad)
    pad->figureSize = '210:210
    pad->layer = 'backdrillSoldermask
    pad->type = 'REGULAR
    pad_list = cons( pad pad_list)

    ; create the global padstack data
    base = make_axlPadStackDrill(
	                        ?usage "Through"
				?holeType 'CIRCLE_DRILL
				?drillDiameter 40
				?plating 'PLATED

				?backdrillDiameter 80
				?backdrillFigureName 'CROSS
				?backdrillFigureChar "F"
				?backdrillFigureWidth 22
				?backdrillFigureHeight 44
				)

    ps_id = axlDBCreatePadStack(name base pad_list t)
    printf("PAD dbid %L\n" ps_id)
    ps_id
))



;-----------------------------------------------------------------------------------
;-----------------------------------------------------------------------------------
;-----------------------------------------------------------------------------------
; Fetching pad data

; Get normal layer data
procedure( FetchNormal()
    (let (padstack pad layer type)

    layer = "TOP"
    type = 'THERMAL
    type = 'KEEPOUT
    type = 'ANTIPAD
    type = 'REGULAR

    unless( (padstack = axlDBFindByName('padstack "thru"))
    	padstack = CreateThru())

    pad = axlDBGetPad(padstack layer type)
))


; Get special layers
procedure( FetchSpecial()
    (let (padstack pad layer )

    layer = 'internal
    layer = 'composite

    unless( (padstack = axlDBFindByName('padstack "thru"))
    	padstack = CreateThru())

    pad = axlDBGetPad(padstack layer 'REGULAR)
))


; Get backdrill layers
procedure( FetchBackdrill()
    (let (padstack pad)

    unless( (padstack = axlDBFindByName('padstack "backdrill"))
    	padstack = CreateBackdrill())

    ;pad = axlDBGetPad(padstack 'backdrillStart 'ANTIPAD)
    pad = axlDBGetPad(padstack 'backdrillSoldermask 'REGULAR)
))

; Get backdrill layers
procedure( FetchCoverlay()
    (let (padstack pad layer)

    layer = "COVERLAY_TOP"
    layer = "COVERLAY_BOTTOM"

    unless( (padstack = axlDBFindByName('padstack "backdrill"))
    	padstack = CreateCoverlayMask())

    pad = axlDBGetPad(padstack layer 'REGULAR)
))

