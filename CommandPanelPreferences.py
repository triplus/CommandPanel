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

"""Command panel for FreeCAD - Preferences."""


import os
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore
import CommandPanelGui as cpg
import CommandPanelCommon as cpc
import CommandPanelToolbars as cpt


p = cpc.p
mw = Gui.getMainWindow()
path = os.path.dirname(__file__) + "/Resources/icons/"

cBoxWb = None
cBoxMenu = None
enabled = None
copyDomain = None
editContext = None


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
    """Current workbench base group."""
    wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
    g = p.GetGroup("User").GetGroup(wb)
    return g


def saveEnabled():
    """Save enabled on change."""
    items = []
    for index in range(enabled.count()):
        items.append(enabled.item(index).data(QtCore.Qt.UserRole))
    domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
    if domain:
        g = cpc.findGroup(domain)
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

    # Button settings
    btnSettings = QtGui.QPushButton("Settings")
    btnSettings.setToolTip("Open settings")

    def onSettings():
        """Stack widget index change."""
        stack.setCurrentIndex(2)

    btnSettings.clicked.connect(onSettings)

    # Button settings done
    btnSettingsDone = QtGui.QPushButton("Done")
    btnSettingsDone.setToolTip("Return to general preferences")

    def onBtnSettingsDone():
        """Return to general preferences."""
        btnSettings.clearFocus()
        stack.setCurrentIndex(0)
        if p.GetBool("Global", 0):
            cBoxWb.setCurrentIndex(cBoxWb.findData("GlobalPanel"))
        else:
            activeWb = Gui.activeWorkbench().__class__.__name__
            cBoxWb.setCurrentIndex(cBoxWb.findData(activeWb))

    btnSettingsDone.clicked.connect(onBtnSettingsDone)

    # Button close
    btnClose = QtGui.QPushButton("Close")
    btnClose.setToolTip("Close the preferences dialog")
    btnClose.clicked.connect(onAccepted)

    stack.insertWidget(0, general(dia, stack, btnClose, btnSettings))
    stack.insertWidget(1, edit(stack))
    stack.insertWidget(2, settings(stack, btnSettingsDone))

    btnClose.setDefault(True)
    btnClose.setFocus()

    return dia


