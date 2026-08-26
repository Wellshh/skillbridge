;;; vias.il - Lazy Allegro via projection and creation operations.

(putd '__abViaLonelyBranches nil)
(defun __abViaLonelyBranches ()
  (axlDBGetLonelyBranches))

(putd '__abCreateViaObject nil)
(defun __abCreateViaObject (padstack at net mirrored rotation)
  (axlDBCreateVia padstack at net mirrored rotation))

(putd '__abViaOnLayer nil)
(defun __abViaOnLayer (via layer)
  (if (null layer)
      t
      (let (found)
        (foreach pad via->pads
          (when (equal layer pad->layer)
            (setq found t)))
        found)))

(putd '__abProjectVia nil)
(defun __abProjectVia (via net)
  (let ((span via->startEnd))
    (list nil
          'padstack via->name
          'net net
          'x (car via->xy)
          'y (cadr via->xy)
          'rotation via->rotation
          'mirroring (if via->isMirrored then "mirrored" else "unmirrored")
          'start_layer (car span)
          'end_layer (cadr span))))

(putd '__abCollectVias nil)
(defun __abCollectVias (branches net layer padstack result)
  (foreach branch branches
    (foreach item branch->children
      (when (and (equal item->objType "via")
                 (or (null padstack) (equal padstack item->name))
                 (__abViaOnLayer item layer))
        (setq result (cons (__abProjectVia item net) result)))))
  result)

(putd '__abProjectVias nil)
(defun __abProjectVias (net layer padstack)
  (letseq ((design (__abFreshDesign))
           result)
    (foreach netObject design->nets
      (when (or (null net) (equal net netObject->name))
        (setq result (__abCollectVias netObject->branches netObject->name
                                     layer padstack result))))
    (when (null net)
      (setq result (__abCollectVias (__abViaLonelyBranches) nil
                                    layer padstack result)))
    (reverse result)))

(putd '__abCreateVia nil)
(defun __abCreateVia (padstack at net mirrored rotation)
  (letseq ((created (__abCreateViaObject padstack at net mirrored rotation))
           (via (when created (car created))))
    (unless via
      (error (sprintf nil "VIA_CREATE_FAILED: %L" padstack)))
    (__abProjectVia via net)))
