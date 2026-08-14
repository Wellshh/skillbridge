(defun _saveSelSet ()
    (list (axlGetSelSet) (axlGetFindFilter nil) (axlGetFindFilter t)))

(defun _restoreSelSet (oldSelSet "l")
    (axlSetFindFilter ?enabled (cons "noall" (nth 1 oldSelSet))
		      ?onButtons (cons "noall" (nth 2 oldSelSet)))
    (axlSingleSelectObject (car oldSelSet))
    t)


(defun findAllOfType (findType "t")
    (let (selSet oldSetData)
	(setq oldSetData (_saveSelSet))
	(axlClearSelSet)
	(axlSetFindFilter ?enabled  (list "noall" findType "invisible") 
			  ?onButtons  (list "noall" findType))
	(axlAddSelectAll)
	(setq selSet (axlGetSelSet))
	(_restoreSelSet oldSetData)

	selSet))


(defun ashFindAllPins ()
    (findAllOfType "PINS"))

(defun ashFindAllVias ()
    (findAllOfType "VIAS"))

(defun ashFindAllClines ()
    (findAllOfType "CLINES"))

(defun ashFindAllClinesegs ()
    (findAllOfType "CLINESEGS"))

(defun ashFindAllLines ()
    (findAllOfType "LINES"))

(defun ashFindAllLinesegs ()
    (findAllOfType "LINESEGS"))

(defun ashFindAllDrcs ()
    (findAllOfType "DRCS"))

(defun ashFindAllText ()
    (findAllOfType "TEXT"))

(defun ashFindAllShapes ()
    (findAllOfType "SHAPES"))

(defun ashFindAllShapesegs ()
    (findAllOfType "SHAPESEGS"))

(defun ashFindAllVoids ()
    (findAllOfType "VOIDS"))

(defun ashFindAllVoidsegs ()
    (findAllOfType "VOIDSEGS"))

(defun ashFindAllSymbols ()
    (findAllOfType "SYMBOLS"))

(defun ashFindAllComponents ()
    (findAllOfType "COMPONENTS"))

(defun ashFindAllNets ()
    (findAllOfType "NETS"))

(defun ashFindAllFigures ()
    (findAllOfType "FIGURES"))