def general(dia, stack, btnClose, btnSettings):
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
    btnResetWb.setIcon(QtGui.QIcon(path + "CommandPanelReset.svg"))

    # Checkbox default menu
    ckDefault = QtGui.QCheckBox()
    ckDefault.setToolTip("Set menu as default workbench menu")

    # Button add workbench menu
    btnAddWbMenu = QtGui.QPushButton()
    btnAddWbMenu.setToolTip("Add new workbench menu")
    btnAddWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelAdd.svg"))

    # Button remove workbench menu
    btnRemoveWbMenu = QtGui.QPushButton()
    btnRemoveWbMenu.setToolTip("Remove selected workbench menu")
    btnRemoveWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelRemove.svg"))

    # Button copy workbench menu
    btnCopyWbMenu = QtGui.QPushButton()
    btnCopyWbMenu.setToolTip("Copy existing workbench menu")
    btnCopyWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelCopy.svg"))

    # Button rename workbench menu
    btnRenameWbMenu = QtGui.QPushButton()
    btnRenameWbMenu.setToolTip("Rename selected workbench menu")
    btnRenameWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelRename.svg"))

    # Button add command
    btnAddCommand = QtGui.QPushButton()
    btnAddCommand.setToolTip("Add selected command")
    btnAddCommand.setIcon(QtGui.QIcon(path + "CommandPanelAddCommand.svg"))

    # Button remove command
    btnRemoveCommand = QtGui.QPushButton()
    btnRemoveCommand.setToolTip("Remove selected command")
    btnRemoveCommand.setIcon(QtGui.QIcon(path +
                                         "CommandPanelRemoveCommand.svg"))

    # Button move up
    btnMoveUp = QtGui.QPushButton()
    btnMoveUp.setToolTip("Move selected command up")
    btnMoveUp.setIcon(QtGui.QIcon(path + "CommandPanelUp.svg"))

    # Button move down
    btnMoveDown = QtGui.QPushButton()
    btnMoveDown.setToolTip("Move selected command down")
    btnMoveDown.setIcon(QtGui.QIcon(path + "CommandPanelDown.svg"))

    # Button add separator
    btnAddSeparator = QtGui.QPushButton()
    btnAddSeparator.setToolTip("Add separator")
    btnAddSeparator.setIcon(QtGui.QIcon(path +
                                        "CommandPanelAddSeparator.svg"))

    # Button add spacer
    btnAddSpacer = QtGui.QPushButton()
    btnAddSpacer.setToolTip("Add spacer")
    btnAddSpacer.setIcon(QtGui.QIcon(path + "CommandPanelAddSpacer.svg"))

    # Button add menu
    btnAddMenu = QtGui.QPushButton()
    btnAddMenu.setToolTip("Add menu")
    btnAddMenu.setIcon(QtGui.QIcon(path + "CommandPanelAddMenu.svg"))

    # Button edit menu
    btnEditMenu = QtGui.QPushButton()
    btnEditMenu.setEnabled(False)
    btnEditMenu.setToolTip("Edit menu")
    btnEditMenu.setIcon(QtGui.QIcon(path + "CommandPanelEditMenu.svg"))

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
    loCBoxMenu.addWidget(btnRenameWbMenu)
    loCBoxMenu.addWidget(btnCopyWbMenu)

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
    loBottom.addWidget(btnSettings)
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
        cBoxWb.insertSeparator(0)
        cBoxWb.insertItem(0,
                          QtGui.QIcon(":/icons/freecad"),
                          "Global panel",
                          "GlobalPanel")
        if p.GetBool("Global", 0):
            cBoxWb.setCurrentIndex(cBoxWb.findData("GlobalPanel"))
        else:
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
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    cBoxWb.currentIndexChanged.connect(onCBoxWb)

    def populateCBoxMenu():
        """Workbench menu combo box."""
        base = baseGroup()
        index = cpc.splitIndex(base)
        ckDefault.blockSignals(True)
        cBoxMenu.blockSignals(True)
        cBoxMenu.clear()
        for i in index:
            name = base.GetGroup(i).GetString("name")
            uid = base.GetGroup(i).GetString("uuid")
            wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
            domain = "CPMenu" + "." + "User" + "." + wb + "." + uid
            try:
                cBoxMenu.insertItem(0, name.decode("UTF-8"), domain)
            except AttributeError:
                cBoxMenu.insertItem(0, name, domain)
        default = base.GetString("default")
        data = cBoxMenu.findData(default)
        cBoxMenu.setCurrentIndex(data)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            cBoxMenu.setCurrentIndex(0)
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        cBoxMenu.blockSignals(False)

    def onCBoxMenu():
        """Load workbench menu data."""
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())

        ckDefault.blockSignals(True)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    cBoxMenu.currentIndexChanged.connect(onCBoxMenu)

    def onBtnResetWb():
        """Reset workbench to defaults."""
        base = baseGroup()
        base.Clear()
        cpc.defaultGroup(base)
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            populateEnabled(cpc.findGroup(domain))
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
            wb = cBoxWb.itemData(cBoxWb.currentIndex())
            domain = "CPMenu" + "." + "User" + "." + wb
            g = cpc.newGroup(domain)
            if g:
                uid = g.GetString("uuid")
                domain = domain + "." + uid
                try:
                    g.SetString("name", text.encode("UTF-8"))
                except TypeError:
                    g.SetString("name", text)
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(domain))
                populateEnabled(g)
        d.deleteLater()
        btnClose.setFocus()

    btnAddWbMenu.clicked.connect(onBtnAddWbMenu)

    def onBtnRemoveWbMenu():
        """Remove selected workbench menu."""
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            cpc.deleteGroup(domain)
        cpc.defaultGroup(base)
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    btnRemoveWbMenu.clicked.connect(onBtnRemoveWbMenu)

    def onBtnRenameWbMenu():
        """Rename existing workbench menu."""
        d = QtGui.QInputDialog(dia)
        d.setModal(True)
        d.setInputMode(QtGui.QInputDialog.InputMode.TextInput)
        text, ok = QtGui.QInputDialog.getText(dia,
                                              "Rename menu",
                                              "Please insert new menu name.")
        if ok:
            domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
            g = cpc.findGroup(domain)
            if g:
                try:
                    g.SetString("name", text.encode("UTF-8"))
                except TypeError:
                    g.SetString("name", text)
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(domain))
                populateEnabled(g)

        d.deleteLater()
        btnClose.setFocus()

    btnRenameWbMenu.clicked.connect(onBtnRenameWbMenu)

    def onCKDefault(checked):
        """Set the checkbox state."""
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if checked:
            base.SetString("default", domain)
        else:
            base.RemString("default")
        cpg.onWorkbench()

    ckDefault.stateChanged.connect(onCKDefault)

    def isDefaultMenu():
        """Check if current menu is the default menu."""
        default = False
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain and base.GetString("default") == domain:
            default = True
        return default

    def populateEnabled(group):
        """Populate enabled commands panel."""
        if group:
            items = group.GetString("commands")
        else:
            items = []
        if items:
            items = items.split(",")
        else:
            items = []
        actions = cpc.actionList()
        enabled.blockSignals(True)
        enabled.clear()
        for i in items:
            item = QtGui.QListWidgetItem(enabled)
            if i == "CPSeparator":
                item.setText("Separator")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path +
                                         "CommandPanelAddSeparator.svg"))
            elif i == "CPSpacer":
                item.setText("Spacer")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path + "CommandPanelAddSpacer.svg"))
            elif i.startswith("CPMenu"):
                g = cpc.findGroup(i)
                if g:
                    try:
                        text = g.GetString("name").decode("UTF-8")
                    except AttributeError:
                        text = g.GetString("name")
                    item.setText("Menu: " + text)
                else:
                    item.setText("Menu")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path + "CommandPanelAddMenu.svg"))
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
        item.setData(QtCore.Qt.UserRole, "CPSeparator")
        item.setIcon(QtGui.QIcon(path + "CommandPanelAddSeparator.svg"))
        saveEnabled()

    btnAddSeparator.clicked.connect(onBtnAddSeparator)

    def onBtnAddSpacer():
        """Add spacer."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Spacer")
        item.setData(QtCore.Qt.UserRole, "CPSpacer")
        item.setIcon(QtGui.QIcon(path + "CommandPanelAddSpacer.svg"))
        saveEnabled()

    btnAddSpacer.clicked.connect(onBtnAddSpacer)

    def onBtnAddMenu():
        """Add menu."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Menu")
        item.setData(QtCore.Qt.UserRole, "CPMenu")
        item.setIcon(QtGui.QIcon(path + "CommandPanelAddMenu.svg"))
        saveEnabled()
        onSelectionChanged()

    btnAddMenu.clicked.connect(onBtnAddMenu)

    def onSelectionChanged():
        """Set enabled state for widgets on selection changed."""
        current = enabled.currentItem()
        if current:
            data = current.data(QtCore.Qt.UserRole)
        if current and data and data.startswith("CPMenu"):
            btnEditMenu.setEnabled(True)
            btnEditMenu.setFocus()
        else:
            btnEditMenu.setEnabled(False)

    enabled.itemSelectionChanged.connect(onSelectionChanged)

    def onEditMenu():
        """Open edit dialog for selected menu ."""
        current = enabled.currentItem()
        if current and current.data(QtCore.Qt.UserRole).startswith("CPMenu"):
            global editContext
            editContext = "Set"
            stack.setCurrentIndex(1)

    btnEditMenu.clicked.connect(onEditMenu)
    enabled.itemDoubleClicked.connect(onEditMenu)

    def onCopyWbMenu():
        """Open copy menu dialog."""
        global editContext
        editContext = "Copy"
        stack.setCurrentIndex(1)

    btnCopyWbMenu.clicked.connect(onCopyWbMenu)

    def onStack(n):
        """Stack widget index change."""
        global copyDomain
        if n == 0:
            row = enabled.currentRow()
            domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
            if domain:
                populateEnabled(cpc.findGroup(domain))
            enabled.setCurrentRow(row)
            btnClose.setDefault(True)
            if copyDomain:
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(copyDomain))
                domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
                populateEnabled(cpc.findGroup(domain))
                copyDomain = None
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
    populateEnabled(cpc.findGroup(cBoxMenu.itemData(cBoxMenu.currentIndex())))

    return w


