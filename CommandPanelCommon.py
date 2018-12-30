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

import uuid
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


def wbIcon(i):
    """Create workbench icon."""
    if str(i.find("XPM")) != "-1":
        icon = []
        for a in ((((i
                     .split('{', 1)[1])
                    .rsplit('}', 1)[0])
                   .strip())
                  .split("\n")):
            icon.append((a
                         .split('"', 1)[1])
                        .rsplit('"', 1)[0])
        icon = QtGui.QIcon(QtGui.QPixmap(icon))
    else:
        icon = QtGui.QIcon(QtGui.QPixmap(i))
    if icon.isNull():
        icon = QtGui.QIcon(":/icons/freecad")
    return icon


def defaultGroup(base):
    """Create default group if no group exist."""
    g = None
    index = base.GetString("index")
    if not index:
        base.SetString("index", "1")
        g = base.GetGroup("1")
        g.SetString("uuid", str(uuid.uuid4()))
        g.SetString("name", "Default")
        cmd = ["Std_ViewAxo",
               "Std_ViewFront",
               "Std_ViewTop",
               "Std_ViewRight"]
        g.SetString("commands", ",".join(cmd))
        base.SetBool("default", 1)
        base.SetString("default", g.GetString("uuid"))
    return g


def newGroup(base):
    """Create new group."""
    index = base.GetString("index")
    if index:
        index = index.split(",")
    else:
        index = []
    x = 1
    while str(x) in index and x < 1000:
        x += 1
    index.append(str(x))
    base.SetString("index", ",".join(index))
    g = base.GetGroup(str(x))
    g.SetString("uuid", str(uuid.uuid4()))
    return g


def findGroup(base, uid):
    """Find group with given uuid."""
    g = None
    index = base.GetString("index")
    if index:
        index = index.split(",")
    else:
        index = []
    if uid:
        for i in index:
            if base.GetGroup(i).GetString("uuid") == uid:
                g = base.GetGroup(i)
    return g


def deleteGroup(base, uid):
    """Delete group with given uuid."""
    temp = []
    index = base.GetString("index")
    if index:
        index = index.split(",")
    else:
        index = []
    for i in index:
        if base.GetGroup(i).GetString("uuid") == uid:
            base.RemGroup(i)
        else:
            temp.append(i)
    base.SetString("index", ",".join(temp))
    defaultGroup(base)
