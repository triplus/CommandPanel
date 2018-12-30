# License: CC BY-SA 3.0
# https://creativecommons.org/licenses/by-sa/3.0/legalcode
# Attribution:
# http://stackoverflow.com/a/34478089

"""Command panel for FreeCAD - EventFilter."""

from PySide import QtGui
from PySide import QtCore


class InstallEvent(QtCore.QObject):
    """Wheel event filter for disabled buttons."""
    def eventFilter(self, obj, event):
        """Wheel event."""
        if obj and not obj.isEnabled() and event.type() == QtCore.QEvent.Wheel:
            newEvent = QtGui.QWheelEvent(obj.mapToParent(event.pos()),
                                         event.globalPos(),
                                         event.delta(),
                                         event.buttons(),
                                         event.modifiers(),
                                         event.orientation())
            QtGui.QApplication.instance().postEvent(obj.parent(), newEvent)
            return True

        return QtCore.QObject.eventFilter(self, obj, event)
