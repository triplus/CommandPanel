# Command panel for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017, 2018 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Command panel for FreeCAD - Gui."""


from PySide import QtGui
from PySide import QtCore
import FreeCADGui as Gui
import CommandPanelCommon as cpc
import CommandPanelCommands as cpcmd
import CommandPanelPreferences as cpp
import CommandPanelFlowLayout as flow


p = cpc.p
layout = None
mw = Gui.getMainWindow()

widget = QtGui.QWidget()
widget.setContentsMargins(0, 0, 0, 0)

scroll = QtGui.QScrollArea()
scroll.setMinimumHeight(16)
scroll.setWidgetResizable(True)
scroll.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
scroll.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
scroll.setWidget(widget)

dock = QtGui.QDockWidget()
dock.setWindowTitle("Commands")
dock.setObjectName("CommandPanel")

invokeMenu = QtGui.QMenu()
invokeMenu.hide()
widgetAction = QtGui.QWidgetAction(invokeMenu)

# Layouts
layoutGlobal = QtGui.QVBoxLayout()
widget.setLayout(layoutGlobal)

layoutFlow = flow.FlowLayout()
layoutGrid = QtGui.QGridLayout()

layoutStretch = QtGui.QVBoxLayout()
layoutStretch.addStretch()

layoutGlobal.insertLayout(0, layoutFlow)
layoutGlobal.insertLayout(1, layoutGrid)
layoutGlobal.insertLayout(2, layoutStretch)


def setLayout():
    """Use Grid or Flow layout"""
    global layout

    if p.GetString("Layout") == "Grid":
        layoutFlow.setEnabled(False)
        layoutGrid.setEnabled(True)
        layoutStretch.setEnabled(True)
        layout = layoutGrid
    else:
        layoutGrid.setEnabled(False)
        layoutStretch.setEnabled(False)
        layoutFlow.setEnabled(True)
        layout = layoutFlow


def setContainer():
    """Use dock or menu as a container."""
    if p.GetBool("Menu", 0):
        mw.removeDockWidget(dock)
        dock.toggleViewAction().setVisible(False)
        widgetAction.setDefaultWidget(scroll)
        invokeMenu.addAction(widgetAction)
        scroll.setFrameShape(QtGui.QFrame.NoFrame)
    else:
        dock.setWidget(scroll)
        mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        dock.toggleViewAction().setVisible(True)
        scroll.setMinimumSize(QtCore.QSize(0, 0))
        scroll.setMaximumSize(QtCore.QSize(16777215, 16777215))
        scroll.setFrameShape(QtGui.QFrame.StyledPanel)
        dock.show()


def accessoriesMenu():
    """Add command panel preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("Command panel")
    pref.setObjectName("CommandPanel")
    pref.triggered.connect(onPreferences)
    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("CommandPanel")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")
        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            action = QtGui.QAction(mw)
            action.setObjectName("AccessoriesMenu")
            action.setIconText("Accessories")
            menu = QtGui.QMenu()
            action.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menu bar."""
                toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")
                if toolsMenu:
                    toolsMenu.addAction(action)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def onPreferences():
    """Open the preferences dialog."""
    cpp.createWidgets()
    dialog = cpp.dialog()
    dialog.show()


def onWorkbench():
    """Populate command panel on workbench activation."""
    workbench = Gui.activeWorkbench().__class__.__name__

    if layout:
        while not layout.isEmpty():
            item = layout.takeAt(0)
            del item

    buttons = cpcmd.workbenchButtons(workbench)

    if p.GetString("Layout") == "Grid":
        columns = p.GetInt("ColumnNumber", 1) - 1
        x = 0
        y = 0
        for btn in buttons:
            if y > columns:
                y = 0
                x += 1
            layout.addWidget(btn, x, y)
            y += 1
        # Set spacing
        layout.setSpacing(p.GetInt("ButtonSpacing", 5))
    else:
        for btn in buttons:
            layout.addWidget(btn)
        # Set spacing
        layout.setSpaceXY()
        layout.update()


def onInvoke():
    """Hide or show command panel at mouse position."""
    enabled = p.GetBool("Menu", 0)
    if enabled and invokeMenu.isVisible():
        invokeMenu.hide()
    elif enabled:
        pos = QtGui.QCursor.pos()
        invokeMenu.setFixedWidth(p.GetInt("MenuWidth", 300))
        invokeMenu.setFixedHeight(p.GetInt("MenuHeight", 300))
        scroll.setFixedWidth(p.GetInt("MenuWidth", 300))
        scroll.setFixedHeight(p.GetInt("MenuHeight", 300))
        invokeMenu.popup(QtCore.QPoint(pos.x() - invokeMenu.width() / 2,
                                       pos.y() - invokeMenu.height() / 2))
    else:
        pass


def onStart():
    """Start command panel."""
    start = False
    try:
        mw.workbenchActivated
        start = True
    except AttributeError:
        pass
    if start:
        t.stop()
        t.deleteLater()
        onWorkbench()
        accessoriesMenu()
        mw.workbenchActivated.connect(onWorkbench)
        a = QtGui.QAction(mw)
        mw.addAction(a)
        a.setText("Invoke command panel")
        a.setObjectName("InvokeCommandPanel")
        a.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
        a.triggered.connect(onInvoke)


setContainer()
setLayout()


t = QtCore.QTimer()
t.timeout.connect(onStart)
t.start(500)
