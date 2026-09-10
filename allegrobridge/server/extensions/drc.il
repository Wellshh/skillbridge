;;; Copyright (c) 2025-2026 Bai Junyan and contributors.
;;; SPDX-License-Identifier: LGPL-3.0-or-later

(putd '__abDrcStableRef nil)
(defun __abDrcStableRef (object)
  (let ((kind object->objType))
    (cond
      ((equal kind "component")
       (list nil 'kind "component" 'refdes object->name))
      ((equal kind "symbol")
       (list nil 'kind "component" 'refdes object->refdes))
      ((equal kind "net")
       (list nil 'kind "net" 'name object->name))
      ((equal kind "pin")
       (letseq ((component object->component)
                (symbol object->parent)
                (refdes (if component then component->name else symbol->refdes)))
         (list nil 'kind "pin" 'refdes refdes 'number object->number))))))

(putd '__abDrcNetRef nil)
(defun __abDrcNetRef (object)
  (let ((kind object->objType) name netObject)
    (if (equal kind "net")
        (setq name object->name)
        (when (member 'net object->?)
          (setq netObject object->net)
          (when netObject
            (setq name (if (stringp netObject) then netObject else netObject->name)))))
    (when (and name (not (equal name "")))
      (list nil 'kind "net" 'name name))))

(putd '__abDrcAddRef nil)
(defun __abDrcAddRef (reference result)
  (if (or (null reference) (member reference result))
      result
      (cons reference result)))

(putd '__abDrcFigurePoint nil)
(defun __abDrcFigurePoint (object)
  (let (xy)
    (when (member 'xy object->?)
      (setq xy object->xy))
    (when xy
      (list nil 'x (car xy) 'y (cadr xy)))))

(putd '__abDrcFigureBBox nil)
(defun __abDrcFigureBBox (object)
  (let (bbox)
    (when (member 'bBox object->?)
      (setq bbox object->bBox))
    (when bbox
      (list nil
            'll (list nil 'x (car (car bbox)) 'y (cadr (car bbox)))
            'ur (list nil 'x (car (cadr bbox)) 'y (cadr (cadr bbox)))))))

(putd '__abDrcFigure nil)
(defun __abDrcFigure (object)
  (letseq ((kind object->objType)
           (isRouteFigure (member kind '("line" "arc")))
           (isArc (equal kind "arc"))
           (ends
             (when (and isRouteFigure (member 'startEnd object->?))
               object->startEnd)))
    (list nil
          'obj_type kind
          'layer (when (member 'layer object->?) object->layer)
          'location (__abDrcFigurePoint object)
          'bbox (__abDrcFigureBBox object)
          'net (__abDrcNetRef object)
          'reference (__abDrcStableRef object)
          'start
            (when ends
              (list nil 'x (car (car ends)) 'y (cadr (car ends))))
          'end
            (when ends
              (list nil 'x (car (cadr ends)) 'y (cadr (cadr ends))))
          'width
            (when (and isRouteFigure (member 'width object->?)) object->width)
          'radius (when (and isArc (member 'radius object->?)) object->radius)
          'is_clockwise
            (when (and isArc (member 'isClockwise object->?))
              object->isClockwise)
          'center
            (when (and isArc (member 'xy object->?))
              (__abDrcFigurePoint object)))))

(putd '__abDrcFigures nil)
(defun __abDrcFigures (marker)
  (let (result)
    (foreach object marker->violations
      (setq result (cons (__abDrcFigure object) result)))
    (reverse result)))

(putd '__abDrcObjects nil)
(defun __abDrcObjects (marker)
  (let (result)
    (foreach object marker->violations
      (let ((parent (when (member 'parent object->?) object->parent)))
        (setq result (__abDrcAddRef (__abDrcStableRef object) result))
        (when parent
          (setq result (__abDrcAddRef (__abDrcStableRef parent) result)))
        (setq result (__abDrcAddRef (__abDrcNetRef object) result))
        (when parent
          (setq result (__abDrcAddRef (__abDrcNetRef parent) result)))))
    (reverse result)))

(putd '__abProjectDrc nil)
(defun __abProjectDrc (marker)
  (let ((bbox marker->bBox))
    (list nil
          'name marker->name
          'category marker->type
          'source marker->source
          'expected marker->expected
          'actual marker->actual
          'layer marker->layer
          'location (list nil 'x (car marker->xy) 'y (cadr marker->xy))
          'bbox (list nil
                      'll (list nil 'x (car (car bbox)) 'y (cadr (car bbox)))
                      'ur (list nil 'x (car (cadr bbox)) 'y (cadr (cadr bbox))))
          'figures (__abDrcFigures marker)
          'objects (__abDrcObjects marker))))

(putd '__abProjectDrcs nil)
(defun __abProjectDrcs ()
  (letseq ((design (__abFreshDesign)) result)
    (foreach marker design->drcs
      (setq result (cons (__abProjectDrc marker) result)))
    (reverse result)))

(putd '__abDrcUpdateDesign nil)
(defun __abDrcUpdateDesign ()
  (axlDRCUpdate nil))

(putd '__abUpdateDrcs nil)
(defun __abUpdateDrcs ()
  (let ((originalEnable (axlDBControl 'drcEnable)))
    (unwindProtect
      (progn
        (__abDrcUpdateDesign)
        (__abProjectDrcs))
      (axlDBControl 'drcEnable originalEnable))))

(putd '__abDrcRouteSegmentMatches nil)
(defun __abDrcRouteSegmentMatches
    (segment layer objType start end width radius isClockwise center)
  (letseq ((ends segment->startEnd)
           (sameEnds
             (or
               (and (equal (car ends) start) (equal (cadr ends) end))
               (and (equal (car ends) end) (equal (cadr ends) start)))))
    (and (equal segment->objType objType)
         (equal segment->layer layer)
         (equal segment->width width)
         sameEnds
         (or
           (not (equal objType "arc"))
           (and (equal segment->radius radius)
                (equal segment->isClockwise isClockwise)
                (equal segment->xy center))))))

(putd '__abFindDrcRoute nil)
(defun __abFindDrcRoute
    (design netName layer objType start end width radius isClockwise center)
  (let (matches)
    (foreach netObject design->nets
      (when (equal netObject->name netName)
        (foreach branch netObject->branches
          (foreach path branch->children
            (when (and (equal path->objType "path") path->isEtch)
              (foreach segment path->segments
                (when (__abDrcRouteSegmentMatches
                        segment layer objType start end width radius
                        isClockwise center)
                  (setq matches (cons segment matches)))))))))
    (cond
      ((null matches) nil)
      ((cdr matches)
       (error
         (sprintf nil "DRC_TARGET_AMBIGUOUS: route/%L/%L/%L/%L"
                  netName layer start end)))
      (t (car matches)))))

(putd '__abFindDrcItem nil)
(defun __abFindDrcItem
    (kind primary secondary @optional
          layer objType start end width radius isClockwise center)
  (letseq ((design (__abFreshDesign))
           target)
    (cond
      ((equal kind "component")
       (foreach component design->components
         (when (equal component->name primary)
           (setq target component))))
      ((equal kind "net")
       (foreach net design->nets
         (when (equal net->name primary)
           (setq target net))))
      ((equal kind "route")
       (setq target
             (__abFindDrcRoute design primary layer objType start end width radius
                               isClockwise center)))
      (t
       (foreach component design->components
         (when (equal component->name primary)
           (foreach pin component->pins
             (when (equal pin->number secondary)
               (setq target pin)))))))
    target))

(putd '__abDrcCheckItem nil)
(defun __abDrcCheckItem (target)
  (axlDRCItem t target))

(putd '__abCheckDrcs nil)
(defun __abCheckDrcs
    (kind primary secondary @optional
          layer objType start end width radius isClockwise center)
  (letseq ((target
             (__abFindDrcItem kind primary secondary layer objType start end
                              width radius isClockwise center))
           markers result)
    (unless target
      (error (sprintf nil "DRC_TARGET_NOT_FOUND: %L/%L/%L"
                     kind primary secondary)))
    (setq markers (__abDrcCheckItem target))
    (foreach marker markers
      (setq result (cons (__abProjectDrc marker) result)))
    (reverse result)))