def edit(stack):
    """Preferences for editable commands."""

    items = []

    # Widgets
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)

    tree = QtGui.QTreeWidget()
    if editContext == "Copy":
        tree.setHeaderLabel("Copy menu: None")
    else:
        tree.setHeaderLabel("Set menu: None")

    # Button edit done
    btnEditDone = QtGui.QPushButton()
    btnEditDone.setText("Done")
    btnEditDone.setToolTip("Return to general preferences")

    # Layout button edit done
    loBtnEditDone = QtGui.QHBoxLayout()
    loBtnEditDone.addStretch()
    loBtnEditDone.addWidget(btnEditDone)

    layout.addWidget(tree)
    layout.insertLayout(1, loBtnEditDone)

    # Functions and connections

    def updateTree():
        """Update tree widget and add available menus."""
        tree.blockSignals = True
        wb = Gui.listWorkbenches()
        currentWb = cBoxWb.itemData(cBoxWb.currentIndex())

        wbSort = list(wb)
        wbSort.sort()
        if currentWb in wbSort:
            wbSort.remove(currentWb)

        def treeItems(currentWb=None,
                      mt=None,
                      cn=None,
                      expanded=False,
                      itemTop=None):
            """Create tree widget items."""
            if currentWb:
                try:
                    icon = cpc.wbIcon(wb[currentWb].Icon)
                except AttributeError:
                    icon = QtGui.QIcon(":/icons/freecad")
            else:
                icon = QtGui.QIcon(":/icons/freecad")

            if not mt:
                mt = wb[currentWb].MenuText
            if not cn:
                cn = wb[currentWb].__class__.__name__

            if itemTop:
                item = QtGui.QTreeWidgetItem(itemTop)
            else:
                item = QtGui.QTreeWidgetItem(tree)

            if cn != "GlobalPanel":
                item.setIcon(0, icon)

            try:
                item.setText(0, mt.decode("UTF-8"))
            except AttributeError:
                item.setText(0, mt)

            item.setExpanded(expanded)

            source = ["User", "System"]
            for s in source:
                itemSource = QtGui.QTreeWidgetItem(item)
                itemSource.setText(0, s)
                itemSource.setExpanded(expanded)

                base = p.GetGroup(s).GetGroup(cn)
                index = cpc.splitIndex(base)
                for i in index:
                    g = base.GetGroup(i)
                    uid = g.GetString("uuid")
                    domain = "CPMenu" + "." + s + "." + cn + "." + uid
                    itemMenu = QtGui.QTreeWidgetItem(itemSource)
                    name = g.GetString("name")
                    try:
                        itemMenu.setText(0, name.decode("UTF-8"))
                    except AttributeError:
                        itemMenu.setText(0, name)
                    itemMenu.setCheckState(0, QtCore.Qt.Unchecked)
                    itemMenu.setData(0, QtCore.Qt.UserRole, domain)
                    items.append(itemMenu)

                if itemSource.childCount() == 0:
                    item.removeChild(itemSource)

        # Current workbench
        if currentWb != "GlobalPanel":
            treeItems(currentWb, None, None, True, None)
        else:
            treeItems(None, "Global", "GlobalPanel", True, None)

        # Other workbenches
        item = QtGui.QTreeWidgetItem(tree)
        item.setText(0, "Workbenches")
        for i in wbSort:
            treeItems(i, None, None, False, item)

        # Remove empty
        for i in reversed(range(item.childCount())):
            if item.child(i).childCount() == 0:
                item.removeChild(item.child(i))

        # Global menus
        if currentWb != "GlobalPanel":
            treeItems(None, "Global", "GlobalPanel", False, None)

        # Toolbars (for copy mode only)
        if editContext == "Copy":
            tree.setHeaderLabel("Copy: None")
            itemsToolbar = QtGui.QTreeWidgetItem(tree)
            itemsToolbar.setText(0, "Toolbars")
            tb = []
            for i in mw.findChildren(QtGui.QToolBar):
                if i.objectName():
                    tb.append(i.objectName())
            tb.sort()
            for name in tb:
                domain = "CPMenu" + "." + "Toolbar" + "." + name
                itemTb = QtGui.QTreeWidgetItem(itemsToolbar)
                itemTb.setText(0, name)
                itemTb.setCheckState(0, QtCore.Qt.Unchecked)
                itemTb.setData(0, QtCore.Qt.UserRole, domain)
                items.append(itemTb)

        # Current (for set mode only)
        if editContext == "Set":
            current = enabled.currentItem()
            if current and (current.data(QtCore.Qt.UserRole)
                            .startswith("CPMenu")):
                data = current.data(QtCore.Qt.UserRole)
                for i in items:
                    if i.data(0, QtCore.Qt.UserRole) == data:
                        i.setCheckState(0, QtCore.Qt.Checked)
                        text = i.text(0)
                        tree.setHeaderLabel("Set menu: " + text)

                        parent = i.parent()
                        while parent:
                            parent.setExpanded(True)
                            parent = parent.parent()

        tree.blockSignals = False

    def onChecked(item):
        """Copy or set menu."""
        global copyDomain
        tree.blockSignals = True
        if item.checkState(0) == QtCore.Qt.Checked:
            for i in items:
                if i.checkState(0) == QtCore.Qt.Checked and i is not item:
                    i.setCheckState(0, QtCore.Qt.Unchecked)
            data = item.data(0, QtCore.Qt.UserRole)
        else:
            data = None

        text = item.text(0)

        if editContext == "Set" and data:
            tree.setHeaderLabel("Set menu: " + text)
            enabled.currentItem().setData(QtCore.Qt.UserRole,
                                          item.data(0, QtCore.Qt.UserRole))
            saveEnabled()
        elif editContext == "Set" and not data:
            tree.setHeaderLabel("Set menu: None")
            enabled.currentItem().setData(QtCore.Qt.UserRole, "CPMenu")
            saveEnabled()
        elif editContext == "Copy" and data:
            tree.setHeaderLabel("Copy: " + text)
            copyDomain = data
        elif editContext == "Copy" and not data:
            tree.setHeaderLabel("Copy: None")
            copyDomain = None
        else:
            pass
        tree.blockSignals = False

    def onEditDone():
        """Switch to general preferences."""
        global copyDomain
        tree.itemChanged.disconnect(onChecked)
        del items[:]
        tree.clear()

        if copyDomain:
            wb = cBoxWb.itemData(cBoxWb.currentIndex())
            domain = "CPMenu" + "." + "User" + "." + wb
            if copyDomain.startswith("CPMenu.Toolbar"):
                name = copyDomain.split(".")[2]
                grpCopy = cpc.newGroup(domain)
                uid = grpCopy.GetString("uuid")
                copyDomain = domain + "." + uid
                grpCopy.SetString("name", name)
                grpCopy.SetString("commands",
                                  ",".join(cpt.toolbarCommands(name)))
            else:
                grpOrigin = cpc.findGroup(copyDomain)
                grpCopy = cpc.newGroup(domain)
                uid = grpCopy.GetString("uuid")
                domain = domain + "." + uid
                if grpOrigin and grpCopy:
                    grpCopy.SetString("name", grpOrigin.GetString("name"))
                    grpCopy.SetString("commands",
                                      grpOrigin.GetString("commands"))
                    copyDomain = domain
                else:
                    copyDomain = None

        stack.setCurrentIndex(0)

    btnEditDone.clicked.connect(onEditDone)

    def onStack(n):
        """Stack widget index change."""
        if n == 1:
            btnEditDone.setDefault(True)
            btnEditDone.setFocus()
            updateTree()
            tree.itemChanged.connect(onChecked)

    stack.currentChanged.connect(onStack)

    return widget


