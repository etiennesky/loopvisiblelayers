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
from loopvisiblelayersdock import LoopVisibleLayersDock

class LoopVisibleLayers:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.groups = QStringList()
        self.groupsRels = list()
        self.dockWidget = None


    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(':/plugins/loopvisiblelayers/icon.png'), \
            'Loop Visible Layers', self.iface.mainWindow())

        # create and show the dock
        self.dockWidget = LoopVisibleLayersDock(self.iface.mainWindow(), self.iface)
        self.restoreDockLocation()
        self.restoreTimerDelay()

        settings = QSettings()
        if not settings.value('/Qgis/enable_render_caching').toBool():
            self.dockWidget.setStatus( 'Enable render caching to improve performance' )

        self.iface.addDockWidget(self.dockWidget.getLocation(), self.dockWidget)
        # show the dialog
        #dlg.show()


    def unload(self):
        # Remove the plugin menu item and icon 
        self.saveTimerDelay()
        self.saveDockLocation()
        self.dockWidget.close()
        self.dockWidget.actionClose() 


    def saveDockLocation(self):
        settings = QSettings()
        #code from dockable mirror map
        floating = self.dockWidget.isFloating()

        if floating:
            nFloating = 1
            position = '%s %s' % (self.dockWidget.pos().x(), self.dockWidget.pos().y())
        else:
            nFloating = 0
            position = u'%s' % self.dockWidget.getLocation()
            
        settings.setValue( '/PythonPlugins/LoopVisibleLayers/floating', floating )
        settings.setValue( '/PythonPlugins/LoopVisibleLayers/position', QString(position) )
        #size = '%s %s' % (dockwidget.size().width(), dockwidget.size().height())
        #QgsProject.instance().writeEntry( 'DockableMirrorMap', '/mirror%s/size' % i, QString(size) )

    def restoreDockLocation(self):
        settings = QSettings()

        floating = settings.value('/PythonPlugins/LoopVisibleLayers/floating').toBool()
        self.dockWidget.setFloating( floating )
        if not floating:
            position = settings.value( '/PythonPlugins/LoopVisibleLayers/position' ).toString()
            if position is None or position=='':
                position = Qt.LeftDockWidgetArea
            else:
                #position = int(position.split(' ')[0])
                position = int(position)
            #position = Qt.LeftDockWidgetArea
            self.dockWidget.setLocation( position )

    def saveTimerDelay(self):
        timerDelay = self.dockWidget.getTimerDelay()
        settings = QSettings()
        timerDelayStr = settings.value('/PythonPlugins/LoopVisibleLayers/delay')
        if ( timerDelayStr.toFloat()[0] != timerDelay ):
            settings.setValue( '/PythonPlugins/LoopVisibleLayers/delay', timerDelay )

    def restoreTimerDelay(self):
        settings = QSettings()
        timerDelayStr = settings.value('/PythonPlugins/LoopVisibleLayers/delay')

        if timerDelayStr is None or timerDelayStr != '':
            timerDelay = timerDelayStr.toFloat()[0]
        else:
            timerDelay = 1.0
        if timerDelay <= 0:
            timerDelay = 1.0

        self.dockWidget.setTimerDelay( timerDelay )
