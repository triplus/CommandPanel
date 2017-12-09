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
import Command_Panel_Gui as cpg
import Command_Panel_Common as cpc


mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/CommandPanel")
path = os.path.dirname(__file__) + "/Resources/icons/"


def createWidgets():
    """Create widgets on preferences dialog start."""
    global cBoxWb
    cBoxWb = QtGui.QComboBox()
    cBoxWb.setSizePolicy(QtGui.QSizePolicy.Expanding,
                         QtGui.QSizePolicy.Preferred)
    global cBoxMenu
    cBoxMenu = QtGui.QComboBox()
    cBoxMenu.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Preferred)
    global enabled
    enabled = QtGui.QListWidget()


def baseGroup():
    """Current group."""
    wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
    g = p.GetGroup("User").GetGroup(wb)
    return g


def saveEnabled():
    """Save enabled on change."""
    items = []
    for index in range(enabled.count()):
        items.append(enabled.item(index).data(QtCore.Qt.UserRole))
    uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
    g = cpc.findGroup(baseGroup(), uid)
    if g:
        g.SetString("commands", ",".join(items))
    cpg.onWorkbench()


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
    dia.setModal(True)
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
    btnClose.clicked.connect(onAccepted)

    stack.insertWidget(0, general(dia, stack, btnClose))
    stack.insertWidget(1, edit(stack))

    btnClose.setDefault(True)
    btnClose.setFocus()

    return dia