def settings(stack, btnSettingsDone):
    """Settings widget for preferences."""

    # Widgets
    widgetSettings = QtGui.QWidget()
    layoutMain = QtGui.QVBoxLayout()
    widgetSettings.setLayout(layoutMain)
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)
    scroll = QtGui.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    layoutMain.addWidget(scroll)

    # Mode
    grpBoxMode = QtGui.QGroupBox("Mode:")
    loMode = QtGui.QVBoxLayout()
    grpBoxMode.setLayout(loMode)

    # Global panel mode
    loGlobal = QtGui.QHBoxLayout()
    lblGlobal = QtGui.QLabel("Global panel")
    ckBoxGlobal = QtGui.QCheckBox()
    ckBoxGlobal.setToolTip("Enable global panel mode")

    loGlobal.addWidget(lblGlobal)
    loGlobal.addStretch()
    loGlobal.addWidget(ckBoxGlobal)
    loMode.insertLayout(0, loGlobal)

    if p.GetBool("Global", 0):
        ckBoxGlobal.setChecked(True)

    def onCkBoxGlobal(checked):
        """Set global panel mode."""
        if checked:
            p.SetBool("Global", 1)
        else:
            p.SetBool("Global", 0)

        cpg.onWorkbench()

    ckBoxGlobal.stateChanged.connect(onCkBoxGlobal)

    # Layout (buttons)
    loLayout = QtGui.QVBoxLayout()
    grpBoxLayout = QtGui.QGroupBox("Layout:")
    grpBoxLayout.setLayout(loLayout)

    rLoFlow = QtGui.QRadioButton("Flow", grpBoxLayout)
    rLoFlow.setObjectName("Flow")
    rLoFlow.setToolTip("Layout buttons based on the available width")
    rLoGrid = QtGui.QRadioButton("Grid", grpBoxLayout)
    rLoGrid.setObjectName("Grid")
    rLoGrid.setToolTip("Layout buttons in a grid")
    loLayout.addWidget(rLoFlow)

    columnSpin = QtGui.QSpinBox()
    columnSpin.setRange(1, 10000)
    columnSpin.setValue(p.GetInt("ColumnNumber", 1))

    loGrid = QtGui.QHBoxLayout()
    loGrid.addWidget(rLoGrid)
    loGrid.addStretch()
    loGrid.addWidget(columnSpin)

    loLayout.insertLayout(1, loGrid)

    loType = p.GetString("Layout")
    if loType == "Grid":
        rLoGrid.setChecked(True)
    else:
        rLoFlow.setChecked(True)

    def onGrpBoxLayout(checked):
        """Set the layout type."""
        if checked:
            for i in grpBoxLayout.findChildren(QtGui.QRadioButton):
                if i.isChecked():
                    p.SetString("Layout", i.objectName())

            cpg.setLayout()
            cpg.onWorkbench()

    rLoFlow.toggled.connect(onGrpBoxLayout)
    rLoGrid.toggled.connect(onGrpBoxLayout)

    def onColumnSpin(n):
        """Set number of columns."""
        p.SetInt("ColumnNumber", n)
        cpg.onWorkbench()

    columnSpin.valueChanged.connect(onColumnSpin)

    # Style
    loStyle = QtGui.QVBoxLayout()
    grpBoxStyle = QtGui.QGroupBox("Style:")
    grpBoxStyle.setLayout(loStyle)
    rBtnIcon = QtGui.QRadioButton("Icon", grpBoxStyle)
    rBtnIcon.setObjectName("Icon")
    rBtnIcon.setToolTip("Buttons with icon only")
    rBtnText = QtGui.QRadioButton("Text", grpBoxStyle)
    rBtnText.setObjectName("Text")
    rBtnText.setToolTip("Buttons with text only")
    rBtnIconText = QtGui.QRadioButton("Icon and text", grpBoxStyle)
    rBtnIconText.setObjectName("IconText")
    rBtnIconText.setToolTip("Buttons with icon and text")
    rBtnTextBelow = QtGui.QRadioButton("Text below the icon", grpBoxStyle)
    rBtnTextBelow.setObjectName("TextBelow")
    rBtnTextBelow.setToolTip("Buttons with icon and text below the icon")
    loStyle.addWidget(rBtnIcon)
    loStyle.addWidget(rBtnText)
    loStyle.addWidget(rBtnIconText)
    loStyle.addWidget(rBtnTextBelow)

    btnStyle = p.GetString("Style")

    if btnStyle == "Text":
        rBtnText.setChecked(True)
    elif btnStyle == "IconText":
        rBtnIconText.setChecked(True)
    elif btnStyle == "TextBelow":
        rBtnTextBelow.setChecked(True)
    else:
        rBtnIcon.setChecked(True)

    def onGrpBoxStyle(checked):
        """Set button style."""
        if checked:
            for i in grpBoxStyle.findChildren(QtGui.QRadioButton):
                if i.isChecked():
                    p.SetString("Style", i.objectName())

            cpg.onWorkbench()

    rBtnIcon.toggled.connect(onGrpBoxStyle)
    rBtnText.toggled.connect(onGrpBoxStyle)
    rBtnIconText.toggled.connect(onGrpBoxStyle)
    rBtnTextBelow.toggled.connect(onGrpBoxStyle)

    ckBoxBtnRaise = QtGui.QCheckBox()
    ckBoxBtnRaise.setText("Auto raise")
    loStyle.addWidget(ckBoxBtnRaise)

    if p.GetBool("AutoRaise", 1):
        ckBoxBtnRaise.setChecked(True)

    def onCkBoxBtnRaise(checked):
        """Set button auto raise."""
        if checked:
            p.SetBool("AutoRaise", 1)
        else:
            p.SetBool("AutoRaise", 0)

        cpg.onWorkbench()

    ckBoxBtnRaise.stateChanged.connect(onCkBoxBtnRaise)

    # Size
    loSize = QtGui.QVBoxLayout()
    grpBoxSize = QtGui.QGroupBox("Size:")
    grpBoxSize.setLayout(loSize)

    ckBoxIconSize = QtGui.QCheckBox()
    ckBoxIconSize.setText("Icon")
    iconSpin = QtGui.QSpinBox()
    iconSpin.setEnabled(False)
    iconSpin.setRange(1, 10000)
    iconSpin.setValue(p.GetInt("IconSize", 16))

    loIcon = QtGui.QHBoxLayout()
    loIcon.addWidget(ckBoxIconSize)
    loIcon.addStretch()
    loIcon.addWidget(iconSpin)

    ckBoxTxtSize = QtGui.QCheckBox()
    ckBoxTxtSize.setText("Text")
    txtSpin = QtGui.QSpinBox()
    txtSpin.setEnabled(False)
    txtSpin.setRange(1, 10000)
    txtSpin.setValue(p.GetInt("TextSize", 8))

    loText = QtGui.QHBoxLayout()
    loText.addWidget(ckBoxTxtSize)
    loText.addStretch()
    loText.addWidget(txtSpin)

    ckBoxBtnWidth = QtGui.QCheckBox()
    ckBoxBtnWidth.setText("Button width")
    btnWidthSpin = QtGui.QSpinBox()
    btnWidthSpin.setEnabled(False)
    btnWidthSpin.setRange(1, 10000)
    btnWidthSpin.setValue(p.GetInt("ButtonWidth", 30))

    loBtnWidth = QtGui.QHBoxLayout()
    loBtnWidth.addWidget(ckBoxBtnWidth)
    loBtnWidth.addStretch()
    loBtnWidth.addWidget(btnWidthSpin)

    ckBoxBtnHeight = QtGui.QCheckBox()
    ckBoxBtnHeight.setText("Button height")
    btnHeightSpin = QtGui.QSpinBox()
    btnHeightSpin.setEnabled(False)
    btnHeightSpin.setRange(1, 10000)
    btnHeightSpin.setValue(p.GetInt("ButtonHeight", 30))

    loBtnHeight = QtGui.QHBoxLayout()
    loBtnHeight.addWidget(ckBoxBtnHeight)
    loBtnHeight.addStretch()
    loBtnHeight.addWidget(btnHeightSpin)

    ckBoxBtnSpacing = QtGui.QCheckBox()
    ckBoxBtnSpacing.setText("Spacing")
    btnSpacingSpin = QtGui.QSpinBox()
    btnSpacingSpin.setEnabled(False)
    btnSpacingSpin.setRange(1, 10000)
    btnSpacingSpin.setValue(p.GetInt("ButtonSpacing", 5))

    loBtnSpacing = QtGui.QHBoxLayout()
    loBtnSpacing.addWidget(ckBoxBtnSpacing)
    loBtnSpacing.addStretch()
    loBtnSpacing.addWidget(btnSpacingSpin)

    loSize.insertLayout(0, loIcon)
    loSize.insertLayout(1, loText)
    loSize.insertLayout(2, loBtnWidth)
    loSize.insertLayout(3, loBtnHeight)
    loSize.insertLayout(4, loBtnSpacing)

    if p.GetBool("EnableIconSize", 0):
        ckBoxIconSize.setChecked(True)
        iconSpin.setEnabled(True)

    if p.GetBool("EnableFontSize", 0):
        ckBoxTxtSize.setChecked(True)
        txtSpin.setEnabled(True)

    if p.GetBool("EnableButtonWidth", 0):
        ckBoxBtnWidth.setChecked(True)
        btnWidthSpin.setEnabled(True)

    if p.GetBool("EnableButtonHeight", 0):
        ckBoxBtnHeight.setChecked(True)
        btnHeightSpin.setEnabled(True)

    if p.GetBool("EnableButtonSpacing", 0):
        ckBoxBtnSpacing.setChecked(True)
        btnSpacingSpin.setEnabled(True)

    def onCkBoxIconSize(checked):
        """Enable icon size setting."""
        if checked:
            p.SetBool("EnableIconSize", 1)
            iconSpin.setEnabled(True)
            p.SetInt("IconSize", iconSpin.value())
        else:
            p.SetBool("EnableIconSize", 0)
            iconSpin.setEnabled(False)

        cpg.onWorkbench()

    ckBoxIconSize.stateChanged.connect(onCkBoxIconSize)

    def onIconSize(n):
        """Set button icon size."""
        p.SetInt("IconSize", n)
        cpg.onWorkbench()

    iconSpin.valueChanged.connect(onIconSize)

    def onCkBoxTxtSize(checked):
        """Enable font size setting."""
        if checked:
            p.SetBool("EnableFontSize", 1)
            txtSpin.setEnabled(True)
            p.SetInt("FontSize", txtSpin.value())
        else:
            p.SetBool("EnableFontSize", 0)
            txtSpin.setEnabled(False)

        cpg.onWorkbench()

    ckBoxTxtSize.stateChanged.connect(onCkBoxTxtSize)

    def onTxtSize(n):
        """Set button font size."""
        p.SetInt("FontSize", n)
        cpg.onWorkbench()

    txtSpin.valueChanged.connect(onTxtSize)

    def onCkBoxBtnWidth(checked):
        """Enable button width size setting."""
        if checked:
            p.SetBool("EnableButtonWidth", 1)
            btnWidthSpin.setEnabled(True)
            p.SetInt("ButtonWidth", btnWidthSpin.value())
        else:
            p.SetBool("EnableButtonWidth", 0)
            btnWidthSpin.setEnabled(False)

        cpg.onWorkbench()

    ckBoxBtnWidth.stateChanged.connect(onCkBoxBtnWidth)

    def onButtonWidth(n):
        """Set button width size."""
        p.SetInt("ButtonWidth", n)
        cpg.onWorkbench()

    btnWidthSpin.valueChanged.connect(onButtonWidth)

    def onCkBoxBtnHeight(checked):
        """Enable button height size setting."""
        if checked:
            p.SetBool("EnableButtonHeight", 1)
            btnHeightSpin.setEnabled(True)
            p.SetInt("ButtonHeight", btnHeightSpin.value())
        else:
            p.SetBool("EnableButtonHeight", 0)
            btnHeightSpin.setEnabled(False)

        cpg.onWorkbench()

    ckBoxBtnHeight.stateChanged.connect(onCkBoxBtnHeight)

    def onButtonHeight(n):
        """Set button height size."""
        p.SetInt("ButtonHeight", n)
        cpg.onWorkbench()

    btnHeightSpin.valueChanged.connect(onButtonHeight)

    def onCkBoxBtnSpacing(checked):
        """Enable buttons spacing setting."""
        if checked:
            p.SetBool("EnableButtonSpacing", 1)
            btnSpacingSpin.setEnabled(True)
            p.SetInt("ButtonSpacing", btnSpacingSpin.value())
        else:
            p.SetBool("EnableButtonSpacing", 0)
            btnSpacingSpin.setEnabled(False)

        cpg.onWorkbench()

    ckBoxBtnSpacing.stateChanged.connect(onCkBoxBtnSpacing)

    def onButtonSpacing(n):
        """Set buttons spacing value."""
        p.SetInt("ButtonSpacing", n)
        cpg.onWorkbench()

    btnSpacingSpin.valueChanged.connect(onButtonSpacing)

    # Invokable menu
    grpBoxMenu = QtGui.QGroupBox("Menu:")
    loInvokeMenu = QtGui.QVBoxLayout()
    grpBoxMenu.setLayout(loInvokeMenu)

    loMenuEnable = QtGui.QHBoxLayout()
    lblMenuEnable = QtGui.QLabel("Enable")
    ckBoxMenuEnable = QtGui.QCheckBox()
    ckBoxMenuEnable.setToolTip("Enable invokable menu")

    loMenuEnable.addWidget(lblMenuEnable)
    loMenuEnable.addStretch()
    loMenuEnable.addWidget(ckBoxMenuEnable)

    lblShortcut = QtGui.QLabel()
    lblShortcut.setText("Shortcut")
    lblShortcutKey = QtGui.QLabel()

    a = mw.findChild(QtGui.QAction, "InvokeCommandPanel")
    if a:
        lblShortcutKey.setText(a.shortcut().toString())
    else:
        lblShortcutKey.setText("Not set.")

    loShortcut = QtGui.QHBoxLayout()
    loShortcut.addWidget(lblShortcut)
    loShortcut.addStretch()
    loShortcut.addWidget(lblShortcutKey)

    lblMenuWidth = QtGui.QLabel()
    lblMenuWidth.setText("Menu width")
    menuWidthSpin = QtGui.QSpinBox()
    menuWidthSpin.setEnabled(False)
    menuWidthSpin.setRange(1, 10000)
    menuWidthSpin.setValue(p.GetInt("MenuWidth", 300))

    loMenuWidth = QtGui.QHBoxLayout()
    loMenuWidth.addWidget(lblMenuWidth)
    loMenuWidth.addStretch()
    loMenuWidth.addWidget(menuWidthSpin)

    lblMenuHeight = QtGui.QLabel()
    lblMenuHeight.setText("Menu height")
    menuHeightSpin = QtGui.QSpinBox()
    menuHeightSpin.setEnabled(False)
    menuHeightSpin.setRange(1, 10000)
    menuHeightSpin.setValue(p.GetInt("MenuHeight", 300))

    loMenuHeight = QtGui.QHBoxLayout()
    loMenuHeight.addWidget(lblMenuHeight)
    loMenuHeight.addStretch()
    loMenuHeight.addWidget(menuHeightSpin)

    if p.GetBool("Menu", 0):
        ckBoxMenuEnable.setChecked(True)
        menuWidthSpin.setEnabled(True)
        menuHeightSpin.setEnabled(True)

    def onCkBoxMenuEnable(checked):
        """Set invokable menu mode."""
        if checked:
            p.SetBool("Menu", 1)
            menuWidthSpin.setEnabled(True)
            menuHeightSpin.setEnabled(True)
        else:
            p.SetBool("Menu", 0)
            menuWidthSpin.setEnabled(False)
            menuHeightSpin.setEnabled(False)

        cpg.setContainer()

    ckBoxMenuEnable.stateChanged.connect(onCkBoxMenuEnable)

    def onMenuWidth(n):
        """Set the menu width."""
        p.SetInt("MenuWidth", n)

    menuWidthSpin.valueChanged.connect(onMenuWidth)

    def onMenuHeight(n):
        """Set the menu height."""
        p.SetInt("MenuHeight", n)

    menuHeightSpin.valueChanged.connect(onMenuHeight)

    loInvokeMenu.insertLayout(0, loMenuEnable)
    loInvokeMenu.insertLayout(1, loShortcut)
    loInvokeMenu.insertLayout(2, loMenuWidth)
    loInvokeMenu.insertLayout(3, loMenuHeight)

    loBtnSettings = QtGui.QHBoxLayout()
    loBtnSettings.addStretch()
    loBtnSettings.addWidget(btnSettingsDone)

    # Layout
    layout.addWidget(grpBoxMode)
    layout.addWidget(grpBoxLayout)
    layout.addWidget(grpBoxStyle)
    layout.addWidget(grpBoxSize)
    layout.addWidget(grpBoxMenu)
    layout.addStretch()
    layoutMain.insertLayout(1, loBtnSettings)

    def onStack(n):
        """Stack widget index change."""
        if n == 2:
            btnSettingsDone.setDefault(True)
            btnSettingsDone.setFocus()

    stack.currentChanged.connect(onStack)

    return widgetSettings
