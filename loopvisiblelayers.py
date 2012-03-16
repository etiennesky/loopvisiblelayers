"""
/***************************************************************************
 LoopVisibleLayers
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from loopvisiblelayerswidget import LoopVisibleLayersWidget

class LoopVisibleLayers:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.loopWidget = None
        self.dockWidget = None

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(':/plugins/loopvisiblelayers/icon.png'), \
            'Loop Visible Layers', self.iface.mainWindow())
        # connect the action
        QObject.connect(self.action, SIGNAL('triggered()'), self.showHideDock)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        #self.iface.addPluginToMenu('Loop Visible Layers', self.action)
        
        # create the loop widget
        self.loopWidget = LoopVisibleLayersWidget(self.iface)
        self.restoreTimerDelay()
        settings = QSettings()
        if not settings.value('/Qgis/enable_render_caching').toBool():
            self.loopWidget.setStatus( 'Enable render caching to improve performance' )
           
        # create and show the dock
        self.dockWidget = QDockWidget('Loop Visible Layers', self.iface.mainWindow() )
        self.dockWidget.setObjectName('Loop Visible Layers')
        self.dockWidget.setWidget(self.loopWidget)       
        QObject.connect(self.dockWidget, SIGNAL('topLevelChanged ( bool )'), self.resizeDock)
        QObject.connect(self.dockWidget, SIGNAL('visibilityChanged ( bool )'), self.loopWidget.onVisibilityChanged)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)

    def showHideDock(self):
        if not self.dockWidget.isVisible():
            self.dockWidget.setVisible( True )
        else:
            self.dockWidget.setVisible( False )

    #resize dock to minimum size if it is floating
    def resizeDock(self, topLevel):
        if topLevel:
            self.dockWidget.resize( self.dockWidget.minimumSize() )

    def unload(self):
        # Remove the plugin menu item and icon
        #self.iface.removePluginMenu('Loop Visible Layers',self.action)
        self.iface.removeToolBarIcon(self.action)
        #remove the dock
        self.saveTimerDelay()
        self.dockWidget.close()
        self.loopWidget.actionClose() 

    def saveTimerDelay(self):
        timerDelay = self.loopWidget.getTimerDelay()
        settings = QSettings()
        timerDelayStr = settings.value('/LoopVisibleLayers/delay')
        if ( timerDelayStr.toFloat()[0] != timerDelay ):
            settings.setValue( '/LoopVisibleLayers/delay', timerDelay )

    def restoreTimerDelay(self):
        settings = QSettings()
        timerDelayStr = settings.value('/LoopVisibleLayers/delay')

        if timerDelayStr is None or timerDelayStr != '':
            timerDelay = timerDelayStr.toFloat()[0]
        else:
            timerDelay = 1.0
        if timerDelay <= 0:
            timerDelay = 1.0

        self.loopWidget.setTimerDelay( timerDelay )
