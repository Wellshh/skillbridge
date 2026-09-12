;;; Stage II-B pad geometry probe.  DBIDs are resolved and consumed per RPC.
(putd '__v2PadPointPure nil)
(defun __v2PadPointPure (p)
  (when p (list nil 'x (car p) 'y (cadr p))))

(putd '__v2PadBoxPure nil)
(defun __v2PadBoxPure (b)
  (when b (list (__v2PadPointPure (car b)) (__v2PadPointPure (cadr b)))))

(putd '__v2PadPolyPure nil)
(defun __v2PadPolyPure (poly)
  (when poly
    (let (verts holes)
      (foreach v poly->vertices
        (setq verts (cons (list nil 'xy (__v2PadPointPure (car v))
                                  'radius (cadr v)) verts)))
      (foreach h poly->holes
        (setq holes (cons (__v2PadPolyPure h) holes)))
      (list nil 'area poly->area 'bBox (__v2PadBoxPure poly->bBox)
            'isHole poly->isHole 'objType poly->objType
            'vertices (reverse verts) 'holes (reverse holes)))))

(putd '__v2PadPathPolysPure nil)
(defun __v2PadPathPolysPure (paths)
  (let (out polys)
    (foreach path paths
      (setq polys (axlPolyFromDB path ?layer "ETCH/TOP" ?padType 'REGULAR))
      (foreach poly polys
        (setq out (cons (__v2PadPolyPure poly) out))))
    (reverse out)))

(putd '__v2PadViaPure nil)
(defun __v2PadViaPure (via)
  (let ((pad (axlDBGetPad via "ETCH/TOP" "REGULAR")) netName)
    (setq netName (cond ((null via->net) nil)
                        ((stringp via->net) via->net)
                        (t via->net->name)))
    (unless pad (error "PAD_GET_REGULAR_TOP_FAILED"))
    (list nil 'via
          (list nil 'name via->name 'net netName 'xy (__v2PadPointPure via->xy)
                'rotation via->rotation
                'mirroring (if via->isMirrored then "mirrored" else "unmirrored")
                'start_layer (car via->startEnd) 'end_layer (cadr via->startEnd))
          'pad
          (list nil 'name pad->name 'figureName pad->figureName
                'bBox (__v2PadBoxPure pad->bBox)
                'offset (__v2PadPointPure pad->offset)
                'layer pad->layer 'type pad->type 'objType pad->objType
                'parent (when pad->parent pad->parent->name)
                'figurePaths (length pad->figure)
                'figurePolys (__v2PadPathPolysPure pad->figure))
          'viaPolys
          (let (polys)
            (foreach poly (axlPolyFromDB via ?layer "ETCH/TOP" ?padType 'REGULAR)
              (setq polys (cons (__v2PadPolyPure poly) polys)))
            (reverse polys)))))

(putd '__v2PadFindVia nil)
(defun __v2PadFindVia (padstack netName x y)
  (letseq ((design (axlDBRefreshId (axlDBGetDesign))) found)
    (foreach netObject design->nets
      (when (or (null netName) (equal netName netObject->name))
        (foreach branch netObject->branches
          (foreach item branch->children
            (when (and (equal item->objType "via")
                       (equal item->name padstack)
                       (equal (car item->xy) x)
                       (equal (cadr item->xy) y))
              (setq found (cons item found)))))))
    (when (null netName)
      (foreach branch (axlDBGetLonelyBranches)
        (foreach item branch->children
          (when (and (equal item->objType "via")
                     (equal item->name padstack)
                     (equal (car item->xy) x)
                     (equal (cadr item->xy) y))
            (setq found (cons item found))))))
    (cond ((null found) nil)
          ((equal (length found) 1) (__v2PadViaPure (car found)))
          (t (error (sprintf nil "PAD_VIA_MATCH_NOT_UNIQUE: %d" (length found)))))))

(putd '__v2PadProbeFind nil)
(defun __v2PadProbeFind (padstack netName x y)
  (__v2PadFindVia padstack netName x y))
