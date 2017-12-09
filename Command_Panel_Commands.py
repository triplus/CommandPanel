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

"""Command panel for FreeCAD - Commands."""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
import Command_Panel_Common as cpc
import Command_Panel_Event_Filter as cpef

mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/CommandPanel")


def workbenchButtons(workbench):
    """Create workbench buttons from command names."""
    g = None
    uid = None
    buttons = []
    actions = cpc.actionList()
    base = p.GetGroup("User").GetGroup(workbench)
    cpc.defaultGroup(base)
    if base.GetBool("default", 0):
        uid = base.GetString("default")
        g = cpc.findGroup(base, uid)
    if g:
        commands = g.GetString("commands")
        if commands:
            commands = commands.split(",")
        else:
            commands = []
        for cmd in commands:
            btn = QtGui.QToolButton()
            btn.setAutoRaise(True)
            btn.installEventFilter((cpef.InstallEvent(btn)))
            if cmd == "CP_Separator":
                btn.setEnabled(False)
                btn.setObjectName("CP_Separator")
            elif cmd == "CP_Spacer":
                btn.setEnabled(False)
                btn.setObjectName("CP_Spacer")
            elif cmd == "CP_Menu":
                menu = QtGui.QMenu()
                btn.setEnabled(False)
                btn.setMenu(menu)
                btn.setIcon(QtGui.QIcon(":/icons/freecad"))
                btn.setPopupMode(QtGui.QToolButton
                                 .ToolButtonPopupMode.MenuButtonPopup)
                btn.setToolTip("Empty menu")
            elif cmd.startswith("CP_Menu_"):
                menu = menuButton(base, cmd, btn, actions)
                btn.setMenu(menu)
                btn.triggered.connect(btn.setDefaultAction)
                btn.setPopupMode(QtGui.QToolButton
                                 .ToolButtonPopupMode.MenuButtonPopup)
            elif cmd in actions:
                btn.setDefaultAction(actions[cmd])
                if btn.icon().isNull():
                    btn.setIcon(QtGui.QIcon(":/icons/freecad"))
            else:
                btn.setEnabled(False)
                btn.setToolTip("Command " +
                               cmd +
                               " is not currently available")
                btn.setIcon(QtGui.QIcon(":/icons/freecad"))
            buttons.append(btn)

    return buttons


def menuButton(base, cmd, btn, actions):
    """Create menu for menu button from command names."""
    menu = QtGui.QMenu(mw)
    try:
        uid = cmd.split("CP_Menu_", 1)[1]
    except IndexError:
        uid = None
    g = cpc.findGroup(base, uid)
    if g:
        commands = g.GetString("commands")
        if commands:
            commands = commands.split(",")
        else:
            commands = []
        for cmd in commands:
            if cmd.startswith("CP_Menu") or cmd.startswith("CP_Spacer"):
                pass
            elif cmd == "CP_Separator":
                menu.addSeparator()
            elif cmd in actions:
                menu.addAction(actions[cmd])
            else:
                a = QtGui.QAction(menu)
                a.setEnabled(False)
                a.setText(cmd)
                a.setIcon(QtGui.QIcon(":/icons/freecad"))
                a.setToolTip("Command " + cmd + " is not currently available")
                menu.addAction(a)
            try:
                btn.setDefaultAction(menu.actions()[0])
            except IndexError:
                pass

    return menu
