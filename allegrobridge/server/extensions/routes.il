;;; Copyright (c) 2025-2026 Bai Junyan and contributors.
;;; SPDX-License-Identifier: LGPL-3.0-or-later
;;; routes.il - Lazy Allegro straight-route projection and creation operations.

(putd '__abRouteLonelyBranches nil)
(defun __abRouteLonelyBranches ()
  (axlDBGetLonelyBranches))

(putd '__abCreateLineObject nil)
(defun __abCreateLineObject (points width layer net)
  (axlDBCreateLine points width layer net))

(putd '__abCreatePathObject nil)
(defun __abCreatePathObject (path layer net)
  (axlDBCreatePath path layer net))

(putd '__abRouteLayerGet nil)
(defun __abRouteLayerGet (layer)
  (axlLayerGet layer))

(putd '__abRouteShell nil)
(defun __abRouteShell (command)
  (axlShell command))

(putd '__abProjectRoutePoint nil)
(defun __abProjectRoutePoint (point)
  (list nil 'x (car point) 'y (cadr point)))

(putd '__abProjectRoute nil)
(defun __abProjectRoute (segment net)
  (let ((ends segment->startEnd)
        (isArc (equal segment->objType "arc")))
    (list nil
          'net net
          'layer segment->layer
          'obj_type segment->objType
          'start (__abProjectRoutePoint (car ends))
          'end (__abProjectRoutePoint (cadr ends))
          'width segment->width
          'length (axlDBGetLength segment)
          'radius (when isArc segment->radius)
          'is_clockwise (when isArc segment->isClockwise)
          'center (when isArc (__abProjectRoutePoint segment->xy)))))

(putd '__abCollectRoutePaths nil)
(defun __abCollectRoutePaths (paths net layer result)
  (foreach path paths
    (when (and (equal path->objType "path") path->isEtch)
      (foreach segment path->segments
        (when (and (member segment->objType '("line" "arc"))
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

(putd '__abRouteNetExists nil)
(defun __abRouteNetExists (design net)
  (let (found)
    (foreach netObject design->nets
      (when (equal net netObject->name)
        (setq found t)))
    found))

(putd '__abConnectRoutes nil)
(defun __abConnectRoutes (net start end layer width)
  (letseq ((design (__abFreshDesign))
           before
           command)
    (unless (__abRouteNetExists design net)
      (error (sprintf nil "ROUTE_CONNECT_NET_NOT_FOUND: %s" net)))
    (unless (__abRouteLayerGet layer)
      (error (sprintf nil "ROUTE_CONNECT_LAYER_NOT_FOUND: %s" layer)))
    (setq before (__abProjectRoutes net nil))
    (setq command
          (lsprintf "add connect -net %s -layer %s -width %L; pick %L %L; pick %L %L; done"
                    net layer width (car start) (cadr start) (car end) (cadr end)))
    (__abRouteShell command)
    before))

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

(putd '__abCreatePath nil)
(defun __abCreatePath (net start stepDescs layer width)
  (letseq ((path (axlPathStart (list start) width))
           created
           paths
           result)
    (foreach step stepDescs
      (let ((typ (get step 'type)))
        (cond
          ((equal typ "line")
           (axlPathLine path nil (get step 'end)))
          ((equal typ "arc")
           (axlPathArcCenter path width (get step 'end) (get step 'clockwise) (get step 'center))))))
    (setq created (__abCreatePathObject path layer net))
    (unless created
      (error (sprintf nil "ROUTE_CREATE_FAILED: %L" net)))
    (setq paths (car created))
    (foreach path paths
      (setq result (__abCollectRoutePaths (list path) (__abRouteNetName path) nil result)))
    (reverse result)))
