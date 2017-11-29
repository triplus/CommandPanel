# Command panel for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017 triplus @ FreeCAD
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

import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from PySide import QtCore
import Command_Panel_Commands as cpcmd
import Command_Panel_Preferences as cpp
import Command_Panel_Flow_Layout as flow


mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/CommandPanel")

layout = flow.FlowLayout()

widget = QtGui.QWidget()
widget.setLayout(layout)

scroll = QtGui.QScrollArea()
scroll.setWidgetResizable(True)
scroll.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
scroll.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
scroll.setWidget(widget)
scroll.setMinimumHeight(16)

dock = QtGui.QDockWidget()
dock.setWindowTitle("Commands")
dock.setObjectName("CommandPanel")
dock.setWidget(scroll)
mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)


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
    item = layout.takeAt(0)
    while item:
        item.widget().hide()
        del item
        item = layout.takeAt(0)
    buttons = cpcmd.workbenchButtons(workbench)
    for btn in buttons:
        layout.addWidget(btn)


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


t = QtCore.QTimer()
t.timeout.connect(onStart)
t.start(500)
