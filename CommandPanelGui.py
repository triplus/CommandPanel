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
import FreeCAD as App
import CommandPanelCommands as cpcmd
import CommandPanelPreferences as cpp
import CommandPanelFlowLayout as flow


mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/CommandPanel")

widget = QtGui.QWidget()

scroll = QtGui.QScrollArea()
scroll.setMinimumHeight(16)
scroll.setWidgetResizable(True)
scroll.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
scroll.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
scroll.setWidget(widget)

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

    layout = widget.layout()
    if layout:
        item = layout.takeAt(0)
        while item:
            del item
            item = layout.takeAt(0)
        # Workaround: reliably unset layout
        temp = QtGui.QWidget()
        temp.setLayout(layout)
        temp.deleteLater()

    if p.GetString("Layout") == "Expand":
        layout = QtGui.QVBoxLayout()
    else:
        layout = flow.FlowLayout()

    widget.setLayout(layout)

    buttons = cpcmd.workbenchButtons(workbench)
    for btn in buttons:
        layout.addWidget(btn)

    if p.GetString("Layout") == "Expand":
        layout.addStretch()


def onInvoke():
    """Hide or show command panel at mouse position."""
    if dock.isVisible():
        dock.toggleViewAction().trigger()
    else:
        dock.setFloating(True)
        pos = QtGui.QCursor.pos()
        dock.move(pos.x() - dock.size().width() / 2,
                  pos.y() - dock.size().height() / 2)
        dock.setVisible(True)


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


t = QtCore.QTimer()
t.timeout.connect(onStart)
t.start(500)
