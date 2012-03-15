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

from PyQt4.QtCore import *
from PyQt4 import QtGui
#from PyQt4.QtGui import *
from PyQt4.QtGui import QIcon, QPixmap
from qgis.core import *
from qgis.gui import *

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
        self.groupNames = None
        self.groupRels = None
        self.bakLayerIds = None
        self.count = 0
        self.location = Qt.LeftDockWidgetArea
        self.freeze = True
        self.updateCount=0
        
        # objects
        self.timer = QTimer(self)       
        QObject.connect(self.timer, SIGNAL('timeout()'), self.actionNext)
        self.state='stop'
        self.iconStart = QIcon()
        self.iconStart.addPixmap(QPixmap(_fromUtf8(':/plugins/loopvisiblelayers/icons/control_play.png')), QIcon.Normal, QIcon.Off)
        self.iconPause = QIcon()
        self.iconPause.addPixmap(QPixmap(_fromUtf8(':/plugins/loopvisiblelayers/icons/control_pause.png')), QIcon.Normal, QIcon.Off)
        self.loopCursor = QtGui.QCursor(QtGui.QPixmap(_fromUtf8(':/plugins/loopvisiblelayers/icons/icon_small.png')))

        #self.legend = self.iface.mainWindow().legend() #not accessible...

        # UI
        timerDelay = self.getTimerDelay( )
        self.ui.spinDelay.setValue( timerDelay )
        self.setStatus( '' ) #invisible by default

        # signals/slots
        self.connect(self, SIGNAL('dockLocationChanged(Qt::DockWidgetArea)'), self.setLocation)
        self.connect(self, SIGNAL('topLevelChanged(bool)'), self.resizeMin)
        QObject.connect(self.ui.btnStart, SIGNAL('clicked()'), self.actionStartPause)
        QObject.connect(self.ui.btnNext, SIGNAL('clicked()'), self.actionNext)
        QObject.connect(self.ui.btnStop, SIGNAL('clicked()'), self.actionStop)

        # signals mapped to groupsChanged (btnRefresh, layers changed)
        # TODO: how to detect that groups and relationships have changed?
        # need something like QTreeWidget::itemChanged() but there is no interface for that
        # changes in my repos. fix this and are required for auto update - https://github.com/etiennesky/Quantum-GIS
        QObject.connect( self.ui.btnRefresh, SIGNAL( 'clicked()' ), self.groupsChanged )
        #QObject.connect( self.iface.legendInterface(), SIGNAL( 'groupIndexChanged ( int, int )' ), self.groupsChanged )
        QObject.connect( self.iface.legendInterface(), SIGNAL( 'itemAdded( int )' ), self.groupsChanged )
        QObject.connect( self.iface.legendInterface(), SIGNAL( 'itemRemoved()' ), self.groupsChanged )
        QObject.connect( self.iface.legendInterface(), SIGNAL( 'groupRelationsChanged()' ), self.groupsChanged )
        #QObject.connect( QgsMapLayerRegistry.instance(), SIGNAL( 'layerWasAdded( QgsMapLayer* )' ), self.groupsChanged )
        #QObject.connect( QgsMapLayerRegistry.instance(), SIGNAL( 'layerWillBeRemoved( QString )' ), self.groupsChanged )
        #QObject.connect( QgsMapLayerRegistry.instance(), SIGNAL( 'removedAll()' ), self.groupsChanged )
        #QObject.connect( self.iface.mapCanvas(), SIGNAL( 'layersChanged()' ), self.groupsChanged)
        QObject.connect( self.iface.mapCanvas(), SIGNAL( 'stateChanged( int )' ), self.groupsChanged )
        #update groups
        self.groupsChanged()

    def groupsChanged(self):

        #print('loopvisiblelayersdoc: groupsChanged() '+str(self.updateCount))
        self.updateCount = self.updateCount+1

        self.groupNames = self.qstrlist2list( self.iface.legendInterface().groups() )
        self.groupRels = self.iface.legendInterface().groupLayerRelationship()

        cbxGroup = self.ui.cbxGroup
        if not cbxGroup is None:
            curItem = cbxGroup.currentText()
            cbxGroup.clear()
            cbxGroup.addItem('<Visible Layers>')
            cbxGroup.addItem('<Root>')
            cbxGroup.addItems( self.iface.legendInterface().groups() )
            curIdx = cbxGroup.findText(curItem)
            if curIdx != -1:
                cbxGroup.setCurrentIndex( curIdx )

    def actionClose(self):
        if self.state!='stop':
            self.state='close'
            self.actionStop()
        self.state='close'

    def actionStartPause(self):
        if self.state=='stop':
            self.actionStart()
        elif self.state=='start':
            self.actionPause()
        elif self.state=='pause':
            self.actionResume()

    def actionStart(self):

        # save visible layers
        self.bakLayerIds = list()
        for layer in self.iface.mapCanvas().layers():
            self.bakLayerIds.append( layer.id() )
