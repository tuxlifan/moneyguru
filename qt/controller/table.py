# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-01
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, QAbstractTableModel

class Table(QAbstractTableModel):
    HEADER = []
    ROWATTRS = []
    
    def __init__(self, doc, view):
        QAbstractTableModel.__init__(self)
        self.doc = doc
        self.view = view
        self.model = self._getModel()
        self.view.setModel(self)
    
    def _getModel(self):
        raise NotImplementedError()
    
    #--- Data Model methods
    def columnCount(self, index):
        return len(self.HEADER)
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            row = self.model[index.row()]
            rowattr = self.ROWATTRS[index.column()]
            return getattr(row, rowattr)
        return None
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        rowattr = self.ROWATTRS[index.column()]
        if self.model.can_edit_cell(rowattr, index.row()):
            flags |= Qt.ItemIsEditable
        return flags
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self.HEADER):
            return self.HEADER[section]
        return None
    
    def revert(self):
        self.model.cancel_edits()
    
    def rowCount(self, index):
        if index.isValid():
            return 0
        return len(self.model)
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            row = self.model[index.row()]
            rowattr = self.ROWATTRS[index.column()]
            value = unicode(value.toString())
            setattr(row, rowattr, value)
            return True
        return False
    
    def submit(self):
        self.model.save_edits()
        return True
    
    #--- model --> view
    def refresh(self):
        self.reset()
    
    def show_selected_row(self):
        pass
    
    def stop_editing(self):
        pass
    
