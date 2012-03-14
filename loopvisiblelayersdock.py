"""
/***************************************************************************
 LoopVisibleLayersDock
                                 A QGIS plugin
 Loop Visible Layers Plugin
                             -------------------
        begin                : 2012-03-12
        copyright            : (C) 2012 by Etienne Tourigny
        email                : etourigny.dev@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4 import QtGui
#from PyQt4.QtGui import *
from PyQt4.QtGui import QIcon, QPixmap
from qgis.core import *
from qgis.gui import *

import pprint

from ui_loopvisiblelayersdock import Ui_LoopVisibleLayersDock

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# create the dock
class LoopVisibleLayersDock(QtGui.QDockWidget):
    def __init__(self, parent, iface):
        QtGui.QDockWidget.__init__(self, parent)
        # Set up the user interface from Designer.
        self.ui = Ui_LoopVisibleLayersDock()
        self.ui.setupUi(self)

        # Save reference to the QGIS interface
        self.iface = iface

        # variables
        self.groups = list()
        self.groupRels = list()
        self.bakLayerId = list()
        self.bakGroupName = list()
        self.bakGroupId = list()
        self.count = 0
        self.location = Qt.LeftDockWidgetArea

        # objects
        self.timer = QTimer(self)       
        QObject.connect(self.timer, SIGNAL("timeout()"), self.actionNext)
        self.state='stop'
        self.iconStart = QIcon()
        self.iconStart.addPixmap(QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_play.png")), QIcon.Normal, QIcon.Off)
        self.iconPause = QIcon()
        self.iconPause.addPixmap(QPixmap(_fromUtf8(":/plugins/loopvisiblelayers/icons/control_pause.png")), QIcon.Normal, QIcon.Off)
        self.loopCursor = QtGui.QCursor(QtGui.QPixmap(_fromUtf8(':/plugins/loopvisiblelayers/icons/icon_small.png')))

        QObject.connect( iface.legendInterface(), SIGNAL( "groupIndexChanged ( int, int )" ), self.groupsChanged )
        #QObject.connect(self, SIGNAL( "closed(PyQt_PyObject)" ), self.actionClose)
        self.connect(self, SIGNAL("dockLocationChanged(Qt::DockWidgetArea)"), self.setLocation)
        self.connect(self, SIGNAL("topLevelChanged(bool)"), self.resizeMin)

        QObject.connect(self.ui.btnStart, SIGNAL("clicked()"), self.actionStartPause)
        QObject.connect(self.ui.btnNext, SIGNAL("clicked()"), self.actionNext)
        QObject.connect(self.ui.btnStop, SIGNAL("clicked()"), self.actionStop)
        QObject.connect( self.ui.btnRefresh, SIGNAL( "clicked()" ), self.groupsChanged )

        self.groupsChanged()

        #get timer delay - default 1.0
        timerDelay = self.getTimerDelay( )
        self.ui.spinDelay.setValue( timerDelay )

    def groupsChanged(self):
        self.groups = self.iface.legendInterface().groups()
        self.groupRels = self.iface.legendInterface().groupLayerRelationship()

        cbxGroup = self.ui.cbxGroup
        if not cbxGroup is None:
            cbxGroup.clear()
            cbxGroup.addItem('<Visible Layers>')
            cbxGroup.addItem('<Root>')
            cbxGroup.addItems( self.groups )
#        for group in self.groups:
#            cbxGroup.addItem( group )

    def actionClose(self):
        self.state='close'
        self.actionStop()

    def actionStartPause(self):
        if self.state=='stop':
            self.actionStart()
        elif self.state=='start':
            self.actionPause()
        elif self.state=='pause':
            self.actionResume()

    def actionStart(self):

        # save visible layers
        self.bakLayerId = list()
        for layer in self.iface.mapCanvas().layers():
            self.bakLayerId.append( layer.id() )
#        print('bakLayerId: '+str(self.bakLayerId))
            
        selGroupIndex = self.ui.cbxGroup.currentIndex()
        selGroupName = self.ui.cbxGroup.currentText()

        pp = pprint.PrettyPrinter()

 #       print('start, delay='+str(self.getTimerDelay( ))+' current= '+str(selGroupIndex))
 #       print('size(cbxGroup)='+str(self.ui.cbxGroup.count())+' size(groups)='+str(self.groups.count()))
        #print('group: '+ self.groups[selGroupIndex])
 #       print('groups: ')
 #       print(str(self.groups))
 #       print('relationships: ')
 #       pp.pprint(self.groupRels)

        # get layers to show
        self.selLayerId = list()
        if selGroupName == '<Visible Layers>':
            self.selLayerId = self.bakLayerId
        else:
            for grp, rels in self.groupRels:
                if ( grp == '' and selGroupName == '<Root>' ) or ( grp == selGroupName ):
                    for rel in rels:
                        self.selLayerId.append(rel)
                elif selGroupName == '<Root>':
                    self.selLayerId.append(grp)

        if len(self.selLayerId) <= 1:
#	    QgsMessageLog.logMessage('Loop Visible Layers Plugin : must select more than one layer.', 'Plugins')
            QtGui.QMessageBox.critical(self, "Error", 'Loop Visible Layers Plugin : must select more than one layer.')
            #print('Error, must select more than one layer')
            return
#        else:
#            print('selLayerId= '+str(self.selLayerId))

        self.state='start'
        self.ui.btnStart.setIcon( self.iconPause )
        self.ui.btnNext.setEnabled( False )
        
        QtGui.QApplication.setOverrideCursor( self.loopCursor )

        # first hide all layers
        ifaceLegend = self.iface.legendInterface()
        ifaceLayers = QgsMapLayerRegistry.instance().mapLayers()
        for layerName, layer in ifaceLayers.iteritems():
            ifaceLegend.setLayerVisible( layer, False )
            
        #delegate to actionNext() to loop visible layers
        self.actionNext()

        # start timer
        self.timer.start( self.getTimerDelay() * 1000 );

    def actionNext(self):
        print('actionNext(), count='+str(self.count))

        ifaceLegend = self.iface.legendInterface()
        ifaceLayers = QgsMapLayerRegistry.instance().mapLayers()

        i=0
        if self.count > len(self.selLayerId)-1:
            self.count = 0

        # get all layers  and all groups as lists
        # slightly ineficient but I want to work with python lists exclusively here
        self.allLayerIds = list()
        for key in ifaceLayers.keys():
            self.allLayerIds.append(str(key) )
        print(str('layers: '+str(self.allLayerIds)))
        self.allGroupIds = list()
        for key in self.groups:
            self.allGroupIds.append( str(key) )
        print(str('groups: '+str(self.allGroupIds)))
        
        # show all items in self.selLayerId
        for layerId in self.selLayerId:
            if i == self.count :
                layerVisible = True
            else:
                layerVisible = False
            if layerId in self.allLayerIds:
                layer = ifaceLayers[QString(layerId)]
#                print('layerID '+str(layerId)+' is a layer')
#                print('i= '+str(i)+' count= '+str(self.count))
                ifaceLegend.setLayerVisible( layer, layerVisible )
                i = i + 1
            elif layerId in self.allGroupIds:
#                print('layerID '+str(layerId))
#                print('i= '+str(i)+' count= '+str(self.count))
                self.setGroupVisible(layerId,layerVisible)

                i = i + 1
            else:
                QgsMessageLog.logMessage('Loop Visible Layers Plugin : layerId '+str(layerId)+' is not a layer nor a group...', 'Plugins')         

        self.count = self.count + 1

    def setGroupVisible(self,layerId,layerVisible):
#        print('setGroupVisible('+str(layerId)+', '+str(layerVisible))
        for grp, rels in self.groupRels:
#            print('tmp grp='+str(grp))
            if ( grp == '' and layerId == '<Root>' ) or ( grp == layerId ):
#                print('relationships: '+str(rels))
                for tmpLayerId in rels:
                    if tmpLayerId in self.allGroupIds:
                        self.setGroupVisible(tmpLayerId,layerVisible)
                    else:
                        layer = QgsMapLayerRegistry.instance().mapLayers()[QString(tmpLayerId)]
                        self.iface.legendInterface().setLayerVisible( layer, layerVisible )


    def actionStop(self):
        self.timer.stop()

        #restore old layers visibility
        for layerName, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.id() in self.bakLayerId:
                self.iface.legendInterface().setLayerVisible( layer, True )
            else:
                self.iface.legendInterface().setLayerVisible( layer, False )
        QtGui.QApplication.restoreOverrideCursor()

        self.count = 0
        if self.state != 'close':
            self.state='stop'
            self.ui.btnStart.setIcon( self.iconStart )
            self.ui.btnNext.setEnabled( False )

    def actionPause(self):

        self.state='pause'

        if self.timer.isActive():
            self.timer.stop()

        self.ui.btnStart.setIcon( self.iconStart )
        self.ui.btnNext.setEnabled( True )

    def actionResume(self):

        self.state='start'

        if not self.timer.isActive():
            self.timer.start( self.getTimerDelay() * 1000 )

        self.ui.btnStart.setIcon( self.iconPause )
        self.ui.btnNext.setEnabled( False )


    def getTimerDelay(self):
        timerDelay = self.ui.spinDelay.value()
        if timerDelay <= 0:
            timerDelay = 1.0
            self.setTimerDelay(timerDelay)
        return timerDelay

    def setTimerDelay(self,timerDelay):
        self.ui.spinDelay.setValue( timerDelay )

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    # minimize widget
    def resizeMin(self):
        if self.isFloating():
            self.resize( self.minimumSize() )

