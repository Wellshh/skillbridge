// Allegro workbench: selection, preview/commit/rollback, cross-probing.
// Re-initializes on Material's document$ so instant navigation stays live.
(function () {
  function setState(rail, label, color) {
    var el = rail.querySelector(".ab-state");
    if (!el) return;
    el.textContent = label;
    el.style.color = color;
  }

  function initWorkbench(root) {
    var wb = root.querySelector(".ab-workbench");
    if (!wb || wb.dataset.wbBound) return;
    wb.dataset.wbBound = "1";

    var token = {
      selection: getComputedStyle(document.body).getPropertyValue("--ab-selection").trim() || "#4fd8e0",
      commit: getComputedStyle(document.body).getPropertyValue("--ab-commit").trim() || "#6fd08c",
      preview: getComputedStyle(document.body).getPropertyValue("--ab-preview").trim() || "#e8a33d",
      error: getComputedStyle(document.body).getPropertyValue("--ab-error").trim() || "#ff665f",
    };

    var r101 = wb.querySelector(".ab-obj-r101");
    var selBox = wb.querySelector(".ab-sel-box");
    var rail = wb.querySelector(".ab-wb-status");
    var cmd = wb.querySelector(".ab-cmd");
    var inspector = wb.querySelector(".ab-wb-inspector");

    var home = { x: 0, y: 0 };
    var dest = { x: 60, y: 40 }; // preview offset in SVG units

    function select() {
      if (r101) r101.classList.add("ab-selected");
      if (selBox) selBox.style.display = "";
      setState(rail, "READ", token.selection);
    }
    function deselect() {
      if (r101) r101.classList.remove("ab-selected");
    }

    // Cross-probing: canvas object and code lines both light up R101.
    if (r101) {
      r101.addEventListener("mouseenter", select);
      r101.addEventListener("mouseleave", function () {
        if (!wb.dataset.wbLocked) deselect();
      });
      r101.addEventListener("click", function () {
        wb.dataset.wbLocked = "1";
        select();
        if (cmd) cmd.textContent = 'pcb.components["R101"]';
      });
    }
    root.querySelectorAll("[data-probe='r101']").forEach(function (line) {
      line.addEventListener("mouseenter", select);
      line.addEventListener("mouseleave", deselect);
    });

    // Layer visibility toggles hide/show matching SVG groups.
    wb.querySelectorAll(".ab-wb-layers input[data-layer]").forEach(function (box) {
      box.addEventListener("change", function () {
        var layer = wb.querySelector("[data-layer-group='" + box.dataset.layer + "']");
        if (layer) layer.style.display = box.checked ? "" : "none";
      });
    });

    // Preview / commit / rollback simulation.
    function act(kind) {
      if (!r101) return;
      wb.dataset.wbLocked = "1";
      r101.classList.add("ab-selected");
      if (kind === "preview") {
        r101.classList.add("ab-ghost");
        r101.setAttribute("transform", "translate(" + dest.x + "," + dest.y + ")");
        setState(rail, "PREVIEW", token.preview);
        if (cmd) cmd.textContent = "components.move.preview R101";
      } else if (kind === "commit") {
        r101.classList.remove("ab-ghost");
        r101.setAttribute("transform", "translate(" + dest.x + "," + dest.y + ")");
        setState(rail, "COMMITTED", token.commit);
        if (cmd) cmd.textContent = "components.move R101";
        var gen = inspector && inspector.querySelector("[data-gen]");
        if (gen) gen.textContent = String(parseInt(gen.textContent, 10) + 1);
      } else if (kind === "rollback") {
        r101.classList.remove("ab-ghost");
        r101.setAttribute("transform", "translate(" + home.x + "," + home.y + ")");
        setState(rail, "ROLLED_BACK", token.error);
        if (cmd) cmd.textContent = "rollback";
        setTimeout(function () { setState(rail, "READY", token.commit); }, 900);
      }
    }

    wb.querySelectorAll(".ab-wb-actions button").forEach(function (btn) {
      btn.addEventListener("click", function () { act(btn.dataset.act); });
    });
  }

  function boot() {
    initWorkbench(document);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();
