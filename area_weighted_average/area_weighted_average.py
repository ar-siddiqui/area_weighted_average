# -*- coding: utf-8 -*-

"""
/***************************************************************************
 AreaWeightedAverage
                                 A QGIS plugin
 Area Area Weighted Average.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-02-21
        copyright            : (C) 2021 by Abdul Raheem Siddiqui
        email                : ars.work.ce@gmail.com
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

__author__ = "Abdul Raheem Siddiqui"
__date__ = "2021-06-25"
__copyright__ = "(C) 2021 by Abdul Raheem Siddiqui"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"

import inspect
import os
import sys

import processing
from qgis.core import QgsApplication, QgsProcessingAlgorithm
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from area_weighted_average.processing import AreaWeightedAverageProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class AreaWeightedAveragePlugin(object):
    def __init__(self, iface):
        self.provider = None
        self.iface = iface

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = AreaWeightedAverageProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        icon = os.path.join(os.path.join(cmd_folder, "icon.png"))
        self.action = QAction(QIcon(icon), "Area Weighted Average", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&Area Weighted Average", self.action)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.iface.removePluginMenu("&Area Weighted Average", self.action)

    def run(self):
        processing.execAlgorithmDialog("Area Weighted Average:Area Weighted Average")
