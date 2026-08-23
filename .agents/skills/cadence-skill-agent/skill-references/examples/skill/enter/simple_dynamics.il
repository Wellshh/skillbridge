;
; Adds a dynamic rectangle on the cursor  and prompts for a pick
;
(defun DynamEx ()
    let( (pts st pick)
    pts = list(0:0 1000:0 1000:1000 0:1000 0:0 ) 
    st = axlPathStart(pts )
    axlAddSimpleMoveDynamics(0:0 st "path" ?ref_point 0:0)
    pick = axlEnterPoint( ?prompts "Enter Location" )
))

axlCmdRegister("dynam" 'DynamEx ?cmdType "interactive")
