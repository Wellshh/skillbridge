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
                      'll (list nil 'x (car (car bbox)) 'y (cadr (car bbox)))
                      'ur (list nil 'x (car (cadr bbox)) 'y (cadr (cadr bbox))))
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

(putd '__abFindDrcItem nil)
(defun __abFindDrcItem (kind primary secondary)
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
(defun __abCheckDrcs (kind primary secondary)
  (letseq ((target (__abFindDrcItem kind primary secondary))
           markers result)
    (unless target
      (error (sprintf nil "DRC_TARGET_NOT_FOUND: %L/%L/%L"
                     kind primary secondary)))
    (setq markers (__abDrcCheckItem target))
    (foreach marker markers
      (setq result (cons (__abProjectDrc marker) result)))
    (reverse result)))
