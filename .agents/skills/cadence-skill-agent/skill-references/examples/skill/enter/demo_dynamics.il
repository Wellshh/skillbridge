
; demostrates various flavors of axlAddSimpleRbandDynamics

(defun DemoDirect ( )
	RBandDemo("directline")
)

(defun DemoHoriz ( )
	RBandDemo("horizline")
)

(defun DemoVert ( )
	RBandDemo("vertline")
)

(defun DemoArc ( )
	RBandDemo("arc")
)

(defun DemoCircle ( )
	RBandDemo("circle")
)

(defun DemoBox ( )
	RBandDemo("box")
)

(defun DemoPath ( )
	RBandDemo("path")
)

(defun DemoFixed ( )
	RBandDemo("fixedline")
)

(defun RBandDemo ( t_rbandType)

	axlClearDynamics()

	; create a simple 2 pin compd
        mypath = axlPathStart(list( -350:0)) ; Start circular pad
        axlPathArcCenter(mypath, 0., -350:0, nil, -300:0)

        ; Load the first pad into the dynamic cursor buffer
        axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)

        mypath = axlPathStart(list( 350:0)) ; Start circular pad
        axlPathArcCenter(mypath, 0., 350:0, nil, 300:0)

        ; Load the other pad into the dynamic cursor buffer
        axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)

        mypath = axlPathStart( ; Start resistor body outline
                list( -200:-100 200:-100 200:100 -200:100 -200:-100))

        ; Load the resistor body outline in the dynamic cursor buf
        axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)

  ; Real part
        ; Load a "path" rubberband to the first pad
        ;axlAddSimpleRbandDynamics(0:0 "path"
                ;?origin 9100:4500 ?var_point -300:0)

        ; Load a "directline" rubberband to the second pad
        axlAddSimpleRbandDynamics(0:0 t_rbandType
                ?origin 9100:4500 ?var_point 300:0)
)
