# Command panel for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017, 2018, 2019 triplus @ FreeCAD
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


import os
from PySide import QtGui
from PySide import QtCore
import FreeCADGui as Gui
import CommandPanelGui as cpg
import CommandPanelCommon as cpc
import CommandPanelEventFilter as cpef


p = cpc.p
menuList = []
buttonList = []
currentMenu = None
mw = Gui.getMainWindow()
mapperShow = QtCore.QSignalMapper()
mapperExpandCollapse = QtCore.QSignalMapper()
path = os.path.dirname(__file__) + "/Resources/icons/"


class CommandButton(QtGui.QToolButton):
    """Clear currentMenu on button press event."""
    def __init__(self):
        super(CommandButton, self).__init__()

    def mousePressEvent(self, event):
        """Press event."""
        global currentMenu
        currentMenu = None
        super(CommandButton, self).mousePressEvent(event)


def buttonFactory():
    """Create button and apply the settings."""
    btn = CommandButton()
    btn.installEventFilter((cpef.InstallEvent(btn)))

    btnStyle = p.GetString("Style")

    if btnStyle == "Text":
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
    elif btnStyle == "IconText":
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    elif btnStyle == "TextBelow":
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
    else:
        pass

    if p.GetBool("EnableIconSize", 0):
        iconSize = p.GetInt("IconSize", 16)
        btn.setIconSize(QtCore.QSize(iconSize, iconSize))

    if p.GetBool("EnableButtonWidth", 0):
        btn.setFixedWidth(p.GetInt("ButtonWidth", 30))

    if p.GetBool("EnableButtonHeight", 0):
        btn.setFixedHeight(p.GetInt("ButtonHeight", 30))

    if p.GetBool("EnableFontSize", 0):
        font = btn.font()
        font.setPointSize(p.GetInt("FontSize", 8))
        btn.setFont(font)

    if p.GetString("Layout") == "Grid":
        policy = btn.sizePolicy()
        policy.setHorizontalPolicy(QtGui.QSizePolicy.Ignored)
        btn.setSizePolicy(policy)

    if p.GetBool("AutoRaise", 1):
        btn.setAutoRaise(True)

    return btn


def workbenchButtons(workbench):
    """Create workbench buttons from command names."""
    clearList(menuList)
    clearList(buttonList)

    g = None
    uid = None
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
            commands = menuCommands(base, commands)
        else:
            commands = []
        for cmd in commands:
            btn = buttonFactory()
            if cmd.startswith("CP_Collapse_"):
                a = QtGui.QAction(btn)
                try:
                    gUid = cmd.split("CP_Collapse_", 1)[1]
                except IndexError:
                    gUid = "No_UID"
                data = ",".join([workbench, gUid, str(0)])
                a.setData(data)
                a.setText("Collapse")
                a.setIcon(QtGui.QIcon(path + "CommandPanelCollapse.svg"))
                a.setToolTip("Collapse menu")
                btn.setDefaultAction(a)
                btn.setObjectName("Collapse")
                mapperExpandCollapse.setMapping(btn, data)
                btn.clicked.connect(mapperExpandCollapse.map)
            elif cmd == "CP_Separator":
                btn.setEnabled(False)
                btn.setObjectName("CP_Separator")
            elif cmd == "CP_Spacer":
                btn.setEnabled(False)
                btn.setObjectName("CP_Spacer")
            elif cmd == "CP_Menu":
                menu = QtGui.QMenu()
                btn.setMenu(menu)
                btn.setIcon(QtGui.QIcon(":/icons/freecad"))
                # Themes support
                btn.setObjectName("qt_toolbutton_menubutton")
                btn.setPopupMode(QtGui.QToolButton
                                 .ToolButtonPopupMode.MenuButtonPopup)
                btn.setToolTip("Empty menu")
            elif cmd.startswith("CP_Menu_"):
                menu = menuButton(workbench, base, cmd, btn, actions)
                btn.setMenu(menu)
                # Theme support
                btn.setObjectName("qt_toolbutton_menubutton")
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
                               " is currently not available")
                btn.setIcon(QtGui.QIcon(":/icons/freecad"))

            if (p.GetString("Layout") == "Grid" and
                    btn.objectName() == "CP_Spacer"):
                pass
            else:
                buttonList.append(btn)
    if p.GetBool("Menu", 0):
        for b in buttonList:
            if b.objectName() != "Collapse":
                b.clicked.connect(cpg.onInvoke)
    for m in menuList:
        m.triggered.connect(onMenuTriggered)

    return buttonList


