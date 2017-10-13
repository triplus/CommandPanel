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

"""Command panel for FreeCAD - Common."""

import FreeCADGui as Gui
from PySide import QtGui


mw = Gui.getMainWindow()


def actionList():
    """Create a dictionary of unique actions."""
    actions = {}
    duplicates = []
    for i in mw.findChildren(QtGui.QAction):
        if i.objectName() and i.text():
            if i.objectName() in actions:
                if i.objectName() not in duplicates:
                    duplicates.append(i.objectName())
            else:
                actions[i.objectName()] = i
    for d in duplicates:
        del actions[d]
    return actions
