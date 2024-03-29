![area weighted average icon](area_weighted_average/icon.png)

# Area-Weighted-Average

Plugin to perform Area Weighted Average analysis in QGIS.

## Installation

Area Weighted Average Plugin can be downloaded from from official QGIS plugin repository or from https://github.com/ar-siddiqui/area_weighted_average/releases

## Algorithm Description

This algorithm calculates weighted average by performing spatial area weighted average analysis on an input polygon layer given an attribute in the overlay polygon layer. Each feature in the input layer will be assigned a spatial area weighted average value of the overlay field. A report of the analysis is generated as a GIS Layer and as HTML.

## Input Parameters

- Input Layer:
  Polygon layer for which area weighted average will be calculated.

- Overlay Layer:
  Polygon layer with source data. Must overlap the Input Layer.

- Field to Average:
  Single numeric field in the Overlay Layer.

- Identifier Field for Report [optional]:
  Name or ID field in the Input Layer. This field will be used to identify features in the report.

- Additional Fields to Keep for Report [optional]:
  Fields in the Overlay Layer that will be included in the reports.

## Outputs

- Result:
  Input layer but with the additional attribute of weighted value.

- Report as Layer:
  Report as a GIS layer.

- Report as HTML [optional]:
  Report containing feature-wise breakdown.

## Citation

Siddiqui, Abdul Raheem. 2021. “Area-Weighted-Average: Plugin to perform Area Weighted Average analysis in QGIS.” Accessed [Month Year] at https://github.com/ar-siddiqui/area_weighted_average.

## Donate

 <p>If this plugin is useful for you, please consider making a donation of any value to the developer.</p>

 <a href="https://www.paypal.com/donate?business=T25JMRWJAL5SQ&item_name=For+Area+Weighted+Average+Plugin&currency_code=USD" target="_blank">
 <img border="0" alt="Donate" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif">
 </a>
