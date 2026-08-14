
;
; Simple example of selecting one or more database objects, loading
; them into the dynamics buffer and putting 1 dynamics line from
; the origin of the 1st object selected to its origin in the dynamics
; buffer

;; to use
;; 1) Load this file -- load "dyntest.il"
;; 2) At skill command prompt type: TestDynamics
;; 3) Adjust find filter
;; 4) select 1 object or window to select multiple or select temp
;;    group mode to pick indivdual objects
;; 5) Objects you selected should be in cursor buffer and one rband
;;	line should be visible -- move your cursor and objects should
;;	move
;; 6) Pick to end command


(defun TestDynamics ( )
    let( (obj objs xy)

    axlClearSelSet()

    ; Allow user to select object(s) they want to load into dynamics buffer
    objs = SelectStuff()

    when(objs
	obj = car(objs)


	; if obj has an origin use that as the anchor point of
	; the rubberband otherwise pick the 1st point of its bounding
	; box
	if(obj->xy then
	   xy = obj->xy
	else
	   xy = car(obj->bBox)
	)

	;; load objects into dynamics system
	axlDynamicsObject(objs xy)

	;; add one rubberband from 1st object's orign to origin same
	;; location in dynamics buffer
	axlAddSimpleRbandDynamics(xy "directline" ?origin xy) 

	;; this just allows you to end the dynamics test
	axlEnterPoint(?prompts "Pick to end dynamics")
	axlClearDynamics()
    )
    axlClearSelSet()

))

 
unless(boundp('_saveOneFindFilter) 
    ;_saveOneFindFilter = '(("NOALL" "ALLTYPES" "NOBOUNDARY_SHAPES" "NAMEFORM") nil)
    _saveOneFindFilter = '(("NOALL" "ALLTYPES" 
		    "NOGROUPMEMBERS" "NAMEFORM" "NOCOMPONENTS"
			"NOFUNCTIONS" 
			"BOUNDARY_SHAPES" "NOSHAPESEGS" "DYNTHEMALS") nil)
)


(defun SelectStuff (@optional types)
    (let (oldPopup sel)
    axlClearSelSet()

    oldPopup = axlUIPopupSet( axlUIPopupDefine(nil 
				'(("Cancel" axlCancelEnterFun))))
    unless( types
	types = cadr(_saveOneFindFilter)
    )

    axlSetFindFilter( ?enabled car(_saveOneFindFilter) ?onButtons types )
    axlControlRaise( 'find)
    axlSelect(?prompt "Set Find filter then select one or more objects")
    axlUIPopupSet(oldPopup)
    ;_saveOneFindFilter = list(axlGetFindFilter(nil) axlGetFindFilter(t))
    _saveOneFindFilter = list(car(_saveOneFindFilter) axlGetFindFilter(t))

    axlGetSelSet()
))

