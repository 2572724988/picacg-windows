# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rank.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Rank(object):
    def setupUi(self, Rank):
        Rank.setObjectName("Rank")
        Rank.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Rank)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Rank)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.h24Layout = QtWidgets.QGridLayout(self.tab)
        self.h24Layout.setObjectName("h24Layout")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.d7Layout = QtWidgets.QGridLayout(self.tab_3)
        self.d7Layout.setObjectName("d7Layout")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.d30Layout = QtWidgets.QGridLayout(self.tab_2)
        self.d30Layout.setObjectName("d30Layout")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Rank)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Rank)

    def retranslateUi(self, Rank):
        _translate = QtCore.QCoreApplication.translate
        Rank.setWindowTitle(_translate("Rank", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Rank", "24小时"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Rank", "7日"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Rank", "30日"))
