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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = "Abdul Raheem Siddiqui"
__date__ = "2021-02-21"
__copyright__ = "(C) 2021 by Abdul Raheem Siddiqui"


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AreaWeightedAverage class from file AreaWeightedAverage.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .area_weighted_average import AreaWeightedAveragePlugin

    return AreaWeightedAveragePlugin(iface)
