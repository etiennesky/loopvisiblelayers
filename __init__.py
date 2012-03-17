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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Loop Visible Layers"
def description():
    return "Loop Visible Layers"
def version():
    return "Version 0.3.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.7"
def classFactory(iface):
    # load LoopVisibleLayers class from file LoopVisibleLayers
    from loopvisiblelayers import LoopVisibleLayers
    return LoopVisibleLayers(iface)
