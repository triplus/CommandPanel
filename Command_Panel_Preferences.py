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

"""Command panel for FreeCAD - Preferences."""

import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore
import Command_Panel_Common as cpc


mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/CommandPanel")
path = os.path.dirname(__file__) + "/Resources/icons/"


def dialog():
    """Command panel preferences dialog."""

    def onAccepted():
        """Close dialog on button close."""
        dia.done(1)

    def onFinished():
        """ Delete dialog on close."""
        dia.deleteLater()

    # Dialog
    dia = QtGui.QDialog(mw)
    dia.resize(900, 500)
    dia.setWindowTitle("Command panel preferences")
    dia.finished.connect(onFinished)

    # Stack
    stack = QtGui.QStackedWidget()
    layout = QtGui.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    dia.setLayout(layout)
    layout.addWidget(stack)

    # Button close
    btnClose = QtGui.QPushButton("Close")
    btnClose.setToolTip("Close the preferences dialog")
    btnClose.setDefault(True)
    btnClose.clicked.connect(onAccepted)

    stack.insertWidget(0, general(btnClose))

    return dia


def general(btnClose):
    """General command panel preferences."""

    # Widgets
    lo = QtGui.QVBoxLayout()
    w = QtGui.QWidget(mw)
    w.setLayout(lo)

    # Search
    search = QtGui.QLineEdit()

    # Available commands
    commands = QtGui.QListWidget()
    commands.setSortingEnabled(True)
    commands.sortItems(QtCore.Qt.AscendingOrder)

    # Layout
    loPanels = QtGui.QHBoxLayout()
    loLeft = QtGui.QVBoxLayout()
    loRight = QtGui.QVBoxLayout()
    loPanels.insertLayout(0, loLeft)
    loPanels.insertLayout(1, loRight)

    loLeft.addWidget(search)
    loLeft.addWidget(commands)

    loBottom = QtGui.QHBoxLayout()
    loBottom.addStretch()
    loBottom.addWidget(btnClose)

    lo.insertLayout(0, loPanels)
    lo.insertLayout(1, loBottom)

    # Functions and connections

    def onSearch(text):
        """Show or hide commands on search."""
        for index in range(commands.count()):
            if text.lower() in commands.item(index).text().lower():
                commands.item(index).setHidden(False)
            else:
                commands.item(index).setHidden(True)

    search.textEdited.connect(onSearch)

    def populateCommands():
        """Populate available commands panel."""
        actions = cpc.actionList()
        commands.blockSignals(True)
        commands.clear()
        for i in actions:
            item = QtGui.QListWidgetItem(commands)
            item.setText(actions[i].text().replace("&", ""))
            item.setIcon(actions[i].icon())
            item.setData(QtCore.Qt.UserRole, actions[i].objectName())
        commands.blockSignals(False)

    populateCommands()

    return w
