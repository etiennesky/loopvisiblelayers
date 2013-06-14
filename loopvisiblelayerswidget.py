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
from PyQt4.QtGui import QIcon, QPixmap
from qgis.core import *
from qgis.gui import *

from ui_loopvisiblelayerswidget import Ui_LoopVisibleLayersWidget as Ui_Widget

# create the widget
class LoopVisibleLayersWidget(QtGui.QWidget, Ui_Widget):
    def __init__(self, iface):

        QtGui.QWidget.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)

        # Save reference to the QGIS interface
        self.iface = iface

        # variables
        self.groupNames = None
        self.groupRels = None
        self.bakLayerIds = None
        self.count = 0
        self.freeze = True
        self.updateCount = 0
        self.signalsLegendIface = False # are the new legendInterface() signals available?
        self.forward = True
        self.visibleDock = False
        
        # objects
        self.timer = QTimer(self)       
        QObject.connect(self.timer, SIGNAL('timeout()'), self.actionNext)
        self.state = 'stop'
        self.iconStart = QIcon()
        self.iconStart.addPixmap(QPixmap(':/plugins/loopvisiblelayers/icons/control_play.png'), QIcon.Normal, QIcon.Off)
        self.iconPause = QIcon()
        self.iconPause.addPixmap(QPixmap(':/plugins/loopvisiblelayers/icons/control_pause.png'), QIcon.Normal, QIcon.Off)
        self.loopCursor = QtGui.QCursor(QtGui.QPixmap(':/plugins/loopvisiblelayers/icons/icon_small.png'))
        #self.btnRefresh.setVisible( False )
        
        #self.legend = self.iface.mainWindow().legend() #not accessible...

        # UI
        timerDelay = self.getTimerDelay( )
        self.spinDelay.setValue( timerDelay )
        self.setStatus( '' ) #invisible by default

        # signals/slots
        QObject.connect(self, SIGNAL('topLevelChanged(bool)'), self.resizeMin)
        QObject.connect(self.btnStart, SIGNAL('clicked()'), self.actionStartPause)
        QObject.connect(self.btnForward, SIGNAL('clicked()'), self.actionForward)
        QObject.connect(self.btnBack, SIGNAL('clicked()'), self.actionBack)
        QObject.connect(self.btnStop, SIGNAL('clicked()'), self.actionStop)
        
        # signals mapped to checkGroupsChanged (btnRefresh, layers changed)
        #QObject.connect( self.btnRefresh, SIGNAL( 'clicked()' ), self.checkGroupsChanged )
        QObject.connect( self, SIGNAL( 'visibilityChanged( bool )' ), self.checkGroupsChanged )
        # need something like QTreeWidget::itemChanged() legendInterface() in but there is no interface for that
        # changes in my repos. fix this and are required for auto update - https://github.com/etiennesky/Quantum-GIS
        # fallback is to use enterEvent, which is be disabled when not needed
        #QObject.connect( self.iface.legendInterface(), SIGNAL( 'groupIndexChanged ( int, int )' ), self.checkGroupsChanged )
        #QObject.connect( QgsMapLayerRegistry.instance(), SIGNAL( 'layerWasAdded( QgsMapLayer* )' ), self.checkGroupsChanged )
        #QObject.connect( QgsMapLayerRegistry.instance(), SIGNAL( 'layerWillBeRemoved( QString )' ), self.checkGroupsChanged )
        #QObject.connect( QgsMapLayerRegistry.instance(), SIGNAL( 'removedAll()' ), self.checkGroupsChanged )
        #QObject.connect( self.iface.mapCanvas(), SIGNAL( 'layersChanged()' ), self.checkGroupsChanged)
        QObject.connect( self.iface.legendInterface(), SIGNAL( 'itemAdded( QModelIndex )' ), self.checkGroupsChangedLegendIface )
        QObject.connect( self.iface.legendInterface(), SIGNAL( 'itemRemoved()' ), self.checkGroupsChangedLegendIface )
        QObject.connect( self.iface.legendInterface(), SIGNAL( 'groupRelationsChanged()' ), self.checkGroupsChangedLegendIface )
        QObject.connect( self.iface.mapCanvas(), SIGNAL( 'stateChanged( int )' ), self.checkGroupsChanged )
        #should we disconnect when unload?

        #update groups on init
        self.checkGroupsChanged()
        
    # this slot triggered by iface.legendInterface(), i.e. when items are added, moved or removed
    # these signals are not yet part of qgis, so enterEvent() is used as a fallback
    def checkGroupsChangedLegendIface(self):
       # when we get this signal for the first time, set signalsLegendIface=True so enterEvent() does nothing 
        if not self.signalsLegendIface:
            self.signalsLegendIface = True
        self.checkGroupsChanged()

    # this does the real work    
    def checkGroupsChanged(self):
        newGroupNames = self.iface.legendInterface().groups()
        newGroupRels = self.iface.legendInterface().groupLayerRelationship()
        if ( newGroupNames == self.groupNames ) and ( newGroupRels == self.groupRels ):
            return
        
        self.groupNames = newGroupNames
        self.groupRels = self.iface.legendInterface().groupLayerRelationship()
        self.updateCount = self.updateCount+1

        cbxGroup = self.cbxGroup
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
        
        #make sure groups are updated
        newGroupNames = self.iface.legendInterface().groups()
        newGroupRels = self.iface.legendInterface().groupLayerRelationship()
        if ( newGroupNames != self.groupNames ) or ( newGroupRels != self.groupRels ):
            self.checkGroupsChanged()
            QtGui.QMessageBox.warning(self, 'Warning', 'Loop Visible Layers Plugin \n\nSelection has been updated, verify and start again')
            return

        # save visible layers
        self.bakLayerIds = list()
        for layer in self.iface.mapCanvas().layers():
            self.bakLayerIds.append( layer.id() )
            
        selGroupIndex = self.cbxGroup.currentIndex()
        selGroupName = self.cbxGroup.currentText()

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

        self.state='start'
        
        # set override cursor
        QtGui.QApplication.setOverrideCursor( self.loopCursor )

        # freeze the canvas
        self.freezeCanvas( True )

        # hide all layers
        ifaceLegend = self.iface.legendInterface()
        ifaceLayers = QgsMapLayerRegistry.instance().mapLayers()
        for layerName, layer in ifaceLayers.iteritems():
            ifaceLegend.setLayerVisible( layer, False )
            
        # activate controls
        if self.getTimerDelay() > 0:
            self.btnStart.setIcon( self.iconPause )
            self.btnForward.setEnabled( False )
            self.btnBack.setEnabled( False )
            self.btnStop.setEnabled( True )
        else:
            self.btnStart.setEnabled( False )
            self.btnForward.setEnabled( True )
            self.btnBack.setEnabled( True )
            self.btnStop.setEnabled( True )

        #delegate to actionNext() to loop visible layers
        self.actionNext()

        # start timer
        if self.getTimerDelay() > 0:
            self.timer.start( self.getTimerDelay() * 1000 );

    def actionForward(self):
        if not self.forward:
            self.count = self.count + 2
        self.forward = True
        self.actionNext()

    def actionBack(self):
        if self.forward:
            self.count = self.count - 2
        self.forward = False
        self.actionNext()

    def actionNext(self):

        # do not update canvas if window is inactive
        if not self.iface.mainWindow().isActiveWindow() and not self.isActiveWindow():
            self.setStatus( 'Window is inactive, not updating canvas' )
            return
        else:
            self.setStatus( '' )
        # do not update canvas if dock is hidden
        if not self.visibleDock:
            return

        ifaceLegend = self.iface.legendInterface()
        ifaceLayers = QgsMapLayerRegistry.instance().mapLayers()

        # update loop counter
        if self.forward:
            i = 0
            if self.count > len(self.selLayerId)-1:
                self.count = 0
            incr = 1
        else:
            i = 0
            #i = len(self.selLayerId)-1
            if self.count < 0 :
                self.count = len(self.selLayerId)-1
            incr = -1

        # get all layers and all groups as lists
        # slightly ineficient but I want to work with python lists exclusively here
        self.allLayerIds = ifaceLayers

        # freeze the canvas
        self.freezeCanvas( True )
        
        # show all items in self.selLayerId
        for layerId in self.selLayerId:
            if i == self.count :
                layerVisible = True
            else:
                layerVisible = False
            if layerId in self.allLayerIds:
                layer = ifaceLayers[str(layerId)]
                ifaceLegend.setLayerVisible( layer, layerVisible )
                i = i + 1
            elif layerId in self.groupNames:
                self.setGroupVisible(layerId,layerVisible)

                i = i + 1
            else:
                QgsMessageLog.logMessage('Loop Visible Layers Plugin : layerId '+str(layerId)+' is not a layer nor a group...', 'Plugins')         
                self.setStatus( 'invalid layer '+layerId )

        # thaw the canvas
        self.freezeCanvas( False )

        #update loop counter
        self.count = self.count + incr

    def setGroupVisible(self,layerId,layerVisible):

        for grp, rels in self.groupRels:
            if ( grp == '' and layerId == '<Root>' ) or ( grp == layerId ):
                for tmpLayerId in rels:
                    if tmpLayerId in self.groupNames:
                        self.setGroupVisible(tmpLayerId,layerVisible)
                    else:
                        layer = QgsMapLayerRegistry.instance().mapLayers()[str(tmpLayerId)]
                        self.iface.legendInterface().setLayerVisible( layer, layerVisible )


    def actionStop(self):

        if self.state == 'stop':
            return

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
            self.btnStart.setIcon( self.iconStart )
            self.btnStart.setEnabled( True )
            self.btnForward.setEnabled( False )
            self.btnBack.setEnabled( False )
            self.btnStop.setEnabled( False )

    def actionPause(self):

        self.state='pause'

        if self.timer.isActive():
            self.timer.stop()

        self.btnStart.setIcon( self.iconStart )
        self.btnForward.setEnabled( True )
        self.btnBack.setEnabled( True )

    def actionResume(self):

        self.state='start'

        if not self.timer.isActive():
            if self.getTimerDelay() > 0:
                self.timer.start( self.getTimerDelay() * 1000 );
                self.btnForward.setEnabled( False )
                self.btnBack.setEnabled( False )
            else:
                self.btnForward.setEnabled( True )
                self.btnBack.setEnabled( True )

        self.btnStart.setIcon( self.iconPause )
        self.btnForward.setEnabled( False )
        self.btnBack.setEnabled( False )
        

    def getTimerDelay(self):
        timerDelay = self.spinDelay.value()
        if timerDelay < 0:
            timerDelay = 1.0
            self.setTimerDelay(timerDelay)
        return timerDelay

    def setTimerDelay(self,timerDelay):
        self.spinDelay.setValue( timerDelay )

    # minimize widget
    def resizeMin(self):
        if self.isFloating():
            self.resize( self.minimumSize() )

    def setStatus(self, status):
        if self.lblStatus.text() == status:
            return
        if status is None or status=='':
            self.lblStatus.setText( '' )
            self.lblStatus.setVisible( False )
        else:
            self.lblStatus.setText( status )
            self.lblStatus.setVisible( True )

    def freezeCanvas(self, setFreeze):
        if self.freeze:
            if setFreeze:
                if not self.iface.mapCanvas().isFrozen():
                    self.iface.mapCanvas().freeze( True )
            else:
                if self.iface.mapCanvas().isFrozen():
                    self.iface.mapCanvas().freeze( False )
                    self.iface.mapCanvas().refresh()

    def enterEvent(self, event):
        # workaround, if signalsLegendIface=False, check groups changed
        if not self.signalsLegendIface:
            self.checkGroupsChanged()
        QtGui.QWidget.enterEvent(self, event)

    def sizeHint(self):
        return self.minimumSize()
        
    def onVisibilityChanged(self,visible):
        self.visibleDock = visible
        if self.state=='start' or self.state=='pause':
            if visible:
                # set override cursor
                QtGui.QApplication.setOverrideCursor( self.loopCursor )
            else:
                # restore override cursor
                QtGui.QApplication.restoreOverrideCursor()
