# Chapter 16: Page Customization

16.1 Introduction
This application provides the ability to define TCL callback procedures to customize the Page
creation and page attribute (size) change processes.
You can specify different TCL procedures that will be called automatically -
- before the page is created (On Pre-create)
- after the page is created (On Post-create)
- when the page size changes (On Options->Schematic Page Properties)
16.2 Use-model and Customization
The page customization TCL callback option can be invoked from the TCL/Tk Applications
Dashboard.

---

This brings up the page customization dialog box:
You can specify your own TCL script path and callback procedures.
You also have the choice to leave any callback procedure empty if you do not wish to specifically
handle any of these callbacks.
These options are persistent across Capture sessions. They are saved in the INI file.
For your reference, Cadence has provided a sample script placed at <Installation
hierarchy>/tclscripts/capCustomeSamples/capcustomizePage.tcl that defines three procedures:
- ::capCustomizePage::onPagePreCreate : to be called before the page is created.
The sample procedure asks the user to specify the page size option before creating the
page
- ::capCustomizePage::onPagePostCreate : to be called after the page is created.
The sample procedure places different titleblocks on the page boundary to give a frame
look.
The boundary titleblocks are placed if the page size chosen is any one of A3, A2, A1 or
A0
The default titleblock placed on the page is removed
- ::capCustomizePage::onPageSizeChange : to be called when the page size changes through
Options->Schematic Page Properties
The sample procedure replaces the titleblocks on the page boundary
The boundary titleblocks are placed if the page size chosen is any one of A3, A2, A1 or
A0

---

The sample uses the titleblock symbols from the library “<Installation
hierarchy>/tclscripts/capCustomSamples/TESTCUSTOMIZEPAGE.OLB”. This library contains the
titleblock symbol for each side for the page sizes A3, A2, A1 and A0 respectively. For example, for
the page size A2, the corresponding titleblock symbols are A2Left, A2Right, A2Top and A2Bottom
respectively. Similarly, there are side-wise titleblock symbols for A3, A1 and A0 as well. You can
extend this by creating titleblock symbols for other page-sizes (A4, A, B, C, D, E, Custom etc.) also.
The sample page created (size A2) with titleblocks on the boundary looks like the following-