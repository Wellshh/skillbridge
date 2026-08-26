;;; Copyright (c) 2025-2026 Bai Junyan and contributors.
;;; SPDX-License-Identifier: LGPL-3.0-or-later
;;; shapes.il - Lazy Allegro shape projection operations.

(putd '__abProjectShapePoint nil)
(defun __abProjectShapePoint (point)
  (list nil 'x (car point) 'y (cadr point)))

(putd '__abProjectShapeBBox nil)
(defun __abProjectShapeBBox (bbox)
  (list nil
        'lower_left (__abProjectShapePoint (car bbox))
        'upper_right (__abProjectShapePoint (cadr bbox))))

(putd '__abShapeNetName nil)
(defun __abShapeNetName (shape)
  (let ((netObject shape->net))
    (when (and netObject
               (not (stringp netObject))
               (not (equal netObject->name "")))
      netObject->name)))

(putd '__abProjectShape nil)
(defun __abProjectShape (shape)
  (list nil
        'net (__abShapeNetName shape)
        'layer shape->layer
        'dynamic (if shape->shapeIsBoundary then "dynamic" else "static")
        'bbox (__abProjectShapeBBox shape->bBox)))

(putd '__abProjectShapes nil)
(defun __abProjectShapes (net layer dynamic)
  (let (result)
    (foreach shape (axlDBGetShapes layer)
      (let ((projected (__abProjectShape shape)))
        (when (and (or (null net) (equal net (get projected 'net)))
                   (or (null dynamic) (equal dynamic (get projected 'dynamic))))
          (setq result (cons projected result)))))
    (reverse result)))
