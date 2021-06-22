def check_avail_plugin_version(plugin_name: str) -> str:
    import requests
    import xml.etree.ElementTree as ET
    from qgis.core import Qgis

    qgis_version = Qgis.QGIS_VERSION.replace("-", ".").split(".")
    qgis_version = qgis_version[0] + "." + qgis_version[1]

    r = requests.get(
        f"https://plugins.qgis.org/plugins/plugins.xml?qgis={qgis_version}"
    )

    xml_str = r.text
    root = ET.fromstring(xml_str)

    for plugin in root.findall("pyqgis_plugin"):
        name = plugin.get("name")
        if name == plugin_name:
            experimental = plugin.find("experimental").text
            if experimental == "False":
                return plugin.find("version").text


def installPlugin():
    import pyplugin_installer

    pyplugin_installer.instance().fetchAvailablePlugins(False)
    pyplugin_installer.instance().installPlugin("area_weighted_average")


def upgradeMessage():
    from qgis.utils import iface
    from qgis.PyQt.QtWidgets import QPushButton
    from qgis.core import Qgis

    widget = iface.messageBar().createMessage(
        "Area Weighted Average Plugin", "Newer version of the plugin is available."
    )
    button = QPushButton(widget)
    button.setText("Upgrade")
    button.pressed.connect(installPlugin)
    widget.layout().addWidget(button)
    iface.messageBar().pushWidget(widget, duration=10)
