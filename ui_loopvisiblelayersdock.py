# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loopvisiblelayersdock.ui'
#
# Created: Fri Mar 16 16:34:35 2012
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
        LoopVisibleLayersDock.resize(365, 199)
        LoopVisibleLayersDock.setWindowTitle(QtGui.QApplication.translate("LoopVisibleLayersDock", "Loop Visible Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.frame = QtGui.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.spinDelay = QtGui.QDoubleSpinBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinDelay.sizePolicy().hasHeightForWidth())
        self.spinDelay.setSizePolicy(sizePolicy)
        self.spinDelay.setDecimals(1)
        self.spinDelay.setMinimum(0.0)
        self.spinDelay.setMaximum(999.0)
        self.spinDelay.setObjectName(_fromUtf8("spinDelay"))
        self.horizontalLayout_2.addWidget(self.spinDelay)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "(sec.)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnStart = QtGui.QPushButton(self.frame)
        self.btnStart.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Start / Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStart.setIcon(icon)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.horizontalLayout.addWidget(self.btnStart)
        self.btnStop = QtGui.QPushButton(self.frame)
        self.btnStop.setEnabled(False)
        self.btnStop.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStop.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon1)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.horizontalLayout.addWidget(self.btnStop)
        self.btnBack = QtGui.QPushButton(self.frame)
        self.btnBack.setEnabled(False)
        self.btnBack.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBack.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_rewind.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBack.setIcon(icon2)
        self.btnBack.setObjectName(_fromUtf8("btnBack"))
        self.horizontalLayout.addWidget(self.btnBack)
        self.btnForward = QtGui.QPushButton(self.frame)
        self.btnForward.setEnabled(False)
        self.btnForward.setToolTip(QtGui.QApplication.translate("LoopVisibleLayersDock", "Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.btnForward.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_fastforward.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnForward.setIcon(icon3)
        self.btnForward.setObjectName(_fromUtf8("btnForward"))
        self.horizontalLayout.addWidget(self.btnForward)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Loop Delay", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        self.label.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Select Group", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.cbxGroup = QtGui.QComboBox(self.frame)
        self.cbxGroup.setObjectName(_fromUtf8("cbxGroup"))
        self.gridLayout_2.addWidget(self.cbxGroup, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.lblStatus = QtGui.QLabel(self.dockWidgetContents)
        self.lblStatus.setEnabled(True)
        self.lblStatus.setText(QtGui.QApplication.translate("LoopVisibleLayersDock", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 3, 0, 1, 1)
        LoopVisibleLayersDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(LoopVisibleLayersDock)
        QtCore.QMetaObject.connectSlotsByName(LoopVisibleLayersDock)

    def retranslateUi(self, LoopVisibleLayersDock):
        pass

import resources_rc