def menuButton(workbench, base, cmd, btn, actions):
    """Create menu for menu button from command names."""
    menu = QtGui.QMenu(mw)
    menuList.append(menu)
    try:
        uid = cmd.split("CP_Menu_", 1)[1]
    except IndexError:
        uid = "No_UID"
    menu.setObjectName(uid)
    g = cpc.findGroup(base, uid)
    if g and uid != "No_UID":
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
                a.setToolTip("Command " + cmd + " is currently not available")
                menu.addAction(a)
        # Set default action
        try:
            btn.setDefaultAction(menu.actions()[0])
            menu.setDefaultAction(menu.actions()[0])
        except IndexError:
            pass

        default = g.GetString("Default")
        for a in menu.actions():
            if a.objectName() == default:
                btn.setDefaultAction(a)
                menu.setDefaultAction(a)

        # Add expand action
        data = ",".join([workbench, uid, str(1)])

        e = QtGui.QAction(menu)
        e.setText("Expand")
        e.setIcon(QtGui.QIcon(path + "CommandPanelExpand.svg"))
        e.setToolTip("Expand menu")
        e.setData(data)

        menu.addSeparator()
        menu.addAction(e)

        mapperExpandCollapse.setMapping(e, data)
        e.triggered.connect(mapperExpandCollapse.map)

        mapperShow.setMapping(menu, data)
        menu.aboutToShow.connect(mapperShow.map)

    return menu


def menuCommands(base, commands):
    """Add command names for expanded menu."""
    names = []
    for cmd in commands:
        if cmd.startswith("CP_Menu_"):
            try:
                uid = cmd.split("CP_Menu_", 1)[1]
            except IndexError:
                uid = "No_UID"
            g = cpc.findGroup(base, uid)
            if g and uid != "No_UID":
                expand = g.GetBool("Expand", 0)
            else:
                expand = 0
            if expand:
                gE = g.GetString("commands")
                if gE:
                    gE = gE.split(",")
                else:
                    gE = []
                for e in gE:
                    if e.startswith("CP_Menu"):
                        pass
                    else:
                        names.append(e)
                # Move spacer after collapse button
                try:
                    last = names.pop()
                except IndexError:
                    last = None
                if last == "CP_Spacer":
                    names.append("CP_Collapse_" + uid)
                    names.append(last)
                elif last:
                    names.append(last)
                    names.append("CP_Collapse_" + uid)
                else:
                    names.append("CP_Collapse_" + uid)
            else:
                names.append(cmd)
        else:
            names.append(cmd)

    return names


def clearList(l):
    """Empty list and delete the items."""
    try:
        item = l.pop()
    except IndexError:
        item = None
    while item:
        item.deleteLater()
        try:
            item = l.pop()
        except IndexError:
            item = None


def onMenuShow(n):
    """Set current menu name on menu aboutToShow"""
    global currentMenu
    currentMenu = n


def onMenuTriggered(a):
    """Set default menu action on menu triggered."""
    try:
        data = currentMenu.split(",")
    except AttributeError:
        data = []
    try:
        wb = data[0]
        uid = data[1]
    except IndexError:
        wb = None
        uid = None
    if wb:
        base = p.GetGroup("User").GetGroup(wb)
    else:
        base = None
    if base and uid:
        g = cpc.findGroup(base, uid)
    else:
        g = None

    for m in menuList:
        if m.objectName() == uid:
            m.setDefaultAction(a)
            for b in buttonList:
                if b.menu() == m:
                    b.setDefaultAction(a)
            name = a.objectName()
            if g and name:
                g.SetString("Default", name)


def onMenuExpandCollapse(s):
    """Set expand or collapse menu parameter."""
    g = None
    base = None
    try:
        data = s.split(",")
    except AttributeError:
        data = []
    try:
        wb = data[0]
        uid = data[1]
        expand = data[2]
    except IndexError:
        wb = None
        uid = None
        expand = None
    if wb:
        base = p.GetGroup("User").GetGroup(wb)
    if base and uid:
        g = cpc.findGroup(base, uid)
    if g and expand == "1":
        g.SetBool("Expand", 1)
    elif g:
        g.SetBool("Expand", 0)
    else:
        pass

    cpg.onWorkbench()


mapperShow.mapped[str].connect(onMenuShow)
mapperExpandCollapse.mapped[str].connect(onMenuExpandCollapse)
