;;; routes.il - Lazy Allegro straight-route projection and creation operations.

(putd '__abRouteLonelyBranches nil)
(defun __abRouteLonelyBranches ()
  (axlDBGetLonelyBranches))

(putd '__abCreateLineObject nil)
(defun __abCreateLineObject (points width layer net)
  (axlDBCreateLine points width layer net))

(putd '__abProjectRoutePoint nil)
(defun __abProjectRoutePoint (point)
  (list nil 'x (car point) 'y (cadr point)))

(putd '__abProjectRoute nil)
(defun __abProjectRoute (segment net)
  (let ((ends segment->startEnd))
    (list nil
          'net net
          'layer segment->layer
          'start (__abProjectRoutePoint (car ends))
          'end (__abProjectRoutePoint (cadr ends))
          'width segment->width)))

(putd '__abCollectRoutePaths nil)
(defun __abCollectRoutePaths (paths net layer result)
  (foreach path paths
    (when (and (equal path->objType "path") path->isEtch)
      (foreach segment path->segments
        (when (and (equal segment->objType "line")
                   (or (null layer) (equal layer segment->layer)))
          (setq result (cons (__abProjectRoute segment net) result))))))
  result)

(putd '__abCollectRoutes nil)
(defun __abCollectRoutes (branches net layer result)
  (foreach branch branches
    (setq result (__abCollectRoutePaths branch->children net layer result)))
  result)

(putd '__abProjectRoutes nil)
(defun __abProjectRoutes (net layer)
  (letseq ((design (__abFreshDesign))
           result)
    (foreach netObject design->nets
      (when (or (null net) (equal net netObject->name))
        (setq result (__abCollectRoutes netObject->branches netObject->name
                                       layer result))))
    (when (null net)
      (setq result (__abCollectRoutes (__abRouteLonelyBranches) nil
                                      layer result)))
    (reverse result)))

(putd '__abRouteNetName nil)
(defun __abRouteNetName (path)
  (let ((netObject path->net))
    (when (and netObject
               (not (stringp netObject))
               (not (equal netObject->name "")))
      netObject->name)))

(putd '__abCreateRoute nil)
(defun __abCreateRoute (net points layer width)
  (letseq ((created (__abCreateLineObject points width layer net))
           (paths (when created (car created)))
           result)
    (unless paths
      (error (sprintf nil "ROUTE_CREATE_FAILED: %L" net)))
    (foreach path paths
      (setq result (__abCollectRoutePaths (list path) (__abRouteNetName path)
                                          nil result)))
    (reverse result)))
