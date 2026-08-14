
; detach all fanout from symbols in a design
(defun DetachAllFanout ()
    foreach( dbid axlDBGetDesign()->symbols
	axlSymbolDetach( dbid 'allClineVia))
)
 
