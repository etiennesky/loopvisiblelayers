#/***************************************************************************
# LoopVisibleLayers
# 
# Loop Visible Layers Plugin
#                             -------------------
#        begin                : 2012-03-12
#        copyright            : (C) 2012 by Etienne Tourigny
#        email                : etourigny.dev@gmail.com
# ***************************************************************************/
# 
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# Makefile for a PyQGIS plugin 

PLUGINNAME = loopvisiblelayers

PY_FILES = loopvisiblelayers.py loopvisiblelayersdock.py __init__.py

EXTRAS = icon.png icons/*

#UI_FILES = ui_loopvisiblelayers.py ui_loopvisiblelayersdock.py
UI_FILES = ui_loopvisiblelayersdock.py

RESOURCE_FILES = resources_rc.py

default: compile

compile:  copy_resource $(UI_FILES) $(RESOURCE_FILES)

copy_resource:
	cp -f resources.qrc resources_rc.qrc

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis/python/plugins
deploy: compile
	mkdir -p $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(UI_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)

# Create a zip package of the plugin named $(PLUGINNAME).zip. 
# This requires use of git (your plugin development directory must be a 
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=Version_0.3.2
package: compile
		rm -f $(PLUGINNAME).zip
		git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
		echo "Created package: $(PLUGINNAME).zip"
