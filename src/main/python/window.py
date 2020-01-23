#!/usr/bin/env python3
import networkx as nx
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot as slot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from models import SpreadsheetTableModel


DEFAULT_COLOR = QColor('white')
INTVW_COLOR = QColor(252, 244, 228)
TMSLT_COLOR = QColor(232, 242, 241)
ERROR_COLOR = QColor(235, 195, 195)


class MainWindow(QMainWindow):
    def __init__(self, context, parent=None):
        super().__init__(parent)
        uic.loadUi(context.get_ui(), self)

        self.sheets = [SpreadsheetTableModel()]
        self.inputTableView.setModel(self.sheets[0])
        self.intvwSpinbox.setStyleSheet('background-color: %s' % INTVW_COLOR.name())
        self.tmsltSpinbox.setStyleSheet('background-color: %s' % TMSLT_COLOR.name())

    @slot()
    def openXlsx(self):
        # dialog = QFileDialog(parent=self)
        # dialog.setFileMode(QFileDialog.ExistingFile)
        # dialog.setNameFilter('Spreadsheets (*.xlsx)')
        # if not dialog.exec_():
        #     return
        # xlsx = dialog.selectedFiles()[0]
        xlsx = 'example.xlsx'
        self.loadXlsx(xlsx)

    @slot(str)
    def loadXlsx(self, xlsx):
        self.sheets[0].populate(xlsx)
        self.updateSheetRanges()
        self.statusbar.showMessage('載入 %d 列資料。' % self.sheets[0].rowCount())

    @slot()
    def computeMatching(self):
        G = nx.Graph()
        intvws = self.sheets[0].range('interviewee')
        tmslts = self.sheets[0].range('timeslot')
        for interviewee, timeslots in zip(intvws, tmslts):
            G.add_node(interviewee, bipartite=0)
            G.add_nodes_from(timeslots.split(', '), bipartite=1)
            G.add_edges_from([(interviewee, t) for t in timeslots.split(', ')])
        matches = {}
        for B in nx.connected_components(G):
            matches.update(nx.bipartite.maximum_matching(G.subgraph(B)))
        # print(matches)
        for interviewee in intvws:
            if interviewee in matches:
                print('%s -> %s' % (interviewee, matches[interviewee]))
        # left = [node[0] for node in G.nodes(data=True) if node[1]['bipartite'] == 0]
        # import matplotlib.pyplot as plt
        # nx.draw(G, pos=nx.bipartite_layout(G, left))
        # nx.draw_networkx_labels(G, pos=nx.bipartite_layout(G, left))
        # plt.show()

    @slot()
    def updateSheetRanges(self):
        rows = self.startRowSpinbox.value(), self.endRowSpinbox.value()
        cols_intvw = (self.intvwSpinbox.value(), ) * 2
        cols_tmslt = (self.tmsltSpinbox.value(), ) * 2
        self.sheets[0].setRange('interviewee', rows, cols_intvw, INTVW_COLOR)
        self.sheets[0].setRange('timeslot', rows, cols_tmslt, TMSLT_COLOR)
