# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loopvisiblelayersdock.ui'
#
# Created: Tue Mar 13 20:44:01 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LoopVisibleLayersDock(object):
    def setupUi(self, LoopVisibleLayersDock):
        LoopVisibleLayersDock.setObjectName(_fromUtf8("LoopVisibleLayersDock"))
        LoopVisibleLayersDock.resize(305, 173)
        LoopVisibleLayersDock.setWindowTitle(QtGui.QApplication.translate("LoopVisibleLayersDock", "Loop Visible Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Select Group", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.cbxGroup = QtGui.QComboBox(self.dockWidgetContents)
        self.cbxGroup.setObjectName(_fromUtf8("cbxGroup"))
        self.gridLayout.addWidget(self.cbxGroup, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Loop Delay (sec.)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnStart = QtGui.QPushButton(self.dockWidgetContents)
        self.btnStart.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Start / Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStart.setIcon(icon)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.horizontalLayout.addWidget(self.btnStart)
        self.btnStop = QtGui.QPushButton(self.dockWidgetContents)
        self.btnStop.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStop.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon1)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.horizontalLayout.addWidget(self.btnStop)
        self.btnNext = QtGui.QPushButton(self.dockWidgetContents)
        self.btnNext.setEnabled(False)
        self.btnNext.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_fastforward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNext.setIcon(icon2)
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.horizontalLayout.addWidget(self.btnNext)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.spinDelay = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.spinDelay.setDecimals(1)
        self.spinDelay.setMinimum(0.1)
        self.spinDelay.setObjectName(_fromUtf8("spinDelay"))
        self.horizontalLayout_2.addWidget(self.spinDelay)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.btnRefresh = QtGui.QPushButton(self.dockWidgetContents)
        self.btnRefresh.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Refresh Groups", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/mActionDrawGrey.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRefresh.setIcon(icon3)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.horizontalLayout_2.addWidget(self.btnRefresh)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 2, 1, 1)
        LoopVisibleLayersDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(LoopVisibleLayersDock)
        QtCore.QMetaObject.connectSlotsByName(LoopVisibleLayersDock)

    def retranslateUi(self, LoopVisibleLayersDock):
        pass

import resources_rc
