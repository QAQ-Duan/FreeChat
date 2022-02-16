from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

def msg_display():
    def __init__(self,TextBrower):
    
    def 
    TextBrower.setTextColor(Qt.green)
    self.grprecvText.ensureCursorVisible()
    cursor = self.grprecvText.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    self.grprecvText.append(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
    self.grprecvText.setTextColor(Qt.black)
    self.grprecvText.setTextCursor(cursor)
    self.grprecvText.ensureCursorVisible()