#        print('bakLayerIds: '+str(self.bakLayerIds))
            
        selGroupIndex = self.ui.cbxGroup.currentIndex()
        selGroupName = self.ui.cbxGroup.currentText()

 #       print('start, delay='+str(self.getTimerDelay( ))+' current= '+str(selGroupIndex))
 #       print('size(cbxGroup)='+str(self.ui.cbxGroup.count())+' size(groups)='+str(self.groups.count()))
 #       print('group: '+ self.groups[selGroupIndex])
 #       print('groups: ')
 #       print(str(self.groups))
 #       print('relationships: ')
 #       pp.pprint(self.groupRels)

        # get layers to show
        self.selLayerId = list()
        if selGroupName == '<Visible Layers>':
            self.selLayerId = self.bakLayerIds
        else:
            #look for duplicate group names
            if len(self.groupNames) != len(set(self.groupNames)):
                QtGui.QMessageBox.critical(self, 'Error', 'Loop Visible Layers Plugin \n\nGroup names must be unique')
                return
            for grp, rels in self.groupRels:
                if ( grp == '' and selGroupName == '<Root>' ) or ( grp == selGroupName ):
                    for rel in rels:
                        self.selLayerId.append(rel)
                elif selGroupName == '<Root>':
                    self.selLayerId.append(grp)

        if len(self.selLayerId) <= 1:
	    #QgsMessageLog.logMessage('Loop Visible Layers Plugin : must select more than one layer.', 'Plugins')
            QtGui.QMessageBox.critical(self, 'Error', 'Loop Visible Layers Plugin \n\nMust select more than one layer')
            return
#        else:
#            print('selLayerId= '+str(self.selLayerId))

        self.state='start'
        self.ui.btnStart.setIcon( self.iconPause )
        self.ui.btnNext.setEnabled( False )
        
        # set override cursor
        QtGui.QApplication.setOverrideCursor( self.loopCursor )

        # freeze the canvas
        self.freezeCanvas( True )

        # hide all layers
        ifaceLegend = self.iface.legendInterface()
        ifaceLayers = QgsMapLayerRegistry.instance().mapLayers()
        for layerName, layer in ifaceLayers.iteritems():
            ifaceLegend.setLayerVisible( layer, False )
            
        #delegate to actionNext() to loop visible layers
        self.actionNext()

        # start timer
        self.timer.start( self.getTimerDelay() * 1000 );

    def actionNext(self):

        ifaceLegend = self.iface.legendInterface()
        ifaceLayers = QgsMapLayerRegistry.instance().mapLayers()

        # update loop counter
        i=0
        if self.count > len(self.selLayerId)-1:
            self.count = 0

#        print('TMP ET actionNext() i='+str(i)+' count='+str(self.count))

        # get all layers and all groups as lists
        # slightly ineficient but I want to work with python lists exclusively here
        self.allLayerIds = self.qstrlist2list( ifaceLayers )
        #print(str('layers: '+str(self.allLayerIds)))
        #print(str('groups: '+str(self.groupNames)))

        # freeze the canvas
        self.freezeCanvas( True )
        
        # show all items in self.selLayerId
        for layerId in self.selLayerId:
            if i == self.count :
                layerVisible = True
            else:
                layerVisible = False
            if layerId in self.allLayerIds:
                layer = ifaceLayers[QString(layerId)]
                #print('layerID '+str(layerId)+' is a layer')
                #print('i= '+str(i)+' count= '+str(self.count))
                ifaceLegend.setLayerVisible( layer, layerVisible )
                i = i + 1
            elif layerId in self.groupNames:
                #print('layerID '+str(layerId))
                #print('i= '+str(i)+' count= '+str(self.count))
                self.setGroupVisible(layerId,layerVisible)

                i = i + 1
            else:
                QgsMessageLog.logMessage('Loop Visible Layers Plugin : layerId '+str(layerId)+' is not a layer nor a group...', 'Plugins')         
                self.setStatus( 'invalid layer '+layerId )

        # thaw the canvas
        self.freezeCanvas( False )

        #update loop counter
        self.count = self.count + 1

    def setGroupVisible(self,layerId,layerVisible):

#        print('setGroupVisible('+str(layerId)+', '+str(layerVisible))
        for grp, rels in self.groupRels:
#            print('tmp grp='+str(grp))
            if ( grp == '' and layerId == '<Root>' ) or ( grp == layerId ):
#                print('relationships: '+str(rels))
                for tmpLayerId in rels:
                    if tmpLayerId in self.groupNames:
                        self.setGroupVisible(tmpLayerId,layerVisible)
                    else:
                        layer = QgsMapLayerRegistry.instance().mapLayers()[QString(tmpLayerId)]
                        self.iface.legendInterface().setLayerVisible( layer, layerVisible )


    def actionStop(self):

        self.timer.stop()

        # freeze the canvas
        self.freezeCanvas( True )

        #restore old layers visibility
        for layerName, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.id() in self.bakLayerIds:
                self.iface.legendInterface().setLayerVisible( layer, True )
            else:
                self.iface.legendInterface().setLayerVisible( layer, False )

        # thaw the canvas
        self.freezeCanvas( False )

        # restore override cursor
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

    def setStatus(self, status):
        if status is None or status=='':
            self.ui.lblStatus.setText( '' )
            self.ui.lblStatus.setVisible( False )
        else:
            self.ui.lblStatus.setText( status )
            self.ui.lblStatus.setVisible( True )

    def freezeCanvas(self, setFreeze):
        if self.freeze:
            if setFreeze:
                if not self.iface.mapCanvas().isFrozen():
                    self.iface.mapCanvas().freeze( True )
            else:
                if self.iface.mapCanvas().isFrozen():
                    self.iface.mapCanvas().freeze( False )

    def qstrlist2list(self, qstrlist):
        tmplist = list()
        for key in qstrlist:
            tmplist.append( str(key) )
        return tmplist