def general(dia, stack, btnClose):
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

    # Reset workbench
    btnResetWb = QtGui.QPushButton()
    btnResetWb.setToolTip("Reset workbench to defaults")
    btnResetWb.setIcon(QtGui.QIcon(path + "CommandPanel_Reset.svg"))

    # Checkbox default menu
    ckDefault = QtGui.QCheckBox()
    ckDefault.setToolTip("Set default workbench menu")

    # Button add workbench menu
    btnAddWbMenu = QtGui.QPushButton()
    btnAddWbMenu.setToolTip("Add new workbench menu")
    btnAddWbMenu.setIcon(QtGui.QIcon(path + "CommandPanel_Add.svg"))

    # Button remove workbench menu
    btnRemoveWbMenu = QtGui.QPushButton()
    btnRemoveWbMenu.setToolTip("Remove currently selected workbench menu")
    btnRemoveWbMenu.setIcon(QtGui.QIcon(path + "CommandPanel_Remove.svg"))

    # Button add command
    btnAddCommand = QtGui.QPushButton()
    btnAddCommand.setToolTip("Add selected command")
    btnAddCommand.setIcon(QtGui.QIcon(path + "CommandPanel_AddCommand.svg"))

    # Button remove command
    btnRemoveCommand = QtGui.QPushButton()
    btnRemoveCommand.setToolTip("Remove selected command")
    btnRemoveCommand.setIcon(QtGui.QIcon(path +
                                         "CommandPanel_RemoveCommand.svg"))

    # Button move up
    btnMoveUp = QtGui.QPushButton()
    btnMoveUp.setToolTip("Move selected command up")
    btnMoveUp.setIcon(QtGui.QIcon(path + "CommandPanel_Up.svg"))

    # Button move down
    btnMoveDown = QtGui.QPushButton()
    btnMoveDown.setToolTip("Move selected command down")
    btnMoveDown.setIcon(QtGui.QIcon(path + "CommandPanel_Down.svg"))

    # Button add separator
    btnAddSeparator = QtGui.QPushButton()
    btnAddSeparator.setToolTip("Add separator")
    btnAddSeparator.setIcon(QtGui.QIcon(path +
                                        "CommandPanel_AddSeparator.svg"))

    # Button add spacer
    btnAddSpacer = QtGui.QPushButton()
    btnAddSpacer.setToolTip("Add spacer")
    btnAddSpacer.setIcon(QtGui.QIcon(path + "CommandPanel_AddSpacer.svg"))

    # Button add menu
    btnAddMenu = QtGui.QPushButton()
    btnAddMenu.setToolTip("Add menu")
    btnAddMenu.setIcon(QtGui.QIcon(path + "CommandPanel_AddMenu.svg"))

    # Button edit menu
    btnEditMenu = QtGui.QPushButton()
    btnEditMenu.setEnabled(False)
    btnEditMenu.setToolTip("Edit menu")
    btnEditMenu.setIcon(QtGui.QIcon(path + "CommandPanel_EditMenu.svg"))

    # Layout
    loPanels = QtGui.QHBoxLayout()
    loLeft = QtGui.QVBoxLayout()
    loRight = QtGui.QVBoxLayout()
    loPanels.insertLayout(0, loLeft)
    loPanels.insertLayout(1, loRight)

    loLeft.addWidget(search)
    loLeft.addWidget(commands)

    loCBoxWb = QtGui.QHBoxLayout()
    loCBoxWb.addWidget(cBoxWb)
    loCBoxWb.addWidget(btnResetWb)

    loCBoxMenu = QtGui.QHBoxLayout()
    loCBoxMenu.addWidget(ckDefault)
    loCBoxMenu.addWidget(cBoxMenu)
    loCBoxMenu.addWidget(btnAddWbMenu)
    loCBoxMenu.addWidget(btnRemoveWbMenu)

    loControls = QtGui.QHBoxLayout()
    loControls.addStretch()
    loControls.addWidget(btnAddCommand)
    loControls.addWidget(btnRemoveCommand)
    loControls.addWidget(btnMoveUp)
    loControls.addWidget(btnMoveDown)
    loControls.addWidget(btnAddSeparator)
    loControls.addWidget(btnAddSpacer)
    loControls.addWidget(btnAddMenu)
    loControls.addWidget(btnEditMenu)

    loRight.insertLayout(0, loCBoxWb)
    loRight.insertLayout(1, loCBoxMenu)
    loRight.addWidget(enabled)
    loRight.insertLayout(3, loControls)

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
            item.setToolTip(actions[i].toolTip())
            icon = actions[i].icon()
            if icon.isNull():
                item.setIcon(QtGui.QIcon(":/icons/freecad"))
            else:
                item.setIcon(icon)
            item.setData(QtCore.Qt.UserRole, actions[i].objectName())
        commands.setCurrentRow(0)
        commands.blockSignals(False)

    def populateCBoxWb():
        """Workbench selector combo box."""
        wb = Gui.listWorkbenches()
        wbSort = list(wb)
        wbSort.sort()
        wbSort.reverse()
        cBoxWb.blockSignals(True)
        cBoxWb.clear()
        for i in wbSort:
            try:
                icon = cpc.wbIcon(wb[i].Icon)
            except AttributeError:
                icon = QtGui.QIcon(":/icons/freecad")
            mt = wb[i].MenuText
            cn = wb[i].__class__.__name__
            cBoxWb.insertItem(0, icon, mt, cn)
        activeWb = Gui.activeWorkbench().__class__.__name__
        cBoxWb.setCurrentIndex(cBoxWb.findData(activeWb))
        cBoxWb.blockSignals(False)

    def onCBoxWb():
        """Activate workbench on selection."""
        base = baseGroup()
        wb = Gui.listWorkbenches()
        current = cBoxWb.itemData(cBoxWb.currentIndex(),
                                  QtCore.Qt.UserRole)
        for i in wb:
            if wb[i].__class__.__name__ == current:
                Gui.activateWorkbench(i)
        cpc.defaultGroup(base)
        populateCommands()
        populateCBoxMenu()
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        populateEnabled(cpc.findGroup(base, uid))
        btnClose.setFocus()

    cBoxWb.currentIndexChanged.connect(onCBoxWb)

    def populateCBoxMenu():
        """Workbench menu combo box."""
        base = baseGroup()
        index = base.GetString("index")
        if index:
            index = index.split(",")
        else:
            index = []
        cBoxMenu.blockSignals(True)
        cBoxMenu.clear()
        for i in index:
            name = base.GetGroup(i).GetString("name")
            uid = base.GetGroup(i).GetString("uuid")
            try:
                cBoxMenu.insertItem(0, name.decode("UTF-8"), uid)
            except AttributeError:
                cBoxMenu.insertItem(0, name, uid)
        ckDefault.blockSignals(True)
        if base.GetBool("default", 0):
            default = base.GetString("default")
            data = cBoxMenu.findData(default)
            cBoxMenu.setCurrentIndex(data)
            if isDefaultMenu():
                ckDefault.setChecked(True)
            else:
                cBoxMenu.setCurrentIndex(0)
                ckDefault.setChecked(False)
        else:
            cBoxMenu.setCurrentIndex(0)
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        cBoxMenu.blockSignals(False)

    def onCBoxMenu():
        """Load workbench menu data."""
        base = baseGroup()
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        ckDefault.blockSignals(True)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        populateEnabled(cpc.findGroup(base, uid))
        btnClose.setFocus()

    cBoxMenu.currentIndexChanged.connect(onCBoxMenu)

    def onBtnResetWb():
        """Reset workbench to defaults."""
        base = baseGroup()
        base.Clear()
        cpc.defaultGroup(base)
        populateCBoxMenu()
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        populateEnabled(cpc.findGroup(base, uid))
        btnClose.setFocus()

    btnResetWb.clicked.connect(onBtnResetWb)

    def onBtnAddWbMenu():
        """Add new workbench menu."""
        d = QtGui.QInputDialog(dia)
        d.setModal(True)
        d.setInputMode(QtGui.QInputDialog.InputMode.TextInput)
        text, ok = QtGui.QInputDialog.getText(dia,
                                              "New menu",
                                              "Please insert menu name.")
        if ok:
            base = baseGroup()
            g = cpc.newGroup(base)
            try:
                g.SetString("name", text.encode("UTF-8"))
            except TypeError:
                g.SetString("name", text)
            populateCBoxMenu()
            cBoxMenu.setCurrentIndex(cBoxMenu.findData(g.GetString("uuid")))
            d.deleteLater()
            populateEnabled(g)
        else:
            d.deleteLater()
        btnClose.setFocus()

    btnAddWbMenu.clicked.connect(onBtnAddWbMenu)

    def onBtnRemoveWbMenu():
        """Remove selected workbench menu."""
        base = baseGroup()
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        cpc.deleteGroup(base, uid)
        cpc.defaultGroup(base)
        populateCBoxMenu()
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        populateEnabled(cpc.findGroup(base, uid))
        btnClose.setFocus()

    btnRemoveWbMenu.clicked.connect(onBtnRemoveWbMenu)

    def onCKDefault(checked):
        """Set the checkbox state."""
        base = baseGroup()
        base.SetBool("default", 1)
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if checked:
            base.SetString("default", uid)
        else:
            base.RemString("default")
        cpg.onWorkbench()

    ckDefault.stateChanged.connect(onCKDefault)

    def isDefaultMenu():
        """Check if current menu is the default menu."""
        d = False
        base = baseGroup()
        uid = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if base.GetBool("default", 0):
            if base.GetString("default") == uid:
                d = True
        return d

    def populateEnabled(group):
        """Populate enabled commands panel."""
        items = group.GetString("commands")
        if items:
            items = items.split(",")
        else:
            items = []
        actions = cpc.actionList()
        enabled.blockSignals(True)
        enabled.clear()
        for i in items:
            item = QtGui.QListWidgetItem(enabled)
            if i == "CP_Separator":
                item.setText("Separator")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path +
                                         "CommandPanel_AddSeparator.svg"))
            elif i == "CP_Spacer":
                item.setText("Spacer")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path + "CommandPanel_AddSpacer.svg"))
            elif i.startswith("CP_Menu"):
                try:
                    g = cpc.findGroup(baseGroup(), i.split("CP_Menu_", 1)[1])
                except IndexError:
                    g = None
                if g:
                    try:
                        text = g.GetString("name").decode("UTF-8")
                    except AttributeError:
                        text = g.GetString("name")
                    item.setText("Menu: " + text)
                else:
                    item.setText("Menu")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path + "CommandPanel_AddMenu.svg"))
            elif i in actions:
                item.setText(actions[i].text().replace("&", ""))
                item.setToolTip(actions[i].toolTip())
                icon = actions[i].icon()
                if icon.isNull():
                    item.setIcon(QtGui.QIcon(":/icons/freecad"))
                else:
                    item.setIcon(icon)
                item.setData(QtCore.Qt.UserRole, i)
            else:
                item.setText(i)
                item.setToolTip("Command " + i + " is not currently available")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/freecad"))
                item.setIcon(QtGui.QIcon(icon.pixmap(256,
                                                     QtGui.QIcon.Disabled)))
                item.setData(QtCore.Qt.UserRole, i)
        enabled.setCurrentRow(0)
        enabled.blockSignals(False)
        cpg.onWorkbench()
        onSelectionChanged()

    def onBtnAddCommand():
        """Add the selected command."""
        row = enabled.currentRow()
        data = commands.currentItem().data(QtCore.Qt.UserRole)
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText(commands.currentItem().text().replace("&", ""))
        item.setToolTip(commands.currentItem().toolTip())
        item.setIcon(commands.currentItem().icon())
        item.setData(QtCore.Qt.UserRole, data)
        saveEnabled()

    btnAddCommand.clicked.connect(onBtnAddCommand)
    commands.itemDoubleClicked.connect(onBtnAddCommand)

    def onBtnRemoveCommand():
        """Remove the selected command."""
        row = enabled.currentRow()
        item = enabled.takeItem(row)
        if item:
            del item
            if row == enabled.count():
                enabled.setCurrentRow(row - 1)
            else:
                enabled.setCurrentRow(row)
            saveEnabled()

    btnRemoveCommand.clicked.connect(onBtnRemoveCommand)

    def onBtnMoveUp():
        """Move selected command up."""
        row = enabled.currentRow()
        if row != 0:
            item = enabled.takeItem(row)
            enabled.insertItem(row - 1, item)
            enabled.setCurrentRow(row - 1)
            saveEnabled()

    btnMoveUp.clicked.connect(onBtnMoveUp)

    def onBtnMoveDown():
        """Move selected command down."""
        row = enabled.currentRow()
        if row != enabled.count() - 1 and row != -1:
            item = enabled.takeItem(row)
            enabled.insertItem(row + 1, item)
            enabled.setCurrentRow(row + 1)
            saveEnabled()

    btnMoveDown.clicked.connect(onBtnMoveDown)

    def onBtnAddSeparator():
        """Add separator."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Separator")
        item.setData(QtCore.Qt.UserRole, "CP_Separator")
        item.setIcon(QtGui.QIcon(path + "CommandPanel_AddSeparator.svg"))
        saveEnabled()

    btnAddSeparator.clicked.connect(onBtnAddSeparator)

    def onBtnAddSpacer():
        """Add spacer."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Spacer")
        item.setData(QtCore.Qt.UserRole, "CP_Spacer")
        item.setIcon(QtGui.QIcon(path + "CommandPanel_AddSpacer.svg"))
        saveEnabled()

    btnAddSpacer.clicked.connect(onBtnAddSpacer)

    def onBtnAddMenu():
        """Add menu."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Menu")
        item.setData(QtCore.Qt.UserRole, "CP_Menu")
        item.setIcon(QtGui.QIcon(path + "CommandPanel_AddMenu.svg"))
        saveEnabled()
        onSelectionChanged()

    btnAddMenu.clicked.connect(onBtnAddMenu)

    def onSelectionChanged():
        """Set enabled state for widgets on selection changed."""
        current = enabled.currentItem()
        if current:
            data = current.data(QtCore.Qt.UserRole)
        if current and data and data.startswith("CP_Menu"):
            btnEditMenu.setEnabled(True)
            btnEditMenu.setFocus()
        else:
            btnEditMenu.setEnabled(False)

    enabled.itemSelectionChanged.connect(onSelectionChanged)

    def onEditMenu():
        """Open menu selection dialog."""
        current = enabled.currentItem()
        if current and current.data(QtCore.Qt.UserRole).startswith("CP_Menu"):
            stack.setCurrentIndex(1)

    btnEditMenu.clicked.connect(onEditMenu)
    enabled.itemDoubleClicked.connect(onEditMenu)

    def onStack(n):
        """Visible widget index change."""
        if n == 0:
            row = enabled.currentRow()
            index = cBoxMenu.currentIndex()
            populateEnabled(cpc.findGroup(baseGroup(),
                                          cBoxMenu.itemData(index)))
            enabled.setCurrentRow(row)
            btnClose.setDefault(True)
        onSelectionChanged()

    stack.currentChanged.connect(onStack)

    # Available workbenches
    populateCBoxWb()
    # Default menu
    cpc.defaultGroup(baseGroup())
    # Available menus
    populateCBoxMenu()
    # Available commands
    populateCommands()
    # Enabled commands
    populateEnabled(cpc.findGroup(baseGroup(),
                                  cBoxMenu.itemData(cBoxMenu.currentIndex())))

    return w


def edit(stack):
    """Preferences for editable commands."""

    # Widgets
    w = QtGui.QWidget()
    lo = QtGui.QVBoxLayout()
    w.setLayout(lo)
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)
    scroll = QtGui.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    lo.addWidget(scroll)

    # Button edit done
    btnEditDone = QtGui.QPushButton()
    btnEditDone.setText("Done")

    # Group box for menus
    grpBoxMenu = QtGui.QGroupBox("Menu:")
    loMenu = QtGui.QVBoxLayout()
    grpBoxMenu.setLayout(loMenu)

    # Layout
    loEditDone = QtGui.QHBoxLayout()
    loEditDone.addStretch()
    loEditDone.addWidget(btnEditDone)

    layout.addWidget(grpBoxMenu)
    layout.addStretch()
    lo.insertLayout(1, loEditDone)

    # Functions and connections

    def onEditDone():
        """Switch to general preferences."""
        stack.setCurrentIndex(0)

    btnEditDone.clicked.connect(onEditDone)

    def onGrpBoxMenu():
        """Set menu on selection."""
        on = False
        for i in grpBoxMenu.findChildren(QtGui.QRadioButton):
            if i.isChecked():
                on = True
                enabled.currentItem().setData(QtCore.Qt.UserRole,
                                              i.objectName())
        if not on:
            enabled.currentItem().setData(QtCore.Qt.UserRole, "CP_Menu")
        saveEnabled()

    def updateMenuList():
        """Fill group box with available menus."""
        uid = None
        current = enabled.currentItem()
        if current:
            data = current.data(QtCore.Qt.UserRole)
        if current and data and data.startswith("CP_Menu_"):
            try:
                uid = current.data(QtCore.Qt.UserRole).split("CP_Menu_", 1)[1]
            except IndexError:
                pass
        grpBoxMenu.blockSignals(True)
        for i in grpBoxMenu.findChildren(QtGui.QRadioButton):
            i.deleteLater()
        base = baseGroup()
        index = base.GetString("index")
        if index:
            index = index.split(",")
        else:
            index = []
        for i in index:
            g = base.GetGroup(i)
            rb = QtGui.QRadioButton(grpBoxMenu)
            try:
                rb.setText(g.GetString("name").decode("UTF-8"))
            except AttributeError:
                rb.setText(g.GetString("name"))
            rb.setObjectName("CP_Menu_" + g.GetString("uuid"))
            if uid and g.GetString("uuid") == uid:
                rb.setChecked(True)
            rb.toggled.connect(onGrpBoxMenu)
            loMenu.addWidget(rb)
        grpBoxMenu.blockSignals(False)

    def onStack(n):
        """Visible widget index change."""
        if n == 1:
            btnEditDone.setDefault(True)
            btnEditDone.setFocus()
            updateMenuList()

    stack.currentChanged.connect(onStack)

    return w
