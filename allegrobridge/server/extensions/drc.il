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
                      'lower_left (list nil 'x (car (car bbox)) 'y (cadr (car bbox)))
                      'upper_right (list nil 'x (car (cadr bbox)) 'y (cadr (cadr bbox))))
          'objects (__abDrcObjects marker))))

(putd '__abProjectDrcs nil)
(defun __abProjectDrcs ()
  (letseq ((design (__abFreshDesign)) result)
    (foreach marker design->drcs
      (setq result (cons (__abProjectDrc marker) result)))
    (reverse result)))
